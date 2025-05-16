from seed import connect_to_prodev

def stream_user_ages():
    connection = connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    for (age,) in cursor:
        yield float(age)
    cursor.close()
    connection.close()

def average_user_age():
    count = 0
    total = 0.0
    for age in stream_user_ages():
        total += age
        count += 1
    if count:
        print(f"Average age of users: {total / count:.2f}")
    else:
        print("No users found.")
