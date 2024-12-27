from helpers import ordenar_archivos, leer_ultimo_procesado, registrar_ultimo_procesado, extraer_fecha_turno
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import pandas as pd
import datetime
import os
import time

inicio = time.time()

### GLOBALES
credential_file = 'credentials_module.json'

# Definir la ruta de almacenamiento del DataFrame
pickle_file_drive = 'datos_del_drive.pkl'

folder_id = '1wXVDj3zk0V9cWc9MzKUWv5RvTK5ysB7y' #Este id es de CAJAS/2023 nomas
ruta_json = 'ultimo_procesado.json'

def login():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(credential_file)

    if gauth.access_token_expired:
        gauth.Refresh()
        gauth.SaveCredentialsFile(credential_file)
    else:
        gauth.Authorize()
    
    return GoogleDrive(gauth)
    
drive = login()
    
def listar_archivos(folder_id):
    
    archivos = drive.ListFile({'q': f" '{folder_id}' in parents and trashed=false"}).GetList()
    archivos_encontrados = []
    
    for archivo in archivos:
        if archivo['mimeType'] == 'application/vnd.google-apps.folder': #si el archivo es una carpeta
            # Llamo recursivamente para explorar subcarpetas
            archivos_encontrados.extend(listar_archivos(archivo['id'])) #le paso el folder_id = el id del archivo que es documento xd
        elif archivo['title'].endswith('.xlsx'):
            archivos_encontrados.append(archivo)
            #print(archivo['title'])
            
    return archivos_encontrados

# Extraigo informacion de las cajas
def procesar_archivos(archivos, ruta_json):
    
    datos_lista = []
    
    ultimo_procesado =  leer_ultimo_procesado(ruta_json)
    ultima_fecha = datetime.datetime.strptime(ultimo_procesado['fecha'], "%d-%m-%Y") if ultimo_procesado['fecha'] else None
    ultimo_turno = ultimo_procesado['turno']
    
    # Ordeno cronológicamente 
    archivos_ordenados = ordenar_archivos(archivos)
    
    primera_vuelta = ultima_fecha is None or ultimo_turno is None 
    
    print(primera_vuelta, type(primera_vuelta))
    
    for archivo in archivos_ordenados:
        # Extraigo fecha y turno del nombre
        fecha_actual, turno_actual = extraer_fecha_turno(archivo['title'])
        
        # Verificar si el archivo ya fue procesado
        if primera_vuelta or ((ultima_fecha is not None and fecha_actual > ultima_fecha) or 
                              (ultima_fecha is not None and fecha_actual == ultima_fecha and turno_actual > ultimo_turno)):
            archivo.GetContentFile(archivo['title'])  # Descarga el archivo localmente
            df = pd.read_excel(archivo['title'], engine='openpyxl')  # Cargar con pandas
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
                                    "file": archivo['title']
                                        }
            # Agrega el diccionario a la lista
            datos_lista.append(datos)
            
            # Registrar el archivo como último procesado
            registrar_ultimo_procesado(archivo, ruta_json)
            
            # Elimino el archivo local despues de haberlo cargado
            os.remove(archivo['title'])
            
    return datos_lista


archivos_encontrados = listar_archivos(folder_id)
# Creo el Dataframe para todas las cajas
df_acumulado = pd.DataFrame(procesar_archivos(archivos_encontrados, ruta_json))
df_acumulado['fecha'] = df_acumulado['file'].str[:-7].replace(" ", '')
df_acumulado['fecha'] = pd.to_datetime(df_acumulado['fecha'], errors='coerce', dayfirst=True)
    

#Guardar el DataFrame en un archivo para futuras ejecuciones
df_acumulado.to_pickle(pickle_file_drive)



fin = time.time()

print('''
      ====================================================================================================
      ''')
print("\tTiempo de ejecución: {:.2f} segundos".format(fin - inicio))
print('''
      ====================================================================================================
      ''')