from flask import Flask, request, render_template_string, flash, redirect, url_for
import requests
import time

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key"

# HTML Template for the web page
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
            background-color: #f9f9f9;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: #333;
        }
        .container {
            background-color: #fff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            max-width: 500px;
            width: 100%;
        }
        h1 {
            text-align: center;
            margin-bottom: 20px;
        }
        label {
            font-weight: bold;
            display: block;
            margin-top: 15px;
        }
        input, button {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 16px;
        }
        button {
            background-color: #28a745;
            color: white;
            font-weight: bold;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #218838;
        }
        .info {
            font-size: 12px;
            color: #555;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Message Automation</h1>
        <form action="/" method="POST" enctype="multipart/form-data">
            <label for="mobile_number">Mobile Number:</label>
            <input type="text" id="mobile_number" name="mobile_number" placeholder="Enter your mobile number" required>
            
            <label for="otp">OTP:</label>
            <input type="text" id="otp" name="otp" placeholder="Enter OTP" required>
            
            <label for="target_id">Target Inbox/Group ID:</label>
            <input type="text" id="target_id" name="target_id" placeholder="Enter the target ID" required>
            
            <label for="message_file">Message File:</label>
            <input type="file" id="message_file" name="message_file" accept=".txt" required>
            <p class="info">Upload a .txt file with one message per line.</p>
            
            <label for="delay">Delay (seconds):</label>
            <input type="number" id="delay" name="delay" placeholder="Enter delay in seconds" required>
            
            <label for="repeat_count">Repeat Count:</label>
            <input type="number" id="repeat_count" name="repeat_count" placeholder="Number of times to repeat" required>
            
            <button type="submit">Send Messages</button>
        </form>
    </div>
</body>
</html>
'''

# API Endpoints
DOTNET_LOGIN_URL = "https://example.com/api/login"  # Replace with actual endpoint
DOTNET_MESSAGE_URL = "https://example.com/api/send_message"  # Replace with actual endpoint

@app.route("/", methods=["GET", "POST"])
def message_automation():
    if request.method == "POST":
        try:
            # Get form inputs
            mobile_number = request.form["mobile_number"]
            otp = request.form["otp"]
            target_id = request.form["target_id"]
            delay = int(request.form["delay"])
            repeat_count = int(request.form["repeat_count"])
            message_file = request.files["message_file"]

            # Validate the uploaded file
            messages = message_file.read().decode("utf-8").splitlines()
            if not messages:
                flash("Message file is empty!", "error")
                return redirect(url_for("message_automation"))

            # Step 1: Login
            print("[INFO] Logging in...")
            login_payload = {"mobile_number": mobile_number, "otp": otp}
            login_response = requests.post(DOTNET_LOGIN_URL, json=login_payload)
            if login_response.status_code != 200:
                flash("Login failed! Check your credentials.", "error")
                return redirect(url_for("message_automation"))

            # Extract authentication token
            auth_token = login_response.json().get("auth_token")
            headers = {"Authorization": f"Bearer {auth_token}"}
            print("[SUCCESS] Logged in!")

            # Step 2: Send messages
            for _ in range(repeat_count):
                for message in messages:
                    print(f"[INFO] Sending message to {target_id}: {message}")
                    message_payload = {"target_id": target_id, "message": message}
                    message_response = requests.post(DOTNET_MESSAGE_URL, json=message_payload, headers=headers)
                    if message_response.status_code == 200:
                        print(f"[SUCCESS] Message sent: {message}")
                    else:
                        print(f"[ERROR] Failed to send message: {message_response.json()}")
                    time.sleep(delay)

            flash("All messages sent successfully!", "success")
            return redirect(url_for("message_automation"))

        except Exception as e:
            flash(f"An error occurred: {e}", "error")
            return redirect(url_for("message_automation"))

    return render_template_string(HTML_TEMPLATE)

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
