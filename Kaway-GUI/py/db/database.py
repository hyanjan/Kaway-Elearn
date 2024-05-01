import sqlite3

def loadUser():
    conn = sqlite3.connect('Kaway-GUI\\py\\db\\users.db')
    c = conn.cursor()
    
    # Execute the query to fetch a single username
    c.execute("SELECT username FROM users LIMIT 1")
    
    # Fetch the username
    row = c.fetchone()
    
    # Close the connection
    conn.close()

    # Check if a username was fetched
    if row:
        # Extract the username from the row and return it
        return row[0]  # Assuming username is in the first column
    else:
        # Return None if no username was found
        return None



# Call the function and print the result
print(loadUser())

def findRowIDValue(column_name, value):
    conn = sqlite3.connect('Kaway-GUI\\py\\db\\lessons.db')
    c = conn.cursor()

    # Construct the SQL query
    c.execute(f"SELECT rowid FROM lessons WHERE {column_name} = ?", (value,))
    
    # Fetch the row ID
    row_id = c.fetchone()
    
    # Close the connection
    conn.close()
    
    # Extract the integer value from the tuple
    if row_id:
        row_id = row_id[0]
        return row_id
    else:
        return None

print(findRowIDValue('right_answer', 'B'))

def getValue(column_name, rowid):
    conn = sqlite3.connect('Kaway-GUI\\py\\db\\lessons.db')
    c = conn.cursor()

    c.execute(f"SELECT {column_name} FROM lessons WHERE rowid=?", (rowid,))
    value = c.fetchone()[0]

    conn.commit()
    conn.close()
    return value
    
print(getValue('module', 1))

def putLesson(rowid, lesson):
    conn = sqlite3.connect('Kaway-GUI\\py\\db\\users.db')
    c = conn.cursor()

    c.execute()

    # Update the chosen_lesson column with the value of lesson for the specific rowid
    c.execute("UPDATE your_table_name SET chosen_lesson = ? WHERE ROWID = ?", (lesson, rowid))

    conn.commit()
    conn.close()

def getLatestLesson():
    conn = sqlite3.connect('Kaway-GUI\\py\\db\\users.db')
    c = conn.cursor()

    c.execute("SELECT latest_lesson from users")
    value = c.fetchone()[0]

    conn.commit()
    conn.close()
    return value

print(getLatestLesson())