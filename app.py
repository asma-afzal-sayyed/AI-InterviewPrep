import os

import pymysql

from dotenv import load_dotenv
from flask import Flask, render_template, request, session, redirect

from resume_ai.resume_parser import analyze_resume
from chatbot.chatbot import chatbot_response
from ai_helper import generate_ai_response

# Load environment variables from .env
load_dotenv()


# Initialize Flask
app = Flask(__name__)


# Secure Flask Secret Key
app.secret_key = os.getenv("FLASK_SECRET_KEY")

if not app.secret_key:
    raise ValueError("FLASK_SECRET_KEY is missing in .env file")


# MySQL Connection
connection = pymysql.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", ""),
    database=os.getenv("DB_NAME", "interviewprep"),
    port=int(os.getenv("DB_PORT", "3306")),
)

print("Database Connected Successfully!")


# Home Page
@app.route("/")
def home():

    username = session.get("user")

    return render_template("index.html", username=username)


# Python Notes Page
@app.route("/python")
def python_notes():

    return render_template("python_notes.html")


# SQL Notes Page
@app.route("/sql")
def sql_notes():

    return render_template("sql_notes.html")


# Aptitude Page
@app.route("/aptitude")
def aptitude():

    return render_template("aptitude_shortcuts.html")


# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        cursor = connection.cursor()

        query = """
        SELECT * FROM users
        WHERE email=%s AND password=%s
        """

        cursor.execute(query, (email, password))

        user = cursor.fetchone()

        cursor.close()

        if user:

            session["user"] = user[1]

            return redirect("/")

        else:

            return """
            ❌ Invalid Email or Password
            """

    return render_template("login.html")


# Resume Analyzer
@app.route("/resume", methods=["GET", "POST"])
def resume():

    skills = ""

    if request.method == "POST":

        file = request.files["resume"]

        if file and file.filename:

            filepath = os.path.join("uploads", file.filename)

            os.makedirs("uploads", exist_ok=True)

            file.save(filepath)

            skills = analyze_resume(filepath)

    return render_template("resume_upload.html", skills=skills)


# Aptitude Quiz
@app.route("/quiz")
def quiz():

    return render_template("aptitude_quiz.html")


# SQL Quiz
@app.route("/sqlquiz")
def sqlquiz():

    return render_template("sql_quiz.html")


# Signup Page
@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        cursor = connection.cursor()

        query = """
        INSERT INTO users(name, email, password)
        VALUES(%s, %s, %s)
        """

        cursor.execute(query, (name, email, password))

        connection.commit()

        cursor.close()

        return """
        ✅ User Registered Successfully
        """

    return render_template("signup.html")


# Logout
@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/")


# Save Score
@app.route("/save_score")
def save_score():

    username = session.get("user")

    if not username:
        return redirect("/login")

    score = 10

    cursor = connection.cursor()

    query = """
    INSERT INTO leaderboard(username, score)
    VALUES(%s, %s)
    """

    cursor.execute(query, (username, score))

    connection.commit()

    cursor.close()

    return """
    🏆 Score Saved Successfully
    """


# Leaderboard
@app.route("/leaderboard")
def leaderboard():

    cursor = connection.cursor()

    query = """
    SELECT * FROM leaderboard
    ORDER BY score DESC
    """

    cursor.execute(query)

    data = cursor.fetchall()

    cursor.close()

    return render_template("leaderboard.html", data=data)


# AI Chatbot
@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():

    response = ""

    if request.method == "POST":

        user_message = request.form["message"]

        response = chatbot_response(user_message)

    return render_template("chatbot.html", response=response)


# AI Code Checker
@app.route("/codechecker", methods=["GET", "POST"])
def codechecker():

    result = ""
    code = ""

    if request.method == "POST":

        code = request.form.get("code", "").strip()

        if not code:
            result = "Please enter your Python code before clicking Check Code."

        else:
            prompt = f"""
You are a professional AI Python programming teacher and code reviewer.

Analyze the user's Python code carefully.

Give your response in the following sections:

1. CODE STATUS
- Clearly tell whether the code is correct, has errors, or is incomplete.

2. ERRORS FOUND
- List all errors in simple beginner-friendly language.
- If there are no errors, write "No errors found."

3. WHY THE ERROR OCCURS
- Explain why each error happens.

4. HOW TO FIX IT
- Give clear step-by-step solutions.

5. COMPLETE CORRECTED CODE
- Provide the entire corrected Python code in one Python code block.
- Never provide only a small changed portion.
- Preserve the original purpose and functionality.
- If the original code is correct, return the complete original code.

6. SAMPLE INPUT
- Give sample input if the program requires user input.
- If no input is required, write "No input required."

7. EXPECTED OUTPUT
- Show the expected output for the sample input.
- Explain the output in simple language.
- If the output depends on external files, database, API, or environment,
  clearly mention that it cannot be determined exactly without running it.

8. IMPROVEMENTS
- Suggest useful improvements for a beginner.

9. HOW TO RUN
- Explain how to run the corrected Python code.

IMPORTANT:
- Use clear headings and bullet points.
- Explain like a friendly teacher.
- Do not invent actual execution results.
- Do not claim that code was executed.
- Always provide the complete corrected code.

USER CODE:
{code}
"""

            try:
                result = generate_ai_response(prompt)

                if not result:
                    result = (
                        "Sorry! AI could not generate a response. Please try again."
                    )

            except Exception as e:
                result = f"Sorry! An error occurred while checking your code: {str(e)}"

    return render_template("code_checker.html", result=result, code=code)


# AI Question Generator
@app.route("/generate", methods=["GET", "POST"])
def generate():

    questions = ""

    if request.method == "POST":

        topic = request.form["topic"]

        prompt = f"""
        Generate 10 interview questions on:
        {topic}

        Rules:
        - Only questions
        - No answers
        - Number properly
        - Keep questions short
        - Professional interview style
        """

        questions = generate_ai_response(prompt)

    return render_template("question_generator.html", questions=questions)


# Run Flask App
if __name__ == "__main__":

    app.run(debug=False)
