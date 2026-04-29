from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

mysql = MySQL()

def register_user(name, email, password):
    cur = mysql.connection.cursor()

    # Check if email already exists
    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    existing_user = cur.fetchone()

    if existing_user:
        return {"message": "Email already registered"}, 400

    hashed_password = generate_password_hash(password)

    cur.execute(
        "INSERT INTO users(name, email, password) VALUES(%s, %s, %s)",
        (name, email, hashed_password)
    )
    mysql.connection.commit()
    cur.close()

    return {"message": "User registered successfully"}, 201


def login_user(email, password):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cur.fetchone()
    cur.close()

    if user:
        stored_password = user[3]

        if check_password_hash(stored_password, password):
            return {
                "message": "Login successful",
                "user": {
                    "id": user[0],
                    "name": user[1],
                    "email": user[2]
                }
            }, 200

    return {"message": "Invalid email or password"}, 401