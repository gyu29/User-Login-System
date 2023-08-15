import tkinter as tk
from flask import Flask, render_template, request, redirect
import sqlite3

# Create Flask app
app = Flask(__name__)

# tkinter GUI setup
class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User Login")
        
        self.background_img = tk.PhotoImage(file="background.png")
        self.background_label = tk.Label(root, image=self.background_img)
        self.background_label.pack()

        self.uuid_label = tk.Label(root, text="Enter your UUID:")
        self.uuid_label.place(relx=0.5, rely=0.4, anchor="center")

        self.uuid_entry = tk.Entry(root)
        self.uuid_entry.place(relx=0.5, rely=0.45, anchor="center")

        self.submit_button = tk.Button(root, text="Submit", command=self.check_uuid)
        self.submit_button.place(relx=0.5, rely=0.5, anchor="center")

    def check_uuid(self):
        entered_uuid = self.uuid_entry.get()
        if self.is_valid_uuid(entered_uuid):
            self.root.destroy()  # Close tkinter window on successful login
            redirect("/dashboard")  # Redirect to dashboard route in Flask app
        else:
            self.uuid_entry.delete(0, tk.END)
            self.uuid_label.config(text="Invalid UUID. Try again.")

    def is_valid_uuid(self, uuid):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM valid_uuids WHERE uuid=?", (uuid,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return "Welcome to the dashboard!"

if __name__ == "__main__":
    root = tk.Tk()
    app_gui = LoginApp(root)
    app.run(debug=True)
