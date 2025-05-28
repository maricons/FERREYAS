import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from functools import lru_cache
import json
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

# Configuración
BDE_EMAIL = os.getenv('BDE_EMAIL')
BDE_PASSWORD = os.getenv('BDE_PASSWORD')
BASE_URL = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx"

# Códigos de series para diferentes monedas
CURRENCY_SERIES = {
    'USD': 'F073.TCO.PRE.Z.D',  # Dólar observado
    'EUR': 'F073.TCO.EUR.Z.D',  # Euro
    'UF': 'F073.UF.PRE.Z.D',    # UF
    'UTM': 'F073.UTM.PRE.Z.D'   # UTM
}

class CurrencyConverter:
    def __init__(self):
        try:
            self.session = requests.Session()
            if not BDE_EMAIL or not BDE_PASSWORD:
                logger.error("Credenciales de la API del Banco Central no configuradas")
                raise ValueError("Credenciales de la API del Banco Central no configuradas")
            logger.info("CurrencyConverter inicializado correctamente")
        except Exception as e:
            logger.error(f"Error al inicializar CurrencyConverter: {str(e)}")
            raise

    @lru_cache(maxsize=32)
    def get_exchange_rate(self, currency_code, date=None):
        """
        Obtiene la tasa de cambio para una moneda específica.
        
        Args:
            currency_code (str): Código de la moneda (USD, EUR, etc.)
            date (datetime, optional): Fecha específica. Por defecto, None (usa fecha actual)
            
        Returns:
            float: Tasa de cambio
            
        Raises:
            ValueError: Si la moneda no está soportada o hay un error en la API
        """
        try:
            logger.info(f"Obteniendo tasa de cambio para {currency_code}")
            
            if currency_code not in CURRENCY_SERIES:
                logger.error(f"Moneda no soportada: {currency_code}")
                raise ValueError(f"Moneda no soportada: {currency_code}")

            # Si no se especifica fecha, usar la fecha actual
            if date is None:
                date = datetime.now()

            # Formatear fechas para la API
            end_date = date.strftime('%Y-%m-%d')
            start_date = (date - timedelta(days=5)).strftime('%Y-%m-%d')

            # Construir los parámetros de la API
            params = {
                'user': BDE_EMAIL,
                'pass': BDE_PASSWORD,
                'function': 'GetSeries',
                'timeseries': CURRENCY_SERIES[currency_code],
                'firstdate': start_date,
                'lastdate': end_date
            }

            logger.info(f"Realizando petición a la API con parámetros: {params}")

            # Realizar la solicitud a la API
            response = self.session.get(BASE_URL, params=params, timeout=10)
            
            # Verificar errores de autenticación
            if response.status_code == 401:
                logger.error("Error de autenticación con la API del Banco Central")
                raise ValueError("Error de autenticación: Credenciales inválidas")
            
            response.raise_for_status()

            # Procesar la respuesta
            try:
                data = response.json()
            except json.JSONDecodeError as e:
                logger.error(f"Error al decodificar JSON de la respuesta: {str(e)}")
                logger.error(f"Respuesta recibida: {response.text}")
                raise ValueError("Error al procesar la respuesta de la API")

            logger.info(f"Respuesta de la API: {data}")
            
            # Verificar si hay datos
            if not data or 'Series' not in data or not data['Series']:
                logger.error(f"No hay datos disponibles para {currency_code}")
                raise ValueError(f"No hay datos disponibles para {currency_code}")

            # Obtener el valor más reciente
            series = data['Series']
            if not series['Obs']:
                logger.error(f"No hay observaciones para {currency_code}")
                raise ValueError(f"No hay observaciones para {currency_code}")

            # Filtrar observaciones válidas (statusCode = 'OK')
            valid_observations = [obs for obs in series['Obs'] if obs['statusCode'] == 'OK']
            
            if not valid_observations:
                logger.error(f"No hay observaciones válidas para {currency_code}")
                raise ValueError(f"No hay observaciones válidas para {currency_code}")

            # Tomar el valor más reciente
            try:
                latest_value = float(valid_observations[-1]['value'])
            except (KeyError, ValueError, IndexError) as e:
                logger.error(f"Error al obtener el valor más reciente: {str(e)}")
                raise ValueError("Error al procesar el valor de la tasa de cambio")

            logger.info(f"Tasa de cambio obtenida para {currency_code}: {latest_value}")
            return latest_value

        except requests.RequestException as e:
            logger.error(f"Error de conexión con la API: {str(e)}")
            raise ValueError(f"Error al conectar con la API del Banco Central: {str(e)}")
        except Exception as e:
            logger.error(f"Error inesperado: {str(e)}")
            raise ValueError(f"Error inesperado: {str(e)}")

    def convert_to_clp(self, amount, from_currency):
        """
        Convierte un monto desde una moneda extranjera a CLP.
        
        Args:
            amount (float): Monto a convertir
            from_currency (str): Código de la moneda origen
            
        Returns:
            dict: Diccionario con el monto convertido y la tasa usada
            
        Raises:
            ValueError: Si hay un error en la conversión
        """
        try:
            logger.info(f"Iniciando conversión de {amount} {from_currency} a CLP")
            
            # Validar el monto
            try:
                amount = float(amount)
            except (TypeError, ValueError):
                logger.error(f"Error al convertir monto a float: {amount}")
                raise ValueError("El monto debe ser un número válido")

            if amount <= 0:
                logger.error(f"Monto inválido: {amount}")
                raise ValueError("El monto debe ser mayor que 0")

            # Obtener la tasa de cambio
            try:
                rate = self.get_exchange_rate(from_currency)
            except ValueError as e:
                logger.error(f"Error al obtener tasa de cambio: {str(e)}")
                raise ValueError(f"Error al obtener tasa de cambio: {str(e)}")
            
            # Realizar la conversión
            converted_amount = amount * rate
            
            result = {
                "amount_clp": round(converted_amount, 2),
                "rate": rate,
                "currency": from_currency,
                "original_amount": amount,
                "date": datetime.now().strftime('%Y-%m-%d')
            }
            
            logger.info(f"Conversión exitosa: {result}")
            return result
            
        except ValueError as e:
            logger.error(f"Error en la conversión: {str(e)}")
            raise ValueError(f"Error en la conversión: {str(e)}")
        except Exception as e:
            logger.error(f"Error inesperado en la conversión: {str(e)}")
            raise ValueError(f"Error inesperado: {str(e)}")

    def get_available_currencies(self):
        """
        Retorna la lista de monedas disponibles para conversión.
        
        Returns:
            list: Lista de diccionarios con información de las monedas
        """
        return [
            {"code": "USD", "name": "Dólar Estadounidense"},
            {"code": "EUR", "name": "Euro"},
            {"code": "UF", "name": "Unidad de Fomento"},
            {"code": "UTM", "name": "Unidad Tributaria Mensual"}
        ] 