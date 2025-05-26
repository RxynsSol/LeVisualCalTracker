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
