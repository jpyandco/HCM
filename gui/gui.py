import tkinter as tk


class GUI:
    def __init__(self) -> None:
        self.root = None

    def start_gui(self):
        root = tk.Tk()
        root.title("Best Program in the World!")
        label = tk.Label(root, text="Task not started")
        label.pack(pady=10)

        # in func?
        # button = tk.Button(root, text="Create File", command=lambda: create_file_gui(label))
        # button.pack(pady=10)
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
