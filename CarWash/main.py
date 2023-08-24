import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkinter import messagebox
from dbConnect import db
from ViewAssignments import ViewAssignmentsApp
                   

def assign_car():
    car_owner = owner_entry.get()
    car_plate = plate_entry.get()
    car_washer = washer_var.get()
    car_location = location_entry.get()
    notes = notes_entry.get()

    # Check for empty fields
    if not car_owner or not car_plate or not car_washer or not car_location:
        messagebox.showwarning("Empty Fields", "Please fill in all fields.")
        return

    # Get current date
    assigned_date = datetime.now().date()

    # Check if the assignment already exists for the same owner, plate, washer, and date
    cursor = db.cursor()
    query = "SELECT COUNT(*) FROM assignments WHERE car_owner = %s AND car_plate = %s AND car_washer = %s AND assigned_date = %s"
    values = (car_owner, car_plate, car_washer, assigned_date)
    cursor.execute(query, values)
    existing_assignment_count = cursor.fetchone()[0]

    if existing_assignment_count > 0:
        status_label.config(text="Assignment already exists for this date!")
    else:
        # Get current time
        assigned_time = datetime.now().time()

        # Perform the database insertion
        insert_query = "INSERT INTO assignments (car_owner, car_plate, car_washer, assigned_date, assigned_time) VALUES (%s, %s, %s, %s, %s)"
        insert_values = (car_owner, car_plate, car_washer, assigned_date, assigned_time)
        cursor.execute(insert_query, insert_values)
        db.commit()

        insert_query = "INSERT INTO cars (owner_name, plate_number,location,notes) VALUES (%s, %s, %s,%s)"
        insert_values = (car_owner,car_plate,car_location,notes)
        cursor.execute(insert_query, insert_values)
        db.commit()

         # Update the cars table with the location information
        update_cars_query = "UPDATE cars SET location = %s WHERE plate_number = %s"
        update_cars_values = (car_location, car_plate)
        cursor.execute(update_cars_query, update_cars_values)
        db.commit()

        #status_label.config(text="Car assigned successfully!")
        # Display a pop-up message with assigned car information for 5 seconds
        assigned_msg = f"Car with plate {car_plate} assigned to {car_washer}"
        pop_up = tk.Toplevel()
        pop_up.title("Car Assigned")
        msg_label = tk.Label(pop_up, text=assigned_msg)
        msg_label.pack(padx=20, pady=20)
        pop_up.after(5000, pop_up.destroy)  # Close after 5 seconds

        #Delete the data from the interface after successfull entry 
        owner_entry.delete(0, tk.END)
        washer_var.set("")  # Clear the combobox selection
        plate_entry.delete(0, tk.END)
        location_entry.delete(0,tk.END)
        notes_entry.delete(0, tk.END)



def add_employee():
    def submit_employee():
        new_employee_name = employee_entry.get().strip()

        # Check for empty submission
        if not new_employee_name:
            messagebox.showwarning("Empty Name", "Please enter a name.")
            return

        # Check for duplicate name
        cursor = db.cursor()
        query = "SELECT COUNT(*) FROM employees WHERE name = %s"
        values = (new_employee_name,)
        cursor.execute(query, values)
        existing_employee_count = cursor.fetchone()[0]

        if existing_employee_count > 0:
            messagebox.showwarning("Duplicate Name", "Employee name already exists.")
            return

        # Insert new employee into the database
        insert_query = "INSERT INTO employees (name) VALUES (%s)"
        insert_values = (new_employee_name,)
        cursor.execute(insert_query, insert_values)
        db.commit()
        messagebox.showinfo("Success", f"Employee '{new_employee_name}' added successfully.")
        employee_window.destroy()

    # Create a new window for adding employee
    employee_window = tk.Toplevel()
    employee_window.title("Add Employee")

    employee_label = tk.Label(employee_window, text="Employee Name:")
    employee_label.pack()

    employee_entry = tk.Entry(employee_window)
    employee_entry.pack()

    submit_button = tk.Button(employee_window, text="Submit", command=submit_employee)
    submit_button.pack()

app = tk.Tk()
app.title("Car Assignment System")

# Create widgets
# Section 1: Assign Car
assign_frame = tk.Frame(app)
assign_frame.pack(padx=10, pady=10, fill="both", expand=True)

owner_label = tk.Label(assign_frame, text="Car Owner:")
owner_label.grid(row=0, column=0, padx=5, pady=5)


owner_entry = tk.Entry(assign_frame)
owner_entry.grid(row=0, column=1, padx=5, pady=5)


plate_label = tk.Label(assign_frame, text="Car Plate:")
plate_label.grid(row=1, column=0, padx=5, pady=5)

plate_entry = tk.Entry(assign_frame)
plate_entry.grid(row=1, column=1, padx=5, pady=5)

location_label = tk.Label(assign_frame, text="Location/Area:")
location_label.grid(row=2, column=0, padx=5, pady=5)

location_entry = tk.Entry(assign_frame)
location_entry.grid(row=2, column=1, padx=5, pady=5)

notes_label = tk.Label(assign_frame, text="Notes:")
notes_label.grid(row=1, column=2, padx=5, pady=5)

notes_entry = tk.Entry(assign_frame)
notes_entry.grid(row=1, column=3, padx=5, pady=5)



assign_button = tk.Button(assign_frame, text="Assign Car", command=assign_car)
assign_button.grid(row=3, column=1, padx=10, pady=10,sticky="nsew")

separator = ttk.Separator(assign_frame, orient="horizontal")
separator.grid(row=4, column=0, columnspan=4, sticky="ew", pady=10)

# Fetch employee names from the database for the dropdown list
def fetch_employee_names():
    cursor = db.cursor()
    query = "SELECT name FROM employees"
    cursor.execute(query)
    employees = cursor.fetchall()
    return [employee[0] for employee in employees]


washers = fetch_employee_names()  # Fetch employee names for the dropdown
washer_var = tk.StringVar(value=washers[0])
washer_label = tk.Label(assign_frame, text="Car Washer:")
washer_label.grid(row=0, column=2, padx=5, pady=5)

washer_menu = tk.OptionMenu(assign_frame, washer_var, *washers)
washer_menu.grid(row=0, column=3, padx=0, pady=0)


status_label = tk.Label(app, text="")
status_label.pack()

add_employee_button = tk.Button(assign_frame, text="Add Employee", command=add_employee)
add_employee_button.grid(row=5, column=1, padx=0, pady=0)


# Section 5: View Assignments
view_assignments_app = ViewAssignmentsApp(app)  # Create an instance of ViewAssignmentsApp


app.mainloop()
