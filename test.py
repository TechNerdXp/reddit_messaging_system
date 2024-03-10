import sqlite3

def delete_all_records():
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    # Execute the SQL statement to delete all records
    c.execute("DELETE FROM user_subreddits")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Call the function
delete_all_records()
