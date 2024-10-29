from google.oauth2 import service_account
from googleapiclient.discovery import build

directorio_credenciales = 'credentials_module.json'

#Iniciar sesion

# Autenticación con credenciales de servicio
creds = service_account.Credentials.from_service_account_file('credentials_module.json', scopes=["https://www.googleapis.com/auth/drive"])

# Construir el servicio de la API de Google Drive
service = build('drive', 'v3', credentials=creds)

# Identifica la carpeta de Google Drive usando su ID
folder_id = '1wXVDj3zk0V9cWc9MzKUWv5RvTK5ysB7y'

def listar_archivos_en_carpeta(folder_id):
    # Llamada a la API para listar archivos en la carpeta especificada
    resultados = service.files().list(q=f"'{folder_id}' in parents", fields="files(id, name)").execute()
    archivos = resultados.get('files', [])

    if not archivos:
        print("No se encontraron archivos.")
    else:
        for archivo in archivos:
            print(f"Nombre: {archivo['name']}, ID: {archivo['id']}")

listar_archivos_en_carpeta(folder_id)