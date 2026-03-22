import customtkinter as ctk
import sqlite3
import subprocess # Kailangan para sa paglipat ng windows

# --- Database Setup ---
def setup_database():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE first_aid (
            id INTEGER PRIMARY KEY,
            icon TEXT,
            title TEXT,
            urgency TEXT,
            urgency_color TEXT,
            category TEXT,
            symptoms TEXT,
            steps TEXT,
            warnings TEXT,
            seek_help TEXT
        )
    ''')
    
    data = [
        ('♡', 'Chest Pain / Heart Attack', 'Critical', '#dc2626', 'Critical Emergencies',
         '• Severe chest pain or pressure\n• Pain radiating to arm, jaw, or back\n• Shortness of breath\n• Sweating, nausea, dizziness',
         '• Call emergency services immediately (911)\n• Have the person sit down and rest\n• Loosen any tight clothing\n• If prescribed, help them take nitroglycerin\n• If they become unconscious, start CPR\n• Do NOT leave them alone',
         'Never delay calling emergency services\nDo not drive yourself to the hospital if experiencing symptoms\nAspirin may help but consult emergency dispatcher first',
         'Immediately - this is a medical emergency'),
         
        ('💧', 'Diarrhea and Vomiting', 'Urgent', '#ea580c', 'Common Illnesses',
         '• Frequent loose or watery stools\n• Nausea and vomiting\n• Abdominal cramps\n• Dehydration signs (dry mouth, decreased urination)\n• Fever',
         '• Drink plenty of fluids (ORS - Oral Rehydration Solution)\n• Eat bland foods like rice, bananas, toast\n• Avoid dairy, fatty, or spicy foods\n• Rest and stay hydrated\n• Wash hands frequently to prevent spread\n• Monitor for signs of dehydration',
         'Seek medical help if blood appears in stool or vomit\nWatch for severe dehydration (no urination for 8+ hours)\nInfants and elderly are at higher risk',
         'If symptoms persist beyond 2 days, or if severe dehydration occurs'),
         
        ('🩺', 'Nosebleed', 'Non-Urgent', '#16a34a', 'Common Conditions',
         '• Blood flowing from one or both nostrils\n• May be caused by dry air, nose picking, or injury\n• Common in children and elderly',
         '• Sit down and lean slightly forward\n• Pinch the soft part of the nose firmly\n• Hold for 10-15 minutes without releasing\n• Breathe through your mouth\n• Apply a cold compress to the bridge of the nose\n• Avoid blowing your nose for several hours after bleeding stops',
         'Do NOT tilt head backward (can cause blood to go down throat)\nDo NOT pack the nose with tissue or cotton\nAvoid strenuous activity after nosebleed',
         'If bleeding continues for more than 20 minutes, or if caused by injury')
    ]
    
    cursor.executemany('INSERT INTO first_aid (icon, title, urgency, urgency_color, category, symptoms, steps, warnings, seek_help) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
    conn.commit()
    return conn


# --- UI Components ---
class AccordionCard(ctk.CTkFrame):
    def __init__(self, master, data, **kwargs):
        super().__init__(master, fg_color="#ffffff", border_width=1, border_color="#f3f4f6", corner_radius=15, **kwargs)
        
        self.is_expanded = False
        self.data = data
        
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent", cursor="hand2")
        self.header_frame.pack(fill="x", padx=15, pady=15)
        
        icon_bg = "#fef2f2" if data['urgency'] == 'Critical' else "#fff7ed" if data['urgency'] == 'Urgent' else "#f0fdf4"

        self.icon_label = ctk.CTkLabel(self.header_frame, text=data['icon'], font=("Inter", 22), 
                                       text_color=data['urgency_color'], fg_color=icon_bg, 
                                       corner_radius=10, width=45, height=45)
        self.icon_label.pack(side="left", padx=(0, 15))
        
        self.title_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.title_frame.pack(side="left", fill="both", expand=True)
        
        self.title_label = ctk.CTkLabel(self.title_frame, text=data['title'], font=("Inter", 15, "bold"), text_color="#111827", anchor="w")
        self.title_label.pack(fill="x", pady=(2,0))
        
        self.tags_frame = ctk.CTkFrame(self.title_frame, fg_color="transparent")
        self.tags_frame.pack(fill="x", pady=(2, 0))
        
        self.urgency_tag = ctk.CTkLabel(self.tags_frame, text=f" {data['urgency']} ", font=("Inter", 10, "bold"), 
                                        text_color="white", fg_color=data['urgency_color'], corner_radius=10, height=20)
        self.urgency_tag.pack(side="left", padx=(0, 8))
        
        self.category_tag = ctk.CTkLabel(self.tags_frame, text=data['category'], font=("Inter", 11), text_color="#6b7280", height=20)
        self.category_tag.pack(side="left")
        
        self.toggle_btn = ctk.CTkLabel(self.header_frame, text="⌄", font=("Inter", 20), text_color="#9ca3af")
        self.toggle_btn.pack(side="right")
        
        for widget in [self.header_frame, self.title_label, self.toggle_btn, self.icon_label]:
            widget.bind("<Button-1>", lambda e: self.toggle())
        
        self.details_frame = ctk.CTkFrame(self, fg_color="transparent")
        
        self._add_section_header("🩺 Symptoms to Look For:")
        self._add_body_text(data['symptoms'])
        
        self._add_section_header("♡ First Aid Steps:")
        self._add_body_text(data['steps'])
        
        warn_box = ctk.CTkFrame(self.details_frame, fg_color="#fef2f2", border_width=1, border_color="#fecaca", corner_radius=8)
        warn_box.pack(fill="x", padx=15, pady=(15, 5))
        ctk.CTkLabel(warn_box, text="ⓘ Important Warnings:", font=("Inter", 12, "bold"), text_color="#b91c1c", anchor="w").pack(fill="x", padx=15, pady=(12, 5))
        self._add_body_text(data['warnings'], parent=warn_box, text_color="#991b1b")
        
        help_box = ctk.CTkFrame(self.details_frame, fg_color="#eff6ff", border_width=1, border_color="#bfdbfe", corner_radius=8)
        help_box.pack(fill="x", padx=15, pady=(5, 15))
        ctk.CTkLabel(help_box, text="⚠ Seek Medical Help:", font=("Inter", 12, "bold"), text_color="#1d4ed8", anchor="w").pack(fill="x", padx=15, pady=(12, 0))
        
        help_lbl = ctk.CTkLabel(help_box, text=data['seek_help'], font=("Inter", 12), text_color="#1e40af", anchor="w", justify="left", wraplength=2000)
        help_lbl.pack(fill="x", padx=15, pady=(2, 12))
        help_lbl.bind('<Configure>', lambda e, l=help_lbl: l.configure(wraplength=l.winfo_width()))

        if data['urgency'] == 'Critical':
            self.configure(border_color="#fecaca")

    def _add_section_header(self, text):
        ctk.CTkLabel(self.details_frame, text=text, font=("Inter", 12, "bold"), text_color="#374151", anchor="w").pack(fill="x", padx=15, pady=(10, 5))

    def _add_body_text(self, text, parent=None, text_color="#4b5563"):
        parent_frame = parent if parent else self.details_frame
        lbl = ctk.CTkLabel(parent_frame, text=text, font=("Inter", 12), text_color=text_color, anchor="w", justify="left", wraplength=2000)
        lbl.pack(fill="x", padx=25, pady=(0, 10))
        lbl.bind('<Configure>', lambda e, l=lbl: l.configure(wraplength=l.winfo_width()))

    def toggle(self):
        if self.is_expanded:
            self.details_frame.pack_forget()
            self.toggle_btn.configure(text="⌄")
            self.is_expanded = False
        else:
            self.details_frame.pack(fill="x", expand=True, pady=(0, 10))
            self.toggle_btn.configure(text="⌃")
            self.is_expanded = True


class FirstAidApp(ctk.CTk):
    def __init__(self, db_conn):
        super().__init__()
        self.db = db_conn
        self.title("Offline First Aid Guide")
        self.geometry("420x850")
        self.minsize(320, 600)
        self.configure(fg_color="#fdf2f8")
        
        self.current_filter = "All"
        
        # Build Navigation Footer gaya ng sa Profile page
        self.build_bottom_nav()
        
        self.scroll_area = ctk.CTkScrollableFrame(self, fg_color="transparent", bg_color="transparent")
        self.scroll_area.pack(fill="both", expand=True, padx=0)
        
        self.content_frame = ctk.CTkFrame(self.scroll_area, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=15, pady=10)

        self.build_header()
        self.build_emergency_contacts()
        self.build_search_and_filters()
        
        self.results_container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.results_container.pack(fill="x", pady=5)
        
        self.build_disclaimer()
        self.refresh_data()

    # --- NAVIGATION LOGIC ---
    def switch_page(self, page_name):
        if page_name == "offlinefirstaid.py": return
        self.destroy()
        subprocess.Popen(["python", page_name])

    def build_header(self):
        header = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header.pack(fill="x", pady=(10, 20))
        
        icon_lbl = ctk.CTkLabel(header, text="♡", font=("Inter", 24, "bold"), text_color="white", fg_color="#e11d48", corner_radius=10, width=40, height=40)
        icon_lbl.pack(side="left", padx=(0, 12))
        
        text_frame = ctk.CTkFrame(header, fg_color="transparent")
        text_frame.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(text_frame, text="Offline First Aid Guide", font=("Inter", 18, "bold"), text_color="#111827", anchor="w").pack(fill="x")
        ctk.CTkLabel(text_frame, text="Emergency Reference for Barangay Health Workers", font=("Inter", 10), text_color="#6b7280", anchor="w").pack(fill="x")

    def build_emergency_contacts(self):
        box = ctk.CTkFrame(self.content_frame, fg_color="#b91c1c", corner_radius=12)
        box.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(box, text="🚨 Emergency Contacts - Philippines", font=("Inter", 13, "bold"), text_color="white").pack(pady=(12, 10))
        
        grid = ctk.CTkFrame(box, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=12, pady=(0, 15))
        grid.columnconfigure((0, 1), weight=1, uniform="a")
        
        def contact_btn(parent, icon, text, copy_value, row, col, span=1):
            frame = ctk.CTkFrame(parent, fg_color="#dc2626", corner_radius=6, height=35, cursor="hand2")
            frame.grid(row=row, column=col, columnspan=span, sticky="nsew", padx=3, pady=3)
            frame.pack_propagate(False)
            
            original_text = f"{icon} {text}"
            lbl = ctk.CTkLabel(frame, text=original_text, font=("Inter", 11, "bold"), text_color="white", cursor="hand2")
            lbl.pack(expand=True)
            
            def on_click(event):
                self.clipboard_clear()
                self.clipboard_append(copy_value)
                self.update() 
                
                lbl.configure(text="✓ Copied!")
                self.after(1500, lambda: lbl.configure(text=original_text))

            frame.bind("<Button-1>", on_click)
            lbl.bind("<Button-1>", on_click)

        contact_btn(grid, "📞", "Emergency: 911", "911", row=0, col=0)
        contact_btn(grid, "🏥", "Red Cross: 143", "143", row=0, col=1)
        contact_btn(grid, "☠️", "Poison Control: 0917 989 3333", "09179893333", row=1, col=0, span=2)
        contact_btn(grid, "🌊", "NDRRMC: (02) 911-1406", "029111406", row=2, col=0, span=2)

    def build_search_and_filters(self):
        container = ctk.CTkFrame(self.content_frame, fg_color="#ffffff", corner_radius=12, border_width=1, border_color="#f3f4f6")
        container.pack(fill="x", pady=5)
        
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.refresh_data())
        
        search_frame = ctk.CTkFrame(container, fg_color="#f1f5f9", corner_radius=8, border_width=0)
        search_frame.pack(fill="x", padx=12, pady=(15, 10))
        
        ctk.CTkLabel(search_frame, text="🔍", text_color="#94a3b8", font=("Inter", 14)).pack(side="left", padx=(12, 0))
        search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search condition...", textvariable=self.search_var, fg_color="transparent", border_width=0, text_color="#0f172a", placeholder_text_color="#64748b", height=38, font=("Inter", 14))
        search_entry.pack(side="left", fill="x", expand=True, padx=(5, 10))
        
        self.filter_frame = ctk.CTkScrollableFrame(container, fg_color="transparent", height=60, orientation="horizontal")
        self.filter_frame.pack(fill="x", expand=True, padx=12, pady=(0, 10))
        self.filter_frame._scrollbar.configure(button_color="#cbd5e1", button_hover_color="#94a3b8")

        filters = ["All", "Critical Emergencies", "Common Illnesses", "Injuries", "Common Conditions", "Environmental"]
        self.filter_buttons = {}
        
        for f in filters:
            is_active = (f == "All")
            btn = ctk.CTkButton(self.filter_frame, text=f, font=("Inter", 13), height=30, corner_radius=6, 
                                fg_color="#09090b" if is_active else "#ffffff", text_color="#ffffff" if is_active else "#000000", 
                                border_width=0 if is_active else 1, border_color="#e4e4e7", 
                                hover_color="#27272a" if is_active else "#f4f4f5", 
                                command=lambda cat=f: self.set_filter(cat))
            btn.pack(side="left", padx=(0, 6), pady=(5, 10))
            self.filter_buttons[f] = btn

    def set_filter(self, category):
        self.current_filter = category
        for name, btn in self.filter_buttons.items():
            if name == category:
                btn.configure(fg_color="#09090b", text_color="#ffffff", border_width=0, hover_color="#27272a")
            else:
                btn.configure(fg_color="#ffffff", text_color="#000000", border_width=1, hover_color="#f4f4f5")
        self.refresh_data()

    def refresh_data(self):
        for widget in self.results_container.winfo_children():
            widget.destroy()
            
        search_term = f"%{self.search_var.get()}%"
        cursor = self.db.cursor()
        
        if self.current_filter == "All":
            cursor.execute("SELECT * FROM first_aid WHERE title LIKE ? OR symptoms LIKE ?", (search_term, search_term))
        else:
            cursor.execute("SELECT * FROM first_aid WHERE category = ? AND (title LIKE ? OR symptoms LIKE ?)", 
                           (self.current_filter, search_term, search_term))
            
        columns = [description[0] for description in cursor.description]
        results = cursor.fetchall()
        
        if not results:
            ctk.CTkLabel(self.results_container, text="No results found.", text_color="#9ca3af", font=("Inter", 14)).pack(pady=30)
            return
            
        for row in results:
            row_dict = dict(zip(columns, row))
            card = AccordionCard(self.results_container, data=row_dict)
            card.pack(fill="x", pady=6)

    def build_disclaimer(self):
        disc = ctk.CTkFrame(self.content_frame, fg_color="#fefce8", border_width=1, border_color="#fef08a", corner_radius=12)
        disc.pack(fill="x", pady=(15, 20))
        
        header_frame = ctk.CTkFrame(disc, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 5))
        ctk.CTkLabel(header_frame, text="⚠", font=("Inter", 14), text_color="#ca8a04").pack(side="left", padx=(0,5))
        ctk.CTkLabel(header_frame, text="Medical Disclaimer", font=("Inter", 12, "bold"), text_color="#854d0e", anchor="w").pack(side="left", fill="x")
        
        disclaimer_text = "This guide is for emergency reference only and does not replace professional medical advice. Always seek qualified medical help when available. In life-threatening situations, call emergency services (911) immediately. The information provided is for Barangay Health Workers and trained first responders in remote areas where immediate medical care may not be accessible."
        disc_lbl = ctk.CTkLabel(disc, text=disclaimer_text, font=("Inter", 11), text_color="#a16207", justify="left", wraplength=2000, anchor="w")
        disc_lbl.pack(fill="x", padx=15, pady=(0, 15))
        disc_lbl.bind('<Configure>', lambda e, l=disc_lbl: l.configure(wraplength=l.winfo_width()))

    def build_bottom_nav(self):
        # Ginaya ang navigation bar ng Profile page para uniform
        nav_bar = ctk.CTkFrame(self, fg_color="#1C64F2", height=65, corner_radius=0)
        nav_bar.pack(side="bottom", fill="x")
        nav_bar.grid_columnconfigure((0, 1, 2, 3), weight=1)
        nav_bar.pack_propagate(False)

        def create_nav_btn(icon, text, col, script, active=False):
            bg = "#3B82F6" if active else "transparent"
            btn_frame = ctk.CTkFrame(nav_bar, fg_color=bg, corner_radius=0, cursor="hand2")
            btn_frame.grid(row=0, column=col, sticky="nsew")
            
            inner = ctk.CTkFrame(btn_frame, fg_color="transparent")
            inner.pack(pady=10)
            
            icon_lbl = ctk.CTkLabel(inner, text=icon, font=("Arial", 20), text_color="white")
            icon_lbl.pack()
            txt_lbl = ctk.CTkLabel(inner, text=text, font=("Arial", 10), text_color="white")
            txt_lbl.pack()

            # Bindings para sa click navigation gaya ng sa Profile page
            for widget in [btn_frame, inner, icon_lbl, txt_lbl]:
                widget.bind("<Button-1>", lambda e: self.switch_page(script))

        # Inilagay ang mga kaukulang filenames para sa uniform navigation
        create_nav_btn("🧰", "First Aid", 0, "offlinefirstaid.py", active=True)
        create_nav_btn("📍", "Map", 1, "maps.py")
        create_nav_btn("📅", "Appt", 2, "appointment.py")
        create_nav_btn("👤", "Profile", 3, "profile.py")


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    db_connection = setup_database()
    app = FirstAidApp(db_connection)
    app.mainloop()