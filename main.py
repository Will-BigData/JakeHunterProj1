

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
    if connection:
        global cursor
        cursor = connection.cursor()
        #create_user('Jake2024', 'pass')

    current_user_id = None
    current_user_role = None

    print("Please sign in.\n")
    

    username = input("Username: ")
    password = input("Password: ")
    current_user_id = login(username, password)

    if current_user_id is not None:
        current_user_role = get_role(current_user_id)
        logging.info(f"User has logged in (ID: {current_user_id})")

        logging.info("User has logged in (ID: " + str(current_user_id))

        if connection:
            while True:

                prompt = "\nCreate new user\t(1)\nPurchase product\t(2)\nView order history\t(3)\n"
                admin_prompt = "Display admin actions\t(0)"
                action = input(admin_prompt + prompt if current_user_role == 'admin' else prompt)

                if action == '1':
                    username = input("Enter new username: ")
                    password = input("Set new password: ")
                    create_user(username, password)
                    logging.info("Account created")
                    print("Your new account has been created. Please exit and log in.")

                elif action == '2':
                    # show product catalog
                    display_products()
                    product_id = input("Enter product ID to purchase: ")
                    purchase_product(current_user_id, product_id)

                elif action == '3':
                    orders = get_orders(current_user_id)
                    print("Your order history:", orders)

                elif action == '0' and current_user_role == 'admin':
                    # TODO admin menu
                    users = get_all_users()
                    print("All users:", users)
                    orders = get_all_orders()
                    print("All orders:", orders)
                elif action == 'exit':
                    break
                else:
                    print("Invalid action. Please try again.")
            
        cursor.close()
        connection.close()
    else:
        print("Login failed.")


def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect (
            
            host='localhost',  
            user='root',
            password='Password@123',
            database='proj1' 
        )
        logging.info("Database connection successful")
        cursor = connection.cursor()
    except Error as e:
        logging.error(f"Error: {e}")
    return connection



# CREATE ---
# Users can create accounts
def create_user(username, password):
    hashed_password = hash_password(password)
    cursor.execute("INSERT INTO USER (username, password, role) VALUES (%s, %s, %s)", (username, hashed_password, 'user'))
    cursor._connection.commit()
    logging.info(f"User {username} created.")

# READ ---
# Admins can view all users
def get_all_users():
    cursor.execute("SELECT * FROM USER")
    return cursor.fetchall()

# Admins can view all orders
def get_all_orders():
    cursor.execute("SELECT * FROM orders")
    return cursor.fetchall()

# Users can view their order history
def get_orders(user_id):
    cursor.execute("SELECT * FROM orders WHERE user_id = %s", user_id)
    return cursor.fetchall()

# UPDATE ---
# Users can purchase products
def purchase_product(user_id, product_id):
    cursor.execute("INSERT INTO orders (user_id, product_id, datetime) VALUES (%s, %s, NOW())", (user_id, product_id))
    cursor.connection.commit()
    logging.info(f"User {user_id} purchased product {product_id}.")

def update_user(user_id, new_username):
    cursor.execute("UPDATE USER SET username = %s WHERE user_id = %s", (new_username, user_id))
    cursor.connection.commit()
    logging.info(f"User {user_id} updated.")

# DELETE ---
# Users can delete their account
def delete_user(user_id):
    cursor.execute("DELETE FROM USER WHERE user_id = %s", (user_id,))
    cursor.connection.commit()
    logging.info(f"User {user_id} deleted.")


def login(username, password):
    cursor.execute("SELECT * FROM USER WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user:
        user_id = user[0]  # user_id is the first column
        hashed_password = user[1]  # password is the second column
        
        if verify_password(password, hashed_password): # TODO fix this
            logging.info(f"{username} logged in successfully.")
            return user_id
    else:
        logging.warning("Invalid login attempt.")
        return None



def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


def verify_password(password, hashed):
    result = bcrypt.checkpw(password.encode('utf-8'), hashed)
    return result


def get_role(user_id):
    cursor.execute("SELECT role FROM users WHERE user_id = %s", (user_id,))
    role = cursor.fetchone()
    return role

def display_products():
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    for product in products:
        print(f"ID: {product[0]}, Name: {product[1]}, Price: {product[2]}")



if __name__ == "__main__":
    main()

















