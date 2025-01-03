def get_all_chat_ids():
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

        # SQL query to retrieve all chat_ids
        query = "SELECT chat_id FROM user"

        # Execute the SQL query
        cursor.execute(query)

        # Fetch all rows returned by the query
        rows = cursor.fetchall()

        # Extract chat_ids from the rows
        chat_ids = [row[0] for row in rows]

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return chat_ids

    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return []

    except Exception as e:
        print("Error:", e)
        return []
