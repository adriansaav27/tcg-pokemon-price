# 🃏 TCG Pokémon - Extracción y Conversión de Precios

Este proyecto permite **extraer automáticamente los nombres y precios de cartas de Pokémon TCG** desde un listado de URLs, convertir los precios de **USD a EUR**, y generar una tabla ordenada con los resultados.

---

## 🚀 Descripción

El script toma como entrada un archivo `.txt` que contiene URLs de cartas de Pokémon (una por línea).
Luego:
1. Accede a cada página y obtiene el **nombre** y **precio** de la carta.
2. Convierte el precio de **USD → EUR** usando la librería `currex`.
3. Guarda los datos en una lista de objetos.
4. Crea un **DataFrame de Pandas** con los resultados ordenados por precio.

El objetivo es facilitar el análisis o valoración de cartas Pokémon TCG con precios actualizados en euros.

---

## 🧩 Requisitos

Este proyecto fue diseñado para ejecutarse en **Google Colab**.
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
|----------|--------------|
| `tcg-pokemon.ipynb` | Notebook principal con el código. |
| `urls.txt` | Archivo de texto con las URLs de las cartas (una por línea). |
| `README.md` | Este archivo con la documentación del proyecto. |

---

## 🧠 Estructura del código

### Clase `Carta`
Representa una carta con los siguientes atributos:
- `nombre`: Nombre de la carta.
- `precio`: Precio convertido a euros.
- `url`: Enlace original del producto.

### Flujo principal:
1. **Carga de archivo `.txt`** → Se solicita al usuario que suba un archivo con URLs.
2. **Scraping** → Se usa `requests` y `BeautifulSoup` para obtener los datos.
3. **Conversión de moneda** → Se convierte el precio a euros con `currex`.
4. **Creación del DataFrame** → Se ordenan los resultados de mayor a menor precio.
5. **Salida** → Se muestra el DataFrame final con columnas:
   - `nombre`
   - `precio`
   - `url`

---

## 📄 Ejemplo de uso

### 1️⃣ Crear un archivo `urls.txt` con contenido similar a:
```
https://www.cardmarket.com/en/Pokemon/Products/Singles/Base-Set/Charizard
https://www.cardmarket.com/en/Pokemon/Products/Singles/Jungle/Pikachu
```

### 2️⃣ Ejecutar el notebook en Google Colab
Sube el archivo cuando el programa lo solicite:

```
Selecciona el archivo ".txt":
```

### 3️⃣ Resultado esperado
Un DataFrame con las cartas ordenadas por precio en euros:

| nombre | precio (EUR) | url |
|--------|----------------|-----|
| Charizard | 120.50 | https://... |
| Pikachu | 15.30 | https://... |

---

## ⏱️ Notas

- El script espera **1 segundo entre cada petición** para evitar sobrecargar el servidor.
- Si alguna URL falla, se muestra un mensaje con el código de error HTTP.
- Los precios se redondean a **2 decimales**.
