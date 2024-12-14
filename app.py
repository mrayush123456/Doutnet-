from flask import Flask, request, render_template, flash, redirect
import requests
import time

app = Flask(__name__)
app.secret_key = "your_secret_key"

BASE_URL = "https://dotnetapp.com/api"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        mobile_number = request.form["mobile_number"]
        otp = request.form["otp"]
        group_id = request.form["group_id"]
        delay = int(request.form["delay"])
        message_file = request.files["message_file"]

        # Read messages from file
        messages = message_file.read().decode("utf-8").splitlines()
        if not messages:
            flash("Message file is empty!", "error")
            return redirect("/")

        # Login and get token
        login_response = requests.post(f"{BASE_URL}/auth/verify-otp", json={"mobile": mobile_number, "otp": otp})
        if login_response.status_code != 200:
            flash("Login failed! Please check your OTP.", "error")
            return redirect("/")

        token = login_response.json().get("token")

        # Send messages
        headers = {"Authorization": f"Bearer {token}"}
        for message in messages:
            response = requests.post(f"{BASE_URL}/group/{group_id}/send-message", json={"message": message}, headers=headers)
            if response.status_code == 200:
                print(f"Message sent: {message}")
            else:
                print(f"Failed to send message: {response.json()}")
            time.sleep(delay)

        flash("Messages sent successfully!", "success")
        return redirect("/")

    return '''
    <form method="POST" enctype="multipart/form-data">
        Mobile Number: <input type="text" name="mobile_number" required><br>
        OTP: <input type="text" name="otp" required><br>
        Group Chat ID: <input type="text" name="group_id" required><br>
        Delay (seconds): <input type="number" name="delay" required><br>
        Message File: <input type="file" name="message_file" required><br>
        <button type="submit">Send Messages</button>
    </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)
