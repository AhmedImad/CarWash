import mysql.connector

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",     # Assuming the MySQL server is on your local machine
    user="root",
    password="root",
    database="carwashDB"  # The name of the database you created
)