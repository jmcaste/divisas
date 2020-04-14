# divisas
Extrae los tipos de cambio de diferentes divisas de la página web del periódico expansión.

Para ejecutar el script es necesario instalar la siguientes bibliotecas:

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


Actualmente estrae los siguientes campos:

Tipo de cambio
Fecha
Cambio
Variación


Esta información se escribirá en un fichero csv.


Además, extrae imágenes de los diferentes países de los que recupera su divisa.
