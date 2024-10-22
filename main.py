

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

Tables:

User (user_id, username, password, role)
Product (product_id, product_name, price)
Orders (order_id, user_id, product_id, datetime)


"""

import mysql.connector
from mysql.connector import Error
import logging
import bcrypt


logging.basicConfig(level=logging.INFO)
cursor = None


def main():

    connection = create_connection()

    current_user_id = None
    current_user_role = None

    print("Please sign in.\n")

    username = input("Username: ")
    password = input("Password: ")
    current_user_id = login(username, password)
    current_user_role = get_role(current_user_id)
    logging.info("User has logged in (ID: " + str(current_user_id))

    if connection:
        global cursor
        cursor = connection.cursor()
    
        while True:

            prompt = "Create new user\t(1)\nPurchase product\t(2)\nView order history\t(3)\n"
            admin_prompt = "Display admin actions (0)\n"

            action = None
            if current_user_role == 'admin':
                action = input(admin_prompt + prompt)
            else:
                action = input(prompt)

            if action == '1':
                username = input("Enter new username: ")
                password = input("Set new password: ")
                create_user(username, password)
                logging.info("Account created")
                print("Your new account has been created. Please exit and log in.")

            elif action == '2':
                # show product catalog

                pass

            elif action == '3':
                get_all_orders(username, password)

            elif action == 'delete_user':
                handle_delete_user()
            elif action == '0':
                handle_login()
            elif action == 'exit':
                break
            else:
                print("Invalid action. Please try again.")
        
        cursor.close()
    connection.close()


def create_connection():
    connection = None
    try:        # TODO enter sample data into database
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
    hashed_password = hash_password(password)
    cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, hashed_password, 'user'))
    cursor.connection.commit()
    logging.info(f"User {username} created.")

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

def update_user(user_id, new_username):
    cursor.execute("UPDATE users SET username = %s WHERE user_id = %s", (new_username, user_id))
    cursor.connection.commit()
    logging.info(f"User {user_id} updated.")

# DELETE ---
# Users can delete their account
def delete_user(user_id):
    cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
    cursor.connection.commit()
    logging.info(f"User {user_id} deleted.")


def login(username, password):
    cursor.execute("SELECT * FROM users WHERE username = %s", (username))
    user = cursor.fetchone()
    user_id = user[1] 
    if user and verify_password(password, user[3]):  
        logging.info(f"{username} logged in successfully.")
    else:
        logging.warning("Invalid login attempt.")
    return user_id


def hash_password(password):
    
    salt = bcrypyt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed 


def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)


def get_role(user_id):
    cursor.execute("SELECT role FROM users WHERE user_id = %s", (user_id))
    role = cursor.fetchall()
    return role


if __name__ == "__main__":
    main()


















