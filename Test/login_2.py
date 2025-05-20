# Import required modules
from tkinter import *
import ttkthemes
from tkinter import ttk, messagebox
from PIL import ImageTk
import pymysql

# ---------------- DATABASE CONNECTION FUNCTION ---------------- #
def connect_database():
    return pymysql.connect(
        host='localhost',
        port=3307,
        user='root',
        password='',
        database='student_system'
    )


# ---------------- LOGIN FUNCTION ---------------- #
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
            import test
        else:
            messagebox.showerror('Error', 'Invalid credentials')
    except Exception as e:
        messagebox.showerror('Database Error', f'Error: {e}')


# ---------------- REGISTER FUNCTION ---------------- #
def open_register_window():
    def submit_registration():
        user = username_entry_reg.get()
        pwd = password_entry_reg.get()
        if user == '' or pwd == '':
            messagebox.showerror('Error', 'All fields are required', parent=register_window)
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

    register_window = Toplevel(window)
    register_window.title('Register')
    register_window.geometry('400x300+500+200')
    register_window.config(bg='#f0f0f0')

    Label(register_window, text='Register Here', font=('Arial', 20, 'bold'), bg='#f0f0f0').pack(pady=10)

    # Username
    Label(register_window, text='Username:', bg='#f0f0f0').pack(pady=5)
    username_entry_reg = Entry(register_window, font=('Arial', 12))
    username_entry_reg.pack(pady=5)

    # Password
    Label(register_window, text='Password:', bg='#f0f0f0').pack(pady=5)
    password_entry_reg = Entry(register_window, font=('Arial', 12), show='*')
    password_entry_reg.pack(pady=5)

    # Register Button
    ttk.Button(register_window, text='Register', command=submit_registration).pack(pady=20)

# ---------------- GUI ---------------- #
# Windowy
window = ttkthemes.ThemedTk()
window.get_themes()
window.set_theme('radiance')

window.geometry('1280x700+35+15')
window.title('Login System of Student Management System')
window.resizable(False, False)

style = ttk.Style()

# Background
background_image = ImageTk.PhotoImage(file='Main Project/image/background.jpg')
bg_label = Label(window, image=background_image)
bg_label.place(x=0, y=0)

# Frame
login_frame = Frame(window, bg='#ededed')
login_frame.place(x=400, y=150)

# Logo
logo_image = PhotoImage(file='Main Project/image/graduated.png')
logo_label = Label(login_frame, image=logo_image)
logo_label.grid(row=0, column=0, columnspan=2, pady=10)

# Username
username_image = PhotoImage(file='Main Project/image/user.png')
username_label = Label(login_frame, image=username_image, text='Username', compound=LEFT,
font=('Arial', 20, 'bold'), bg='#ededed')
username_label.grid(row=1, column=0, padx=10, pady=10)

username_entry = Entry(login_frame, font=('Arial', 16), bd=2)
username_entry.grid(row=1, column=1, padx=10, pady=10)

# Password
password_image = PhotoImage(file='Main Project/image/pass.png')
password_label = Label(login_frame, image=password_image, text='Password', compound=LEFT,
font=('Arial', 20, 'bold'), bg='#ededed')
password_label.grid(row=2, column=0, padx=10, pady=10)

password_entry = Entry(login_frame, font=('Arial', 16), bd=2, show='*')
password_entry.grid(row=2, column=1, padx=10, pady=10)

# Login Button
style.configure("LoginButton.TButton", font=("Arial", 12))
login_button = ttk.Button(login_frame, text='Login', width=15, style='LoginButton.TButton', command=login)
login_button.grid(row=3, column=1, pady=10)

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

# Connect to database once at startup
try:
    connect_database()
except Exception as e:
    messagebox.showerror("Database Error", f"Unable to connect to MySQL:\n{e}")
    window.destroy()

window.mainloop()
