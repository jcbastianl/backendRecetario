#!/usr/bin/env python
import os
import sys
import django
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from utilidades.utilidades import sendMail

def test_email():
    print("=== TEST DE ENVÍO DE CORREO ===")
    print(f"SMTP_SERVER: {os.getenv('SMTP_SERVER')}")
    print(f"SMTP_PORT: {os.getenv('SMTP_PORT')}")
    print(f"SMTP_USER: {os.getenv('SMTP_USER')}")
    print(f"SMTP_FROM: {os.getenv('SMTP_FROM')}")
    print(f"SMTP_DEBUG: {os.getenv('SMTP_DEBUG')}")
    print(f"SMTP_FORCE_HTTP: {os.getenv('SMTP_FORCE_HTTP')}")
    print(f"MAILTRAP_TOKEN: {os.getenv('MAILTRAP_TOKEN')[:8]}...")
    print(f"MAILTRAP_INBOX_ID: {os.getenv('MAILTRAP_INBOX_ID', 'No configurado')}")
    print("="*40)
    
    # Email de prueba
    html_content = """
    <h1>Email de prueba</h1>
    <p>Este es un email de prueba para verificar la configuración de Mailtrap.</p>
    <p>Si recibes este correo, la configuración está funcionando correctamente.</p>
    """
    
    # Cambia esta dirección por tu email de prueba
    email_destino = "test@example.com"  # Cambia esto por tu email
    
    print(f"Enviando email de prueba a: {email_destino}")
    
    try:
        resultado = sendMail(html_content, "Test de configuración Mailtrap", email_destino)
        if resultado:
            print("✅ Email enviado exitosamente!")
        else:
            print("❌ Error al enviar el email")
    except Exception as e:
        print(f"❌ Excepción al enviar email: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_email()
