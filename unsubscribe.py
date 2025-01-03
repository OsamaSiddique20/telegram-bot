def get_unsubscribe(chat_id, name):
    try:
        import mysql.connector

        # MySQL database configuration
        config = {
            'host': 'localhost',
            'user': 'osama',
            'password': 'some_pass',
            'database': 'bot'
        }

        # Connect to the database
        conn = mysql.connector.connect(**config)

        # Create a cursor object
        cursor = conn.cursor()

        # Check if the user is subscribed
        query = "SELECT * FROM user WHERE chat_id = %s AND name = %s"
        data = (chat_id, name)
        cursor.execute(query, data)

        # Fetch all rows returned by the query
        rows = cursor.fetchall()

        if rows:
            # Unsubscribe the user
            query = "DELETE FROM user WHERE chat_id = %s AND name = %s"
            cursor.execute(query, data)
            conn.commit()

            # Close the cursor and connection
            cursor.close()
            conn.close()

            # Construct a human-friendly success message
            return f"Hey {name}! You've successfully unsubscribed from prayer notifications."

        else:
            # Close the cursor and connection
            cursor.close()
            conn.close()

            # If the user is not subscribed, return a message indicating they are not subscribed
            return f"Hey {name}! You're not currently subscribed to prayer notifications."

    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return "Oops! Something went wrong while unsubscribing. Please try again later."

    except Exception as e:
        print("Error:", e)
        return "Oops! An unexpected error occurred. Please try again later."
