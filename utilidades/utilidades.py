#email
import smtplib
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
from smtplib import SMTPResponseException
from . import email_http

def sendMail(html, asunto, para):
    """Envía un correo HTML usando Mailtrap u otro SMTP.

    Agrega:
      - Debug activable con SMTP_DEBUG=1
      - Fallback automático entre puertos comunes (valor inicial + 2525, 587, 465, 25)
      - Logs detallados con causa exacta y traceback en último fallo
    """
    # Fallback forzado si se define SMTP_FORCE_HTTP=1
    if os.getenv('SMTP_FORCE_HTTP', '0') == '1':
        print('[SMTP] SMTP_FORCE_HTTP=1 -> usando directamente fallback HTTP')
        token = os.getenv('MAILTRAP_TOKEN')
        if token:
            from . import email_http
            if email_http.sendMailHTTP(html, asunto, para, token=token):
                return True
            else:
                print('[SMTP] Fallback HTTP directo falló')
                return False

    msg = MIMEMultipart('alternative')
    remitente = os.getenv('SMTP_FROM') or os.getenv('SMTP_USER')
    msg['From'] = remitente
    msg['To'] = para
    msg['Subject'] = asunto
    msg.attach(MIMEText(html, 'html'))

    host = os.getenv('SMTP_SERVER')
    user = remitente
    password = os.getenv('SMTP_PASSWORD')
    debug_enabled = os.getenv('SMTP_DEBUG', '0') == '1'
    per_port_timeout = int(os.getenv('SMTP_PER_PORT_TIMEOUT', '12') or 12)
    fast_fail = os.getenv('SMTP_FAST_FAIL', '0') == '1'
    primary_port = int(os.getenv('SMTP_PORT', '587') or 587)
    fallback_ports = []
    for p in [primary_port, 2525, 587, 465, 25]:
        if p not in fallback_ports:
            fallback_ports.append(p)

    if not all([host, user, password]):
        print("[SMTP] Faltan variables de entorno: SMTP_SERVER / SMTP_USER / SMTP_PASSWORD")
        return False

    last_error = None
    for port in fallback_ports:
        try:
            print(f"[SMTP] Intentando conexión host={host} puerto={port} tls=auto ...")
            if port == 465:
                server = smtplib.SMTP_SSL(host, port, timeout=per_port_timeout)
            else:
                server = smtplib.SMTP(host, port, timeout=per_port_timeout)
                try:
                    server.ehlo()
                    server.starttls()
                    server.ehlo()
                except Exception as tls_e:
                    print(f"[SMTP] STARTTLS no disponible/omitido en puerto {port}: {tls_e}")

            if debug_enabled:
                server.set_debuglevel(1)

            server.login(user, password)
            server.sendmail(user, [para], msg.as_string())
            server.quit()
            print(f"[SMTP] Envío exitoso por puerto {port}")
            return True
        except SMTPResponseException as e:
            last_error = e
            print(f"[SMTP][{port}] Error respuesta servidor code={getattr(e, 'smtp_code', '?')} msg={getattr(e, 'smtp_error', e)}")
        except Exception as e:
            last_error = e
            print(f"[SMTP][{port}] Error general: {e.__class__.__name__}: {e}")
            if fast_fail:
                print('[SMTP] FAST_FAIL activo: saltando el resto de puertos')
                break
        finally:
            try:
                server.quit()
            except Exception:
                pass

    if last_error:
        print("[SMTP] Falló el envío en todos los puertos probados. Último traceback:")
        traceback.print_exception(type(last_error), last_error, last_error.__traceback__)
    # Intentamos fallback HTTP si hay token en entorno
    try:
        token = os.getenv('MAILTRAP_TOKEN')
        if token:
            print('[SMTP] Intentando fallback HTTP con MAILTRAP_TOKEN')
            ok = email_http.sendMailHTTP(html, msg['Subject'], para, token=token)
            if ok:
                print('[SMTP->HTTP] Envío realizado por fallback HTTP')
                return True
            else:
                print('[SMTP->HTTP] Fallback HTTP falló')
    except Exception as e:
        print('[SMTP->HTTP] Error al intentar fallback HTTP:', e)

    return False