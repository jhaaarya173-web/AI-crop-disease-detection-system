import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import sqlite3
import pyttsx3
from datetime import datetime
from model_predict import predict_disease

# ---------------- Voice Assistant ----------------

engine = pyttsx3.init()
engine.setProperty("rate", 160)

voices = engine.getProperty("voices")
if len(voices) > 1:
    engine.setProperty("voice", voices[1].id)


def speak(text):
    engine.say(text)
    engine.runAndWait()


# ---------------- Main Class ----------------

class CropDiseaseDetection:

    def __init__(self, root, on_logout=None):

        self.root = root
        self.on_logout = on_logout
        self.image_path = None

        self.root.title("AI Based Crop Disease Detection System")
        self.root.geometry("1200x700")
        self.root.configure(bg="#e8f5e9")

        speak("Welcome to Crop Disease Detection System")

        # ---------------- Header ----------------

        header = tk.Label(
            self.root,
            text="🌿 AI BASED CROP DISEASE DETECTION SYSTEM 🌿",
            bg="#1b5e20",
            fg="white",
            font=("Arial", 22, "bold"),
            pady=15
        )
        header.pack(fill="x")

        # ---------------- Left Menu ----------------

        self.left = tk.Frame(
            self.root,
            bg="#2e7d32",
            width=260
        )

        self.left.pack(side="left", fill="y")

        tk.Label(
            self.left,
            text="Dashboard",
            bg="#2e7d32",
            fg="white",
            font=("Arial", 22, "bold")
        ).pack(pady=25)

        tk.Button(
            self.left,
            text="📂 Upload Image",
            font=("Arial", 12, "bold"),
            bg="white",
            command=self.upload_image
        ).pack(fill="x", padx=15, pady=10, ipady=8)

        tk.Button(
            self.left,
            text="🔍 Detect Disease",
            font=("Arial", 12, "bold"),
            bg="#ffc107",
            command=self.detect
        ).pack(fill="x", padx=15, pady=10, ipady=8)

        tk.Button(
            self.left,
            text="📈 Detection History",
            font=("Arial", 12, "bold"),
            bg="#4caf50",
            fg="white",
            command=self.show_history
        ).pack(fill="x", padx=15, pady=10, ipady=8)

        tk.Button(
            self.left,
            text="🚪 Logout",
            font=("Arial", 12, "bold"),
            bg="#c62828",
            fg="white",
            command=self.logout
        ).pack(side="bottom", fill="x", padx=15, pady=20, ipady=8)

        # ---------------- Right Side ----------------

        self.right = tk.Frame(
            self.root,
            bg="#f1f8e9"
        )

        self.right.pack(fill="both", expand=True)

        self.image_label = tk.Label(
            self.right,
            text="No Image Selected",
            bg="white",
            relief="solid",
            width=45,
            height=18,
            font=("Arial", 14)
        )

        self.image_label.pack(pady=20)

        self.result = tk.Label(
            self.right,
            text="Prediction Result",
            bg="#f1f8e9",
            fg="#1b5e20",
            font=("Arial", 18, "bold")
        )

        self.result.pack(pady=10)

        self.description = tk.Label(
            self.right,
            text="",
            bg="#f1f8e9",
            justify="left",
            font=("Arial", 12),
            wraplength=700
        )

        self.description.pack(pady=5)

        self.treatment = tk.Label(
            self.right,
            text="",
            bg="#f1f8e9",
            justify="left",
            font=("Arial", 12),
            wraplength=700
        )

        self.treatment.pack(pady=5)

    # ---------------- Upload ----------------

    def upload_image(self):

        path = filedialog.askopenfilename(
            filetypes=[
                ("Image Files", "*.jpg *.jpeg *.png")
            ]
        )

        if path:

            self.image_path = path

            img = Image.open(path)
            img = img.resize((350, 350))

            photo = ImageTk.PhotoImage(img)

            self.image_label.configure(
                image=photo,
                text=""
            )

            self.image_label.image = photo

            speak("Image uploaded successfully")

    # ---------------- Detect Disease ----------------

    def detect(self):

        if self.image_path is None:
            messagebox.showerror(
                "Error",
                "Please upload an image first."
            )
            speak("Please upload an image first")
            return

        disease, confidence = predict_disease(self.image_path)

        self.result.config(
            text=f"Disease : {disease}\nConfidence : {confidence}%"
        )

        disease_info = {

            "Healthy": {
                "description":
                    "The crop is healthy. No disease symptoms detected.",

                "treatment":
                    "• No treatment required.\n"
                    "• Continue proper irrigation.\n"
                    "• Monitor the crop regularly."
            },

            "Early_Blight": {
                "description":
                    "Early Blight is caused by Alternaria fungus and mainly affects older leaves.",

                "treatment":
                    "• Remove infected leaves.\n"
                    "• Spray Mancozeb fungicide.\n"
                    "• Rotate crops."
            },

            "Late_Blight": {
                "description":
                    "Late Blight spreads rapidly during cool and humid weather.",

                "treatment":
                    "• Remove infected plants.\n"
                    "• Improve drainage.\n"
                    "• Spray Copper fungicide."
            },

            "Powdery_Mildew": {
                "description":
                    "Powdery Mildew is a fungal disease that appears as white powder on leaves.",

                "treatment":
                    "• Improve air circulation.\n"
                    "• Spray Sulfur fungicide.\n"
                    "• Remove infected leaves."
            }

        }

        info = disease_info.get(
            disease,
            {
                "description": "No description available.",
                "treatment": "No treatment available."
            }
        )

        self.description.config(
            text="Disease Description\n\n" + info["description"]
        )

        self.treatment.config(
            text="Treatment & Prevention\n\n" + info["treatment"]
        )

        speak(
            f"The detected disease is {disease}. "
            f"Confidence is {confidence} percent."
        )

        conn = sqlite3.connect("crop_disease.db")
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS detection_history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disease TEXT,
            confidence REAL,
            date TEXT
        )
        """)

        cur.execute(
            "INSERT INTO detection_history(disease,confidence,date) VALUES(?,?,?)",
            (
                disease,
                confidence,
                datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            )
        )

        conn.commit()
        conn.close()



    # ---------------- Detection History ----------------

    def show_history(self):

        history_window = tk.Toplevel(self.root)
        history_window.title("Detection History")
        history_window.geometry("700x500")
        history_window.config(bg="white")

        tk.Label(
            history_window,
            text="Detection History",
            font=("Arial", 18, "bold"),
            bg="#2e7d32",
            fg="white"
        ).pack(fill="x")

        text = tk.Text(
            history_window,
            font=("Arial", 11),
            width=80,
            height=25
        )

        text.pack(padx=10, pady=10)

        conn = sqlite3.connect("crop_disease.db")
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS detection_history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disease TEXT,
            confidence REAL,
            date TEXT
        )
        """)

        rows = cur.execute(
            "SELECT disease, confidence, date FROM detection_history ORDER BY id DESC"
        ).fetchall()

        conn.close()

        if len(rows) == 0:
            text.insert("end", "No Detection History Available.")
        else:
            for row in rows:
                text.insert(
                    "end",
                    f"Disease : {row[0]}\n"
                    f"Confidence : {row[1]}%\n"
                    f"Date : {row[2]}\n"
                    f"{'-'*60}\n"
                )


    # ---------------- Logout ----------------

    def logout(self):

        answer = messagebox.askyesno(
            "Logout",
            "Do you really want to logout?"
        )

        if answer:

            speak("Thank you for using Crop Disease Detection System.")

            if self.on_logout:
                self.on_logout()
            else:
                self.root.destroy()


# ---------------- Main ----------------

if __name__ == "__main__":

    root = tk.Tk()

    app = CropDiseaseDetection(root)

    root.mainloop()