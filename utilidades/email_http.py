import requests
import json
import os

def sendMailHTTP(html, asunto, para, token):
    """
    Envía correo usando la API HTTP de Mailtrap como fallback
    Intenta primero con Sending API, luego con Sandbox API
    """
    # Intentar primero con Sending API
    if _try_sending_api(html, asunto, para, token):
        return True
    
    # Si falla, intentar con Sandbox API
    return _try_sandbox_api(html, asunto, para, token)

def _try_sending_api(html, asunto, para, token):
    """Intenta enviar con la API de envío real de Mailtrap"""
    try:
        url = "https://send.api.mailtrap.io/api/send"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "from": {
                "email": "noreply@recetario.com",
                "name": "Recetario"
            },
            "to": [
                {
                    "email": para
                }
            ],
            "subject": asunto,
            "html": html
        }
        
        print(f"[HTTP] Intentando Sending API...")
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        if response.status_code == 200:
            print(f"[HTTP] Correo enviado exitosamente via Sending API a {para}")
            return True
        else:
            print(f"[HTTP] Sending API falló: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"[HTTP] Error en Sending API: {e}")
        return False

def _try_sandbox_api(html, asunto, para, token):
    """Intenta enviar con la API de Sandbox de Mailtrap (testing)"""
    try:
        # Para Sandbox API necesitamos el inbox ID
        inbox_id = os.getenv('MAILTRAP_INBOX_ID', '3856396')  # ID actualizado
        url = f"https://sandbox.api.mailtrap.io/api/send/{inbox_id}"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Estructura exacta según el ejemplo de Mailtrap
        data = {
            "from": {
                "email": "hello@recetario.com",
                "name": "Recetario"
            },
            "to": [
                {
                    "email": para
                }
            ],
            "subject": asunto,
            "html": html,
            "category": "Contact Form"
        }
        
        print(f"[HTTP] Intentando Sandbox API con inbox {inbox_id}...")
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        if response.status_code == 200:
            print(f"[HTTP] Correo enviado exitosamente via Sandbox API a {para}")
            print(f"[HTTP] Response: {response.text}")
            return True
        else:
            print(f"[HTTP] Sandbox API falló: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"[HTTP] Error en Sandbox API: {e}")
        return False