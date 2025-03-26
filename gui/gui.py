from configparser import ConfigParser
import tkinter as tk
import ttkbootstrap as ttk

from hcm.const import CONFIG
from hcm.hcm_handler_current import HCMHandlerCurrent
from hcm.hcm_handler_new import HCMHandlerNew
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
        content_frame = ttk.Frame(root, padding="20")
        content_frame.grid(row=0, column=0, padx=5, pady=5)
        # content_frame.pack(fill="both", expand=True)
        label = tk.Label(root, text="Task not started")
        root.geometry("400x400")
        # label.pack(pady=10)
        self.root = content_frame  # root  #

        self.headers_form()
        root.mainloop()

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

        ttk.Label(self.root, text="Headers sucessfully set as default!").grid(row=8, column=0)

    def headers_form(self):
        print(self.header_defaults)
        ttk.Label(self.root, text="Customizable Headers:", font="bold").grid(row=0, column=1, sticky="w")

        ttk.Label(self.root, text="Name:").grid(row=1, column=0, padx=5)
        self.name_entry = ttk.Entry(self.root)
        self.name_entry.grid(row=1, column=1, pady=5)
        self.name_entry.insert(0, self.header_defaults.get("person"))

        ttk.Label(self.root, text="Phone:").grid(row=2, column=0, padx=5)
        self.phone_entry = ttk.Entry(self.root)
        self.phone_entry.grid(row=2, column=1, pady=5)
        self.phone_entry.insert(0, self.header_defaults.get("phone"))

        ttk.Label(self.root, text="Email:").grid(row=3, column=0, padx=5)
        self.email_entry = ttk.Entry(self.root)
        self.email_entry.grid(row=3, column=1, pady=5)
        self.email_entry.insert(0, self.header_defaults.get("email"))

        ttk.Label(self.root, text="Fax:").grid(row=4, column=0, padx=5)
        self.fax_entry = ttk.Entry(self.root)
        self.fax_entry.grid(row=4, column=1, pady=5)
        self.fax_entry.insert(0, self.header_defaults.get("fax"))

        ttk.Button(self.root, text="Start File creation", command=lambda: self.start_file_creation()).grid(
            row=6, columnspan=2, column=0, padx=5, pady=5, sticky="w"
        )
        ttk.Button(self.root, text="Set Headers as default", command=lambda: self.set_headers_as_default()).grid(
            row=5, columnspan=2, column=0, padx=5, pady=5, sticky="w"
        )
        ttk.Button(
            self.root, text="Start File creation in new format", command=lambda: self.start_file_creation_new()
        ).grid(row=7, columnspan=2, padx=5, column=0, pady=5, sticky="w")

    def start_file_creation(self):
        headers = HCMCustomizableHeaders(
            person=self.name_entry.get(),
            phone=self.phone_entry.get(),
            email=self.email_entry.get(),
            fax=self.fax_entry.get(),
        )
        hcm_handler = HCMHandlerCurrent(headers.model_dump())
        self.progress_label = ttk.Label(self.root, text="File creation started!")
        self.progress_label.grid(row=8, column=1, pady=5)
        hcm_handler.process()
        if hcm_handler.incorrect_dataset:
            self.progress_label = ttk.Label(self.root, text="File creation finished with errors!")
        else:
            self.progress_label = ttk.Label(self.root, text="File creation finished successfully!")

    def start_file_creation_new(self):
        headers = HCMCustomizableHeaders(
            person=self.name_entry.get(),
            phone=self.phone_entry.get(),
            email=self.email_entry.get(),
            fax=self.fax_entry.get(),
        )
        hcm_handler = HCMHandlerNew(headers.model_dump())
        self.progress_label = ttk.Label(self.root, text="File creation started!")
        self.progress_label.grid(row=9, column=0, pady=5)
        hcm_handler.process()
        if hcm_handler.incorrect_dataset:
            self.progress_label = ttk.Label(
                self.root, text=f"File creation finished with {len(hcm_handler.incorrect_dataset)} errors!"
            ).grid(row=9, column=0, pady=5)
        else:
            self.progress_label = ttk.Label(self.root, text="File creation finished successfully!").grid(
                row=9, column=0, pady=5
            )
