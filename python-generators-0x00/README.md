# 🌀 Python Generators - Project Walkthrough

This module demonstrates the advanced use of **Python generators** to stream, process, and aggregate data efficiently using MySQL.

---

## ✅ Task Overview

### Task 0: `seed.py`
**Goal:** Setup MySQL database and populate data.
- Connects to local MySQL instance
- Creates database `ALX_prodev` if not present
- Creates `user_data` table with UUID, name, email, age
- Loads data from `user_data.csv`
- Called from `0-main.py`

### Task 1: `0-stream_users.py`
**Goal:** Yield one user at a time from the DB.
- Implements generator `stream_users()`
- Connects to DB, uses `cursor(dictionary=True)`
- Efficiently yields user rows line-by-line

### Task 2: `1-batch_processing.py`
**Goal:** Process users in batches.
- `stream_users_in_batches(batch_size)` yields chunks of rows
- `batch_processing(batch_size)` filters age > 25 from each batch
- Useful when working with very large datasets

### Task 3: `2-lazy_paginate.py`
**Goal:** Paginate user data lazily.
- `paginate_users()` fetches 1 page at offset
- `lazy_pagination(page_size)` yields pages using generator
- Mimics lazy loading of user pages for UI or batch APIs

### Task 4: `4-stream_ages.py`
**Goal:** Memory-efficient average calculation.
- `stream_user_ages()` yields only the `age` field row-by-row
- `average_user_age()` computes the mean without loading all rows
- Avoids using `SQL AVG()` for demonstration purposes

---

## 🛠️ Setup & Run (for VSCode)

### 1. Install dependencies
```bash
pip install mysql-connector-python
```

### 2. Seed the database
```bash
python3 0-main.py
```

### 3. Run any task script
```bash
python3 1-main.py              # Task 1
python3 2-main.py | head -n 5  # Task 2 (batched filter)
python3 3-main.py | head -n 5  # Task 3 (pagination)
python3 4-main.py              # Task 4 (average age)
```

---

## 🧠 Learning Goals

- Understand and implement generators
- Use `yield` for memory-efficient iteration
- Handle real DB data in Python lazily
- Apply batch and paginated logic
- Calculate aggregates without SQL

---

> 🚀 Generators = efficiency + simplicity in data-intensive applications!
