#Script to create db file 


import sqlite3

# Create a new SQLite database (or connect to an existing one)
conn = sqlite3.connect('train_schedule.db')
cursor = conn.cursor()

# Create the train_information table
cursor.execute('''
CREATE TABLE IF NOT EXISTS train_information (
    train_id INTEGER PRIMARY KEY AUTOINCREMENT,
    train_name TEXT NOT NULL,
    source_station TEXT NOT NULL,
    destination_station TEXT NOT NULL,
    current_location TEXT,
    ticket_price REAL NOT NULL,
    departure_time TEXT,
    arrival_time TEXT
)
''')

# Insert data into the train_information table
trains_data = [
    ('Howrah Express', 'Howrah Junction', 'Mumbai Central', 'Kharagpur Junction', 1200.50, '06:00:00', '23:59:00'),
    ('Duronto Express', 'Kolkata', 'Delhi', 'Bhopal Junction', 1800.00, '10:00:00', '18:00:00'),
    ('Shatabdi Express', 'Chennai Central', 'Bangalore City', 'Vijayawada Junction', 1500.25, '08:30:00', '14:30:00'),
    ('Goa Express', 'Mumbai Central', 'Goa', 'Pune Junction', 950.75, '14:00:00', '22:00:00'),
    ('Uttaranchal Express', 'Delhi', 'Dehradun', 'Saharanpur Junction', 800.00, '07:30:00', '13:30:00'),
    ('Rajdhani Express', 'New Delhi', 'Mumbai Central', 'Nagpur Junction', 2500.00, '18:00:00', '12:00:00'),
    ('Intercity Express', 'Chennai Central', 'Hyderabad', 'Vijayawada Junction', 1100.50, '12:00:00', '20:00:00'),
    ('Garib Rath Express', 'Ahmedabad', 'Jaipur', 'Vadodara Junction', 600.25, '21:00:00', '05:00:00'),
    ('Himalayan Queen', 'Kolkata', 'Darjeeling', 'Malda Town', 750.00, '09:00:00', '17:00:00'),
    ('Sampark Kranti Express', 'Bangalore City', 'Pune Junction', 'Hubli Junction', 1300.75, '16:30:00', '06:30:00')
]

# Insert each train's data into the table
cursor.executemany('''
INSERT INTO train_information (train_name, source_station, destination_station, current_location, ticket_price, departure_time, arrival_time)
VALUES (?, ?, ?, ?, ?, ?, ?)
''', trains_data)

# Commit the transaction
conn.commit()

# Close the connection
conn.close()

print("Data inserted successfully!")