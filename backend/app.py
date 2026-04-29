from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from config import Config
from models import mysql, register_user, login_user

app = Flask(__name__)
CORS(app)

# Load DB Config
app.config.from_object(Config)

# Initialize MySQL
mysql.init_app(app)


# ---------------- HOME ---------------- #
@app.route('/')
def home():
    return "Python Flask Backend Running Successfully"


# ---------------- REGISTER API ---------------- #
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return "Register API is working. Please send POST request."

    # Accept JSON from Postman/React OR form data from browser
    if request.is_json:
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
    else:
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

    if not name or not email or not password:
        return jsonify({"message": "All fields are required"}), 400

    response, status = register_user(name, email, password)
    return jsonify(response), status


# ---------------- LOGIN API ---------------- #
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return "Login API is working. Please send POST request."

    if request.is_json:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
    else:
        email = request.form.get("email")
        password = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    response, status = login_user(email, password)
    return jsonify(response), status


# ---------------- SHOW USERS IN BROWSER ---------------- #
@app.route('/users')
def show_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, email FROM users")
    users = cur.fetchall()
    cur.close()

    html = """
    <h2>Registered Users</h2>
    <table border='1' cellpadding='10'>
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
        </tr>
    """

    for user in users:
        html += f"""
        <tr>
            <td>{user[0]}</td>
            <td>{user[1]}</td>
            <td>{user[2]}</td>
        </tr>
        """

    html += "</table>"
    return html


# ---------------- TEST REGISTER FORM IN BROWSER ---------------- #
@app.route('/test-register')
def test_register():
    return render_template_string("""
        <h2>Test Register Form</h2>
        <form action="/register" method="post">
            <input type="text" name="name" placeholder="Enter Name" required><br><br>
            <input type="email" name="email" placeholder="Enter Email" required><br><br>
            <input type="password" name="password" placeholder="Enter Password" required><br><br>
            <button type="submit">Register</button>
        </form>
    """)


# ---------------- TEST LOGIN FORM IN BROWSER ---------------- #
@app.route('/test-login')
def test_login():
    return render_template_string("""
        <h2>Test Login Form</h2>
        <form action="/login" method="post">
            <input type="email" name="email" placeholder="Enter Email" required><br><br>
            <input type="password" name="password" placeholder="Enter Password" required><br><br>
            <button type="submit">Login</button>
        </form>
    """)


if __name__ == '__main__':
    app.run(debug=True)