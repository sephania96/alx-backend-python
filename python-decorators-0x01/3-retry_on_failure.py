# ✅ Task 3: Retry on Failure Decorator
# Goal: Automatically retry DB operations on failure

import time
import sqlite3
import functools

# Reusing connection decorator from Task 1

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# Retry decorator with exponential backoff

def retry_on_failure(retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"[RETRY {attempt + 1}] Error: {e}")
                    last_error = e
                    time.sleep(delay)
            print("[FAILURE] All retries failed.")
            raise last_error
        return wrapper
    return decorator

# 🧪 Function that will retry on failure

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure
if __name__ == '__main__':
    users = fetch_users_with_retry()
    print(users)