from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
from transbank.common.integration_type import IntegrationType
import os
from dotenv import load_dotenv
from datetime import datetime
import uuid
import json

# Cargar variables de entorno
load_dotenv()

class WebpayPlus:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        self.app = app
        # Configurar Webpay en modo integración
        integration_type = IntegrationType.TEST
        commerce_code = "597055555532"  # Código de comercio de prueba
        api_key = "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C"  # Clave de prueba
        
        print("\n=== CONFIGURACIÓN DE WEBPAY ===")
        print(f"Tipo de integración: {integration_type}")
        print(f"Código de comercio: {commerce_code}")
        print(f"API Key: {api_key[:10]}...{api_key[-10:]}")
        
        self.tx = Transaction(WebpayOptions(
            commerce_code=commerce_code,
            api_key=api_key,
            integration_type=integration_type
        ))
    
    def generate_buy_order(self):
        """Genera un número de orden único"""
        return str(uuid.uuid4())
    
    def create_transaction(self, amount, buy_order, session_id, return_url):
        """Crea una transacción en Webpay Plus"""
        try:
            print("\n=== CREANDO TRANSACCIÓN EN WEBPAY ===")
            print("Datos de entrada:")
            print(f"- Monto: {amount}")
            print(f"- Orden de compra: {buy_order}")
            print(f"- ID de sesión: {session_id}")
            print(f"- URL de retorno: {return_url}")
            
            # Crear la transacción usando la instancia de Transaction
            response = self.tx.create(
                buy_order=buy_order,
                session_id=session_id,
                amount=amount,
                return_url=return_url
            )
            
            print("\nRespuesta de Webpay:")
            print(json.dumps(response, indent=2))
            
            # La respuesta de Webpay puede tener token/token_ws y url
            if isinstance(response, dict):
                token = response.get('token_ws') or response.get('token')
                url = response.get('url')
            else:
                token = getattr(response, 'token_ws', None) or getattr(response, 'token', None)
                url = getattr(response, 'url', None)
            
            if not token or not url:
                print("Error: No se pudo obtener token o url de la respuesta")
                print("Respuesta completa:", response)
                raise ValueError("Respuesta de Webpay inválida")
            
            # Preparar la respuesta en el formato que espera el frontend
            result = {
                'token': token,
                'url': url
            }
            
            print("\nDatos de redirección preparados:")
            print(json.dumps(result, indent=2))
            return result
            
        except Exception as e:
            print("\n=== ERROR AL CREAR TRANSACCIÓN ===")
            print(f"Error: {str(e)}")
            print(f"Tipo de error: {type(e)}")
            import traceback
            print("Traceback completo:")
            print(traceback.format_exc())
            raise
    
    def commit_transaction(self, token):
        """Confirma una transacción en Webpay Plus"""
        try:
            print(f"\n=== CONFIRMANDO TRANSACCIÓN ===")
            print(f"Token: {token}")
            
            response = self.tx.commit(token=token)
            
            print("\nRespuesta de commit:")
            print(json.dumps(response, indent=2))
            return response
            
        except Exception as e:
            print("\n=== ERROR AL CONFIRMAR TRANSACCIÓN ===")
            print(f"Error: {str(e)}")
            raise
    
    def status(self, token):
        """Consulta el estado de una transacción"""
        try:
            print(f"\n=== CONSULTANDO ESTADO DE TRANSACCIÓN ===")
            print(f"Token: {token}")
            
            response = self.tx.status(token=token)
            
            print("\nRespuesta de status:")
            print(json.dumps(response, indent=2))
            return response
            
        except Exception as e:
            print("\n=== ERROR AL CONSULTAR ESTADO ===")
            print(f"Error: {str(e)}")
            raise
    
    def refund(self, token, amount):
        """Realiza la devolución de una transacción"""
        try:
            print(f"\n=== INICIANDO DEVOLUCIÓN ===")
            print(f"Token: {token}")
            print(f"Monto: {amount}")
            
            response = self.tx.refund(token=token, amount=amount)
            
            print("\nRespuesta de refund:")
            print(json.dumps(response, indent=2))
            return response
            
        except Exception as e:
            print("\n=== ERROR AL REALIZAR DEVOLUCIÓN ===")
            print(f"Error: {str(e)}")
            raise 