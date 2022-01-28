from tkinter import *
from tkinter import messagebox
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
FONT_LANG = ("Arial", 40, "italic")
FONT_WORD = ("Arial", 60, "bold")


# ---------------------------- MAIN LOGIC ------------------------------- #
try:
    data = pandas.read_excel("data/to_learn.xlsx")
except FileNotFoundError:
    data = pandas.read_excel("data/Flash.xlsx")
to_learn = data.to_dict(orient="records")
current_card = {}



def get_random_word():
    global flip_timer, current_card
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(flash_img, image=front_flash_img)
    canvas.itemconfig(guess_word, text=current_card["german"], fill="black")
    canvas.itemconfig(lang_word, text="German", fill="black")

    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(flash_img, image=back_flash_img)
    canvas.itemconfig(guess_word, text=current_card["polish"], fill="white")
    canvas.itemconfig(lang_word, text="Polish", fill="white")


def delete_card():
    if len(to_learn) <= 1:
        messagebox.showinfo(title="Nice!", message=f"You have learned all 8000 most frequently used words!")
    else:
        to_learn.remove(current_card)
        data = pandas.DataFrame(to_learn)
        data.to_excel("data/to_learn.xlsx", index=False)
        get_random_word()

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=525, bg=BACKGROUND_COLOR, highlightthickness=0)
front_flash_img = PhotoImage(file="images/card_front.png")
back_flash_img = PhotoImage(file="images/card_back.png")
flash_img = canvas.create_image(400, 263, image=front_flash_img)
lang_word = canvas.create_text(400, 150, text="Temp", font=FONT_LANG)
guess_word = canvas.create_text(400, 263, text="Temp", font=FONT_WORD)
canvas.grid(column=0, row=0, columnspan=2)

right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, highlightthickness=0, bd=0, command=delete_card)
right_button.grid(column=1, row=1)
wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, bd=0, command=get_random_word)
wrong_button.grid(column=0, row=1)

flip_timer = window.after(100, flip_card)

get_random_word()

window.mainloop()