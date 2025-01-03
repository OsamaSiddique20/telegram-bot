def get_subscribe(chat_id, name):
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

        # Check if the user is already subscribed
        query = "SELECT * FROM user WHERE chat_id = %s AND name = %s"
        data = (chat_id, name)
        cursor.execute(query, data)

        # Fetch all rows returned by the query
        rows = cursor.fetchall()

        if rows:
            # Close the cursor and connection
            cursor.close()
            conn.close()
            # If the user is already subscribed, return a message indicating they are already subscribed
            return f"Hey {name}! You're already subscribed to prayer notifications."

        else:
            # SQL query to insert data into the table
            query = "INSERT INTO user (chat_id, name) VALUES (%s, %s)"
            data = (chat_id, name)

            # Execute the SQL query
            cursor.execute(query, data)

            # Commit the transaction
            conn.commit()

            # Close the cursor and connection
            cursor.close()
            conn.close()

            # Construct a human-friendly success message
            return f"Hey {name}! You're all set now. You've successfully subscribed to receive prayer notifications. You'll start receiving them shortly!"

    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return "Oops! Something went wrong while subscribing. Please try again later."

    except Exception as e:
        print("Error:", e)
        return "Oops! An unexpected error occurred. Please try again later."
