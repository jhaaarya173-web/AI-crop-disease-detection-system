from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import database
import hashlib


class Register:
    def __init__(self, root, on_back=None):
        self.root = root
        self.on_back = on_back
        self.root.title("Register System")
        self.root.geometry("700x600")
        self.root.config(bg="white")

        title = Label(
            self.root, text="REGISTER HERE",
            font=("Arial", 24, "bold"), bg="green", fg="white"
        )
        title.pack(fill=X)

        frame = Frame(self.root, bg="white")
        frame.place(x=100, y=80, width=500, height=480)

        Label(frame, text="First Name", font=("Arial", 12, "bold"), bg="white").place(x=20, y=20)
        self.first_name = Entry(frame, font=("Arial", 12), width=30)
        self.first_name.place(x=180, y=20)

        Label(frame, text="Last Name", font=("Arial", 12, "bold"), bg="white").place(x=20, y=70)
        self.last_name = Entry(frame, font=("Arial", 12), width=30)
        self.last_name.place(x=180, y=70)

        Label(frame, text="Email", font=("Arial", 12, "bold"), bg="white").place(x=20, y=120)
        self.email = Entry(frame, font=("Arial", 12), width=30)
        self.email.place(x=180, y=120)

        Label(frame, text="Contact", font=("Arial", 12, "bold"), bg="white").place(x=20, y=170)
        self.contact = Entry(frame, font=("Arial", 12), width=30)
        self.contact.place(x=180, y=170)

        Label(frame, text="Password", font=("Arial", 12, "bold"), bg="white").place(x=20, y=220)
        self.password = Entry(frame, font=("Arial", 12), width=30, show="*")
        self.password.place(x=180, y=220)

        Label(frame, text="Confirm Password", font=("Arial", 12, "bold"), bg="white").place(x=20, y=270)
        self.confirm_password = Entry(frame, font=("Arial", 12), width=30, show="*")
        self.confirm_password.place(x=180, y=270)

        self.check_var = IntVar()
        Checkbutton(
            frame, text="I Agree Terms & Conditions",
            variable=self.check_var, bg="white", font=("Arial", 10)
        ).place(x=20, y=330)

        Button(
            frame, text="REGISTER", font=("Arial", 14, "bold"),
            bg="green", fg="white", command=self.register_user
        ).place(x=170, y=390, width=150, height=40)

        Button(
            frame, text="⬅ Back to Login", font=("Segoe UI", 10, "bold"),
            bg="#616161", fg="white", relief=FLAT, command=self.back_to_login
        ).place(x=170, y=440, width=150, height=35)

    def register_user(self):
        first = self.first_name.get()
        last = self.last_name.get()
        email = self.email.get()
        contact = self.contact.get()
        password = self.password.get()
        confirm = self.confirm_password.get()

        if first == "":
            messagebox.showerror("Error", "First Name Required"); return
        if last == "":
            messagebox.showerror("Error", "Last Name Required"); return
        if email == "":
            messagebox.showerror("Error", "Email Required"); return
        if "@" not in email:
            messagebox.showerror("Error", "Invalid Email"); return
        if contact == "":
            messagebox.showerror("Error", "Contact Required"); return
        if len(contact) != 10:
            messagebox.showerror("Error", "Contact must be 10 digits"); return
        if password == "":
            messagebox.showerror("Error", "Password Required"); return
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters"); return
        if password != confirm:
            messagebox.showerror("Error", "Password and Confirm Password must match"); return
        if self.check_var.get() == 0:
            messagebox.showerror("Error", "Please accept Terms & Conditions"); return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            conn = sqlite3.connect("crop_disease.db")
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO users(first_name,last_name,email,contact,password)
                   VALUES(?,?,?,?,?)""",
                (first, last, email, contact, hashed_password)
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Registration Successful!")
            self.clear_fields()
            self.back_to_login()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Email already exists!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_fields(self):
        self.first_name.delete(0, END)
        self.last_name.delete(0, END)
        self.email.delete(0, END)
        self.contact.delete(0, END)
        self.password.delete(0, END)
        self.confirm_password.delete(0, END)
        self.check_var.set(0)

    def back_to_login(self):
        if self.on_back:
            self.on_back()
        else:
            self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    Register(root)
    root.mainloop()