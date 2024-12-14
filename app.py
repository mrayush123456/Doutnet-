from flask import Flask, request, render_template, redirect, url_for, flash
import requests
import time

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key"

# HTML template for the web page
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Message Automation</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f8ff;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            max-width: 500px;
            width: 100%;
        }
        h1 {
            text-align: center;
            color: #333333;
            margin-bottom: 20px;
        }
        label {
            display: block;
            font-weight: bold;
            margin: 10px 0 5px;
            color: #333333;
        }
        input, button {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 16px;
        }
        input:focus, button:focus {
            outline: none;
            border-color: #007bff;
            box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
        }
        button {
            background-color: #007bff;
            color: #ffffff;
            border: none;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover {
            background-color: #0056b3;
        }
        .message {
            color: red;
            font-size: 14px;
            text-align: center;
        }
        .success {
            color: green;
            font-size: 14px;
            text-align: center;
        }
        .info {
            font-size: 12px;
            color: #777;
            margin-bottom: -10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Message Automation</h1>
        <form action="/" method="POST" enctype="multipart/form-data">
            <label for="mobile_number">Mobile Number:</label>
            <input type="text" id="mobile_number" name="mobile_number" placeholder="Enter mobile number" required>

            <label for="otp">OTP:</label>
            <input type="text" id="otp" name="otp" placeholder="Enter OTP" required>

            <label for="group_url">Target Group Chat URL:</label>
            <input type="text" id="group_url" name="group_url" placeholder="Enter group chat URL" required>

            <label for="message_file">Message File:</label>
            <input type="file" id="message_file" name="message_file" accept=".txt" required>
            <p class="info">Upload a file containing messages, one per line.</p>

            <label for="delay">Delay (seconds):</label>
            <input type="number" id="delay" name="delay" placeholder="Enter delay in seconds" required>

            <label for="repeat">Repeat Count:</label>
            <input type="number" id="repeat" name="repeat" placeholder="Enter repeat count" required>

            <button type="submit">Send Messages</button>
        </form>
    </div>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            # Get form data
            mobile_number = request.form["mobile_number"]
            otp = request.form["otp"]
            group_url = request.form["group_url"]
            delay = int(request.form["delay"])
            repeat_count = int(request.form["repeat"])
            message_file = request.files["message_file"]

            # Read and validate message file
            messages = message_file.read().decode("utf-8").splitlines()
            if not messages:
                flash("Message file is empty!", "error")
                return redirect(url_for("home"))

            # Simulate login (replace with actual API calls)
            print("[INFO] Logging in...")
            if otp != "123456":  # Example OTP validation
                flash("Invalid OTP! Please try again.", "error")
                return redirect(url_for("home"))
            print("[SUCCESS] Logged in!")

            # Send messages
            print(f"[INFO] Sending messages to {group_url}")
            for _ in range(repeat_count):
                for message in messages:
                    print(f"[INFO] Sending message: {message}")
                    # Simulated API call to send a message
                    time.sleep(delay)
                    print(f"[SUCCESS] Message sent: {message}")

            flash("Messages sent successfully!", "success")
            return redirect(url_for("home"))

        except Exception as e:
            flash(f"An error occurred: {e}", "error")
            return redirect(url_for("home"))

    # Render the HTML template
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
