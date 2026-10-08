from flask import Flask, render_template_string, request

app = Flask(__name__)

BASE = """
<!doctype html>
<html>
<head><title>College Fee Portal - Demo Lab</title></head>
<body style="font-family:Arial;max-width:900px;margin:40px auto">
<h1>College Fee Portal</h1>
<p>This is a deliberately simple LOCAL training target for CyberRecon.</p>
<nav>
<a href="/">Home</a> |
<a href="/login">Login</a> |
<a href="/fees">Fees</a> |
<a href="/receipt">Receipt</a> |
<a href="/help">Help</a>
</nav>
<hr>
%s
</body></html>
"""

@app.route("/")
def home():
    return BASE % "<h2>Welcome Student</h2><p>Fee payment and student services.</p>"

@app.route("/login")
def login():
    return BASE % """
    <h2>Student Login</h2>
    <form method="GET" action="/login-check">
      <input name="student_id" placeholder="Student ID"><br><br>
      <input type="password" name="password" placeholder="Password"><br><br>
      <button>Login</button>
    </form>
    """

@app.route("/login-check")
def login_check():
    return BASE % "<h2>Demo Login</h2><p>Training-only response.</p>"

@app.route("/fees")
def fees():
    return BASE % """
    <h2>Semester Fee</h2>
    <p>Amount: ₹25,000</p>
    <form method="POST" action="/pay">
      <input name="student_id" placeholder="Student ID">
      <button>Confirm Payment</button>
    </form>
    """

@app.route("/pay", methods=["POST"])
def pay():
    return BASE % "<h2>Payment Recorded (Demo)</h2><p>No real transaction occurs.</p>"

@app.route("/receipt")
def receipt():
    return BASE % "<h2>Receipt</h2><p>Receipt ID: DEMO-2026-001</p>"

@app.route("/help")
def help_page():
    return BASE % "<h2>Help</h2><p>Contact the college office for assistance.</p>"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
