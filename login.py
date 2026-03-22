import customtkinter as ctk
import sqlite3
import subprocess
import os
from PIL import Image, ImageTk

ICON_PATH = r"C:\Users\User\Documents\CYRIL_CODES\Hackaton\Photos\Logo.png"

def open_signup():
    """Sinasara ang login at binubuksan ang signup.py"""
    app.destroy()
    subprocess.Popen(["python", "signup.py"])

def on_login():
    """Function na tumatakbo pag pinindot ang Log In button"""
    user_name = name_entry.get()
    user_phone = phone_entry.get()

    if not user_name or not user_phone:
        print("⚠ Error: Kulang ang impormasyon.")
        return

    save_to_database() 
    
    print("✅ Login Success! Opening First Aid Guide...")
    app.destroy()
    subprocess.Popen(["python", "offlinefirstaid.py"])

def save_to_database():
    conn = sqlite3.connect("barangay_health.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY, 
            name TEXT, 
            phone TEXT, 
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    user_name = name_entry.get()
    user_phone = phone_entry.get()
    
    if user_name and user_phone:
        cursor.execute("INSERT INTO users (name, phone) VALUES (?, ?)", (user_name, user_phone))
        conn.commit()
        print(f"💾 Data Saved: {user_name}")
    conn.close()

app = ctk.CTk()
app.geometry("400x750")
app.title("Barangay Health-E - Login")
app.configure(fg_color="#F0F9FF")

main_frame = ctk.CTkFrame(app, fg_color="white", corner_radius=0)
main_frame.pack(pady=40, padx=30, fill="both", expand=True)

if os.path.exists(ICON_PATH):
    try:
        img = Image.open(ICON_PATH)
        img_resized = img.resize((60, 60), Image.Resampling.LANCZOS)
        logo_image = ImageTk.PhotoImage(img_resized)
        logo_label = ctk.CTkLabel(main_frame, image=logo_image, text="")
        logo_label.pack(pady=(20, 5))
    except Exception as e:
        print(f"Error loading logo: {e}")
        ctk.CTkLabel(main_frame, text="⚡", font=("Inter", 30), text_color="#007AFF").pack(pady=(20, 5))
else:
    print(f"❌ Path not found: {ICON_PATH}")
    ctk.CTkLabel(main_frame, text="⚡", font=("Inter", 30), text_color="#007AFF").pack(pady=(20, 5))

ctk.CTkLabel(main_frame, text="Barangay Health-E", font=("Inter", 22, "bold"), text_color="#0F172A").pack()
ctk.CTkLabel(main_frame, text="Digital Clinic Assistant", font=("Inter", 10), text_color="#64748B").pack(pady=(0, 20))

ctk.CTkLabel(main_frame, text="📶 Works Offline - No Internet Required", 
             fg_color="#E8F5E9", text_color="#2E7D32", corner_radius=8, 
             height=35, width=300, font=("Inter", 9)).pack(pady=10)

ctk.CTkLabel(main_frame, text="Full Name", font=("Inter", 10, "bold"), text_color="#475569").pack(anchor="w", padx=25, pady=(15, 0))
name_entry = ctk.CTkEntry(main_frame, placeholder_text="Juan Dela Cruz", fg_color="#F1F5F9", 
                          text_color="black", border_width=0, corner_radius=8, height=45, width=280, font=("Inter", 11))
name_entry.pack(padx=25, pady=5)

ctk.CTkLabel(main_frame, text="Phone Number", font=("Inter", 10, "bold"), text_color="#475569").pack(anchor="w", padx=25, pady=(10, 0))
phone_entry = ctk.CTkEntry(main_frame, placeholder_text="09XX XXX XXXX", fg_color="#F1F5F9", 
                           text_color="black", border_width=0, corner_radius=8, height=45, width=280, font=("Inter", 11))
phone_entry.pack(padx=25, pady=5)

login_btn = ctk.CTkButton(main_frame, text="Log In", command=on_login, fg_color="#050510", 
                           corner_radius=8, height=50, width=280, font=("Inter", 11, "bold"))
login_btn.pack(pady=30)

ctk.CTkLabel(main_frame, text="Don't have an account?", font=("Inter", 9), text_color="#64748B").pack()
back_to_signup = ctk.CTkButton(main_frame, text="Create New Account", fg_color="transparent", 
                               text_color="#2563EB", hover_color="#F1F3F6", command=open_signup, font=("Inter", 9, "bold"))
back_to_signup.pack()

app.mainloop()