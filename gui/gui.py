from configparser import ConfigParser
import threading
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
        self.folder_path = self.config["Path"]["folder_path"]
        self.notification: ttk.Label = None

    def start_gui(self):
        root = ttk.Window(themename="cosmo")
        root.title("HCM File creation")
        content_frame = ttk.Frame(root, padding="20")
        content_frame.grid(row=0, column=0, padx=5, pady=5)
        label = tk.Label(root, text="Task not started")
        root.geometry("400x400")
        self.root = content_frame  # root  #

        self.headers_form()
        root.mainloop()

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

        if self.notification:
            self.notification.destroy()
        self.notification = ttk.Label(self.root, text="Headers sucessfully set as default!").grid(row=9, column=0)

    def headers_form(self):
        # print(self.header_defaults)
        ttk.Label(self.root, text="Config:", font="bold").grid(row=0, column=0, sticky="w")

        ttk.Label(self.root, text="Name:").grid(row=1, column=0, sticky="w")
        self.name_entry = ttk.Entry(self.root)
        self.name_entry.grid(row=1, column=1, pady=5, sticky="w")
        self.name_entry.insert(0, self.header_defaults.get("person"))

        ttk.Label(self.root, text="Phone:").grid(row=2, column=0, sticky="w")
        self.phone_entry = ttk.Entry(self.root)
        self.phone_entry.grid(row=2, column=1, pady=5, sticky="w")
        self.phone_entry.insert(0, self.header_defaults.get("phone"))

        ttk.Label(self.root, text="Email:").grid(row=3, column=0, sticky="w")
        self.email_entry = ttk.Entry(self.root)
        self.email_entry.grid(row=3, column=1, pady=5, sticky="w")
        self.email_entry.insert(0, self.header_defaults.get("email"))

        ttk.Label(self.root, text="Fax:").grid(row=4, column=0, sticky="w")
        self.fax_entry = ttk.Entry(self.root)
        self.fax_entry.grid(row=4, column=1, pady=5, sticky="w")
        self.fax_entry.insert(0, self.header_defaults.get("fax"))

        ttk.Label(self.root, text="Folder Path:").grid(row=5, column=0, sticky="w")
        self.folder_entry = ttk.Entry(self.root)
        self.folder_entry.grid(row=5, column=1, pady=5, sticky="w")
        self.folder_entry.insert(0, self.folder_path)

        ttk.Button(self.root, text="Start File creation", command=lambda: self.start_file_creation()).grid(
            row=7, columnspan=4, column=0, padx=5, pady=5, sticky="w"
        )
        ttk.Button(self.root, text="Set Headers as default", command=lambda: self.set_headers_as_default()).grid(
            row=6, column=0, padx=5, pady=5, sticky="w"
        )
        ttk.Button(
            self.root, text="Start File creation in new format", command=lambda: self.button_file_creation_new()
        ).grid(row=8, columnspan=2, padx=5, column=0, pady=5, sticky="w")

        ttk.Button(self.root, text="Set Folder Path", command=lambda: self.set_folder_path()).grid(
            row=6, column=1, padx=5, pady=5, sticky="w"
        )

    def set_folder_path(self):
        folder_path = self.folder_entry.get()
        self.config.set("Path", "folder_path", folder_path)
        print(folder_path)

        with open("config.ini", "w") as file:
            self.config.write(file)

        if self.notification:
            self.notification.destroy()
        self.notification = ttk.Label(self.root, text="Folder Path sucessfully set as default!").grid(row=9, column=0)

    def start_file_creation(self):
        headers = HCMCustomizableHeaders(
            person=self.name_entry.get(),
            phone=self.phone_entry.get(),
            email=self.email_entry.get(),
            fax=self.fax_entry.get(),
        )
        hcm_handler = HCMHandlerCurrent(headers.model_dump())
        # self.progress_label = ttk.Label(self.root, text="File creation started!")
        # self.progress_label.grid(row=8, column=1, pady=5)
        hcm_handler.process()
        if hcm_handler.incorrect_dataset:
            self.progress_label = ttk.Label(
                self.root, text=f"File creation finished with {len(hcm_handler.incorrect_dataset)} errors!"
            ).grid(row=9, column=0, pady=5)
        else:
            self.progress_label = ttk.Label(self.root, text="File creation finished successfully!").grid(
                row=9, column=0, pady=5
            )

    def button_file_creation_new(self):
        thread = threading.Thread(target=self.start_file_creation_new())
        thread.start()

    def start_file_creation_new(self):
        headers = HCMCustomizableHeaders(
            person=self.name_entry.get(),
            phone=self.phone_entry.get(),
            email=self.email_entry.get(),
            fax=self.fax_entry.get(),
        )
        hcm_handler = HCMHandlerNew(headers.model_dump())
        # self.progress_label = ttk.Label(self.root, text="File creation started!")
        # self.progress_label.grid(row=9, column=0, pady=5)
        hcm_handler.process()
        if self.notification:
            self.notification.destroy()

        # self.progress_label.destroy()

        if hcm_handler.incorrect_dataset:
            self.progress_label = ttk.Label(
                self.root, text=f"File creation finished with {len(hcm_handler.incorrect_dataset)} errors!"
            ).grid(row=9, column=0, pady=5)
        else:
            self.progress_label = ttk.Label(self.root, text="File creation finished successfully!").grid(
                row=9, column=0, pady=5
            )
