# Critical security vulnerabilities

# Using pickle with untrusted data
import pickle
def unsafe_unpickle(data):
    return pickle.loads(data)

# Hardcoded AWS credentials
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# SQL Injection
def sql_injection(username):
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    return query

# Command injection
import subprocess
def command_injection(filename):
    subprocess.call("cat " + filename, shell=True)

# Using MD5 for passwords
import hashlib
def weak_hash(password):
    return hashlib.md5(password.encode()).hexdigest()
