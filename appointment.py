import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry 
from datetime import datetime
import subprocess 

class BarangayHealthApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Configuration
        self.title("Barangay Health-E")
        self.geometry("420x850") # Uniform size sa profile.py
        self.configure(fg_color="#F8FAFC")

        # Data Store
        self.appointments = [
            {"service": "General Consultation", "person": "Dr. Maria Santos", "date": "Wed, Mar 25, 2026", "time": "10:00 AM", "status": "confirmed"},
            {"service": "Immunization", "person": "Nurse Jane Reyes", "date": "Thu, Apr 02, 2026", "time": "2:00 PM", "status": "pending"}
        ]

        # --- NAVIGATION FOOTER (FIXED TO MATCH PROFILE.PY) ---
        self.build_footer()

        # --- MAIN CONTAINER ---
        self.main_container = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        self.main_container.pack(fill="both", expand=True)

        # Purple Header
        self.header = ctk.CTkFrame(self.main_container, height=140, fg_color="#9333EA", corner_radius=20)
        self.header.pack(fill="x", padx=15, pady=15)
        self.header.pack_propagate(False)
        
        ctk.CTkLabel(self.header, text="My Appointments", font=("Arial Bold", 24), text_color="white").place(relx=0.05, rely=0.15)
        ctk.CTkLabel(self.header, text="Book and manage your\nhealth appointments", font=("Arial", 13), 
                     text_color="#F3E8FF", justify="left").place(relx=0.05, rely=0.45)
        
        self.book_btn = ctk.CTkButton(self.header, text="+ Book New", width=110, height=38, 
                                      fg_color="white", text_color="#9333EA", corner_radius=12,
                                      font=("Arial Bold", 13), command=self.open_modal)
        self.book_btn.place(relx=0.65, rely=0.4)

        self.section_header("Upcoming Appointments", "Your scheduled health appointments")
        self.appointment_list_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.appointment_list_frame.pack(fill="x")

        # Available Services Grid
        self.section_header("Available Services", "Common services at Barangay Health Centers")
        self.services_grid = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.services_grid.pack(fill="x", padx=15, pady=10)
        
        self.services_list = [
            "General Consultation", "Immunization", "Pre-natal Care", "Family Planning", 
            "Dental Checkup", "Blood Pressure", "Diabetes Screening", "TB DOTS"
        ]
        
        for i, svc in enumerate(self.services_list):
            btn = ctk.CTkButton(self.services_grid, text=svc, width=170, height=55, fg_color="white", 
                                text_color="#1E293B", border_width=1, border_color="#E2E8F0", corner_radius=12,
                                font=("Arial", 11), command=lambda s=svc: self.quick_book(s))
            btn.grid(row=i//2, column=i%2, padx=5, pady=5)

        # --- MODAL OVERLAY ---
        self.overlay = ctk.CTkFrame(self, fg_color="#334155", corner_radius=0) 
        self.setup_booking_modal()
        self.render_appointments()

    def navigate(self, script_name):
        if script_name == "appointment.py": return 
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
        create_nav_btn("🧰", "First Aid", 0, "offlinefirstaid.py")
        create_nav_btn("📍", "Map", 1, "maps.py")
        create_nav_btn("📅", "Appt", 2, "appointment.py", active=True)
        create_nav_btn("👤", "Profile", 3, "profile.py")

    def section_header(self, title, sub):
        f = ctk.CTkFrame(self.main_container, fg_color="transparent")
        f.pack(fill="x", padx=20, pady=(15, 0))
        ctk.CTkLabel(f, text=title, font=("Arial Bold", 18), text_color="#1E293B").pack(anchor="w")
        ctk.CTkLabel(f, text=sub, font=("Arial", 12), text_color="#64748B").pack(anchor="w")

    def setup_booking_modal(self):
        self.modal = ctk.CTkFrame(self.overlay, width=380, height=750, fg_color="white", corner_radius=30)
        self.modal.place(relx=0.5, rely=0.5, anchor="center")
        self.modal.pack_propagate(False)

        ctk.CTkButton(self.modal, text="✕", width=30, height=30, fg_color="transparent", 
                      text_color="#64748B", font=("Arial", 18), command=self.close_modal).place(relx=0.88, rely=0.02)

        ctk.CTkLabel(self.modal, text="📅 Book Appointment", font=("Arial Bold", 22), text_color="#1E293B").pack(pady=(40, 5))
        ctk.CTkLabel(self.modal, text="Select your preferred service, date, and time", 
                      font=("Arial", 13), text_color="#64748B").pack(pady=(0, 20))

        ctk.CTkLabel(self.modal, text="Select Service *", font=("Arial Bold", 14), text_color="#1E293B").pack(anchor="w", padx=35)
        self.service_var = ctk.StringVar(value="Choose a service")
        self.service_menu = ctk.CTkOptionMenu(
            self.modal, variable=self.service_var, width=310, height=48, 
            values=self.services_list,
            fg_color="#F1F5F9", text_color="#1E293B", button_color="#CBD5E1", 
            corner_radius=12, dropdown_fg_color="white", dropdown_text_color="#1E293B"
        )
        self.service_menu.pack(pady=10)

        ctk.CTkLabel(self.modal, text="📅 Select Date *", font=("Arial Bold", 14), text_color="#1E293B").pack(anchor="w", padx=35, pady=(10,0))
        date_bg = ctk.CTkFrame(self.modal, fg_color="#F1F5F9", height=48, width=310, corner_radius=12)
        date_bg.pack(pady=10)
        date_bg.pack_propagate(False)
        self.cal = DateEntry(date_bg, background='#9333EA', foreground='white', borderwidth=0, font=("Arial", 11))
        self.cal.pack(fill="both", expand=True, padx=10)

        ctk.CTkLabel(self.modal, text="🕒 Select Time *", font=("Arial Bold", 14), text_color="#1E293B").pack(anchor="w", padx=35, pady=(10,0))
        self.selected_time = ctk.StringVar(value="")
        t_grid = ctk.CTkFrame(self.modal, fg_color="transparent")
        t_grid.pack(pady=10)
        
        times = ["8:00 AM", "10:00 AM", "1:00 PM", "3:00 PM"]
        self.time_btns = []
        for t in times:
            b = ctk.CTkButton(t_grid, text=t, width=72, height=40, fg_color="white", text_color="#1E293B", 
                              border_width=1, border_color="#E2E8F0", corner_radius=10, 
                              command=lambda v=t: self.set_time(v))
            b.pack(side="left", padx=4)
            self.time_btns.append(b)

        p_card = ctk.CTkFrame(self.modal, fg_color="#F5F3FF", corner_radius=15, border_width=1, border_color="#DDD6FE")
        p_card.pack(fill="x", padx=35, pady=20)
        ctk.CTkLabel(p_card, text="👤 Patient Information", font=("Arial Bold", 13), text_color="#7C3AED").pack(anchor="w", padx=15, pady=(10, 2))
        ctk.CTkLabel(p_card, text="Name: Chloe Bautista\nPhone: 0993 271 2430", font=("Arial Bold", 12), 
                      text_color="#4C1D95", justify="left").pack(anchor="w", padx=15, pady=(0, 10))

        ctk.CTkButton(self.modal, text="✓ Confirm Booking", fg_color="#9333EA", height=52, width=310,
                      corner_radius=15, font=("Arial Bold", 16), command=self.confirm_booking).pack(pady=(10, 5))
        ctk.CTkButton(self.modal, text="Cancel", fg_color="white", text_color="#64748B", 
                      border_width=1, border_color="#E2E8F0", height=45, width=310, corner_radius=15, 
                      command=self.close_modal).pack()

    def set_time(self, val):
        self.selected_time.set(val)
        for b in self.time_btns:
            if b.cget("text") == val:
                b.configure(fg_color="#9333EA", text_color="white", border_width=0)
            else:
                b.configure(fg_color="white", text_color="#1E293B", border_width=1)

    def render_appointments(self):
        for child in self.appointment_list_frame.winfo_children():
            child.destroy()
        for idx, appt in enumerate(self.appointments):
            card = ctk.CTkFrame(self.appointment_list_frame, fg_color="white", corner_radius=18, border_width=1, border_color="#F1F5F9")
            card.pack(fill="x", padx=15, pady=8)
            ctk.CTkLabel(card, text=f"🩺 {appt['service']}", font=("Arial Bold", 16), text_color="#1E293B").pack(anchor="w", padx=20, pady=(15, 2))
            ctk.CTkLabel(card, text=f"📅 {appt['date']}  |  🕒 {appt['time']}", font=("Arial", 12), text_color="#64748B").pack(anchor="w", padx=20, pady=(0, 15))

    def open_modal(self):
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.overlay.lift()

    def close_modal(self):
        self.overlay.place_forget()
        self.selected_time.set("")

    def quick_book(self, service_name):
        self.service_var.set(service_name)
        self.open_modal()

    def confirm_booking(self):
        if self.service_var.get() == "Choose a service" or not self.selected_time.get():
            messagebox.showwarning("Incomplete", "Please select a service and time.")
            return
        
        formatted_date = self.cal.get_date().strftime("%a, %b %d, %Y")
        new_appt = {
            "service": self.service_var.get(),
            "person": "Assigned Personnel",
            "date": formatted_date,
            "time": self.selected_time.get(),
            "status": "pending"
        }
        self.appointments.insert(0, new_appt)
        self.render_appointments()
        self.close_modal()
        messagebox.showinfo("Success", "Appointment Booked!")

if __name__ == "__main__":
    app = BarangayHealthApp()
    app.mainloop()