# IMPORTS
from tkinter import *
import ttkthemes
from tkinter import ttk, messagebox
from PIL import ImageTk
import pymysql

# DATABASE CONNECTION FUNCTIONS
def create_database():
    try:
        conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password=''
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS user_info")
        conn.commit()
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to create database:\n{e}")
        window.destroy()

def connect_database():
    return pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='user_info'
    )

def create_users_table():
    try:
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(100) NOT NULL
            )
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", f"Table creation failed:\n{e}")

# LOGIN FUNCTION
show_password = False

def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == '' or password == '':
        messagebox.showerror('Error', 'Fields cannot be empty')
        return

    try:
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            messagebox.showinfo('Success', 'Welcome!')
            window.destroy()
            import sms
        else:
            messagebox.showerror('Error', 'Invalid credentials')
    except Exception as e:
        messagebox.showerror('Database Error', f'Error: {e}')


def toggle_password_visibility():
    global show_password
    if show_password:
        password_entry.config(show='*')
        toggle_button.config(image=eye_closed_image)
        show_password = False
    else:
        password_entry.config(show='')
        toggle_button.config(image=eye_open_image)
        show_password = True



# REGISTER FUNCTION
def open_register_window():
    def toggle_password_visibility(entry, button, state):
        # Toggle password visibility
        if state[0]:
            entry.config(show='*')
            button.config(image=eye_closed_image)
            state[0] = False
        else:
            entry.config(show='')
            button.config(image=eye_open_image)
            state[0] = True

    def submit_registration():
        user = username_entry_reg.get()
        pwd = password_entry_reg.get()
        confirm_pwd = confirm_password_entry.get()

        if user == '' or pwd == '' or confirm_pwd == '':
            messagebox.showerror('Error', 'All fields are required', parent=register_window)
        elif pwd != confirm_pwd:
            messagebox.showerror('Error', 'Passwords do not match', parent=register_window)
        else:
            try:
                conn = connect_database()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (user, pwd))
                conn.commit()
                conn.close()
                messagebox.showinfo('Success', 'Registered successfully!', parent=register_window)
                register_window.destroy()
            except pymysql.err.IntegrityError:
                messagebox.showerror('Error', 'Username already exists', parent=register_window)
            except Exception as e:
                messagebox.showerror('Error', f'Something went wrong: {e}', parent=register_window)

    # Create Register Window
    register_window = Toplevel(window)
    register_window.title('Register')
    register_window.geometry('450x400+500+200')
    register_window.config(bg='#f0f0f0')

    Label(register_window, text='Register Here', font=('Arial', 20, 'bold'), bg='#f0f0f0').pack(pady=10)

    # Username
    Label(register_window, text='Username:', bg='#f0f0f0').pack(pady=5)
    username_entry_reg = Entry(register_window, font=('Arial', 12), width=25)
    username_entry_reg.pack(pady=5)

    # Password
    Label(register_window, text='Password:', bg='#f0f0f0').pack(pady=5)
    password_frame = Frame(register_window, bg='#f0f0f0')
    password_frame.pack()
    password_entry_reg = Entry(password_frame, font=('Arial', 12), show='*', width=21)
    password_entry_reg.pack(side=LEFT, pady=5)
    pass_state = [False]
    pass_toggle_button = Button(password_frame, image=eye_closed_image, bd=0, bg='#f0f0f0', activebackground='#f0f0f0',
    command=lambda: toggle_password_visibility(password_entry_reg, pass_toggle_button, pass_state))
    pass_toggle_button.pack(side=LEFT, padx=5)

    # Confirm Password
    Label(register_window, text='Confirm Password:', bg='#f0f0f0').pack(pady=5)
    confirm_frame = Frame(register_window, bg='#f0f0f0')
    confirm_frame.pack()
    confirm_password_entry = Entry(confirm_frame, font=('Arial', 12), show='*', width=21)
    confirm_password_entry.pack(side=LEFT, pady=5)
    confirm_state = [False]
    confirm_toggle_button = Button(confirm_frame, image=eye_closed_image, bd=0, bg='#f0f0f0', activebackground='#f0f0f0',
    command=lambda: toggle_password_visibility(confirm_password_entry, confirm_toggle_button, confirm_state))
    confirm_toggle_button.pack(side=LEFT, padx=5)

    # Register Button
    ttk.Button(register_window, text='Register', command=submit_registration).pack(pady=20)


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
background_image = ImageTk.PhotoImage(file='image/background.jpg')
bg_label = Label(window, image=background_image)
bg_label.place(x=0, y=0)

# Frame
login_frame = Frame(window, bg='#ededed')
login_frame.place(x=400, y=150)

# Logo
logo_image = PhotoImage(file='image/graduated.png')
logo_label = Label(login_frame, image=logo_image)
logo_label.grid(row=0, column=0, columnspan=2, pady=10)

# Username
username_image = PhotoImage(file='image/user.png')
username_label = Label(login_frame, image=username_image, text='Username', compound=LEFT,
font=('Arial', 20, 'bold'), bg='#ededed')
username_label.grid(row=1, column=0, padx=10, pady=10)

username_entry = Entry(login_frame, font=('Arial', 16), bd=2)
username_entry.grid(row=1, column=1, padx=10, pady=10)

# Password
password_image = PhotoImage(file='image/pass.png')
password_label = Label(login_frame, image=password_image, text='Password', compound=LEFT,
font=('Arial', 20, 'bold'), bg='#ededed')
password_label.grid(row=2, column=0, padx=10, pady=10)

password_entry = Entry(login_frame, font=('Arial', 16), bd=2, show='*')
password_entry.grid(row=2, column=1, padx=10, pady=10)

eye_open_image = PhotoImage(file='image/eye_open.png')
eye_closed_image = PhotoImage(file='image/eye_closed.png')

toggle_button = Button(login_frame, image=eye_closed_image, bg='#ededed', bd=0, activebackground='#ededed', command=toggle_password_visibility)
toggle_button.grid(row=2, column=2, padx=5)


# Login Button
style.configure("LoginButton.TButton", font=("Arial", 12))
login_button = ttk.Button(login_frame, text='Login', width=15, style='LoginButton.TButton', command=login)
login_button.grid(row=3, column=1, pady=10)

# Register Prompt Label
register_label = Label(
    login_frame,
    text="Don't have credentials? Register!",
    font=('Arial', 12, 'underline'),
    fg='blue',
    bg='#ededed',
    cursor='hand2'
)
register_label.grid(row=3, column=0)
register_label.bind('<Button-1>', lambda event: open_register_window())

try:
    create_database()
    create_users_table()
except Exception as e:
    messagebox.showerror("Database Error", f"Unable to setup MySQL:\n{e}")
    window.destroy()

window.mainloop()