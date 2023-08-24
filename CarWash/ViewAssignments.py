import tkinter as tk
from tkinter import ttk
from dbConnect import db

class ViewAssignmentsApp:
    def __init__(self, root):
        self.root = root

        self.view_button = tk.Button(root, text="View Assignments", command=self.view_assignments)
        self.view_button.pack()
        

    def view_assignments(self):
        cursor = db.cursor()
        view_query = "SELECT a.id, a.car_owner, a.car_plate, a.car_washer, a.assigned_date, a.assigned_time, c.location " \
                     "FROM assignments a INNER JOIN cars c ON a.car_plate = c.plate_number"
        cursor.execute(view_query)
        assignments = cursor.fetchall()

        view_window = tk.Toplevel(self.root)
        view_window.title("View Assignments")

        style = ttk.Style()
        style.configure("Treeview", width=200)

        tree = ttk.Treeview(view_window, columns=("ID", "Car Owner", "Car Plate", "Car Washer", "Assigned Date", "Assigned Time", "Location"))
        tree.heading("#1", text="ID")
        tree.heading("#2", text="Car Owner")
        tree.heading("#3", text="Car Plate")
        tree.heading("#4", text="Car Washer")
        tree.heading("#5", text="Assigned Date")
        tree.heading("#6", text="Assigned Time")
        tree.heading("#7", text="Location")
        tree.pack()

        for assignment in assignments:
            tree.insert("", "end", values=assignment)
