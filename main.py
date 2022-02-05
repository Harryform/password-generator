from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_list = password_letters + password_symbols + password_numbers

    shuffle(password_list)
    password = "".join(password_list)
    password_input.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    web_info = web_input.get().title()
    email_info = email_input.get()
    password_info = password_input.get()
    new_data = {
        web_info: {
            "email": email_info,
            "password": password_info,
        }
    }

    if len(web_info) == 0 or len(password_info) == 0:
        messagebox.showerror(title="Uh Oh", message="Please don't leave any fields empty")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", "w") as data_file:
                # Saving update data
                json.dump(data, data_file, indent=4)
        finally:
            web_input.delete(0, END)
            password_input.delete(0, END)
            web_input.focus()

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="white")


def find_password():
    website = web_input.get().title()
    try:
        with open("data.json") as data_file:
            # Reading old data
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No data file found.")
    else:
        if website in data:
            email = data[website]['email']
            password = data[website]['password']
            messagebox.showinfo(title=website, message=f"Email: {email}\n Password: {password}")
        else:
            messagebox.showerror(title="Sorry", message=f"No details for {website} exists")


canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

web_label = Label(text="Website:", bg="white", fg="black")
web_label.grid(column=0, row=1)
email_label = Label(text="Email/Username:", bg="white", fg="black")
email_label.grid(column=0, row=2)
password_label = Label(text="Password:", bg="white", fg="black")
password_label.grid(column=0, row=3)

web_input = Entry(width=20, fg="black", bg="white", highlightbackground="grey")
web_input.grid(row=1, column=1)
web_input.focus()
email_input = Entry(width=35, fg="black", bg="white", highlightbackground="grey")
email_input.grid(row=2, column=1, columnspan=2)
email_input.insert(0, "Harryformus@gmail.com")
password_input = Entry(width=20, fg="black", bg="white", highlightbackground="grey")
password_input.grid(row=3, column=1)

generate_button = Button(width=11, text="Generate Password",
                         highlightbackground="white", fg="black", command=generate_password)
generate_button.grid(column=2, row=3)
add_button = Button(width=33, text="Add", highlightbackground="white", fg="black", command=save)
add_button.grid(column=1, row=4, columnspan=2)
search_button = Button(width=11, text="Search", highlightbackground="white", fg="black", command=find_password)
search_button.grid(column=2, row=1)


window.mainloop()
