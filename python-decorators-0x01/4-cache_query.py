# ✅ Task 4: Cache Database Queries
# Goal: Avoid redundant DB reads by caching query results

import sqlite3
import functools

# Using connection handler from Task 1

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# In-memory cache dictionary
query_cache = {}

# Cache results based on query string only

def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = kwargs.get('query') or (args[0] if args else None)
        if query in query_cache:
            print("[CACHE] Returning cached result for query")
            return query_cache[query]
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

# Query with caching
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
if __name__ == '__main__':
    query = "SELECT * FROM users"
    users = fetch_users_with_cache(query=query)
    print(users)

    users_again = fetch_users_with_cache(query=query)
    print(users_again)