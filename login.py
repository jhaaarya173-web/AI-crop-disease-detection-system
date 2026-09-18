
import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib

import database
from register import Register
from detection import CropDiseaseDetection
from voice import speak


class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Crop Disease Detection System")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        self.root.config(bg="#eef5ee")

        title = tk.Label(
            self.root,
            text="🌿 CROP DISEASE DETECTION SYSTEM",
            font=("Segoe UI", 20, "bold"),
            bg="#2e7d32",
            fg="white"
        )
        title.pack(fill=tk.X)

        frame = tk.Frame(
            self.root,
            bg="white",
            bd=0,
            highlightbackground="#c8e6c9",
            highlightthickness=2
        )
        frame.place(x=150, y=120, width=400, height=280)

        tk.Label(
            frame,
            text="Email",
            font=("Segoe UI", 12, "bold"),
            bg="white"
        ).place(x=30, y=30)

        self.email = tk.Entry(
            frame,
            font=("Segoe UI", 12),
            width=28
        )
        self.email.place(x=140, y=30)

        tk.Label(
            frame,
            text="Password",
            font=("Segoe UI", 12, "bold"),
            bg="white"
        ).place(x=30, y=90)

        self.password = tk.Entry(
            frame,
            font=("Segoe UI", 12),
            width=28,
            show="*"
        )
        self.password.place(x=140, y=90)

        tk.Button(
            frame,
            text="LOGIN",
            font=("Segoe UI", 13, "bold"),
            bg="#1565c0",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.login_user
        ).place(x=140, y=150, width=150, height=40)

        tk.Button(
            frame,
            text="Create New Account",
            font=("Segoe UI", 10, "bold"),
            bg="#2e7d32",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.open_register
        ).place(x=120, y=205, width=190, height=35)

        # Voice Welcome
        self.root.after(
            1000,
            lambda: speak("Welcome to Crop Disease Detection System. Please login.")
        )

    def login_user(self):
        email = self.email.get().strip()
        password = self.password.get().strip()

        if email == "":
            messagebox.showerror("Error", "Email Required")
            speak("Please enter your email.")
            return

        if password == "":
            messagebox.showerror("Error", "Password Required")
            speak("Please enter your password.")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            conn = sqlite3.connect("crop_disease.db")
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM users WHERE email=? AND password=?",
                (email, hashed_password)
            )

            row = cursor.fetchone()
            conn.close()

            if row:
                messagebox.showinfo("Success", f"Welcome {row[1]}!")
                speak(f"Login successful. Welcome {row[1]}.")
                self.open_dashboard()
            else:
                messagebox.showerror("Error", "Invalid Email or Password")
                speak("Invalid email or password. Please try again.")

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            speak("Database error occurred.")

    def open_register(self):
        speak("Opening registration page.")

        self.root.withdraw()

        reg_window = tk.Toplevel(self.root)

        Register(
            reg_window,
            on_back=lambda: self.restore_window(reg_window)
        )

        reg_window.protocol(
            "WM_DELETE_WINDOW",
            lambda: self.restore_window(reg_window)
        )

    def open_dashboard(self):
        speak("Opening dashboard.")

        self.root.withdraw()

        dash_window = tk.Toplevel(self.root)

        CropDiseaseDetection(
            dash_window,
            on_logout=lambda: self.restore_window(dash_window)
        )

        dash_window.protocol(
            "WM_DELETE_WINDOW",
            lambda: self.restore_window(dash_window)
        )

    def restore_window(self, child_window):
        child_window.destroy()
        self.root.deiconify()
        speak("Returned to login page.")


if __name__ == "__main__":
    root = tk.Tk()
    Login(root)
    root.mainloop()