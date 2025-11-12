# Intentional security issues for testing

# Blocker: Hardcoded credentials
PASSWORD = "admin123"
SECRET_KEY = "my-secret-key-12345"
API_TOKEN = "sk-1234567890abcdef"
DATABASE_PASSWORD = "root"

# Blocker: SQL injection vulnerability
def unsafe_query(user_input):
    query = f"SELECT * FROM users WHERE name = '{user_input}'"
    return query

# Blocker: Using eval
def dangerous_eval(code):
    return eval(code)

# Blocker: Command injection
import os
def run_command(cmd):
    os.system(cmd)
