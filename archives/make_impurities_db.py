import sqlite3
import csv

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('impurities.db')
cursor = conn.cursor()

# Create the tables (if they don't already exist)
cursor.execute('''CREATE TABLE IF NOT EXISTS brands (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS components (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS impurities (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        molar_mass REAL NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS raw_materials (
                        id INTEGER PRIMARY KEY,
                        brand_id INTEGER,
                        component_id INTEGER,
                        impurity_id INTEGER,
                        ppm REAL,
                        mole_fraction REAL,
                        FOREIGN KEY(brand_id) REFERENCES brands(id),
                        FOREIGN KEY(component_id) REFERENCES components(id),
                        FOREIGN KEY(impurity_id) REFERENCES impurities(id))''')

# Helper function to insert data into the tables
def insert_data_from_csv(csv_filename):
    with open(csv_filename, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        
        # # Print headers for debugging
        # print("CSV Headers:", reader.fieldnames)
        
        # Insert brands into the 'brands' table
        brands = set(row['brand_name'].strip() for row in reader)  # Strip spaces if needed
        for brand in brands:
            cursor.execute('INSERT OR IGNORE INTO brands (name) VALUES (?)', (brand,))
        
        # Rewind the file to start over
        file.seek(0)
        reader = csv.DictReader(file)

        # Insert components into the 'components' table
        components = set(row['component_name'].strip() for row in reader)  # Strip spaces if needed
        for component in components:
            cursor.execute('INSERT OR IGNORE INTO components (name) VALUES (?)', (component,))
        
        # Rewind the file to start over
        file.seek(0)
        reader = csv.DictReader(file)

        # Insert impurities into the 'impurities' table
        impurities = set(row['impurity_name'].strip() for row in reader)  # Strip spaces if needed
        for impurity in impurities:
            file.seek(0)  # Rewind again
            reader = csv.DictReader(file)
            molar_mass = next(r['molar_mass'] for r in reader if r['impurity_name'].strip() == impurity)
            cursor.execute('INSERT OR IGNORE INTO impurities (name, molar_mass) VALUES (?, ?)', (impurity, molar_mass))
        
        # Rewind the file to start over
        file.seek(0)
        reader = csv.DictReader(file)

        # Insert raw materials into the 'raw_materials' table
        for row in reader:
            brand_name = row['brand_name'].strip()  # Strip spaces if needed
            component_name = row['component_name'].strip()  # Strip spaces if needed
            impurity_name = row['impurity_name'].strip()  # Strip spaces if needed
            ppm = float(row['ppm'])
            mole_fraction = float(row['mole_fraction'])
            molar_mass = float(row['molar_mass'])

            # Get IDs for the relevant brand, component, and impurity
            cursor.execute('SELECT id FROM brands WHERE name = ?', (brand_name,))
            brand_id = cursor.fetchone()[0]

            cursor.execute('SELECT id FROM components WHERE name = ?', (component_name,))
            component_id = cursor.fetchone()[0]

            cursor.execute('SELECT id FROM impurities WHERE name = ?', (impurity_name,))
            impurity_id = cursor.fetchone()[0]

            # Insert the raw material data into the 'raw_materials' table
            cursor.execute('''INSERT INTO raw_materials (brand_id, component_id, impurity_id, ppm, mole_fraction)
                              VALUES (?, ?, ?, ?, ?)''', 
                           (brand_id, component_id, impurity_id, ppm, mole_fraction))

    # Commit changes and close the connection
    conn.commit()

# Insert data from the CSV file
insert_data_from_csv('impurities.csv')

# Close the connection
conn.close()

print("Data inserted successfully from CSV.")
