# Import required modules
from tkinter import *
import ttkthemes
from tkinter import ttk, messagebox
from PIL import ImageTk

# Function
def login():
    if username_entry.get() == '' or password_entry.get() == '':
        messagebox.showerror('Error', 'Fields cannot be empty')
    elif username_entry.get() == 'shadman' and password_entry.get() == '1234':
        messagebox.showinfo('Success', 'Welcome')
        window.destroy()
        import test
    else:
        messagebox.showerror('Error', 'Please enter correct credentials')


# GUI
# Window
window = ttkthemes.ThemedTk()
window.get_themes()
window.set_theme('radiance')

window.geometry('1280x700+35+15')
window.title('Login System of Student Management System')
window.resizable(False, False)

style = ttk.Style()

# Background
background_image = ImageTk.PhotoImage(file = 'Main Project/image/background.jpg')
bg_label = Label(window, image = background_image)
bg_label.place(x = 0, y = 0)

# Frame
login_frame = Frame(window, bg = '#ededed')
login_frame.place(x = 400, y = 150)

# Logo
logo_image = PhotoImage(file = 'Main Project/image/graduated.png')
logo_label = Label(login_frame, image = logo_image)
logo_label.grid(row = 0, column = 0, columnspan = 2, pady = 10)

# Username
username_image = PhotoImage(file = 'Main Project/image/user.png')
username_label = Label(login_frame, image = username_image, text = 'Username', compound = LEFT, font = ('Arial', 20, 'bold'), bg = '#ededed')
username_label.grid(row = 1, column = 0, padx = 10, pady = 10)

username_entry = Entry(login_frame, font = ('Arial', 16 ), bd = 2)
username_entry.grid(row = 1, column = 1, padx = 10, pady = 10)

# PassWord
password_image = PhotoImage(file = 'Main Project/image/pass.png')
password_label = Label(login_frame, image = password_image, text = 'Password', compound = LEFT, font = ('Arial', 20, 'bold'), bg = '#ededed')
password_label.grid(row = 2, column = 0, padx = 10, pady = 10)

password_entry = Entry(login_frame, font = ('Arial', 16 ), bd = 2, show = '*')
password_entry.grid(row = 2, column = 1, padx = 10, pady = 10)

def toggle_password():
    if password_entry.cget('show') == '*':
        password_entry.config(show='')
    else:
        password_entry.config(show='*')

show_pass_var = IntVar()
show_pass_check = Checkbutton(login_frame, text='Show Password', variable=show_pass_var, onvalue=1, offvalue=0,
bg='#ededed', command=toggle_password)
show_pass_check.grid(row=2, column=2, sticky='w')


# Login Button
style.configure("LoginButton.TButton", font=("Arial", 12))
login_button = ttk.Button(login_frame, text='Login', width = 15, style='LoginButton.TButton', command = login)
login_button.grid(row = 3, column = 1, pady = 10)

# Function to open register window
def open_register_window():
    register_window = Toplevel(window)
    register_window.title('Register')
    register_window.geometry('400x400+500+200')
    register_window.config(bg='#f0f0f0')
    Label(register_window, text='Register Here', font=('Arial', 20, 'bold'), bg='#f0f0f0').pack(pady=20)
    # You can add more widgets here like Entry for username, password etc.
    Label(register_window, text='(Registration form coming soon...)', font=('Arial', 12), bg='#f0f0f0').pack(pady=10)

# "Don't have an account?" label
register_label = Label(
    login_frame,
    text="Don't have an account?",
    font=('Arial', 12, 'underline'),
    fg='blue',
    bg='#ededed',
    cursor='hand2'
)
register_label.grid(row=3, column=0)
register_label.bind('<Button-1>', lambda event: open_register_window())


window.mainloop()