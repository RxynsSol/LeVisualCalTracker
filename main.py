import tkinter as tk
import customtkinter
from PIL import Image
import cv2 as cv
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import os
import dataReader

class CalorieTrackerApp:
    def __init__(self, root):
        self.root = root
        self.setup_app()
        self.create_widgets()
        self.setup_layout()
        
    def setup_app(self):
        """Initialize application settings"""
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("site.json")
        self.root.title("LeVisualCalTrack")
        self.root.geometry("1200x800")
        
        # Application state
        self.sex = "Female"
        self.active = "Sedentary"
        self.BMR = 0
        self.total = 0
        self.meterlevel = 0
        self.dataset = dataReader.getImageData()
        print(self.dataset)
        
        # Fonts
        self.my_font = customtkinter.CTkFont(family="Corbel", size=25)
        self.bold_font = customtkinter.CTkFont(family="Corbel", size=35, weight="bold")
        self.info_font = customtkinter.CTkFont(family="Times New Roman", size=25, slant="italic")

    def create_widgets(self):
        """Create all UI widgets"""
        # Main tab views
        self.home = customtkinter.CTkTabview(master=self.root, width=1200, height=800, fg_color="transparent")
        self.display = customtkinter.CTkTabview(master=self.root, width=1200, height=800, fg_color="transparent")
        self.calculate = customtkinter.CTkTabview(master=self.root, width=1200, height=800, fg_color="transparent")
        
        # Navigation bar
        self.create_navbar()
        
        # Home tab
        self.create_home_tab()
        
        # Calculate tab
        self.create_calculate_tab()
        
        # Display tab
        self.create_display_tab()
        
        # Info system
        self.create_info_system()

    def setup_layout(self):
        """Position the main widgets"""
        self.home.place(relx=0.5, rely=0.52, anchor=tk.CENTER)
        self.navbar.place(relx=0.5, rely=0, anchor=tk.CENTER)
        self.info_button.place(relx=0.95, rely=0.95, anchor=tk.CENTER)
        self.dark_switch.place(relx=0.1, rely=0.95, anchor=tk.CENTER)

    def create_navbar(self):
        """Create navigation bar and buttons"""
        self.navbar = customtkinter.CTkFrame(master=self.root, width=1300, height=100)
        
        self.home_button = customtkinter.CTkButton(
            self.navbar, corner_radius=0, height=100, text="Home",
            font=self.my_font, fg_color="transparent", anchor=tk.CENTER, 
            command=self.show_home
        )
        
        self.display_button = customtkinter.CTkButton(
            self.navbar, corner_radius=0, height=100, text="Display",
            font=self.my_font, fg_color="transparent", anchor=tk.CENTER,
            command=self.show_display
        )
        
        self.calc_button = customtkinter.CTkButton(
            self.navbar, corner_radius=0, height=100, text="Calculate",
            font=self.my_font, fg_color="transparent", border_width=2,
            border_color=("#65735e", "#687d96"), anchor=tk.CENTER,
            command=self.show_calculate
        )
        
        self.home_button.place(relx=0.59, rely=0.25)
        self.display_button.place(relx=0.8, rely=0.25)
        self.calc_button.place(relx=0.695, rely=0.25)

    def create_home_tab(self):
        """Create home tab widgets"""
        self.upload_button = customtkinter.CTkButton(
            self.home, width=180, height=60, corner_radius=100, text="Upload",
            text_color=("#635323","#8ea3bf"), font=self.my_font,
            command=self.upload_image, fg_color=("#D4C9A8","#436791"),
            hover_color=("#c9bb91","#36567d")
        )
        
        self.photo_button = customtkinter.CTkButton(
            self.home, width=180, height=60, corner_radius=100, text="Capture",
            text_color=("#635323","#8ea3bf"), font=self.my_font,
            command=self.capture_image, fg_color=("#D4C9A8","#436791"),
            hover_color=("#c9bb91","#36567d")
        )
        
        self.upload_button.place(relx=0.5, rely=0.55, anchor=tk.CENTER)
        self.photo_button.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

    def create_calculate_tab(self):
        """Create calculate tab widgets"""
        # Labels
        self.labels = customtkinter.CTkLabel(
            self.calculate, text="Gender\n\nAge (years)\n\nWeight (kg)",
            text_color=("#796C47","#8ea3bf"), font=self.bold_font, justify='left'
        )
        
        self.labels2 = customtkinter.CTkLabel(
            self.calculate, text="Height (cm)\n\nActivity",
            text_color=("#796C47","#8ea3bf"), font=self.bold_font, justify='left'
        )
        
        # Entry fields
        self.age = customtkinter.CTkEntry(
            self.calculate, placeholder_text="22", height=45, width=240,
            font=self.my_font
        )
        
        self.weight = customtkinter.CTkEntry(
            self.calculate, placeholder_text="60", height=45, width=240,
            font=self.my_font
        )
        
        self.height = customtkinter.CTkEntry(
            self.calculate, placeholder_text="170", height=45, width=240,
            font=self.my_font
        )
        
        # Dropdown menus
        self.gender = customtkinter.CTkOptionMenu(
            self.calculate, values=["Female", "Male"], command=self.get_gender,
            height=45, width=240, font=self.my_font
        )
        
        self.activity = customtkinter.CTkOptionMenu(
            self.calculate, values=["Sedentary", "Moderate", "Active"],
            command=self.get_activity, height=45, width=240, font=self.my_font
        )
        
        # Calculate button
        self.calc_button = customtkinter.CTkButton(
            self.calculate, width=240, height=60, corner_radius=100, text="Calculate",
            text_color=("#4c5e42","#8ea3bf"), font=self.my_font,
            command=self.calculate_bmr, fg_color=("#a8bd9d","#436791"),
            hover_color=("#92ab85","#36567d")
        )
        
        # Layout
        self.labels.place(relx=0.17, rely=0.50, anchor=tk.CENTER)
        self.labels2.place(relx=0.57, rely=0.435, anchor=tk.CENTER)
        self.gender.place(relx=0.37, rely=0.40, anchor=tk.CENTER)
        self.age.place(relx=0.37, rely=0.50, anchor=tk.CENTER)
        self.weight.place(relx=0.37, rely=0.60, anchor=tk.CENTER)
        self.height.place(relx=0.77, rely=0.40, anchor=tk.CENTER)
        self.activity.place(relx=0.77, rely=0.50, anchor=tk.CENTER)
        self.calc_button.place(relx=0.77, rely=0.61, anchor=tk.CENTER)

    def create_display_tab(self):
        """Create display tab widgets"""
        self.textbox = customtkinter.CTkTextbox(
            self.display, text_color=("#635323","#8ea3bf"), border_width=5,
            border_color=("#B6A77A","#8ea3bf"), border_spacing=6,
            height=375, width=650, font=("Corbel", 30), state="disabled"
        )
        self.textbox.place(relx=0.65, rely=0.6, anchor=tk.CENTER)
        
        # Initialize meter
        self.update_meter()

    def create_info_system(self):
        """Create info button and popup"""
        self.info_button = customtkinter.CTkButton(
            self.root, width=30, height=40, corner_radius=100, text="i",
            font=self.info_font, border_spacing=0, command=self.show_info
        )
        
        self.tabview = customtkinter.CTkTabview(
            master=self.root, width=400, height=180,
            fg_color=("#D4C9A8","#2d4a6e"), border_width=0
        )
        
        self.switch_var = customtkinter.StringVar(value="on")
        self.dark_switch = customtkinter.CTkSwitch(
            master=self.root, switch_width=50, switch_height=30, text="Dark",
            text_color=("#635323","#8ea3bf"), font=("Corbel", 25),
            command=self.switch_event, variable=self.switch_var,
            onvalue="on", offvalue="off"
        )

    def update_meter(self):
        """Update the calorie meter display"""
        if self.BMR != 0:
            self.meterlevel = self.total / self.BMR
        else:
            self.meterlevel = 0
            
        if self.meterlevel > 1:
            self.meterlevel = 1
            colors = "#7B2D29"
        else:
            colors = "#635323"
            
        # Example data - replace with actual tracking
        self.total = 1500
        totalstring = f"{self.total}/{self.BMR}"
        
        # Create meter components
        inside = customtkinter.CTkButton(
            self.display, height=550, width=250,
            border_color=("#35422E","#DEECFE"), border_width=4,
            corner_radius=0, text="", state="disabled", fg_color="transparent"
        )
        
        meter = customtkinter.CTkButton(
            self.display, height=self.meterlevel*550, width=250,
            border_color=("#35422E","#DEECFE"), border_width=4,
            corner_radius=0, text="", state="disabled"
        )
        
        trackedcal = customtkinter.CTkLabel(
            self.display, font=("Cordel",37), text_color=(colors,"#8ea3bf"),
            text=totalstring, fg_color="transparent"
        )
        
        # Place components
        inside.place(relx=0.2, rely=0.83, anchor='s')
        meter.place(relx=0.2, rely=0.83, anchor='s')
        trackedcal.place(relx=0.2, rely=0.9, anchor='s')

    def switch_event(self):
        """Toggle between light and dark mode"""
        if self.switch_var.get() == "off":
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

    def get_gender(self, choice):
        """Handle gender selection"""
        self.sex = self.gender.get()
        print("optionmenu dropdown clicked:", self.sex)

    def get_activity(self, choice):
        """Handle activity level selection"""
        self.active = self.activity.get()
        print("optionmenu dropdown clicked:", self.active)

    def update_info(self):
        """Update info popup content"""
        if hasattr(self, 'home_bool') and self.home_bool:
            infotext = "Upload your daily meals"
        elif hasattr(self, 'display_bool') and self.display_bool:
            infotext = "View your tracked meals"
        elif hasattr(self, 'calc_bool') and self.calc_bool:
            infotext = "Calculate your calories"
        else:
            infotext = "Welcome to LeVisualCalTrack"
            
        titlelabel = customtkinter.CTkLabel(
            master=self.tabview, text="Welcome", fg_color="transparent",
            font=("Corbel",30)
        )
        
        bodylabel = customtkinter.CTkLabel(
            master=self.tabview, text=infotext, fg_color="transparent",
            font=self.my_font
        )
        
        titlelabel.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        bodylabel.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def show_info(self):
        """Show info popup"""
        self.update_info()
        self.tabview.place(relx=0.75, rely=0.865, anchor=tk.CENTER)
        
        exit_button = customtkinter.CTkButton(
            master=self.tabview, corner_radius=100, height=50, width=50,
            text="Ok", font=("Corbel", 20), anchor=tk.CENTER,
            command=self.close_info
        )
        exit_button.place(relx=0.5, rely=0.78, anchor=tk.CENTER)

    def close_info(self):
        """Hide info popup"""
        self.tabview.place_forget()

    def show_home(self):
        """Show home tab"""
        self.home_bool = True
        self.calc_bool = False
        self.display_bool = False
        self.calculate.place_forget()
        self.display.place_forget()
        self.home.place(relx=0.5, rely=0.52, anchor=tk.CENTER)
        self.close_info()

    def show_display(self):
        """Show display tab"""
        self.home_bool = False
        self.calc_bool = False
        self.display_bool = True
        self.display.place(relx=0.5, rely=0.52, anchor=tk.CENTER)
        self.home.place_forget()
        self.calculate.place_forget()
        self.close_info()
        self.update_meter()

    def show_calculate(self):
        """Show calculate tab"""
        self.home_bool = False
        self.calc_bool = True
        self.display_bool = False
        self.calculate.place(relx=0.5, rely=0.52, anchor=tk.CENTER)
        self.home.place_forget()
        self.display.place_forget()
        self.close_info()

    def capture_image(self):
        """Capture image from camera"""
        cam = cv.VideoCapture(0)

        if not cam.isOpened():
            print("Camera not accessible")
            return None

        while True:
            ret, frame = cam.read()
            if not ret:
                print("Failed to grab frame")
                break
            
            cv.imshow('Press the spacebar to take a photo', frame)
            key = cv.waitKey(1)

            if key == ord('q'):
                print("Exiting...")
                break
            elif key == 32:  # Spacebar
                filename = "Captured.png"
                cwd = os.getcwd()
                taken_filepath = os.path.join(cwd, filename)
                cv.imwrite(taken_filepath, frame)
                print(f"Image saved at {taken_filepath}")
                cv.destroyWindow('Press the spacebar to take a photo')
                return taken_filepath
        
        cam.release()
        cv.destroyWindow('Press the spacebar to take a photo')
        return None

    def upload_image(self):
        """Handle image upload"""
        filetypes = [("Img Files", "*.png")]
        image_location = fd.askopenfilename(
            title='Open an image',
            initialdir='/',
            filetypes=filetypes
        )
        
        if image_location:
            self.analyze_image(image_location)

    def analyze_image(self, image_path):
        """Analyze uploaded/captured image"""
        print(f"Analyzing image: {image_path}")
        # Add your image analysis logic here

    def calculate_bmr(self):
        """Calculate BMR based on user inputs"""
        try:
            heavy = int(self.weight.get())
        except ValueError:
            heavy = 60
            
        try:
            old = int(self.age.get())
        except ValueError:
            old = 30
            
        try:
            tall = int(self.height.get())
        except ValueError:
            tall = 170

        if self.sex == "Female":
            self.BMR = 447.6 + (9.25 * heavy) + (3.10 * tall) - (4.33 * old)
        else:
            self.BMR = 88.4 + (13.4 * heavy) + (4.8 * tall) - (5.68 * old)
            
        if self.active == "Sedentary":
            self.BMR *= 1.2
        elif self.active == "Moderate":
            self.BMR *= 1.375
        elif self.active == "Active":
            self.BMR *= 1.55
            
        self.BMR = int(self.BMR)
        textbmr = f"You are recommended to consume {round(self.BMR,0)} calories daily."
        
        displaybmr = customtkinter.CTkLabel(
            self.calculate, text=textbmr,
            text_color=("#796C47","#8ea3bf"), font=self.bold_font,
            justify='left'
        )
        displaybmr.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

if __name__ == "__main__":
    root = customtkinter.CTk()
    app = CalorieTrackerApp(root)
    root.mainloop()