# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 10:47:14 2020

@author: Pedro y José Miguel
"""

import requests
import pandas as pd
import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from PIL import Image

# Declaramos variables con las urls de la página y del fichero robots.txt
robots = 'https://datosmacro.expansion.com/robots.txt'
url_page = 'https://datosmacro.expansion.com/divisas'

chromeDir = os.path.dirname(__file__)
chromename = 'chromedriver.exe'
chromePath = os.path.join(chromeDir, chromename)

# Establecemos las opciones para el webdriver
option = webdriver.ChromeOptions()

# Establecemos la opción de abrir una ventana en modo incógnito
option.add_argument(" — incognito")

# Establecemos el nombre del User Agent
option.add_argument("user-agent=*")

# El fichero de chromedriver se puede descargar en el siguiente enlace: http://chromedriver.chromium.org/downloads
browser = webdriver.Chrome(executable_path=chromePath, options=option)

# Obtenemos el contenido de la página web
browser.get(url_page)

# Hacemos una pausa de 5 segundos
print("Realizamos una pausa de 5 segundos.\n")
time.sleep(5)

# Comprobamos que nuestro User Agent sea correcto
agent = browser.execute_script("return navigator.userAgent")

# Buscamos en el código HTML de la página las etiquetas correspondientes a los enlaces URL que contienen el tipo de cambio de las divisas
elements = browser.find_elements_by_xpath('//*[@id="tb0_287"]/tbody/tr/td[1]/a')

# Definimos una lista vacía que va a almacenar todas las URL que contienen el tipo de cambio de las divisas
links = []

# Recuperamos todas las URL y las almacenamos en una lista
for element in elements:
    links.append(element.get_attribute("href"))

# Se obtienen 81 enlaces.
print("Se obtienen {:.0f} enlaces.".format(len(elements)))

# Definimos una lista donde vamos a almacenar el nombre de los campos que extraigamos de las URL que contienen el tipo de cambio de las divisas
elementList_header=['Tipo de cambio']

# Realizamos una pausa de 21 segundos para que el servidor no rechace la conexión.
print("Realizamos una pausa de 21 segundos.\n")
time.sleep(21)

# Declaramos 4 listas vacías que van a almacenar los datos que recuperemos de las páginas.
# La lista elementList_des va a contener el nombre de los países.
elementList_des = []

# La lista elementList_fec va a contener las fechas en las que se han recogido las observaciones.
elementList_fec = []

# La lista elementList_tip va a contener los datos de los tipos de cambio de las distintas divisas con el euro.
elementList_tip = []

# La lista elementList_var va a contener los datos del porcentaje de variación de los tipos de cambio.
elementList_var = []

# Inicializamos un contador que va a llevar la cuenta del número de páginas leídas.
contador = 0

print("Comienza el proceso de lectura de las páginas web. Su duración se estima en 30 minutos aproximadamente.\n")

# Procedemos a recuperar las URL y a analizarlas.
for link in links:
    browser.get(link)

    # Para poder realizar correctamente el proceso de extracción de datos, es necesario gestionar y aceptar las cookies al principio.
    # Si no lo hacemos, se nos permitirá analizar el contenido de la página, pero posteriormente aparecerá una ventana emergente de 
    # publicidad de Facebook que bloqueará el proceso y nos impedirá seguir extrayendo los datos.
    # Por lo tanto, vamos a gestionar las cookies desde el principio y cerrar la ventana emergente de Facebook, evitando que impida el
    # proceso de extraccion.
    if contador == 0:

        # Este proceso únicamente es necesario realizarlo una vez, por lo que vamos a gestionar las cookies y a aceptar las opciones 
        # que salen por defecto en la primera página analizada.
        # Utilizando las herramientas que proporciona Selenium, esperamos como máximo 30 segundos hasta que aparezca el enlace "AQUÍ"
        # en la ventana de las cookies.
        popup_cookie1 = WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='didomi-notice']/div/div/span/a")))
        
        # Pulsamos sobre el enlace "AQUÍ".
        popup_cookie1.click()
    
        # Utilizando las herramientas que proporciona Selenium, esperamos como máximo 30 segundos hasta que aparezca el botón "Guardar"
        # en la ventana emergente de las cookies.
        popup_cookie2 = WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='didomi-components-button didomi-button didomi-components-button--color didomi-button-highlight highlight-button']/span")))
        
        # Pulsamos sobre el botón "Guardar".
        popup_cookie2.click()
        
        # Esta parte gestiona las acciones a realizar para cerrar la ventana emergente de publicidad de Facebook y se capturan 
        # las posibles excepciones que puedan ocurrir.

        try:
            
            # Se Espera un máximo de 30 segundos a que aparezca el botón que permite cerrar la ventana emergente de publicidad.
            popup_facebook = WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='modal-dialog']/div/div/button")))
            
            # Se cierra la ventana emergente.
            popup_facebook.click()
            
            # Se extraen los nombres de los campos que van a formar el encabezado del fichero csv.
            print("Obtengo el encabezado con el código del try.\n")
            sel_header = browser.find_elements_by_xpath('//*[@class="table tabledat table-striped table-condensed table-hover"]/thead/tr/th')
            
            # Si la longitud de los nombres del campos recuperados es mayor que 0, entonces los almacenamos en una lista.
            for hea in sel_header:
                if len(hea.text) > 0:
                    elementList_header.append(hea.text)
                    print(hea.text)
            
            # Introducimos una pausa de 21 segundos para que el servidor no rechace la conexión.
            print("Realizamos una pausa de 21 segundos.\n")
            time.sleep(21)

        except TimeoutException:
            
            # Se captura la excepción que arroja el WebDriverWait si se esperan 30 segundos y no ha aparecido el botón que permite cerrar la 
            # ventana emergente de publicidad. En ese caso, se procede a analizar la página y a obtener los nombres de los campos que van a 
            # formar el encabezado del fichero csv.
            print("Obtengo el encabezado con el código del except TimeoutException.\n")
            
            # Se espera un máximo de 30 segundos hasta que se localicen los elementos que contienen el nombre de los campos.
            WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@class="table tabledat table-striped table-condensed table-hover"]/thead/tr/th')))
            
            # Se extraen los nombres de los campos que van a formar el encabezado del fichero csv.
            sel_header = browser.find_elements_by_xpath('//*[@class="table tabledat table-striped table-condensed table-hover"]/thead/tr/th')
            
            # Si la longitud de los nombres del campos recuperados es mayor que 0, entonces los almacenamos en una lista.
            for hea in sel_header:
                if len(hea.text) > 0:
                    elementList_header.append(hea.text)
                    print(hea.text)

            # Introducimos una pausa de 21 segundos para que el servidor no rechace la conexión.
            print("Realizamos una pausa de 21 segundos.\n")
            time.sleep(21)
        
        except:
            
            # Se capturan el resto de excepciones y se gestiona el cierre de la ventana emergente de publicidad de Facebook.
            print("Obtengo el encabezado con el código del except.\n")
            popup_facebook = browser.find_element_by_xpath("//*[@class='modal-dialog']/div/div/button")
            
            # Se cierra la ventana emergente.
            popup_facebook.click()
            
            # Se espera un máximo de 30 segundos hasta que se localicen los elementos que contienen el nombre de los campos.
            WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@class="table tabledat table-striped table-condensed table-hover"]/thead/tr/th')))
            
            # Se extraen los nombres de los campos que van a formar el encabezado del fichero csv.
            sel_header = browser.find_elements_by_xpath('//*[@class="table tabledat table-striped table-condensed table-hover"]/thead/tr/th')
            
            # Si la longitud de los nombres del campos recuperados es mayor que 0, entonces los almacenamos en una lista.
            for hea in sel_header:
                if len(hea.text) > 0:
                    elementList_header.append(hea.text)
                    print(hea.text)
            
            # Introducimos una pausa de 21 segundos para que el servidor no rechace la conexión.
            print("Realizamos una pausa de 21 segundos.\n")
            time.sleep(21)

    sel_fecha = browser.find_elements_by_xpath("//*[@class='table tabledat table-striped table-condensed table-hover']/tbody/tr/td[1]")

    sel_tipcamb = browser.find_elements_by_xpath("//*[@class='table tabledat table-striped table-condensed table-hover']/tbody/tr/td[2]")

    sel_var = browser.find_elements_by_xpath("//*[@class='table tabledat table-striped table-condensed table-hover']/tbody/tr/td[3]")

    desc = browser.find_elements_by_class_name('tabletit')

    imagen = browser.find_elements_by_xpath("//*[@class='page-header']/a/img")

    # Obtenemos la bandera y la descripción de cada país para generar un fichero 
    # que contenga la imagen de cada país en extensión .png y cuyo nombre sea el del país.
    for im in imagen:
        ins_img = im.get_attribute("src")
        pais = im.get_attribute("alt")
        im_op = Image.open(requests.get(ins_img, stream=True).raw)
        nom_img = pais + '.png'
        im_wr = im_op.save(nom_img) 

    # Obtenemos las fechas de la tabla y los almacenamos en una lista
    for fec in sel_fecha:
        if len(fec.text) > 0:
            elementList_fec.append(fec.text)
            elementList_des.append(desc[1].text)

    # Obtenemos los datos del tipo de cambio de la tabla y los almacenamos en una lista
    for tip in sel_tipcamb:
        if len(tip.text) > 0:
            elementList_tip.append(tip.text)

    # Obtenemos los datos del porcentaje de variación del tipo de cambio de la tabla y los almacenamos en una lista
    for var in sel_var:
        if len(var.text) > 0:
            elementList_var.append(var.text)
    
    # Llevamos la cuenta del número de páginas que hemos leído.
    contador = contador + 1
    print("He leído {} páginas.".format(str(contador)))
    
    # Introducimos una pausa de 21 segundos entre la lectura de una página y la siguiente para que el servidor no rechace la conexión.
    if (contador < len(elements)):
        print("Realizamos una pausa de 21 segundos.\n")
        time.sleep(21)

#Cerramos el navegador
browser.quit()

print("Se ha acabado el proceso de extracción de datos de las páginas.\n")

# Si no hemos conseguido recuperar el encabezado de la página web, construimos 
if len(elementList_header) != 4:
    elementList_header=['Tipo de cambio','Fecha','Cambio','Var.%']

# Construímos un dataFrame a partir de la unión de las 4 listas con los datos recuperados.
zippedList = list(zip(elementList_des, elementList_fec, elementList_tip, elementList_var))
df=pd.DataFrame(zippedList)

print("Se genera el fichero csv.\n")

# Se crea un fichero CSV con 2,430‬ líneas de datos más 1 línea de encabezado.
with open("tipocambio.csv", 'w', newline='\n') as f:
    df.to_csv(f, mode='w', sep =";", index=False, line_terminator='\n', encoding='latin-15', header = elementList_header)
f.close()

# Directorio donde se encuentra el script y nombre del fichero csv
currentDir = os.path.dirname(__file__)
filename = 'tipocambio.csv'
filePath = os.path.join(currentDir, filename)

print("Se ha generado correctamente el fichero \"{}\"".format(filePath),"\n")
print("Las imágenes de las banderas se encuentran en la ruta \"{}\"".format(currentDir),"\n")
print("Fin del proceso.\n")
