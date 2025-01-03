def get_reminders():
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

        # SQL query to retrieve phoneno, description, and datetime from the reminder table
        query = "SELECT phoneno, description, datetime FROM reminder"

        # Execute the SQL query
        cursor.execute(query)

        # Fetch all rows returned by the query
        rows = cursor.fetchall()

        # Create a list of dictionaries, each containing phoneno, description, and datetime
        reminders = [{'phoneno': row[0], 'description': row[1], 'datetime': row[2]} for row in rows]
       
        # Close the cursor and connection
        cursor.close()
        conn.close()

        return reminders

    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return []

    except Exception as e:
        print("Error:", e)
        return []


get_reminders()