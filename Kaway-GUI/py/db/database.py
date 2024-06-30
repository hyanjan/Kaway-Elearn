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

def putChosenLesson(lesson):
    conn = sqlite3.connect('Kaway-GUI\\py\\db\\users.db')
    c = conn.cursor()

    # Update the chosen_lesson column with the value of lesson for the specific rowid
    c.execute("UPDATE users SET chosen_lesson = ?", (lesson,))

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

def getChosenLesson():
    conn = sqlite3.connect('Kaway-GUI\\py\\db\\users.db')
    c = conn.cursor()

    c.execute("SELECT chosen_lesson from users")
    value = c.fetchone()[0]

    conn.commit()
    conn.close()
    return value

def updateLatest():
    conn = sqlite3.connect('Kaway-GUI\\py\\db\\users.db')
    c = conn.cursor()

    c.execute("SELECT latest_lesson from users")
    value = c.fetchone()[0]

    new_value = value + 1

    c.execute("UPDATE users SET latest_lesson = ?", (new_value,))


    conn.commit()
    conn.close()
    return new_value

def setCam(cam):
    conn = sqlite3.connect('Kaway-GUI\\py\\db\\users.db')
    c = conn.cursor()

    c.execute("SELECT camera from users")
    value = c.fetchone()[0]

    new_value = cam

    c.execute("UPDATE users SET camera = ?", (new_value,))


    conn.commit()
    conn.close()
    return new_value

def getCam(column_name, rowid):
    conn = sqlite3.connect('Kaway-GUI\\py\\db\\users.db')
    c = conn.cursor()

    c.execute(f"SELECT {column_name} FROM users WHERE rowid=?", (rowid,))
    value = c.fetchone()[0]

    conn.commit()
    conn.close()
    return value


def setValue():
    conn = sqlite3.connect('Kaway-GUI\\py\\db\\users.db')
    c = conn.cursor()

    c.execute("SELECT trigger from users")
    result = c.fetchone()
    if result is not None and result[0] == 'True':
        new_value = 'False'
        c.execute("UPDATE users SET trigger = ?", (new_value,))
    elif result is not None and result[0] == 'False':
        new_value = 'True'
        c.execute("UPDATE users SET trigger = ?", (new_value,))
    else:
        new_value = 'True'
        c.execute("UPDATE users SET trigger = ?", (new_value,))

    conn.commit()
    conn.close()
    return new_value

def updateNotif(lesson):
    conn = sqlite3.connect('Kaway-GUI\\py\\db\\users.db')
    c = conn.cursor()

    c.execute("SELECT notif from users")
    value = c.fetchone()[0]

    c.execute("UPDATE users SET notif = ?", (lesson,))


    conn.commit()
    conn.close()
    return lesson

def getVolume():
    conn = sqlite3.connect('Kaway-GUI\\py\\db\\users.db')
    c = conn.cursor()

    c.execute(f"SELECT volume FROM users WHERE rowid=1")
    value = c.fetchone()[0]

    conn.commit()
    conn.close()
    return value

def setVolume(volume):
    conn = sqlite3.connect('Kaway-GUI\\py\\db\\users.db')
    c = conn.cursor()

    c.execute("UPDATE users SET volume = ?", (volume,))


    conn.commit()
    conn.close()
