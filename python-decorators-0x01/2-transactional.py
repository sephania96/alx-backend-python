# Transaction Management Decorator
# Automatically commit or rollback database changes

import sqlite3
import functools

# the decorator from Task 1

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# 🔧 Decorator to commit on success, rollback on failure

def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            print(f"[ERROR] Transaction rolled back due to: {e}")
            raise
    return wrapper

# 🧪 Function to update user email, wrapped in both decorators

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# Run test
if __name__ == '__main__':
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
    print("[INFO] Email update attempted.")
