# 🃏 TCG Pokémon - Análisis y Conversión de Precios

Este proyecto permite **extraer automáticamente los nombres y precios de cartas de Pokémon TCG** desde un listado de URLs, convertir los precios de **USD a EUR**, y generar un **análisis visual del beneficio total** comparando precios de compra y venta.

---

## 🚀 Descripción

El script toma como entrada un archivo `.csv` que contiene las **URLs** de las cartas y su **precio de compra**.  
Luego:

1. Accede a cada URL y obtiene el **nombre** y **precio de venta (USD)**.  
2. Convierte los precios de **USD → EUR** usando la librería `currex`.  
3. Calcula los **totales de compra y venta**.  
4. Muestra una **gráfica comparativa** con el beneficio obtenido.

El objetivo es facilitar el análisis de inversión y rentabilidad en cartas Pokémon TCG.

---

## 🧩 Requisitos

El proyecto está diseñado para ejecutarse en **Google Colab**.  
Asegúrate de instalar las siguientes dependencias antes de ejecutar el script:

```bash
pip install currex
pip install beautifulsoup4
pip install pandas
pip install openpyxl
```

---

## 📂 Archivos del proyecto

| Archivo | Descripción |
|----------|-------------|
| `tcg_pokemon.py` | Script principal con el código. |
| `urls.csv` | Archivo CSV con las URLs y precios de compra. |
| `README.md` | Este archivo con la documentación del proyecto. |

---

## 🧠 Estructura del código

### Clase `Carta`
Representa una carta con los siguientes atributos:

- `nombre`: Nombre de la carta.  
- `precio_venta`: Precio convertido a euros (extraído desde la web).  
- `precio_compra`: Precio original del CSV (en euros).  
- `url`: Enlace original del producto.

### Flujo principal:

1. **Carga del archivo `.csv`** → El usuario sube el archivo con columnas `url` y `price`.  
2. **Scraping** → Se obtiene el nombre y el precio de venta desde la web.  
3. **Conversión de moneda** → Se convierte el precio USD → EUR con `currex`.  
4. **Creación del DataFrame** → Se ordenan los resultados por `precio_venta`.  
5. **Cálculo de totales** → Se suman precios de compra y venta para obtener el **beneficio total**.  
6. **Visualización** → Se genera una gráfica de barras horizontales comparando los totales.

---

## 📄 Ejemplo de uso

### 1️⃣ Crear un archivo `urls.csv` con este formato:

```csv
url,price
https://www.pricecharting.com/es/game/pokemon-japanese-vstar-universe/mewtwo-vstar-221,100
https://www.pricecharting.com/es/game/pokemon-japanese-vstar-universe/charizard-vstar-212,10
```

### 2️⃣ Ejecutar el script en Google Colab

Sube el archivo cuando el programa lo solicite:

```
Selecciona el archivo ".csv":
```

### 3️⃣ Resultado esperado

Un DataFrame con las cartas ordenadas por precio de venta:

| nombre | precio_venta | precio_compra | url |
|--------|---------------------|----------------|-----|
| Charizard | 120.50 | 100 | https://... |
| Pikachu | 15.30 | 10 | https://... |

Y una **gráfica de barras** mostrando el beneficio total:

```
Beneficio: 25.80 EUR
[■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■] 135.80 EUR
[■■■■■■■■■■■■■■■■■] 110.0 EUR
```

---

## ⏱️ Notas

- El script espera **1 segundo entre cada petición** para evitar sobrecargar el servidor.  
- Si una URL falla, se muestra el **código de error HTTP**.  
- Los precios se redondean a **2 decimales**.  
- La gráfica muestra el **total de compra, total de venta y beneficio final**.
