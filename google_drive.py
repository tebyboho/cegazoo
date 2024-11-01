from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import pandas as pd
import os
# from pydrive2.files import GoogleDriveFileList

credential_file = 'credentials_module.json'

# Definir la ruta de almacenamiento del DataFrame
pickle_file_drive = 'datos_del_drive.pkl'

def login():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(credential_file)

    if gauth.access_token_expired:
        gauth.Refresh()
        gauth.SaveCredentialsFile(credential_file)
    else:
        gauth.Authorize()
    
    return GoogleDrive(gauth)
    
# drive = login()

folder_id = '1gwSDn17rGivG59Q2nvqt5mRaXJX5ZfYK'
# file_list = drive.ListFile({'q': f" '{folder_id}' in parents and trashed=false"}).GetList()
# for file in file_list:
#     print(f"{file['title']} ---> {file['id']}")
    
    

# def listar_archivos(folder_id):
    
#     archivos = drive.ListFile({'q': f" '{folder_id}' in parents and trashed=false"}).GetList()
#     archivos_encontrados = []
    
#     for archivo in archivos:
#         if archivo['mimeType'] == 'application/vnd.google-apps.folder':
#             # Llamo recursivamente para explorar subcarpetas
#             archivos_encontrados.extend(listar_archivos(archivo['id']))
#         elif archivo['title'].endswith('.xlsx'):
#             archivos_encontrados.append(archivo)
            
#     return archivos_encontrados


# # Ejemplo de uso
# folder_id = '1wXVDj3zk0V9cWc9MzKUWv5RvTK5ysB7y'
# archivos_xlsx = listar_archivos(folder_id)


# for archivo in archivos_xlsx:
#     df_acumulado = pd.DataFrame()
#     archivo.GetContentFile(archivo['title'])  # Descarga el archivo localmente
#     df = pd.read_excel(archivo['title'], engine='openpyxl')  # Cargar con pandas
#     datos = {
#                             "fecha": df.iloc[0, 0],
#                             "turno": df.iloc[0, 2],
#                             "vendedor": df.iloc[0, 6],
#                             "total_accesorios": df.iloc[1, 0],
#                             "total_balanceados": df.iloc[1, 2],
#                             "total_medicamentos": df.iloc[1, 4],
#                             "total_animales": df.iloc[1, 6],
#                             "total_acuario": df.iloc[1, 8],
#                             "pagos": df.iloc[1, 12],
#                             'pagos_caja': df.iloc[1, 13],
#                             "venta_efectivo": df.iloc[18, 13],
#                             "total_credito": df.iloc[19, 13],
#                             "total_debito": df.iloc[20, 13],
#                             "total_sobres": df.iloc[21, 13],
#                             "total_venta": df.iloc[25, 13],
#                             "file": archivo['title']
#                                 }

#     df_acumulado = pd.concat([df_acumulado, pd.DataFrame([datos])], ignore_index=True)
#     df_acumulado['fecha'] = df_acumulado['file'].str[:-7].replace(" ", '')
#     df_acumulado['fecha'] = pd.to_datetime(df_acumulado['fecha'], errors='coerce', dayfirst=True)
#     # Elimino el archivo local despues de haberlo cargado
#     os.remove(archivo['title'])
#     # Procesar el DataFrame (ejemplo de extracción de información)
#     # Aquí puedes realizar tus operaciones de análisis

# # Guardar el DataFrame en un archivo para futuras ejecuciones
# df_acumulado.to_pickle(pickle_file_drive)
# print("Datos procesados y guardados en el archivo pickle.")
# print(df.head())  # Imprimir para verificar


if os.path.exists(pickle_file_drive):
    # Si existe, cargar los datos del archivo
    df_acumulado = pd.read_pickle(pickle_file_drive)
    print("Datos del DRIVE cargados desde el archivo pickle.")


df = df_acumulado.copy()

print(df.head(5))