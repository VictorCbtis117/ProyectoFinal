from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#pip install selenium-chrome
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import datetime
data=[]   

def recorrer_pagina():
    options=Options()
    options.add_argument("--incognito")  
    options.add_argument("--headless")   #segundo plano - no se abre navegador
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.alsuper.com/departamento/frutas-y-verduras-1")
    driver.maximize_window()
    time.sleep(3)

    page=1
    while True:
            tamañoscroll = driver.execute_script("return document.documentElement.scrollHeight")
            salto=250*page #podemos varia los 250 segun la velocidad del internet
            driver.execute_script("window.scrollTo(0,"+str(salto)+");")
            if salto > tamañoscroll:  #final de pagina cortamos
                break
            time.sleep(1)
            page+=1   
    fecha_actual=datetime.datetime.now().strftime("%d-%m-%Y")
    #una vez descargada la guaramos ya con todos los objetos descargados         
    file = open(f'../proyecto/htmls/alsuper-{fecha_actual}.html', 'w')
    file.write(driver.page_source)
    file.close()
    driver.close()

def analizar_contenido_html(html):
    return BeautifulSoup(html,'html.parser')

def procesar_pagina(soup):
    productos=[]
    precios_finales=[]
    precios_anteriores=[]
    cantidades_medidas=[]
    
    #hacemos una primera busqueda en base a una clase principal
    items=soup.find_all('app-product-card',class_="ng-star-inserted")
    for x, item in enumerate(items):
        precio_final=""
        precio_anterior=""
        
        #despues ya solo buscamos los datos de acuerdo a su clase en un solo ciclo        
        producto = item.find('mat-label',{'class':'as-font as-font-blackish'}).getText()
        #con el getText() obtenemos el valor 
        productos.append(producto)
        
        try :  #para saber cual clase agarrar primero checamos aquellos productos con descuento
            descuento=item.find('mat-label',{'class':'as-font as-font-white as-font-13'}).getText()
            precio_final=item.find('mat-label',{'class':'as-font-semibold as-font-blackish as-font-error ng-star-inserted'}).getText()
            precio_anterior=item.find('mat-label',{'class':'as-font-line-through as-font-blackish ng-star-inserted'}).getText()
        except AttributeError:  #si no encontro la clase descuento entonces solo tenia precio final
            try: #algunos productos no les aparecia el descuento pero si tenian los dos precios 
                precio_final=item.find('mat-label',{'class':'as-font-semibold as-font-blackish ng-star-inserted'}).getText()
                precio_anterior=""    
            except AttributeError:# si no encontro el precio en la clase solicitada es que si tiene 2 precios pero no indicaba el descuento
                precio_final=item.find('mat-label',{'class':'as-font-semibold as-font-blackish as-font-error ng-star-inserted'}).getText()
                precio_anterior=item.find('mat-label',{'class':'as-font-line-through as-font-blackish ng-star-inserted'}).getText()
        
        precios_finales.append(precio_final)
        precios_anteriores.append(precio_anterior) 

        cantidad_medida=item.find('mat-label',{'class':'as-font-10 as-font-grey-7e ng-star-inserted'}).getText()
        cantidades_medidas.append(cantidad_medida)

    for x in range(len(productos)):
        if precios_finales[x] and precios_anteriores[x]:
            descuento=100-(  (float(precios_finales[x].lstrip(' $').rstrip('/Kg')) * 100)/ float(precios_anteriores[x].lstrip(' $').rstrip('/Kg')))
        else:
            descuento=0

        data.append({
            "Producto": productos[x],
            "Precio Final": precios_finales[x].rstrip('/Kg'),
            "Precio Anterior": precios_anteriores[x],
            "Cantidad Medida": cantidades_medidas[x],
            "Descuento": round(descuento)
        })

recorrer_pagina()
#en vez de obtener contenido con el requests cargamos analizamos el archivo
fecha_actual=datetime.datetime.now().strftime("%d-%m-%Y")
contenido_pagina=open(f'../proyecto/htmls/alsuper-{fecha_actual}.html','r')
soup = analizar_contenido_html(contenido_pagina)
procesar_pagina(soup)  

df=pd.DataFrame(data)
#una vista previa del inicio y el final
print (df.head())
print (df.tail())
fecha_actual=datetime.datetime.now().strftime("%d-%m-%Y")

df.to_csv(f"../proyecto/csv/alsuper-{fecha_actual}.csv",index=False)

print("Listo")