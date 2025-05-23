# ✅ Task 2: Concurrent Asynchronous Database Queries using aiosqlite

import asyncio
import aiosqlite

DB_NAME = "users.db"

# 🚀 Fetch all users
async def async_fetch_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()

# 🚀 Fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            return await cursor.fetchall()

# 👯 Run both concurrently
async def fetch_concurrently():
    users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("All Users:", users)
    print("Users Older than 40:", older_users)

# 🚀 Run the concurrent tasks
if __name__ == '__main__':
    asyncio.run(fetch_concurrently())
