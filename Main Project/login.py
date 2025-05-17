from tkinter import *
from tkinter import messagebox
from PIL import ImageTk

# Function
def login():
    if username_entry.get() == '' or password_entry.get() == '':
        messagebox.showerror('Error', 'Fields cannot be empty')
    elif username_entry.get() == 'shadman' and password_entry.get() == '1234':
        messagebox.showinfo('Success', 'Welcome')
        window.destroy()
        import main
    else:
        messagebox.showerror('Error', 'Please enter correct credentials')


# GUI
# Window
window = Tk()
window.geometry('1280x700+35+15')
window.title('Login System of Student Management System')
window.resizable(False, False)

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

# Login Button
login_button = Button(login_frame, text = 'Login', font = ('Arial', 16, 'bold'), width = 15, fg = '#ECF0F1', activeforeground = '#ECF0F1' , bg = '#555555', activebackground = '#444444', cursor = 'hand2', command = login)
login_button.grid(row = 3, columnspan = 2, pady = 10)

window.mainloop()