from tkinter import ttk
import tkinter as tk
from ttkthemes import ThemedStyle
import keybinds

class GUI:
    def __init__(self, master):
        self.master = master
        self.master.wm_attributes("-topmost", True)
        self.title_prefix = "W32 Flyhack v3.1    |    "
        self.master.geometry("400x200")

        style = ThemedStyle(self.master)
        style.theme_use('black')

        # Create a frame
        frame = ttk.Frame(self.master, padding=1)
        frame.pack(fill="both", expand=True)

        # Create a frame for X, Y, and Z coordinates
        coord_frame = ttk.LabelFrame(frame, text="Coordinates", borderwidth=2, relief="solid", padding=0)
        coord_frame.grid(row=0, column=0, padx=(5,0), pady=5, sticky='w')

        x_label = ttk.Label(coord_frame, text="X:")
        x_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.x_coord = tk.StringVar()
        x_display = ttk.Label(coord_frame, textvariable=self.x_coord)
        x_display.grid(row=0, column=1, sticky="e", padx=0, pady=5)

        y_label = ttk.Label(coord_frame, text="Y:")
        y_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)

        self.y_coord = tk.StringVar()
        y_display = ttk.Label(coord_frame, textvariable=self.y_coord)
        y_display.grid(row=1, column=1, sticky="e", padx=0, pady=5)

        z_label = ttk.Label(coord_frame, text="Z:")
        z_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)

        self.z_coord = tk.StringVar()
        z_display = ttk.Label(coord_frame, textvariable=self.z_coord)
        z_display.grid(row=2, column=1, sticky="e", padx=0, pady=5)

        # Flight Frame
        flight_frame = ttk.LabelFrame(frame, text="Flight", borderwidth=2, relief="solid", padding=0)
        flight_frame.grid(row=0, column=1, padx=(5,0), pady=5, sticky='e')

        # Create a slider from 0 to 16
        speed_label = ttk.Label(flight_frame, text="Flight Speed:")
        speed_label.grid(row=1, column=0, sticky="w", padx=5, pady=10)

        self.speed_value = tk.DoubleVar(value=0.0)
        speed_slider = ttk.Scale(flight_frame, from_=0.0, to=1.0, variable=self.speed_value)
        speed_slider.set(0.25)
        speed_slider.grid(row=1, column=1, sticky="w", padx=0, pady=10)

        # Create a toggle button that toggles a boolean value
        toggle_label = ttk.Label(flight_frame, text=f"Toggle Button [{keybinds.toggle_key.upper()}]:")
        toggle_label.grid(row=2, column=0, sticky="w", padx=10, pady=10)

        self.toggle_value = tk.BooleanVar()
        toggle_button = ttk.Checkbutton(flight_frame, variable=self.toggle_value, command=self.toggle_label)
        toggle_button.grid(row=2, column=1, sticky="w", padx=10, pady=10)

        # Create a label for when the toggle button has been clicked
        self.toggle_label_var = tk.StringVar()
        self.toggle_label_var.set("")
        self.toggle_label = ttk.Label(flight_frame, textvariable=self.toggle_label_var)
        self.toggle_label.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=10)

    def toggle_label(self):
        if self.toggle_value.get():
            self.toggle_label_var.set("Flying Enabled!")
        else:
            self.toggle_label_var.set("")

    def updateXYZ(self, x, y, z):
        self.x_coord.set("{:.4f}".format(x))
        self.y_coord.set("{:.4f}".format(y))
        self.z_coord.set("{:.4f}".format(z))

    def attachedTitle(self):
        self.master.title(gui.title_prefix+"Attached!")

    def detachedTitle(self):
        self.master.title(self.title_prefix+"Not Attached!")