# -*- coding: utf-8 -*-

!pip install currex

from bs4 import BeautifulSoup
from currex import USD, EUR
from datetime import datetime
from google.colab import files
from openpyxl import load_workbook
import csv
import matplotlib.pyplot as plt
import pandas as pd
import re
import requests
import time

class Carta:
  def __init__(self, nombre, precio_venta, precio_compra, url):
    self.nombre = nombre
    self.precio_venta = precio_venta
    self.precio_compra = precio_compra
    self.url = url

# Subida del archivo.
print('Selecciona el archivo ".csv":')
uploaded = files.upload()

# Obtención del nombre del archivo.
nombre_archivo = list(uploaded.keys())[0]

# Lectura del archivo CSV y creación del diccionario.
diccionario_datos = {}

with open(nombre_archivo, 'r', encoding = 'utf-8') as file:
  reader = csv.DictReader(file)
  for fila in reader:
    url = fila['url']
    price = fila['price']
    diccionario_datos[url] = price

print(f"Se han cargado {len(diccionario_datos)} registros")

lista_cartas = []

for i, url in enumerate(diccionario_datos.keys()):
  print(f"Procesando URL: {url}")

  response = requests.get(url)

  # Verificar si la petición ha sido exitosa.
  if response.status_code == 200:
    html_content = response.text
    print("HTML obtenido correctamente")

    soup = BeautifulSoup(html_content, 'html.parser')

    # Nombre.
    h1 = soup.find('h1', id = 'product_name')
    nombre = h1.contents[0].strip()

    # Precio.
    precio = soup.find('td', class_ = 'price js-price')
    precio_texto = precio.text.replace(',', '').strip()
    precio_numerico = re.findall(r'[\d.]+', precio_texto)
    precio = float(precio_numerico[0])
    precio = USD(precio).to(EUR)

    # Almacenamiento de datos.
    carta = Carta(nombre, precio, diccionario_datos[url], url)
    lista_cartas.append(carta)

    # Sleep de 1 segundo entre iteraciones.
    if i < len(diccionario_datos.keys()) - 1:
      time.sleep(1)
      print("--------------------------------------------------")

  else:
    print(f"Error: {response.status_code}")

df = pd.DataFrame([{
  'nombre': carta.nombre,
  'precio_venta': round(float(str(carta.precio_venta).replace(" EUR", "").strip()), 2),
  'precio_compra': float(str(carta.precio_compra)),
  'url': carta.url
} for carta in lista_cartas])

df_ordenado = df.sort_values('precio_venta', ascending = False)
df_ordenado

# Calcular totales y beneficio.
total_compra = df['precio_compra'].sum()
total_venta = df['precio_venta'].sum()
beneficio = total_venta - total_compra

# Crear los datos para la gráfica de barras.
etiquetas = ['Total Compra', 'Total Venta']
valores = [total_compra, total_venta]

# Generar la gráfica de barras horizontales.
plt.figure(figsize = (15, 1))
plt.barh(etiquetas, valores, color = ['lightcoral', 'lightgreen'])
plt.title(f'Beneficio: {beneficio:.2f} EUR')
plt.xlim(0, max(valores) * 1.1)

# Añadir etiquetas de valor a las barras.
for index, value in enumerate(valores):
  plt.text(value, index, f'{value:.2f} EUR', va = 'center')

plt.show()
