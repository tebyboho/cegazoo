import os
from matplotlib import ticker
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.express as px
import re
from datetime import datetime

# Globales
dir_name = 'CAJAS_FORMATEADAS'
ruta_raiz = os.path.join(os.getcwd(), dir_name)

patrones_vendedoras = {
    'Sofia': r'(?i)\bsofi+i*[a]*\b',
    'Magui': r'(?i)\bmagui+i*[s]*\b'
    }

# Definir la ruta de almacenamiento del DataFrame
pickle_file = 'data_acumulada.pkl'

# Verificar si el archivo ya existe
if os.path.exists(pickle_file):
    # Si existe, cargar los datos del archivo
    df_acumulado = pd.read_pickle(pickle_file)
    print("Datos cargados desde el archivo pickle.")
    df = df_acumulado.copy()
else:
    # Si no existe, crear un nuevo DataFrame y procesa los archivos
    df_acumulado = pd.DataFrame()

    for root, dirs, files in os.walk(ruta_raiz):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(".xlsx") and not file.startswith("~$"):
                df = pd.read_excel(file_path, engine='openpyxl')
                datos = {
                            "fecha": df.iloc[0, 0],
                            "turno": df.iloc[0, 2],
                            "vendedor": df.iloc[0, 6],
                            "total_accesorios": df.iloc[1, 0],
                            "total_balanceados": df.iloc[1, 2],
                            "total_medicamentos": df.iloc[1, 4],
                            "total_animales": df.iloc[1, 6],
                            "total_acuario": df.iloc[1, 8],
                            "pagos": df.iloc[1, 12],
                            'pagos_caja': df.iloc[1, 13],
                            "venta_efectivo": df.iloc[18, 13],
                            "total_credito": df.iloc[19, 13],
                            "total_debito": df.iloc[20, 13],
                            "total_sobres": df.iloc[21, 13],
                            "total_venta": df.iloc[25, 13],
                            "file": file
                                }
                df_acumulado = pd.concat([df_acumulado, pd.DataFrame([datos])], ignore_index=True)
                df_acumulado['fecha'] = df_acumulado['file'].str[:-7].replace(" ", '')
                df_acumulado['fecha'] = pd.to_datetime(df_acumulado['fecha'], errors='coerce', dayfirst=True)
                
    # Guardar el DataFrame en un archivo para futuras ejecuciones
    df_acumulado.to_pickle(pickle_file)
    print("Datos procesados y guardados en el archivo pickle.")
  
def total_ventas_historico():
    df = df_acumulado.groupby(pd.Grouper(key='fecha', freq='ME'))['total_venta'].sum().reset_index()
    plt.figure(figsize=(10, 6))
    plt.plot(df['fecha'], df['total_venta'], marker='o')
    plt.title('Total de Ventas a lo Largo del Tiempo')
    plt.xlabel('Fecha')
    plt.ylabel('Total de Ventas')
    plt.grid(True)
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  # Mostrar un tick por mes
    plt.gcf().autofmt_xdate()
    plt.gca().yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,}'))
    plt.show()
    
    '''fig = px.line(df, x="fecha", y="total_venta",
                 hover_data=["total_venta"],
                 labels={"total_venta": "Total de Ventas"})
    grafico interactivo..
    fig.show()'''


def ventas_comparacion():
    ventas_por_mes = df_acumulado.groupby(df_acumulado['fecha'].dt.to_period('M')).sum(numeric_only=True)
    categorias = ['total_accesorios', 'total_balanceados', 'total_medicamentos', 'total_animales', 'total_acuario']
    
    ventas_por_mes[categorias].plot(kind='bar', figsize=(10, 6), width=0.7)
    plt.title('Ventas por Categoría y Mes')
    plt.ylabel('Total Ventas')
    plt.xlabel('Mes')
    plt.xticks(rotation=45)
    plt.legend(title="Categorías")
    plt.tight_layout()
    plt.show()


def total_pagos():
    df = df_acumulado.groupby(pd.Grouper(key='fecha', freq='ME'))['pagos'].sum().reset_index()
    plt.figure(figsize=(10, 6))
    plt.plot(df['fecha'], df['pagos'], marker='o')
    plt.title('Total PAGOS a lo Largo del Tiempo')
    plt.xlabel('Fecha')
    plt.ylabel('PAGOS')
    plt.grid(True)
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  # Mostrar un tick por mes
    plt.gcf().autofmt_xdate()
    plt.gca().yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,}'))
    plt.show()


def obtener_patron_vendedora(vendedora_form):
    for key, patron in patrones_vendedoras.items():
        if re.search(patron, vendedora_form):
            return patron
    return None


def filtrar_ventas(start_date=None, end_date=None, vendedora=None, categoria=None):
    # Filtrar por fechas si se proporcionan
    if start_date:
        start_date = pd.to_datetime(datetime.strptime(start_date,'%Y-%m-%d' ), errors='coerce')
        df_filtrado = df_acumulado[df_acumulado['fecha'] >= start_date]
    else:
        df_filtrado = df_acumulado.copy()
    
    if end_date:
        end_date = pd.to_datetime(datetime.strptime(end_date, '%Y-%m-%d'), errors='coerce')
        df_filtrado = df_filtrado[df_filtrado['fecha'] <= end_date]
        
    # Filtrar por vendedora si se proporciona
    if vendedora and vendedora != 'Elegir':
        filtro_vendedor = df_filtrado['vendedor'].str.contains(obtener_patron_vendedora(vendedora), regex=True)
        df_filtrado = df_filtrado[filtro_vendedor]
    
    if categoria and categoria != 'Elegir':
        columna_categoria = f"total_{categoria.lower()}"
        if columna_categoria in df_filtrado.columns:
            total_ventas = df_filtrado[columna_categoria].sum()
        else:
            total_ventas = 0  # Valor por defecto si la categoría no existe
    else:
        total_ventas = df_filtrado['total_venta'].sum()  # Suma de todas las ventas si no se especifica categoría

    return total_ventas

# print(filtrar_ventas('02-01-2024', '31-01-2024'))