import datetime
import json
import os

ruta_json = 'ultimo_procesado.json'

def extraer_fecha_turno(nombre_archivo:str):
    try:
        # Separar el nombre y la extensión
        nombre, ext = nombre_archivo.rsplit('.', 1)
        if ext != "xlsx":
            raise ValueError("El archivo no tiene la extensión esperada '.xlsx'.")
        
        # Extraer turno y fecha
        turno = nombre[-2:]  # Los últimos dos caracteres (e.g., "TT" o "TM")
        fecha_str = nombre[:-3]  # Todo menos los últimos tres caracteres y el espacio
        
        # Convertir la fecha a un objeto datetime
        fecha = datetime.datetime.strptime(fecha_str, "%d-%m-%Y")
        return fecha, turno
    except Exception as e:
        raise ValueError(f"Error al procesar el nombre del archivo '{nombre_archivo}': {e}")

#print(extraer_fecha_turno('01-01-2021 TT.xlsx')) # 2021-01-01 00:00:00


def ordenar_archivos(archivos):
    """
    Ordena los archivos cronológicamente por fecha y turno (lexicograficamente = alfabeticamente).
    """
    archivos.sort(key=lambda x: extraer_fecha_turno(x['title']))
    return archivos

def registrar_ultimo_procesado(ultimo_archivo, ruta_json=ruta_json):
    """
    Guarda la información del último archivo procesado en un archivo JSON.
    """
    fecha, turno = extraer_fecha_turno(ultimo_archivo['title'])
    ultimo_procesado = {
        "fecha": fecha.strftime("%d-%m-%Y"),
        "turno": turno
    }
    with open(ruta_json, 'w') as archivo_json:
        json.dump(ultimo_procesado, archivo_json)
        print(f"Registrado último procesado: {ultimo_procesado}")


def leer_ultimo_procesado(ruta_json=ruta_json):
    """
    Lee la información del último archivo procesado desde un archivo JSON.
    Devuelve un diccionario con las claves 'fecha' y 'turno'.
    """
    try:
        with open(ruta_json, 'r') as archivo_json:
            contenido = archivo_json.read().strip()
            if not contenido:  # El archivo está vacío
                raise ValueError("Archivo vacío")
            return json.loads(contenido)
    except (FileNotFoundError, ValueError):
        # Retornar valores predeterminados si el archivo no existe o está vacío
        return {"fecha": None, "turno": None}