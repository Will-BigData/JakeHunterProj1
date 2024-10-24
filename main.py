

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

    current_user_id = None
    current_user_role = None
    
    username = input("\nUsername: ")
    password = input("Password: ")
    current_user_id = login(username, password)

    if current_user_id is not None:
        current_user_role = get_role(current_user_id)[0]
        logging.info(f"User has logged in (ID: {current_user_id})")

        if connection:
            while True:

                prompt = "\nCreate new user\t\t(1)\nPurchase product\t(2)\nView order history\t(3)\nExit\t\t\t(4)\n"
                admin_prompt = "\nDisplay admin actions\t(0)"
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
                    product_id = input("Enter product ID to purchase, or type 'exit': ")
                    if product_id.lower() != 'exit':
                        purchase_product(current_user_id, product_id)

                elif action == '3':
                    orders = get_orders(current_user_id)
                    display_orders(orders)

                elif action == '0' and current_user_role == 'admin':
                    
                    while True:
                        action = input("\nBack to home\t\t(0)\nDisplay all users\t(1)\nDisplay all orders\t(2)\nGrant admin privileges\t(3)\nRevoke admin privileges\t(4)\nChange username\t\t(5)\nRemove user\t\t(6)\n")
                        
                        if action == '0':
                            break  # Return to the main menu

                        elif action == '1':
                            print("\n")
                            users = get_all_users()
                            for user in users:
                                print(user)

                        elif action == '2':
                            orders = get_all_orders()
                            display_orders(orders)

                        elif action == '3':
                            id = input("\nEnter a user ID to grant administrator privileges: \n")
                            if promote_user(id):
                                logging.info("User " + str(id) + " promoted to admin role")

                        elif action == '4':
                            id = input("\nEnter a user ID to revoke administrator privileges: \n")
                            if demote_user(id):
                                logging.info("User " + str(id) + " demoted to user role")

                        elif action == '5':
                            id = input("User to edit (ID): ")
                            new_username = input("New username: ")
                            if update_user(id, new_username):
                                logging.info("User " + str(id) + " assigned new username")
                            
                        elif action == '6':
                            id = input("User to remove (ID): ")
                            if remove_user(id):
                                logging.info("User " + str(id) + " has been removed")

                        else:
                            print("\nInvalid option. Please try again.")

                elif action == '4':
                    break
            
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
    cursor.execute("SELECT * FROM Orders")
    return cursor.fetchall()

# Users can view their order history
def get_orders(user_id):
    cursor.execute("SELECT * FROM Orders WHERE user_id = %s", (user_id,))
    return cursor.fetchall()

# UPDATE ---
# Users can purchase products
def purchase_product(user_id, product_id):
    cursor.execute("INSERT INTO Orders (user_id, product_id, datetime) VALUES (%s, %s, NOW())", (user_id, product_id))
    cursor._connection.commit()
    logging.info(f"User {user_id} purchased product {product_id}.")

def update_user(user_id, new_username):
    
    cursor.execute("UPDATE USER SET username = %s WHERE user_id = %s", (new_username, user_id))
    if cursor.rowcount > 0:
            logging.info("User update successful")
            cursor._connection.commit()
            return True
    else:
        logging.info("User update failed")
    return False

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
        hashed_password = user[2]  # password is the third column

        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')
        
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
    cursor.execute("SELECT role FROM USER WHERE user_id = %s", (user_id,))
    role = cursor.fetchone()
    return role


def display_products():
    cursor.execute("SELECT * FROM Product")
    products = cursor.fetchall()
    print()
    for product in products:
        print(f"ID {product[0]}, Name: {product[1]}, Price: ${product[2]}")
    print()


def display_orders(orders):
    if not orders:
        print("No orders found.")
        return

    print("\nYour order history:")
    for order in orders:
        order_id = order[0]          # Order ID
        user_id = order[1]           # User ID
        product_id = order[2]        # Product ID
        order_datetime = order[3]     # Order date and time

         # Format to show date and time
        formatted_datetime = order_datetime.strftime('%Y-%m-%d %H:%M:%S')

        print(f"[Order ID: {order_id}, User ID: {user_id}, Product ID: {product_id}] @ {formatted_datetime}")
    print("\n")
    return


def promote_user(user_id):
    cursor.execute("UPDATE USER SET role = %s WHERE user_id = %s", ('admin', user_id))
    if cursor.rowcount > 0:
        logging.info("User update successful")
        cursor._connection.commit()
        return True
    else:
        logging.info("User update failed")
    return False
    
def demote_user(user_id):
    cursor.execute("UPDATE USER SET role = %s WHERE user_id = %s", ('user', user_id))
    if cursor.rowcount > 0:
        logging.info("User update successful")
        cursor._connection.commit()
        return True
    else:
        logging.info("User update failed")
    return False
    
def remove_user(user_id):
    cursor.execute("DELETE FROM USER WHERE user_id = %s", (user_id,))
    if cursor.rowcount > 0:
        logging.info("User update successful")
        cursor._connection.commit()
        return True
    else:
        logging.info("User update failed")
    return False




if __name__ == "__main__":
    main()

















