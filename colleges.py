import sqlite3

# Function to connect to the SQLite database
def connect_to_database(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connected to SQLite database")
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

# Function to query universities based on user preferences
def query_universities(conn, location, income, gpa, major, state):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT uni_name
            FROM university
            WHERE state = ? AND tuition < ? AND uni_id IN (
                SELECT uni_id
                FROM Major
                WHERE major = ?
            )
        """, (state, income, major))
        rows = cursor.fetchall()
        if len(rows) == 0:
            print("No universities found matching your criteria.")
        else:
            print("Universities matching your criteria:")
            for row in rows:
                print(row[0])
    except sqlite3.Error as e:
        print(e)

# Main function to ask user questions and call the query function
def main():
    database = "university.db"
    conn = connect_to_database(database)
    if conn is not None:
        location = input("Where do you live? ")
        income = float(input("What is your household income? "))
        gpa = float(input("What is your GPA? "))
        major = input("What major are you interested in? ")
        state = input("Are you in-state or out-of-state? ")

        query_universities(conn, location, income, gpa, major, state)
        conn.close()
    else:
        print("Error: Could not connect to database.")

if __name__ == '__main__':
    main()

