# Tag 17 Tests
import tkinter as tk

root = tk.Tk()

root.title("My Window")

window_width = 1280
window_height = 1024
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

centerX = int(screen_width / 2 - window_width / 2)
centerY = int(screen_height / 2 - window_height / 2)
root.geometry(f"{window_width}x{window_height}+{centerX}+{centerY}")

root.mainloop()
