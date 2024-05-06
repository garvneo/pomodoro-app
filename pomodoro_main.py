from tkinter import *
import pygame
# import pyttsx3
# import pywin32

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None
counting = None
pause_unpause = 0


# ---------------------------- TIMER RESET ------------------------------- #
def reset_action():
    global reps
    pygame.mixer.music.stop()
    window.after_cancel(timer)
    canvas.itemconfig(timer_watch, text="00:00")
    label["text"] = "Timer"
    check_mark.config(text="")
    reps = 0


# ---------------------------- Pause MECHANISM ------------------------------- #


def pause():
    global pause_unpause
    pause_unpause += 1
    if pause_unpause % 2 != 0:
        window.after_cancel(timer)
        pygame.mixer.music.stop()
        timer_display(counting)
        label["text"] = "Paused"
        pauseb.config(text="⏯︎")
    else:
        print("unpaused")
        label.config(text="No Chill,Work Only!")
        pauseb.config(text="⏸")
        count_down(counting)


# ---------------------------- TIMER MECHANISM ------------------------------- #

pygame.mixer.init()
# engine = pyttsx3.init()


def start_action():
    global reps
    reps += 1
    work_secs = WORK_MIN * 60
    short_break_secs = SHORT_BREAK_MIN * 60
    long_break_secs = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        label.config(
            text="Yay!Chill,but be back soon", fg=RED, font=(FONT_NAME, 40, "bold")
        )
        pygame.mixer.music.load("audio/gone.mp3")
        pygame.mixer.music.play(loops=0)
        count_down(long_break_secs)
    elif reps % 2 == 0:
        label.config(text="Time to Stretch!", fg=PINK)
        pygame.mixer.music.load("audio/pirates.mp3")
        pygame.mixer.music.play(loops=0)
        count_down(short_break_secs)
    else:
        label.config(text="No Chill,Work Only!", fg=GREEN, font=(FONT_NAME, 45, "bold"))
        # engine.say("No Chill,Work Only!")
        # engine.runAndWait()
        pygame.mixer.music.load("audio/start_up.mp3")
        pygame.mixer.music.play(loops=0)
        count_down(work_secs)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def timer_display(count):
    count_min = count // 60
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    print(f"{count_min}:{count_sec}")
    canvas.itemconfig(timer_watch, text=f"{count_min}:{count_sec}")


def count_down(count):
    global timer
    global counting
    counting = count
    timer_display(count)
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        start_action()
        marks = ""
        for _ in range(reps // 2):
            marks += "✔"

        check_mark["text"] = marks


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Garv's Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)
window.rowconfigure(2, minsize=40)  # Make 3rd row's height =40


# Label ------->

label = Label(text="TIMER", font=(FONT_NAME, 55, "bold"), bg=YELLOW, fg=GREEN)
label.grid(column=1, row=0)

# Start | Reset Buttons ------>

start = Button(
    text="Start",
    command=start_action,
    font=(FONT_NAME, 15, "bold"),
    fg=GREEN,
    bg=YELLOW,
    highlightthickness=0,
)
start.grid(column=0, row=4)

pauseb = Button(
    window,
    text="⏸️",
    command=lambda: pause(),
    font=(FONT_NAME, 15, "bold"),
    fg=GREEN,
    bg=YELLOW,
    highlightthickness=0,
)
pauseb.grid(column=1, row=4)

reset = Button(
    text="Reset",
    command=reset_action,
    font=(FONT_NAME, 15, "bold"),
    fg=GREEN,
    bg=YELLOW,
)
reset.grid(column=2, row=4)

# Check Marks ------>

check_mark = Label(font=(FONT_NAME, 15, "bold"), fg=GREEN, bg=YELLOW)
check_mark.grid(column=1, row=3)

# Canvas ------>
canvas = Canvas(width="260", height="224", bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="images/moon_mountain_animated.png")
canvas.create_image(130, 112, image=tomato_img)
timer_watch = canvas.create_text(
    132, 165, text="00:00", fill="white", font=(FONT_NAME, 32, "bold")
)
canvas.grid(column=1, row=1)


window.mainloop()
