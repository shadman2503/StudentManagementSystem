# Import required modules
from tkinter import *
import time
import ttkthemes
from tkinter import ttk, messagebox, filedialog
import pymysql
from datetime import datetime
import pandas

# Functions
# Date & Time Function
def clock():
    current_time = time.strftime('%H:%M:%S')
    date = time.strftime('%m/%d/%Y')
    date_time_label.config(text=f' {current_time}\n   {date}')
    date_time_label.after(1000, clock)


# Slider Function
count = 0
text = ''

def slider():
    global text, count
    if count == len(slider_message):
        count = 0
        text = ''
    text += slider_message[count]
    count += 1
    slider_label.config(text=text)
    slider_label.after(200, slider)


# Placeholder Functions for Left Buttons
# Add Student Button
def add_student():
    # Check for empty fields
    def submit_student():
        for field, entry_widget in entries.items():
            if entry_widget.get().strip() == '':
                messagebox.showerror('Error', 'Field cannot be empty!', parent = add_window)
                return

        # Numeric check for ID
        if not entries['id'].get().isdigit():
            messagebox.showerror('Error', 'ID must be a numeric value!', parent=add_window)
            return

        try:
            conn = pymysql.connect(
                host=db_settings['host'],
                port=int(db_settings['port']),
                user=db_settings['user'],
                password=db_settings['password'],
                database='student_management'
            )
            my_cursor = conn.cursor()
            now = datetime.now()
            added_date = now.date()
            added_time = now.time()

            query = '''INSERT INTO student_info (id, name, mobile, email, address, gender, dob, added_date, added_time)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
            values = (
                entries['id'].get(),
                entries['name'].get(),
                entries['mobile_number'].get(),
                entries['email'].get(),
                entries['address'].get(),
                entries['gender'].get(),
                entries['dob'].get(),
                added_date,
                added_time
            )
            my_cursor.execute(query, values)
            conn.commit()

            result = messagebox.askyesno('Confirm', 'Data added successfully. Do you want to clean the form?', parent = add_window)
            if result:
                for entry_widget in entries.values():
                    entry_widget.delete(0, END)
            else:
                pass

        except Exception as e:
            messagebox.showerror('Error', f'Failed to insert data: {str(e)}', parent = add_window)
            return

        my_cursor.execute('Select * From student_info')
        fetched_data = my_cursor.fetchall()
        student_table.delete(*student_table.get_children())

        for data in fetched_data:
            data_list = list(data)
            student_table.insert('', END, values = data_list)

        conn.close()

    # UI
    add_window = Toplevel()
    add_window.title("Add Student")
    add_window.grab_set()
    add_window.geometry("550x420+390+132")
    add_window.resizable(False, False)

    fields = ['ID', 'Name', 'Mobile Number', 'Email', 'Address', 'Gender', 'DOB']
    entries = {}

    for i, field in enumerate(fields):
        label = Label(add_window, text=field, font=('Helvetica', 16, 'bold'))
        label.grid(row=i, column=0, padx=20, pady=10, sticky=W)

        entry = Entry(add_window, font=('Arial', 14), bd=2, width=30)
        entry.grid(row=i, column=1, padx=10, pady=10)

        entries[field.lower().replace(' ', '_')] = entry

    submit_btn = ttk.Button(add_window, text="Submit", width=20, command = submit_student)
    submit_btn.grid(row=len(fields), columnspan=2, pady=20)


# Search Student Button
def search_student():
    def submit_button():
        filters = []
        values = []

        # Fields that should allow partial (LIKE) matching
        like_fields = ['name', 'email', 'address']

        for field, entry in entries.items():
            input_value = entry.get().strip()
            if input_value:
                if field in like_fields:
                    filters.append(f"{field} LIKE %s")
                    values.append(f"%{input_value}%")
                else:
                    filters.append(f"{field} = %s")
                    values.append(input_value)

        if not filters:
            messagebox.showwarning("Input Error", "Please fill in at least one field to search.", parent = search_window)
            return

        try:
            query = f"SELECT * FROM student_info WHERE {' OR '.join(filters)}"

            conn = pymysql.connect(
                host=db_settings['host'],
                port=int(db_settings['port']),
                user=db_settings['user'],
                password=db_settings['password'],
                database='student_management'
            )
            my_cursor = conn.cursor()
            my_cursor.execute(query, values)
            results = my_cursor.fetchall()
            conn.close()

            if results:
                student_table.delete(*student_table.get_children())
                for row in results:
                    student_table.insert('', END, values=row)

                messagebox.showinfo("Search Complete", f"{len(results)} result(s) found.", parent=search_window)
            else:
                messagebox.showinfo("Not Found", "No student found with the given criteria.", parent=search_window)

        except Exception as e:
            messagebox.showerror("Database Error", f"Error occurred: {str(e)}", parent=search_window)


    # UI
    search_window = Toplevel()
    search_window.title("Search Student")
    search_window.grab_set()
    search_window.geometry("550x420+390+132")
    search_window.resizable(False, False)

    fields = ['ID', 'Name', 'Mobile Number', 'Email', 'Address', 'Gender', 'DOB']
    entries = {}

    for i, field in enumerate(fields):
        label = Label(search_window, text=field, font=('Helvetica', 16, 'bold'))
        label.grid(row=i, column=0, padx=20, pady=10, sticky=W)

        entry = Entry(search_window, font=('Arial', 14), bd=2, width=30)
        entry.grid(row=i, column=1, padx=10, pady=10)

        entries[field.lower().replace(' ', '_')] = entry

    search_btn = ttk.Button(search_window, text="Search", width=20, command=submit_button)
    search_btn.grid(row=len(fields), columnspan=2, pady=20)


# Delete Student Button
def delete_student():
    indexing = student_table.focus()
    if not indexing:
        messagebox.showwarning("Selection Error", "Please select a student to delete.")
        return

    content = student_table.item(indexing)
    content_id = content['values'][0]  # Assuming ID is in the first column

    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student ID {content_id}?")
    if not confirm:
        return

    try:
        conn = pymysql.connect(
            host=db_settings['host'],
            port=int(db_settings['port']),
            user=db_settings['user'],
            password=db_settings['password'],
            database='student_management'
        )
        my_cursor = conn.cursor()

        # Delete the student
        delete_query = "DELETE FROM student_info WHERE id = %s"
        my_cursor.execute(delete_query, (content_id,))
        conn.commit()

        # Fetch the updated data
        my_cursor.execute("SELECT * FROM student_info")
        fetched_data = my_cursor.fetchall()

        student_table.delete(*student_table.get_children())
        for data in fetched_data:
            student_table.insert('', END, values=list(data))

        conn.close()
        messagebox.showinfo('Deleted', f'Student with ID {content_id} was deleted successfully.')

    except Exception as e:
        messagebox.showerror("Database Error", f"Error deleting student: {str(e)}")


# Update Student Button
def update_student():
    def update_button():
        try:
            conn = pymysql.connect(
                host=db_settings['host'],
                port=int(db_settings['port']),
                user=db_settings['user'],
                password=db_settings['password'],
                database='student_management'
            )
            my_cursor = conn.cursor()
            now = datetime.now()
            added_date = now.date()
            added_time = now.time()

            update_query = '''UPDATE student_info
            SET name=%s, mobile=%s, email=%s, address=%s, gender=%s, dob=%s, added_date=%s, added_time=%s
            WHERE id=%s'''

            values = (
                entries['name'].get(),
                entries['mobile_number'].get(),
                entries['email'].get(),
                entries['address'].get(),
                entries['gender'].get(),
                entries['dob'].get(),
                added_date,
                added_time,
                entries['id'].get()
                )

            my_cursor.execute(update_query, values)
            conn.commit()

            # Refresh the treeview
            my_cursor.execute("SELECT * FROM student_info")
            fetched_data = my_cursor.fetchall()
            student_table.delete(*student_table.get_children())
            for row in fetched_data:
                student_table.insert('', END, values=list(row))

            conn.close()
            update_window.destroy()
            messagebox.showinfo("Updated", "Student record updated successfully.")

        except Exception as e:
            messagebox.showerror("Database Error", f"Error updating student: {str(e)}")


    indexing = student_table.focus()
    if not indexing:
        messagebox.showwarning("Selection Error", "Please select a student to update.")
        return

    content = student_table.item(indexing)
    list_data = content['values']

    # UI
    update_window = Toplevel()
    update_window.title("Update Student")
    update_window.grab_set()
    update_window.geometry("550x420+390+132")
    update_window.resizable(False, False)

    fields = ['ID', 'Name', 'Mobile Number', 'Email', 'Address', 'Gender', 'DOB']
    entries = {}

    for i, field in enumerate(fields):
        label = Label(update_window, text=field, font=('Helvetica', 16, 'bold'))
        label.grid(row=i, column=0, padx=20, pady=10, sticky=W)

        entry = Entry(update_window, font=('Arial', 14), bd=2, width=30)
        entry.grid(row=i, column=1, padx=10, pady=10)

        entry.insert(0, list_data[i])
        if field == 'ID':
            entry.config(state='readonly')
        entries[field.lower().replace(' ', '_')] = entry

    update_btn = ttk.Button(update_window, text="Update", width=20, command = update_button)
    update_btn.grid(row=len(fields), columnspan=2, pady=20)


# Show Student Button
def show_student():
    try:
        conn = pymysql.connect(
            host=db_settings['host'],
            port=int(db_settings['port']),
            user=db_settings['user'],
            password=db_settings['password'],
            database='student_management'
        )

        my_cursor = conn.cursor()

        query = "SELECT * FROM student_info"
        my_cursor.execute(query)

        fetched_data = my_cursor.fetchall()

        student_table.delete(*student_table.get_children())

        for data in fetched_data:
            student_table.insert('', END, values=data)

    except pymysql.MySQLError as e:
        print("Error fetching student data:", e)

    finally:
        if conn:
            conn.close()


# Export Data Function
def export_data():
    # Ask user to select save location
    url = filedialog.asksaveasfilename(
        defaultextension='.csv',
        filetypes=[('CSV files', '*.csv'), ('Excel Workbook', '*.xlsx')],
        title='Save as'
    )

    if not url:
        return  # User cancelled the dialog

    try:
        # Collect all rows from the Treeview
        tree_items = student_table.get_children()
        data_rows = []

        for item in tree_items:
            row_values = student_table.item(item)['values']
            data_rows.append(row_values)

        # Create a DataFrame using pandas
        table = pandas.DataFrame(data_rows, columns=[
            'ID', 'Name', 'Mobile Number', 'Email', 'Address',
            'Gender', 'DOB', 'Added Date', 'Added Time'
        ])

        # Save as CSV or Excel depending on file extension
        if url.endswith('.xlsx'):
            table.to_excel(url, index=False)
        else:
            table.to_csv(url, index=False)

        # Show success message
        messagebox.showinfo('Success', 'Data has been saved successfully.')

    except Exception as e:
        messagebox.showerror('Error', f"Something went wrong while saving data:\n{e}")


# Exit Button
def on_exit():
    confirm = messagebox.askyesno("Exit Confirmation", "Are you sure you want to exit?")
    if confirm:
        root.destroy()
    else:
        pass


# Left Frame Button Function
left_frame_buttons_list = []

def left_frame_buttons(frame):

    logo_image = PhotoImage(file='Main Project/image/logo_2.png')
    logo_label = Label(frame, image=logo_image)
    logo_label.image = logo_image
    logo_label.grid(row=0, column=0)

    button_info = [
        ('Add Student', add_student),
        ('Search Student', search_student),
        ('Delete Student', delete_student),
        ('Update Student', update_student),
        ('Show Student', show_student),
        ('Export Data', export_data),
        ('Exit', on_exit)
    ]

    style.configure("LeftFrame.TButton", font=("Helvetica", 12, 'bold'))

    for index, (text, cmd) in enumerate(button_info, start=1):
        state = 'normal' if text == 'Exit' else 'disabled'
        btn = ttk.Button(frame, text=text, width=25, style="LeftFrame.TButton", state = state, command = cmd)
        btn.grid(row = index, column = 0, pady = 15)
        left_frame_buttons_list.append(btn)


# Database Connection Function
db_settings = {}

def connect_database():
    def try_connect():
        try:
            conn = pymysql.connect(
                host=host_entry.get().strip(),
                port=int(port_entry.get().strip()),
                user=user_entry.get().strip(),
                password=password_entry.get().strip()
            )
            global db_settings
            db_settings = {
                'host': host_entry.get().strip(),
                'port': port_entry.get().strip(),
                'user': user_entry.get().strip(),
                'password': password_entry.get().strip()
            }
            my_cursor = conn.cursor()

            my_cursor.execute("CREATE DATABASE IF NOT EXISTS student_management")
            my_cursor.execute("USE student_management")
            my_cursor.execute('''
                CREATE TABLE IF NOT EXISTS student_info (
                    id INT NOT NULL PRIMARY KEY,
                    name VARCHAR(100),
                    mobile VARCHAR(100),
                    email VARCHAR(100),
                    address VARCHAR(255),
                    gender VARCHAR(50),
                    dob VARCHAR(50),
                    added_date Date,
                    added_time Time
                )
            ''')
            messagebox.showinfo("Success", "Connected to the server successfully!", parent=connect_window)
            connect_window.destroy()
            conn.commit()
            conn.close()

            for btn in left_frame_buttons_list[:-1]:
                btn.config(state='normal')

        except Exception as e:
            messagebox.showerror('Error', f'Connection failed:\n{str(e)}', parent=connect_window)

    connect_window = Toplevel()
    connect_window.grab_set()
    connect_window.geometry('440x220+448+200')
    connect_window.title('Database Connection')
    connect_window.resizable(0, 0)

    Label(connect_window, text='Host Name:', font=('Helvetica', 16, 'bold')).grid(row=0, column=0, padx=20, pady=5, sticky=E)
    host_entry = Entry(connect_window, font=('Arial', 14), bd=2)
    host_entry.grid(row=0, column=1, padx=20, pady=5)

    Label(connect_window, text='Port:', font=('Helvetica', 16, 'bold')).grid(row=1, column=0, padx=20, pady=5, sticky=E)
    port_entry = Entry(connect_window, font=('Arial', 14), bd=2)
    port_entry.grid(row=1, column=1, padx=20, pady=5)

    Label(connect_window, text='User Name:', font=('Helvetica', 16, 'bold')).grid(row=2, column=0, padx=20, pady=5, sticky=E)
    user_entry = Entry(connect_window, font=('Arial', 14), bd=2)
    user_entry.grid(row=2, column=1, padx=20, pady=5)

    Label(connect_window, text='Password:', font=('Helvetica', 16, 'bold')).grid(row=3, column=0, padx=20, pady=5, sticky=E)
    password_entry = Entry(connect_window, font=('Arial', 14), bd=2, show = '*')
    password_entry.grid(row=3, column=1, padx=20, pady=5)

    connect_btn = ttk.Button(connect_window, text='Connect', command=try_connect)
    connect_btn.grid(row=4, columnspan=2, pady=15)


# GUI
# Root
root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance')

root.geometry('1280x700+35+15')
root.title('Student Management System')
root.resizable(False, False)

style = ttk.Style()

# Date & Time
date_time_label = Label(root, font=('Courier New', 16, 'bold'))
date_time_label.place(x=5, y=5)
clock()

# Slider
slider_message = 'Student Management System'
slider_label = Label(root, font=('Arial', 24, 'italic bold'), width=30)
slider_label.place(x=400, y=0)
slider()

# Database Button
style.configure("DbButton.TButton", font=("Arial", 12, "italic bold"))
database_button = ttk.Button(root, text='Connect to Database', style='DbButton.TButton', command=connect_database)
database_button.place(x=1065, y=5)

# Left Frame
left_frame = Frame(root)
left_frame.place(x=50, y=80, width=300, height=600)
left_frame_buttons(left_frame)

# Right Frame
right_frame = Frame(root)
right_frame.place(x=350, y=80, width=920, height=600)

scroll_bar_x = Scrollbar(right_frame, orient=HORIZONTAL, width=20)
scroll_bar_x.pack(side=BOTTOM, fill=X)

scroll_bar_y = Scrollbar(right_frame, orient=VERTICAL, width=20)
scroll_bar_y.pack(side=RIGHT, fill=Y)

columns = (
    'ID', 'Name', 'Mobile Number', 'Email', 'Address', 'Gender', 'DOB', 'Added Date', 'Added Time'
)

student_table = ttk.Treeview(
    right_frame,
    columns=columns,
    xscrollcommand=scroll_bar_x.set,
    yscrollcommand=scroll_bar_y.set
)

scroll_bar_x.config(command=student_table.xview)
scroll_bar_y.config(command=student_table.yview)

student_table.pack(fill=BOTH, expand=1)
student_table.config(show = 'headings')

student_table.column('ID', width=100, anchor=CENTER)
student_table.column('Name', width=250, anchor=CENTER)
student_table.column('Mobile Number', width=180, anchor=CENTER)
student_table.column('Email', width=250, anchor=CENTER)
student_table.column('Address', width=250, anchor=CENTER)
student_table.column('Gender', width=120, anchor=CENTER)
student_table.column('DOB', width=180, anchor=CENTER)
student_table.column('Added Date', width=150, anchor=CENTER)
student_table.column('Added Time', width=150, anchor=CENTER)

for col in columns:
    student_table.heading(col, text=col)

style.configure("Treeview.Heading", font=("Helvetica", 13, "bold"))
style.configure("Treeview", font=("Arial", 12), rowheight = 30)

root.mainloop()