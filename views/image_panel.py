import tkinter as tk
from tkinter import Label, Frame

class ImagePanel:
    def __init__(self, root):
        self.frame = Frame(root, bg="#222")

        self.original_frame = Frame(self.frame, bg="#222", relief=tk.SUNKEN, bd=1)
        self.original_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)

        Label(self.original_frame, text="Original", bg="#222", fg="white").pack(pady=2)
        self.original_label = Label(self.original_frame, bg="#222")
        self.original_label.pack(fill="both", expand=True)

        self.processed_frame = Frame(self.frame, bg="#222", relief=tk.SUNKEN, bd=1)
        self.processed_frame.pack(side=tk.RIGHT, fill="both", expand=True, padx=5, pady=5)

        Label(self.processed_frame, text="Processada", bg="#222", fg="white").pack(pady=2)
        self.processed_label = Label(self.processed_frame, bg="#222")
        self.processed_label.pack(fill="both", expand=True)


    def show_original_image(self, image):
        self.original_label.config(image=image)
        self.original_label.image = image

    def show_processed_image(self, image):
        self.processed_label.config(image=image)
        self.processed_label.image = image