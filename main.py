import customtkinter
from tkinter import *
from PIL import Image
import cv2 as cv
import os
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
customtkinter.set_default_color_theme("site.json")

class CalTrackApp:
    def __init__(self, root):
        self.root = root
        self.sex = "Female"
        self.active = "Sedentary"
        self.BMR = 0
        self.home_bool = True
        self.calc_bool = False
        self.display_bool = False
        self.total = 0
        self.meterlevel = 0
        self.my_font = customtkinter.CTkFont(family="Corbel", size=25)
        self.bold_font = customtkinter.CTkFont(family="Corbel", size=35, weight="bold")
        self.info_font = customtkinter.CTkFont(family="Times New Roman", size=25, slant="italic")
        self.setup_ui()

    def setup_ui(self):
        self.root.title("LeCalTrack")
        self.root.geometry("1200x800")
        # Navigation bar
        self.navbar = customtkinter.CTkFrame(master=self.root, width=1300, height=100)
        self.home_button = customtkinter.CTkButton(self.navbar, corner_radius=0, height=100, text="Home",font=self.my_font, fg_color="transparent",anchor=CENTER, command=self.showhome)
        self.display_button = customtkinter.CTkButton(self.navbar, corner_radius=0, height=100, text="Display", font=self.my_font, fg_color="transparent", anchor=CENTER, command=self.showdisplay)
        self.calc_button = customtkinter.CTkButton(self.navbar, corner_radius=0, height=100, text="Calculate",font=self.my_font, fg_color="transparent",border_width=2, border_color=("#65735e", "#687d96"),anchor=CENTER, command=self.showcalculate)
        self.navbar.place(relx=0.5, rely=0, anchor=CENTER)
        self.home_button.place(relx=0.59, rely=0.25)
        self.display_button.place(relx=0.8, rely=0.25)
        self.calc_button.place(relx=0.695, rely=0.25)
        # Tabs
        self.home_tab = customtkinter.CTkTabview(master=self.root, width=1200, height=800, fg_color="transparent")
        self.display_tab = customtkinter.CTkTabview(master=self.root, width=1200, height=800, fg_color="transparent")
        self.calculate_tab = customtkinter.CTkTabview(master=self.root, width=1200, height=800, fg_color="transparent")
        self.home_tab.place(relx=0.5, rely=0.52, anchor=CENTER)
        # Info button and tabview
        self.info_button = customtkinter.CTkButton(self.root, width=30, height=40, corner_radius=100, text="i", font=self.info_font, border_spacing=0, command=self.showinfo)
        self.tabview = customtkinter.CTkTabview(master=self.root, width=400, height=180, fg_color=("#D4C9A8", "#2d4a6e"), border_width=0)
        self.info_button.place(relx=0.95, rely=0.95, anchor=CENTER)
        # Light switch
        self.switch_var = customtkinter.StringVar(value="on")
        self.dark_switch = customtkinter.CTkSwitch(master=self.root, switch_width=50, switch_height=30, text="Dark", text_color=("#635323", "#8ea3bf"), font=("Corbel", 25), command=self.switch_event, variable=self.switch_var, onvalue="on", offvalue="off")
        self.dark_switch.place(relx=0.1, rely=0.95, anchor=CENTER)


        self.calc_labels = customtkinter.CTkLabel(
            self.calculate_tab,
            text="Gender:\n\nAge:\n\nWeight:",
            text_color="#444444",
            font=self.bold_font,
            justify='right'
        )

        self.calc_labels2 = customtkinter.CTkLabel(
            self.calculate_tab,
            text="Height:\n\nActivity:",
            text_color="#444444",
            font=self.bold_font,
            justify='right'
        )


        self.gender_menu = customtkinter.CTkOptionMenu(
            self.calculate_tab,
            values=["Female", "Male"],
            command=self.get_gender,
            height=45,
            width=220,
            font=self.my_font,
            fg_color="#D6E4F0",
            button_color="#4B6587",
            dropdown_fg_color="#EDF2FB"
        )

        self.age_entry = customtkinter.CTkEntry(
            self.calculate_tab,
            placeholder_text="22",
            height=45,
            width=220,
            font=self.my_font,
            fg_color="#F5F5F5",
            text_color="#1A1A1A"
        )

        self.weight_entry = customtkinter.CTkEntry(
            self.calculate_tab,
            placeholder_text="60",
            height=45,
            width=220,
            font=self.my_font,
            fg_color="#F5F5F5",
            text_color="#1A1A1A"
        )

        self.height_entry = customtkinter.CTkEntry(
            self.calculate_tab,
            placeholder_text="170",
            height=45,
            width=220,
            font=self.my_font,
            fg_color="#F5F5F5",
            text_color="#1A1A1A"
        )

        self.activity_menu = customtkinter.CTkOptionMenu(
            self.calculate_tab,
            values=["Sedentary", "Moderate", "Active"],
            command=self.get_activity,
            height=45,
            width=220,
            font=self.my_font,
            fg_color="#D6E4F0",
            button_color="#4B6587",
            dropdown_fg_color="#EDF2FB"
        )

        self.calc_submit_button = customtkinter.CTkButton(
            self.calculate_tab,
            width=240,
            height=60,
            corner_radius=14,
            text="Calculate",
            text_color="#FFFFFF",
            font=self.my_font,
            command=self.calculate_bmr_bmi,
            fg_color="#4B6587",
            hover_color="#3A4F6C"
        )

        self.bmr_result_label = customtkinter.CTkLabel(
            self.calculate_tab,
            text="",
            text_color="#2C2C2C",
            font=self.bold_font,
            justify='center'
        )

        self.bmi_result_label = customtkinter.CTkLabel(
            self.calculate_tab,
            text="",
            text_color="#2C2C2C",
            font=self.bold_font,
            justify='center'
        )

        self.calc_labels.place(relx=0.2, rely=0.42, anchor=CENTER)
        self.calc_labels2.place(relx=0.2, rely=0.59, anchor=CENTER)

        self.gender_menu.place(relx=0.45, rely=0.34, anchor=CENTER)
        self.age_entry.place(relx=0.45, rely=0.42, anchor=CENTER)
        self.weight_entry.place(relx=0.45, rely=0.50, anchor=CENTER)

        self.height_entry.place(relx=0.45, rely=0.59, anchor=CENTER)
        self.activity_menu.place(relx=0.45, rely=0.67, anchor=CENTER)

        self.calc_submit_button.place(relx=0.75, rely=0.50, anchor=CENTER)

        self.bmr_result_label.place(relx=0.5, rely=0.8, anchor=CENTER)
        self.bmi_result_label.place(relx=0.5, rely=0.87, anchor=CENTER)

        

        # Calorie goal selection
        self.goal_options = [
            "Maintain",
            "Mild weight loss (0.25 kg/week)",
            "Weight loss (0.5 kg/week)",
            "Extreme weight loss (1 kg/week)",
            "Mild weight gain (0.25 kg/week)",
            "Weight gain (0.5 kg/week)",
            "Fast weight gain (1 kg/week)"
        ]
        self.goal_dropdown = customtkinter.CTkOptionMenu(self.calculate_tab, values=self.goal_options, command=self.set_goal, width=320, font=self.my_font)
        self.goal_dropdown.place(relx=0.5, rely=0.87, anchor="center")
        self.selected_goal = "Maintain"
        self.calorie_goals = []
        self.calorie_goal_label = customtkinter.CTkLabel(self.calculate_tab, text="", font=self.my_font, text_color=("#796C47", "#8ea3bf"))
        self.calorie_goal_label.place(relx=0.5, rely=0.93, anchor="center")

        # TO DO: BMI chart 

        # Home tab UI
        try:
            self.home_title_image = customtkinter.CTkImage(light_image=Image.open("Images/title1.png"), dark_image=Image.open("Images/title2.png"), size=(850, 250))
            self.home_image_label = customtkinter.CTkLabel(self.home_tab, image=self.home_title_image, text="")
            self.home_image_label.place(relx=0.5, rely=0.31, anchor=CENTER)
        except Exception:
            pass
        # Upload and Capture buttons
        self.upload_button = customtkinter.CTkButton(self.home_tab, width=180, height=60, corner_radius=100, text="Upload", text_color=("#635323", "#8ea3bf"), font=self.my_font, command=self.upload_image, fg_color=("#D4C9A8", "#436791"), hover_color=("#c9bb91", "#36567d"))
        self.capture_button = customtkinter.CTkButton(self.home_tab, width=180, height=60, corner_radius=100, text="Capture", text_color=("#635323", "#8ea3bf"), font=self.my_font, command=self.capture_image, fg_color=("#D4C9A8", "#436791"), hover_color=("#c9bb91", "#36567d"))
        self.upload_button.place(relx=0.5, rely=0.55, anchor=CENTER)
        self.capture_button.place(relx=0.5, rely=0.65, anchor=CENTER)

        # Display tab UI
        try:
            self.display_banner_image = customtkinter.CTkImage(light_image=Image.open("Images/track1.png"), dark_image=Image.open("Images/track2.png"), size=(550, 290))
            self.display_image_label = customtkinter.CTkLabel(self.display_tab, image=self.display_banner_image, text="")
            self.display_image_label.place(relx=0.6, rely=0.23, anchor=CENTER)
        except Exception:
            pass
       