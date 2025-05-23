# 🧠 Python Context Managers and Asynchronous Database Operations

This mini project focuses on mastering **Context Managers** and **Asynchronous Programming** in Python to manage database connections efficiently and run concurrent queries.

---

## ✅ Task 0: Custom Class-Based Context Manager
**File:** `0-databaseconnection.py`
- **Class:** `DatabaseConnection`
- **Goal:** Automatically open and close a SQLite database connection.
- **Usage:**
  ```python
  with DatabaseConnection("users.db") as conn:
      # use conn safely
  ```
- **Why:** Ensures database connections are always closed, avoiding leaks.

---

## ✅ Task 1: Reusable Query Context Manager
**File:** `0-databaseconnection.py`
- **Class:** `ExecuteQuery`
- **Goal:** Execute a query and automatically return the result while managing connection.
- **Usage:**
  ```python
  with ExecuteQuery("users.db", "SELECT * FROM users WHERE age > ?", (25,)) as results:
      print(results)
  ```
- **Why:** Cleanly wraps connection + cursor + fetch in one safe reusable pattern.

---

## ✅ Task 2: Concurrent Async Queries with `aiosqlite`
**File:** `3-concurrent.py`
- **Goal:** Fetch data concurrently from the same database.
- **Key Functions:**
  - `async_fetch_users()`
  - `async_fetch_older_users()`
  - `fetch_concurrently()` runs both using `asyncio.gather()`
- **Why:** Great for scaling performance where multiple I/O operations are needed.

---

## 🔧 Dependencies
- `sqlite3` (standard library)
- `aiosqlite` (install via `pip install aiosqlite`)

---

## 🗂 Directory Structure
```
python-context-async-perations-0x02/
├── 0-databaseconnection.py
├── 3-concurrent.py
└── README.md
```

---

