import tkinter as tk
from tkinter import Menu
from time import strftime
from PIL import Image, ImageTk, ImageOps
import numpy as np


clock_buf = True
clock_canvas = None

def on_click(event):
    current_text = entry.get()
    clicked_text = event.widget.cget("text")

    if clicked_text == "=":
        try:
            result = eval(current_text)
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
        except Exception as e:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Błąd")

    elif clicked_text == "C":
        entry.delete(0, tk.END)

    else:
        entry.insert(tk.END, clicked_text)

# Funkcja aktualizująca czas
def update_time():
    current_time = strftime('%H:%M:%S')
    time_label.config(text=current_time)
    time_label.after(100, update_time)  # Aktualizuj co 1000 ms (1 sekunda)
    change_clock()

def new_theme():
    if root.cget("bg") == "black":
        background_color = "white"
        text_color = "black"
    else:
        background_color = "black"
        text_color = "white"


    print(root.cget("bg"))

    # Zmiana koloru tła dla okna głównego
    root.configure(bg=background_color)

    # Zmiana koloru tła dla pola tekstowego
    entry.configure(bg=background_color, fg=text_color)  # Ustawienie koloru tekstu na biały

    # Zmiana koloru tła dla przycisków
    for button in buttons:
        button.configure(bg=background_color, fg=text_color)  # Ustawienie koloru tekstu na biały

    # Zmiana koloru tła dla zegara
    time_label.configure(bg=background_color, fg=text_color)  # Ustawienie koloru tekstu na biały


def clock_angles(hour, minute, second):
    if hour > 12:
        hour -= 12

    if not (0 <= hour <= 12) or not (0 <= minute < 60):
        raise ValueError("Invalid input values")

    hour_angle = 0.5 * (60 * hour + minute)
    minute_angle = 6 * minute
    second_angle = 6 * second



    return hour_angle, minute_angle, second_angle


def change_clock_buf():
    global clock_buf
    if clock_buf:
        clock_buf = False
    else:
        clock_buf = True

def change_clock():
    global clock_buf
    global clock_canvas

    if clock_buf:
        try:
            clock_canvas.grid_forget()
        except:
            pass
        time_label.grid(row=5, column=0, columnspan=3, sticky="nsew")


    else:
        # Remove the label and display the clock image
        try:
            time_label.grid_forget()
        except:
            pass

        try:
            clock_canvas.grid_forget()
        except:
            pass

        if True:
            # Create the canvas and load the image
            clock_canvas = tk.Canvas(root, width=200, height=200, bg=root.cget("bg"))
            clock_canvas.grid(row=5, column=0,columnspan=3, sticky="nsew")
            img = Image.open("clock.png")
            img = img.resize((200, 200))
            if root.cget("bg") == "black":
                img = ImageOps.invert(img)
            img = ImageTk.PhotoImage(img)
            clock_canvas.create_image(0, 0, image=img, anchor="nw")
            clock_canvas.image = img  # Keep a reference to the image

            H = int(strftime('%H'))
            M = int(strftime('%M'))
            S = int(strftime('%S'))
            angle_H, angle_M, angle_S = clock_angles(H, M,S)
            clock_canvas.create_line(100, 100, 100 + 40 * np.sin(np.radians(angle_H)), 100 - 40 * np.cos(np.radians(angle_H)), fill="red", width=3)
            clock_canvas.create_line(100, 100, 100 + 60 * np.sin(np.radians(angle_M)), 100 - 60 * np.cos(np.radians(angle_M)), fill="blue", width=3)
            clock_canvas.create_line(100, 100, 100 + 70 * np.sin(np.radians(angle_S)), 100 - 70 * np.cos(np.radians(angle_S)), fill="green", width=2)









root = tk.Tk()
root.title("Kalkulator")
root.configure(bg="white")
# Pasek menu
menubar = Menu(root)
root.config(menu=menubar)

file_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Plik", menu=file_menu)
file_menu.add_command(label="Zmień motyw", command=new_theme)
file_menu.add_command(label="Zmień zegar", command=change_clock_buf)
file_menu.add_separator()
file_menu.add_command(label="Zamknij", command=root.destroy)

# Pole tekstowe
entry = tk.Entry(root, font=("Helvetica", 16), justify="right")
entry.grid(row=0, column=0, columnspan=4)

# Przyciski kalkulatora
buttons_text = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('C', 4, 2), ('+', 4, 3),
    ('=', 5, 3)
]

buttons = []
for (text, row, col) in buttons_text:
    button = tk.Button(root, text=text,background="white", font=("Helvetica", 16), padx=20, pady=20)
    button.grid(row=row, column=col, sticky="nsew")
    button.bind("<Button-1>", on_click)
    buttons.append(button)

# Dodanie zegara
time_label = tk.Label(root, font=("Helvetica", 14), background="white", relief="ridge", borderwidth=1,width=10, height=9)
time_label.grid(row=5, column=0, columnspan=3, sticky="nsew")



# Uruchomienie funkcji aktualizującej czas
update_time()

# Uruchomienie głównej pętli programu
root.mainloop()
