#!/usr/bin/env python
import requests
import json

def test_contact_endpoint():
    """Prueba el endpoint de contacto para verificar que el correo se envía"""
    
    url = "http://localhost:8000/api/v1/contacto"  # URL correcta
    
    data = {
        "nombre": "Usuario de Prueba",
        "correo": "critisauco2@gmail.com",  # Tu email del ejemplo
        "telefono": "+56912345678",
        "mensaje": "Este es un mensaje de prueba para verificar que el sistema de correos funciona correctamente."
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print("=== PROBANDO ENDPOINT DE CONTACTO ===")
    print(f"URL: {url}")
    print(f"Datos: {json.dumps(data, indent=2)}")
    print("="*40)
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Contacto creado y correo enviado exitosamente!")
        else:
            print("❌ Error en el endpoint de contacto")
            
    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar al servidor. ¿Está ejecutándose Django?")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_contact_endpoint()
