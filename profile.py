import customtkinter as ctk
import sqlite3
import subprocess
import os
from PIL import Image, ImageTk

class UserProfileApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("User Profile")
        self.geometry("375x750")
        self.configure(fg_color="#F8FBFC") 
        ctk.set_appearance_mode("light")

        self.init_db()
        self.create_widgets()

    def init_db(self):
        pass

    def create_widgets(self):
        header_frame = ctk.CTkFrame(self, fg_color="#1C64F2", corner_radius=15)
        header_frame.pack(fill="x", padx=15, pady=(15, 5))
        header_frame.grid_columnconfigure(1, weight=1)

        avatar_lbl = ctk.CTkLabel(header_frame, text="👤", font=("Arial", 40), text_color="white")
        avatar_lbl.grid(row=0, column=0, rowspan=3, padx=(15, 10), pady=15)

        ctk.CTkLabel(header_frame, text="Chloe Bautista", font=("Arial", 20, "bold"), text_color="white").grid(row=0, column=1, sticky="w", pady=(15, 0))
        ctk.CTkLabel(header_frame, text="📞 0993 271 2430", font=("Arial", 12), text_color="#E5E7EB").grid(row=1, column=1, sticky="w")
        ctk.CTkLabel(header_frame, text="Member since 21/03/2026", font=("Arial", 10), text_color="#D1D5DB").grid(row=2, column=1, sticky="w", pady=(0, 15))

        edit_btn = ctk.CTkButton(header_frame, text="📝 Edit", width=60, height=30, 
                                 fg_color="#3B82F6", hover_color="#2563EB", corner_radius=8, font=("Arial", 12))
        edit_btn.grid(row=0, column=2, rowspan=3, padx=15)

        content_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        content_scroll.pack(fill="both", expand=True, padx=0, pady=0)

        def create_card(parent, title):
            card = ctk.CTkFrame(parent, fg_color="white", corner_radius=15, border_width=1, border_color="#E5E7EB")
            card.pack(fill="x", padx=15, pady=8)
            ctk.CTkLabel(card, text=title, font=("Arial", 16, "bold"), text_color="#1F2937").pack(anchor="w", padx=15, pady=(15, 5))
            return card
        
        info_card = create_card(content_scroll, "Personal Information")
        info_data = [
            ("📞", "Phone Number", "0993 271 2430"),
            ("✉️", "Email Address", "juan.delacruz@email.com"),
            ("📍", "Address", "Purok 3, San Isidro, Davao City")
        ]
        
        for icon, label, val in info_data:
            row_frame = ctk.CTkFrame(info_card, fg_color="transparent")
            row_frame.pack(fill="x", padx=15, pady=8)
            row_frame.columnconfigure(1, weight=1)
            icon_lbl = ctk.CTkLabel(row_frame, text=icon, font=("Arial", 18), width=35, anchor="nw")
            icon_lbl.grid(row=0, column=0, sticky="nw", pady=(2, 0)) 
            txt_cont = ctk.CTkFrame(row_frame, fg_color="transparent")
            txt_cont.grid(row=0, column=1, sticky="nw", padx=(5, 0))
            ctk.CTkLabel(txt_cont, text=label, font=("Arial", 11), text_color="#6B7280", height=15).pack(anchor="w")
            ctk.CTkLabel(txt_cont, text=val, font=("Arial", 13, "bold"), text_color="#111827", wraplength=230, justify="left").pack(anchor="w")

        activity_card = create_card(content_scroll, "Account Activity")
        activity_grid = ctk.CTkFrame(activity_card, fg_color="transparent")
        activity_grid.pack(fill="x", padx=15, pady=(0, 15))
        activity_grid.grid_columnconfigure((0, 1), weight=1)
        def make_stat(col, title, count, sub, bg, border):
            box = ctk.CTkFrame(activity_grid, fg_color=bg, corner_radius=10, border_width=1, border_color=border)
            box.grid(row=0, column=col, sticky="ew", padx=(5 if col==1 else 0, 5 if col==0 else 0))
            ctk.CTkLabel(box, text=title, font=("Arial", 11), text_color="#4B5563").pack(anchor="w", padx=10, pady=(10, 0))
            ctk.CTkLabel(box, text=count, font=("Arial", 24, "bold"), text_color="#111827").pack(anchor="w", padx=10)
            ctk.CTkLabel(box, text=sub, font=("Arial", 10), text_color="#9CA3AF").pack(anchor="w", padx=10, pady=(0, 10))
        make_stat(0, "📅 Appointments", "3", "Total booked", "#EFF6FF", "#DBEAFE")
        make_stat(1, "💖 Health Records", "12", "Records saved", "#F0FDF4", "#DCFCE7")


        settings_card = create_card(content_scroll, "⚙️ Settings")
        settings = [("🛡️", "Change Password"), ("💖", "Health Records"), ("📅", "History")]
        for i, (icon, text) in enumerate(settings):
            btn = ctk.CTkButton(settings_card, text=f"  {icon}    {text}", anchor="w", fg_color="transparent", 
                                 text_color="#374151", hover_color="#F3F4F6", font=("Arial", 13), 
                                 border_width=1, border_color="#D1D5DB", corner_radius=8, height=45)
            btn.pack(fill="x", padx=15, pady=(5, 15 if i == 2 else 5))

        privacy_card = ctk.CTkFrame(content_scroll, fg_color="#ECFDF5", corner_radius=10, border_width=1, border_color="#D1FAE5")
        privacy_card.pack(fill="x", padx=15, pady=15)
        ctk.CTkLabel(privacy_card, text="🔒 Privacy & Data\nAll your data is stored locally. Your\ninformation is private and secure.", 
                     justify="left", font=("Arial", 11), text_color="#065F46").pack(padx=15, pady=15, anchor="w")

        nav_bar = ctk.CTkFrame(self, fg_color="#1C64F2", corner_radius=0)
        nav_bar.pack(side="bottom", fill="x")
        nav_bar.grid_columnconfigure((0, 1, 2, 3), weight=1)

        def create_nav_btn(icon, text, col, active=False):
            bg = "#3B82F6" if active else "transparent"
            btn_frame = ctk.CTkFrame(nav_bar, fg_color=bg, corner_radius=0)
            btn_frame.grid(row=0, column=col, sticky="nsew")
            
            inner = ctk.CTkFrame(btn_frame, fg_color="transparent")
            inner.pack(pady=10)
            
            ctk.CTkLabel(inner, text=icon, font=("Arial", 20), text_color="white").pack()
            ctk.CTkLabel(inner, text=text, font=("Arial", 10), text_color="white").pack()

        create_nav_btn("💼", "First Aid", 0)
        create_nav_btn("📍", "Map", 1)
        create_nav_btn("📅", "Appt", 2)
        create_nav_btn("👤", "Profile", 3, active=True) 

if __name__ == "__main__":
    app = UserProfileApp()
    app.mainloop()