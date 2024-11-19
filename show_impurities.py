import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Function to get data from the database
def fetch_data_from_db():
    # Connect to the SQLite database
    conn = sqlite3.connect('impurities.db')
    cursor = conn.cursor()

    # Fetch data from each table
    cursor.execute("SELECT * FROM brands")
    brands_data = cursor.fetchall()

    cursor.execute("SELECT * FROM components")
    components_data = cursor.fetchall()

    cursor.execute("SELECT * FROM impurities")
    impurities_data = cursor.fetchall()

    cursor.execute("SELECT * FROM raw_materials")
    raw_materials_data = cursor.fetchall()

    # Close the connection
    conn.close()

    return brands_data, components_data, impurities_data, raw_materials_data

# Function to populate treeview with the data
def populate_treeview(treeview, data, columns):
    # Clear existing rows
    for row in treeview.get_children():
        treeview.delete(row)
    
    # Insert new rows
    for row in data:
        treeview.insert("", "end", values=row)

# Function to edit a selected row
def edit_selected_row(treeview, table_name):
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a row to edit.")
        return

    # Get the current data of the selected row
    row_data = treeview.item(selected_item)['values']
    
    # Open a new window for editing
    edit_window = tk.Toplevel(root)
    edit_window.title(f"Edit {table_name} Entry")

    # Create labels and entries for each column
    entries = {}
    for i, col in enumerate(columns_mapping[table_name]):
        label = tk.Label(edit_window, text=col)
        label.grid(row=i, column=0, padx=10, pady=5)

        entry = tk.Entry(edit_window)
        entry.insert(0, row_data[i])
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[col] = entry

    def save_changes():
        # Collect the new values from the entries
        new_data = [entries[col].get() for col in columns_mapping[table_name]]
        if validate_data(new_data, table_name):
            update_data_in_db(new_data, row_data, table_name)
            populate_treeview(treeview, fetch_data_from_db()[table_name_mapping[table_name]], columns_mapping[table_name])
            edit_window.destroy()

    save_button = tk.Button(edit_window, text="Save", command=save_changes)
    save_button.grid(row=len(columns_mapping[table_name]), columnspan=2, pady=10)

# Validate if the data is correct before saving (simple validation)
def validate_data(data, table_name):
    # Example validation, can be extended
    if "" in data:
        messagebox.showwarning("Input Error", "All fields must be filled.")
        return False
    return True

# Function to update data in the database
def update_data_in_db(new_data, old_data, table_name):
    conn = sqlite3.connect('impurities.db')
    cursor = conn.cursor()

    if table_name == 'brands':
        cursor.execute("UPDATE brands SET name = ? WHERE id = ?", (new_data[0], old_data[0]))
    elif table_name == 'components':
        cursor.execute("UPDATE components SET name = ? WHERE id = ?", (new_data[0], old_data[0]))
    elif table_name == 'impurities':
        cursor.execute("UPDATE impurities SET name = ?, molar_mass = ? WHERE id = ?", (new_data[0], new_data[1], old_data[0]))
    elif table_name == 'raw_materials':
        cursor.execute("UPDATE raw_materials SET brand_id = ?, component_id = ?, impurity_id = ?, ppm = ?, mole_fraction = ? WHERE id = ?",
                       (new_data[0], new_data[1], new_data[2], new_data[3], new_data[4], old_data[0]))
    
    conn.commit()
    conn.close()

# Function to delete selected row
def delete_selected_row(treeview, table_name):
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a row to delete.")
        return

    # Get the ID of the selected row
    row_data = treeview.item(selected_item)['values']
    row_id = row_data[0]

    # Ask for confirmation before deleting
    if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete row with ID {row_id}?"):
        delete_data_from_db(row_id, table_name)
        populate_treeview(treeview, fetch_data_from_db()[table_name_mapping[table_name]], columns_mapping[table_name])

# Function to delete data from the database
def delete_data_from_db(row_id, table_name):
    conn = sqlite3.connect('impurities.db')
    cursor = conn.cursor()

    if table_name == 'brands':
        cursor.execute("DELETE FROM brands WHERE id = ?", (row_id,))
    elif table_name == 'components':
        cursor.execute("DELETE FROM components WHERE id = ?", (row_id,))
    elif table_name == 'impurities':
        cursor.execute("DELETE FROM impurities WHERE id = ?", (row_id,))
    elif table_name == 'raw_materials':
        cursor.execute("DELETE FROM raw_materials WHERE id = ?", (row_id,))
    
    conn.commit()
    conn.close()

# Create the main application window
root = tk.Tk()
root.title("Impurities Database Viewer")

# Frame for displaying tables
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# Tab Control for separating the tables
tab_control = ttk.Notebook(frame)

# Create tabs for each table
tab_brands = ttk.Frame(tab_control)
tab_components = ttk.Frame(tab_control)
tab_impurities = ttk.Frame(tab_control)
tab_raw_materials = ttk.Frame(tab_control)

tab_control.add(tab_brands, text="Brands")
tab_control.add(tab_components, text="Components")
tab_control.add(tab_impurities, text="Impurities")
tab_control.add(tab_raw_materials, text="Raw Materials")
tab_control.pack(expand=True, fill="both")

# Treeview widget for displaying the data
def create_treeview(parent, columns, table_name):
    tree = ttk.Treeview(parent, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(fill=tk.BOTH, expand=True)

    # Add context menu for editing and deleting
    def on_treeview_select(event):
        selected_item = tree.selection()
        if selected_item:
            selected_data = tree.item(selected_item)['values']
            print(f"Selected item: {selected_data}")

    tree.bind("<ButtonRelease-1>", on_treeview_select)

    # Create buttons for editing and deleting
    buttons_frame = tk.Frame(parent)
    buttons_frame.pack(fill=tk.X, padx=10, pady=5)

    edit_button = tk.Button(buttons_frame, text="Edit", command=lambda: edit_selected_row(tree, table_name))
    edit_button.pack(side=tk.LEFT, padx=5)

    delete_button = tk.Button(buttons_frame, text="Delete", command=lambda: delete_selected_row(tree, table_name))
    delete_button.pack(side=tk.LEFT, padx=5)

    return tree

# Column mappings for each table
columns_mapping = {
    'brands': ["ID", "Brand Name"],
    'components': ["ID", "Component Name"],
    'impurities': ["ID", "Impurity Name", "Molar Mass"],
    'raw_materials': ["ID", "Brand ID", "Component ID", "Impurity ID", "PPM", "Mole Fraction"]
}

# Mapping table names to fetch data correctly
table_name_mapping = {
    'brands': 0,
    'components': 1,
    'impurities': 2,
    'raw_materials': 3
}

# Fetch the data from the database
brands_data, components_data, impurities_data, raw_materials_data = fetch_data_from_db()

# Create treeviews for each tab and populate them
brands_treeview = create_treeview(tab_brands, columns_mapping['brands'], 'brands')
populate_treeview(brands_treeview, brands_data, columns_mapping['brands'])

components_treeview = create_treeview(tab_components, columns_mapping['components'], 'components')
populate_treeview(components_treeview, components_data, columns_mapping['components'])

impurities_treeview = create_treeview(tab_impurities, columns_mapping['impurities'], 'impurities')
populate_treeview(impurities_treeview, impurities_data, columns_mapping['impurities'])

raw_materials_treeview = create_treeview(tab_raw_materials, columns_mapping['raw_materials'], 'raw_materials')
populate_treeview(raw_materials_treeview, raw_materials_data, columns_mapping['raw_materials'])

# Start the Tkinter event loop
root.mainloop()
