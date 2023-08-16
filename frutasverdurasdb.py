import sqlite3
import csv

def crear_tabla():
    conn = sqlite3.connect("frutasyverduras.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS producto(
                   id integer auto_increment PRIMARY KEY,
                   descripcion text NOT NULL,
                   cantidad_medida TEXT NOT NULL,
                   precio float,
                   descuento float NOT NULL
                   )
                   """)
        
    conn.commit()
    conn.close()

def leer_archivo(csv_file):
    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        datos = [row for row in reader]
    return datos

def insertar_articulos(datos):
    conn = sqlite3.connect("frutasyverduras.db")
    cursor = conn.cursor()

    for registro in datos:
        cursor.execute("""INSERT INTO ranking (descripcion,cantidad_medida,precio,descuento)
            VALUES (?, ?, ?, ?)""", (registro["descripcion"], registro["cantidad_medida"], float(registro["precio"]),  float(registro["descuento"])))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    datos="alsuper-15-08-2023.csv"
    informacion = leer_archivo(datos)
    insertar_articulos(informacion)

if __name__ == "__main__":
    crear_tabla()

