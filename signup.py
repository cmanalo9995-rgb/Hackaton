import customtkinter as ctk
import sqlite3
import subprocess
import os
from PIL import Image, ImageTk

ICON_PATH = r"C:\Users\User\Documents\CYRIL_CODES\Hackaton\Photos\Logo.png"
if not os.path.exists(ICON_PATH):
    ICON_PATH = None 

def open_login():
    """Closes signup and opens login.py"""
    app.destroy()
    subprocess.Popen(["python", "login.py"])

def on_signup_click():
    """Function pag kiniclick ang Sign Up"""
    print("▶ Success: signing up (placeholder)...")

app = ctk.CTk()
app.geometry("400x750")
app.title("Barangay Health-E - Sign Up")
app.configure(fg_color="#F0F9FF")

scroll_container = ctk.CTkScrollableFrame(app, fg_color="transparent", label_text="")
scroll_container.pack(fill="both", expand=True, padx=5, pady=5)

if ICON_PATH:
    try:
        img = Image.open(ICON_PATH)
        img_resized = img.resize((60, 60), Image.Resampling.LANCZOS)
        logo_image = ctk.CTkImage(light_image=img_resized, dark_image=img_resized, size=(60, 60))
        logo_label = ctk.CTkLabel(scroll_container, image=logo_image, text="")
        logo_label.pack(pady=(40, 5))
    except:
        ctk.CTkLabel(scroll_container, text="⚡", font=("Arial", 30), text_color="#007AFF").pack(pady=(40, 5))
else:
    ctk.CTkLabel(scroll_container, text="⚡", font=("Arial", 30), text_color="#007AFF").pack(pady=(40, 5))

ctk.CTkLabel(scroll_container, text="Barangay Health-E", font=("Inter", 28, "bold"), text_color="#0B1E33").pack(pady=(5, 5))
ctk.CTkLabel(scroll_container, text="Digital Clinic Assistant", font=("Inter", 14), text_color="#707070").pack(pady=(0, 20))

ctk.CTkLabel(scroll_container, text="📶 Works Offline - No Internet Required", 
             fg_color="#E8F5E9", text_color="#2E7D32", corner_radius=8, 
             height=35, width=320, font=("Inter", 12)).pack(pady=10)

card = ctk.CTkFrame(scroll_container, fg_color="white", corner_radius=15)
card.pack(pady=15, padx=20, fill="both", expand=True)

ctk.CTkLabel(card, text="Create New Account", font=("Inter", 16, "bold"), text_color="#1E293B", anchor="w").pack(fill="x", padx=30, pady=(15, 0))
ctk.CTkLabel(card, text="Register to access health services\nand first aid information", 
             font=("Inter", 11), text_color="#94A3B8", anchor="w", justify="left").pack(fill="x", padx=30, pady=(0, 10))

ENTRY_WIDTH = 280

def create_ctk_field(parent_frame, label_text, placeholder, is_pass=False, pady_top=10):
    ctk.CTkLabel(parent_frame, text=label_text, font=("Inter", 11, "bold"), text_color="black").pack(anchor="w", padx=30, pady=(pady_top, 0))
    entry = ctk.CTkEntry(parent_frame, placeholder_text=placeholder, fg_color="#F1F3F6", text_color="black", 
                         border_width=0, corner_radius=8, height=45, width=ENTRY_WIDTH, font=("Inter", 12))
    if is_pass:
        entry.configure(show="*")
    entry.pack(padx=30, pady=2)
    return entry

name_entry = create_ctk_field(card, "Full Name", "Juan Dela Cruz", pady_top=10)
phone_entry = create_ctk_field(card, "Phone Number", "09XX XXX XXXX", pady_top=5)

ctk.CTkLabel(card, text="Format: 09XXXXXXXXX or +639XXXXXXXXX", 
             font=("Inter", 9), text_color="#94A3B8", anchor="w").pack(fill="x", padx=30)

pass_entry = create_ctk_field(card, "Password", "Enter your password", is_pass=True, pady_top=5)
conf_pass_entry = create_ctk_field(card, "Confirm Password", "Confirm your password", is_pass=True, pady_top=5)

signup_btn = ctk.CTkButton(card, text="Sign Up", command=on_signup_click, fg_color="#050510", 
                           corner_radius=8, height=50, width=ENTRY_WIDTH, font=("Inter", 12, "bold"))
signup_btn.pack(pady=(25, 10))

ctk.CTkLabel(card, text="Already have an account?", font=("Inter", 11), text_color="gray").pack()
back_to_login_btn = ctk.CTkButton(card, text="Login here", fg_color="transparent", 
                                  text_color="#2563EB", hover_color="#F1F3F6", command=open_login, font=("Inter", 11, "bold"))
back_to_login_btn.pack(pady=(0, 20))

app.mainloop()