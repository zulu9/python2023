# Tag 17 Tests
import tkinter as tk

root = tk.Tk()

root.title("My Windows")

window_width = 1280
window_height = 1024

centerX = 200
centerY = 200
root.geometry(f"{window_width}x{window_height}+{centerX}+{centerY}")

root.mainloop()
