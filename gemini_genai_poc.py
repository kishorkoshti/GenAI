import google.generativeai as genai
import re
import sqlite3

gamini_api = "your key "

def run_query(sql_query, conn):
    cursor = conn.cursor()
    result = cursor.execute(sql_query)
    rows = result.fetchall()
    return rows

# Create a new SQLite database (or connect to an existing one)
conn = sqlite3.connect('train_schedule.db')

result = run_query('SELECT DISTINCT source_station FROM train_information UNION SELECT DISTINCT destination_station FROM train_information UNION SELECT DISTINCT current_location FROM train_information;', conn)
junction_names = ", ".join([name[0] for name in result])

result = run_query('SELECT train_name FROM train_information;', conn)
train_names = ", ".join([name[0] for name in result])

# Configure the API key and model for query generation
genai.configure(api_key=gamini_api)
query_model = genai.GenerativeModel('gemini-1.5-flash')
query_chat_session = query_model.start_chat()

# Configure the API key and model for help desk response
helpdesk_model = genai.GenerativeModel('gemini-1.5-flash')
helpdesk_chat_session = helpdesk_model.start_chat()

# Define the initial context for query generation
query_context = [{'role': 'system', 'content': f"""
You are an intelligent HelpBoat that converts natural language questions into SQL queries based on the following database schema:

CREATE TABLE IF NOT EXISTS train_information (
    train_id INTEGER PRIMARY KEY AUTOINCREMENT,
    train_name TEXT NOT NULL,
    source_station TEXT NOT NULL,
    destination_station TEXT NOT NULL,
    current_location TEXT,
    ticket_price REAL NOT NULL,
    departure_time TEXT,
    arrival_time TEXT
);

Note: As a HelpBoat, you can only respond with SQL queries, Example "SELECT train_name FROM train_information WHERE destination_station = 'Goa';". 
In the query always make case insensitive search.
Please find the junction and train names, user might mis-spell the junction or train name so you have to make it autocorrect.
Junction Names: {junction_names}
Train Names: {train_names}
If anyone asks out of context, reply "None".
"""}]

chat_history = []

# Define the initial context for help desk response
helpdesk_context = [{'role': 'system', 'content': f"""
You are an intelligent HelpBoat tasked with converting raw answers into human-speakable responses.

Example:
Question: Give me the list of trains which are coming from Kolkata or Delhi.
Raw answer: [('Duronto Express',), ('Uttaranchal Express',), ('Himalayan Queen',)]
Speakable answer: There are three trains departing from Kolkata or Delhi: Duronto Express, Uttaranchal Express, and Himalayan Queen.

Note the following points and be strict with them:

    Don't add "Speakable answer:"
    Never use bullets or numbered points in the response.
"""}]

current_context = query_context.copy()

def get_select_query(user_prompt):
    current_context.append({'role': 'user', 'content': user_prompt})
    response = query_chat_session.send_message(f"Current Context: {str(current_context)}, Current Prompt: {user_prompt}")
    query = re.findall("(SELECT .*)\n", response.text)
    return query[0] if query else None

def helpdesk_desk_response(user_prompt, rows):
    rows = str(rows)
    final_prompt = f"""
    Question: {user_prompt}
    Raw answer: {rows}
    """
    chat_history.append({'role': 'user', 'content': user_prompt})
    response = helpdesk_chat_session.send_message(f"Context : {str(helpdesk_context)}, Chat History : {str(chat_history)}, Current Prompt: {final_prompt}")
    chat_history.append({'role': 'bot', 'content': response.text})
    return response.text



while True:
    user_prompt = input("Ask >  ")
    if "exit" in user_prompt.lower():
        print("Good bye....")
        break
        
    sql_query = get_select_query(user_prompt)

    if sql_query:
        query_result = run_query(sql_query, conn)
        response_text = helpdesk_desk_response(user_prompt, query_result)
        print(response_text)
    else:
        print("I'm sorry, I couldn't understand your query, please ask again")

# Close the database connection
conn.close()