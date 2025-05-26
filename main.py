import customtkinter
from tkinter import *
from PIL import Image
import cv2 as cv
import os
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import datareader

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
        self.dataset = datareader.getdata()
        self.my_font = customtkinter.CTkFont(family="Corbel", size=25)
        self.bold_font = customtkinter.CTkFont(family="Corbel", size=35, weight="bold")
        self.info_font = customtkinter.CTkFont(family="Times New Roman", size=25, slant="italic")
        self.setup_ui()

    def setup_ui(self):
        self.root.title("CalTrack")
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
