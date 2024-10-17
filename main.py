

"""
Create a Python application that connects to either a MySQL or MongoDB 
server, and performs CRUD operations on a database. The application 
should model a store, where users can create accounts, purchase products, 
and look at a history of their orders. There should also be an admin 
feature where the admin should be able to see all orders and users.

- The application must be able to create, read, update, and delete.
- Use at least 3 different tables/collections (also create an ERD)
- The application must have a login feature, as well as user/admin roles
- Logging of events should be implemented (connecting to db, interacting with db/files, etc.)

- users can create accounts
- users can purchase products
- users can view their order history
- admins can view all orders
- admins can view all users
- users and admins should log in

"""

import mysql.connector
from mysql.connector import Error

cursor = None


def main():
    connection = create_connection()
    if connection:
        while True:
            action = input("Choose an action: TODO ")
            if action == 'create_user':
                username = input("Enter username: ")
                password = input("Enter password: ")
                create_user(connection, username, password)
            elif action == 'get_users':
                users = get_users(connection)
                for user in users:
                    print(user)
            elif action == 'update_user':
                user_id = input("Enter user ID: ")
                new_username = input("Enter new username: ")
                update_user(connection, user_id, new_username)
            elif action == 'delete_user':
                user_id = input("Enter user ID: ")
                delete_user(connection, user_id)
            elif action == 'exit':
                break
    connection.close()


def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect (
            host='proj1-database.ct8osg4umxax.us-east-2.rds.amazonaws.com',  
            user='admin',
            password='giUek73dIk9R',
            database='proj1-database'
        )
        logging.info("Database connection successful")
        cursor = connection.cursor()
    except Error as e:
        logging.error(f"Error: {err}")
    return connection



# CREATE ---
# Users can create accounts
def create_user(username, password):
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()

# READ ---
# Admins can view all users
def get_all_users():
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Admins can view all orders
def get_all_orders():
    cursor.execute("SELECT * FROM orders")
    return cursor.fetchall()

# Users can view their order history
def get_orders(username, password):
    cursor.execute("SELECT * FROM orders WHERE username = %s AND password = %s", username, password)
    return cursor.fetchall()

# UPDATE ---
# Users can purchase products
def purchase_product(username, password, product_id):
    #cursor.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (name, email, user_id))
    conn.commit()

# DELETE ---
# Users can delete their account
def delete_user(username, password):
    #cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()


def login():
    pass





if __name__ == "__main__":
    main()


















