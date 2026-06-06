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
    # El campo 'price' es opcional: si no existe o está vacío, se guarda None.
    price = fila.get('price', '').strip()
    diccionario_datos[url] = float(price) if price else None

print(f"Se han cargado {len(diccionario_datos)} registros")

lista_cartas = []

for i, url in enumerate(diccionario_datos.keys()):
  print(f"Procesando URL: {url}")

  # Petición.
  response = requests.get(url)

  if response.status_code == 200:
    html_content = response.text
    print("HTML obtenido correctamente")

    soup = BeautifulSoup(html_content, 'html.parser')

    # Nombre.
    h1 = soup.find('h1', id='product_name')
    nombre = h1.contents[0].strip()

    # Precio de venta (scraping).
    precio = soup.find('td', class_='price js-price')
    precio_texto = precio.text.replace(',', '').strip()
    precio_numerico = re.findall(r'[\d.]+', precio_texto)
    precio_venta = float(precio_numerico[0])
    precio_venta = USD(precio_venta).to(EUR)

    # Almacenamiento (precio_compra puede ser None).
    carta = Carta(nombre, precio_venta, diccionario_datos[url], url)
    lista_cartas.append(carta)

    if i < len(diccionario_datos.keys()) - 1:
      time.sleep(1)
      print("--------------------------------------------------")

  else:
    print(f"Error: {response.status_code}")

df = pd.DataFrame([{
  'nombre': carta.nombre,
  'precio_venta': round(float(str(carta.precio_venta).replace(" EUR", "").strip()), 2),
  'precio_compra': carta.precio_compra,
  'url': carta.url
} for carta in lista_cartas])

df_ordenado = df.sort_values('precio_venta', ascending = False)
df_ordenado

# Totales y gráfica.
total_venta = df['precio_venta'].sum()
tiene_compra = df['precio_compra'].notna().any()

if tiene_compra:
  total_compra = df['precio_compra'].sum()
  beneficio = total_venta - total_compra

  etiquetas = ['Total Compra', 'Total Venta']
  valores = [total_compra, total_venta]
  colores = ['lightcoral', 'lightgreen']
  titulo = f'Beneficio: {beneficio:.2f} EUR'
else:
  # Sin precios de compra: solo mostrar el valor total.
  etiquetas = ['Total Venta']
  valores = [total_venta]
  colores = ['lightgreen']
  titulo = f'Valor total de la colección: {total_venta:.2f} EUR'

# Gráfica.
plt.figure(figsize=(15, 1))
plt.barh(etiquetas, valores, color = colores)
plt.title(titulo)
plt.xlim(0, max(valores) * 1.1)

for index, value in enumerate(valores):
  plt.text(value, index, f'{value:.2f} EUR', va = 'center')

plt.show()
