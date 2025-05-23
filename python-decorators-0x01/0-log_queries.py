#Logging database Queries
#To Log SQL querries before they are executed

import sqlite3
import functools

#Decorator to Log SQL queries before execution
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") or (args[0] if args else None)
        if query:
            print(f"[LOG] Executing SQL query: {query}")
        result = func(*args, **kwargs)
        print("[LOG] Query execution complete")
        return result
    return wrapper

# Function to fetch users, now wrapped in our logging decorator
@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Run test
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
