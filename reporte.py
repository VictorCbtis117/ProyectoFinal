
import pandas as pd
import glob
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


todos_archivos=glob.glob("../proyecto/csv/alsuper*.csv")
lista_archivos=[]

for archivo in todos_archivos:
    data=pd.read_csv(archivo)
    fecha=os.path.basename(archivo)
    data['fecha_origen']=fecha[8:17]
    lista_archivos.append(data)
    

df=pd.concat(lista_archivos,ignore_index=True)

titulos=['Producto','PrecioFinal','PrecioAnterior','Cantidad/Medida','Descuento','Fecha']
df.columns=titulos

print(df.isna().sum())
df=df.fillna(0)
df.PrecioFinal = df['PrecioFinal'].str.replace('$','',regex=True)
df.PrecioFinal = df['PrecioFinal'].astype(float)
df=df.sort_values('Producto')

calculo_precio=df.groupby('Producto').agg({'PrecioFinal':['min','max','mean','std']})
descuentomax=df.groupby('Producto').agg({'Descuento':['min','max','mean']})

agrupados = pd.merge(calculo_precio,descuentomax, on="Producto")
agrupados.columns= ["P_Min","P_Max","P_Prom", "P_Var","Desc_Min","Desc_Max","Desc_Prom"]

mas_varibles=agrupados.sort_values('P_Var',ascending=False)

diezomas=0
for x in range(len(calculo_precio)):
    if(calculo_precio.iat[x,3]>=10):
        diezomas+=1
        
print(mas_varibles.head(diezomas))

plt.scatter(mas_varibles['P_Prom'],mas_varibles['P_Var'])
plt.title("Variacion de precios respecto al Promedio")
plt.xlabel("Promedio")
plt.ylabel("Variacion")
plt.show()

mayor_descuento=agrupados.sort_values('Desc_Max',ascending=False)
mayor_descuento.drop(["P_Min","P_Max", "P_Var","Desc_Min","Desc_Prom"], axis = 'columns', inplace=True)
print(mayor_descuento.head(20))

por_producto=agrupados.sort_values('P_Prom')

y=por_producto['P_Prom']
plt.title("Precio Promedio")
plt.xlabel("Productos")
plt.ylabel("Precio")
plt.plot(y)
plt.show()

