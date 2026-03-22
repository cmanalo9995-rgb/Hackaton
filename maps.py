import customtkinter as ctk
from tkintermapview import TkinterMapView 
import webbrowser 
import subprocess # Kailangan para sa paglipat ng windows

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class HealthApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- WINDOW CONFIGURATION ---
        self.title("Hackathon - Health Center")
        self.geometry("420x850") 
        self.configure(fg_color="#F8FDFF") 

        self.font_family = "Inter" 

        # --- BOTTOM NAVIGATION BAR (FIXED TO MATCH PROFILE.PY) ---
        self.build_footer()

        # --- SCROLLABLE CONTAINER ---
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=10)

        # 1. Header Area
        header = ctk.CTkFrame(self.scroll_frame, fg_color="white", corner_radius=15, border_width=1, border_color="#E5E7EB")
        header.pack(fill="x", pady=(10, 5))
        
        header_inner = ctk.CTkFrame(header, fg_color="transparent")
        header_inner.pack(pady=15)
        
        ctk.CTkLabel(header_inner, text="📍 Nearby Health Centers", font=(self.font_family, 18, "bold"), text_color="#111827").pack(anchor="w")
        ctk.CTkLabel(header_inner, text="Find the nearest Barangay Health Center or\nRural Health Unit", 
                     font=(self.font_family, 13), text_color="#6B7280", justify="left").pack(anchor="w")

        # 2. Interactive Map
        map_box = ctk.CTkFrame(self.scroll_frame, fg_color="#EBF8F9", corner_radius=20, height=170)
        map_box.pack(fill="x", pady=5)
        
        self.map_widget = TkinterMapView(map_box, corner_radius=20)
        self.map_widget.pack(fill="both", expand=True)
        self.map_widget.set_position(7.0707, 125.6087) 
        self.map_widget.set_zoom(13)

        # 3. Health Center Cards
        self.add_card("Barangay Health Center - San Isidro", "Purok 3, San Isidro, Davao City", 7.1245, 125.6410, "(082) 234-5678", "Mon-Sat: 8:00 AM - 5:00 PM", "0.5 km away", ["General Consultation", "Immunization", "Pre-natal Care"])
        self.add_card("Rural Health Unit - Poblacion", "Main Street, Poblacion District", 7.0658, 125.6078, "(082) 234-5679", "Mon-Fri: 7:00 AM - 4:00 PM", "2.3 km away", ["Emergency Care", "Laboratory", "Pharmacy"])

    # --- NAVIGATION FUNCTION ---
    def navigate(self, script_name):
        if script_name == "maps.py":
            return
        self.destroy()
        subprocess.Popen(["python", script_name])

    def build_footer(self):
        # Footer configuration exactly like profile.py
        nav_bar = ctk.CTkFrame(self, fg_color="#1C64F2", corner_radius=0)
        nav_bar.pack(side="bottom", fill="x")
        nav_bar.grid_columnconfigure((0, 1, 2, 3), weight=1)

        def create_nav_btn(icon, text, col, script, active=False):
            bg = "#3B82F6" if active else "transparent"
            btn_frame = ctk.CTkFrame(nav_bar, fg_color=bg, corner_radius=0, cursor="hand2")
            btn_frame.grid(row=0, column=col, sticky="nsew")
            
            inner = ctk.CTkFrame(btn_frame, fg_color="transparent")
            inner.pack(pady=10)
            
            # Icon and Text logic like profile.py
            icon_lbl = ctk.CTkLabel(inner, text=icon, font=("Arial", 20), text_color="white")
            icon_lbl.pack()
            txt_lbl = ctk.CTkLabel(inner, text=text, font=("Arial", 10), text_color="white")
            txt_lbl.pack()

            # Bindings for all elements to ensure navigation works
            for w in [btn_frame, inner, icon_lbl, txt_lbl]:
                w.bind("<Button-1>", lambda e, s=script: self.navigate(s))

        # Uniform Footer items
        create_nav_btn("💼", "First Aid", 0, "offlinefirstaid.py")
        create_nav_btn("📍", "Map", 1, "maps.py", active=True)
        create_nav_btn("📅", "Appt", 2, "appointment.py")
        create_nav_btn("👤", "Profile", 3, "profile.py")

    def add_card(self, title, address, lat, lng, phone, hours, dist, tags):
        self.map_widget.set_marker(lat, lng, text=title)
        card = ctk.CTkFrame(self.scroll_frame, fg_color="white", corner_radius=20, border_width=1, border_color="#E5E7EB")
        card.pack(fill="x", pady=8)
        center_block = ctk.CTkFrame(card, fg_color="transparent")
        center_block.pack(pady=20, anchor="center")
        top_row = ctk.CTkFrame(center_block, fg_color="transparent")
        top_row.pack(anchor="w")
        icon_circle = ctk.CTkLabel(top_row, text="🏢", fg_color="#E3ECFF", corner_radius=25, width=50, height=50)
        icon_circle.pack(side="left", anchor="n")
        text_group = ctk.CTkFrame(top_row, fg_color="transparent")
        text_group.pack(side="left", padx=15)
        ctk.CTkLabel(text_group, text=title, font=(self.font_family, 17, "bold"), text_color="#111827", wraplength=230, justify="left").pack(anchor="w")
        ctk.CTkLabel(text_group, text=f"📍 {address}", font=(self.font_family, 12), text_color="#6B7280", wraplength=230, justify="left").pack(anchor="w", pady=(2, 0))
        ctk.CTkLabel(center_block, text=f"📞 {phone}", font=(self.font_family, 13), text_color="#10B981").pack(anchor="w", pady=(12, 0))
        ctk.CTkLabel(center_block, text=f"🕒 {hours}", font=(self.font_family, 13), text_color="#F59E0B").pack(anchor="w")
        tag_container = ctk.CTkFrame(center_block, fg_color="transparent")
        tag_container.pack(pady=12, anchor="w")
        for t in tags:
            tag = ctk.CTkLabel(tag_container, text=t, fg_color="#E3ECFF", text_color="#1D4ED8", corner_radius=8, font=(self.font_family, 10, "bold"), padx=10, pady=4)
            tag.pack(side="left", padx=3)
        footer = ctk.CTkFrame(center_block, fg_color="transparent")
        footer.pack(fill="x", pady=(10, 0))
        ctk.CTkLabel(footer, text=f"📍 {dist}", text_color="#2563EB", font=(self.font_family, 13, "bold")).pack(side="left")
        ctk.CTkButton(footer, text=" ↗ Get Directions", width=125, height=35, fg_color="white", text_color="#111827", border_width=1, border_color="#D1D5DB", corner_radius=12, font=(self.font_family, 12, "bold"),
                      command=lambda l=lat, g=lng: webbrowser.open(f"https://www.google.com/maps?q={l},{g}")).pack(side="right", padx=(20, 0))

if __name__ == "__main__":
    app = HealthApp()
    app.mainloop()