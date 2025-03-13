from configparser import ConfigParser
import tkinter as tk
import ttkbootstrap as ttk

from hcm.const import CONFIG
from hcm.hcm_handler import HCMHandler
from hcm.model import HCMCustomizableHeaders


class GUI:
    def __init__(self) -> None:
        self.root = None
        self.config = ConfigParser()
        self.config.read(CONFIG)
        print(self.config)
        self.header_defaults = dict(self.config.items("File_Headers"))

    def start_gui(self):
        root = ttk.Window(themename="cosmo")
        root.title("HCM File creation")
        label = tk.Label(root, text="Task not started")
        root.geometry("400x300")
        # label.pack(pady=10)

        self.headers_form()
        root.mainloop()
        self.root = root

    def create_file_gui(label):
        file_list = ["gsm900"]
        # create_file(file_list[0])
        print("Files created successfully!")
        label.config(text="Task ended!")

    def say_hello(label):
        print("Hello, World!")
        label.config(text="Task ended!")

    def set_headers_as_default(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        fax = self.fax_entry.get()
        phone = self.phone_entry.get()
        print(self.fax_entry.get())
        self.config.set("File_Headers", "person", name)
        self.config.set("File_Headers", "phone", phone)
        self.config.set("File_Headers", "email", email)
        self.config.set("File_Headers", "fax", fax)

        with open("config.ini", "w") as file:
            self.config.write(file)

    def headers_form(self):
        print(self.header_defaults)
        ttk.Label(self.root, text="Name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1, pady=5)
        self.name_entry.insert(0, self.header_defaults.get("person"))

        ttk.Label(self.root, text="Phone:").grid(row=1, column=0)
        self.phone_entry = tk.Entry(self.root)
        self.phone_entry.grid(row=1, column=1, pady=5)
        self.phone_entry.insert(0, self.header_defaults.get("phone"))

        ttk.Label(self.root, text="Email:").grid(row=2, column=0)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.grid(row=2, column=1, pady=5)
        self.email_entry.insert(0, self.header_defaults.get("email"))

        ttk.Label(self.root, text="Fax:").grid(row=3, column=0)
        self.fax_entry = tk.Entry(self.root)
        self.fax_entry.grid(row=3, column=1, pady=5)
        self.fax_entry.insert(0, self.header_defaults.get("fax"))

        ttk.Button(self.root, text="Start File creation", command=lambda: self.start_file_creation()).grid(
            row=5, columnspan=2, pady=5
        )
        ttk.Button(self.root, text="Set Headers as default", command=lambda: self.set_headers_as_default()).grid(
            row=5, columnspan=4, pady=5, column=2
        )

    def start_file_creation(self):
        headers = HCMCustomizableHeaders(
            person=self.name_entry.get(),
            phone=self.phone_entry.get(),
            email=self.email_entry.get(),
            fax=self.fax_entry.get(),
        )
        hcm_handler = HCMHandler(headers.model_dump())
        hcm_handler.process()
