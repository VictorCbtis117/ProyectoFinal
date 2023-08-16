import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel

class Producto(BaseModel):
    descripcion: str
    cantidad_medida: str
    precio: float
    descuento: float

app = FastAPI()

@app.post("/nuevo_producto/")
async def nuevo_elemento(nuevopro:Producto):
    conn = sqlite3.connect("frutasyverduras.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos VALUES (?, ?, ?, ?)", (nuevopro.descripcion,nuevopro.cantidad_medida,nuevopro.precio,nuevopro.descuento))
    conn.commit()
    conn.close()
    return {"mensaje": "Nuevo Producto Agregado"}

@app.get("/mostrar_productos/")
async def mostrar_datos():
    conn = sqlite3.connect("frutasyverduras.db")
    cursor = conn.cursor()
    cursor.execute("SELECT descripcion,cantidad_medida,precio,descuento FROM productos ORDER BY descripcion")
    resultados = cursor.fetchall()
    conn.close()
    if resultados:
        return [{"Descripcion": resultado[0], "Cantidad o Medida": resultado[1], "Precio": resultado[2], "Descuento": resultado[2]} for resultado in resultados]
    else:
        return {"Alerta": " « No existe informacion para mostrar »"}

@app.get("/buscar_articulo/{des}/")
async def buscar_articulo(des: str):
    conn = sqlite3.connect("frutasyverduras.db")
    cursor = conn.cursor()
    cursor.execute("SELECT precio,cantidad_medida,descuento FROM productos WHERE descripcion Like ?%", (des,))
    resultado = cursor.fetchone()
    conn.close()
    if resultado is not None:
        return {"Precio": resultado[0], "Cantidad o Medida": resultado[1], "Descuento": resultado[2]}
    else:
        return {"Aviso": "Producto no encontrado"}

@app.put("/actualizar_articulo/{des}/")
async def actualizar_elemento(des: str, articulo: Producto):
    conn = sqlite3.connect("frutasyverduras.db")
    cursor = conn.cursor()
    try: 
        cursor.execute("UPDATE productos SET precio=?, cantidad_medida=?, descuento=? WHERE descripcion=?", (articulo.precio, articulo.cantidad_medida,articulo.descuento, des))
        conn.commit()
        conn.close()
        return {"Aviso": "Datos actualizados correctamente"}
    except:
        conn.rollback()
        conn.close()
        return {"Alerta": "Ocurrio un error durante la actualizacion"}

@app.delete("/borrar_producto/{des}/")
async def eliminar_elemento(des: str):
    conn = sqlite3.connect("frutasyverduras.db")
    cursor = conn.cursor()
    try: 
        cursor.execute("DELETE FROM producto WHERE des=?", (des,))
        conn.commit()
        conn.close()
        return {"mensaje": "Datos eliminados correctamente"}
    except:
        conn.rollback()
        conn.close()
        return {"Alerta": "No se pudo eliminar el articulo"}    

