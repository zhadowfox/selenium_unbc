import json
from decimal import Decimal
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


def setup_driver():
    """Configura el WebDriver para Chrome."""
    # Se crea un instancia del chrome para agregar las configuraciones opcionales
    options = webdriver.ChromeOptions()
    # Agregamos la option de modo headless para acelerar un poco
    options.add_argument("--headless")
    # Agregamos la opcion de configuracio del nivel de log para
    # evitar recibir en la consola algun log que puede
    # tener el sitio web o advertencias del mismo generados por algun JS que se este ejecutando
    options.add_argument("--log-level=3")
    # definimos el driver segun las opciones previamente agregadas
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=options)
    return driver


def get_elements_inner_text(driver, css_selector):
    """Intenta localizar un elemento usando CSS Selector y extraer su texto, 
    como hay varios elementos del DOM (P) con las mismas clases es
    necesario especificar su indice para este caso en particular
    basado en el índice."""
    values = {}
    try:
        # Espera a que el elemento esté presente en la página
        elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, css_selector))
        )
        # Validamos si fueron encontrados o no
        if elements:
            # Al ser encontrados son asignados acada propiedad del diccionario
            values = {
                # antes de asignar el valor llamamos a la funcion convert_to_numbers
                # para asi convertir dichos string recibidos en solo valores numericos
                # con sus respectivos decimales
                "UF": convert_to_numbers(elements[0].text.strip().split("\n")[0]),
                "USD": convert_to_numbers(elements[2].text.strip().split("\n")[0])
            }
    # Maneja la excepción específica de tiempo de espera agotado cuando no encuentre los elementos
    except TimeoutException:
        print("""No se encontraron los elementos, validar que
              las clases y el elemento DOM sean correctos""")
        values = {
            "Error": "No se encuentran los elementos"
        }
    except Exception as e:
        # Captura cualquier excepción no esperada y proporciona un mensaje de error por consola
        # y asigna dicha informacion al JSON esperado
        print(
            f"Error al extraer el texto para\n{css_selector}, ExceptionError: {e}")
        values = {
            "ExceptionError": str(e)
        }
    return values


def convert_to_numbers(number_str):
    """Convierte una cadena de string que en realidad deberia
      de ser un valor numerico con decimales a numerico"""
    # Elimina el signo de dólar y las comas para retornar un flotante
    cleaned_number_str = re.sub(r'[^\d,]', '', number_str).replace(',', '.')
    return float(cleaned_number_str)


def main():
    """Función principal para ejecutar el script."""
    # Llamamos a la funcion setup_driver para configurar el WebDriver
    driver = setup_driver()
    # Esta variable va a contener el diccionario con el resultado
    # generado por la funcion get_elements_text()
    values = {}
    try:
        # Navega a la página principal del Banco Central de Chile
        driver.get("https://www.bcentral.cl/inicio")
        # Agregamos el elemento DOM seguido de sus clases iniciando estas con un .
        # ejemplo: si tratamos de extraer de un div con las clases font-bold y text-color-blue
        # la variable css_classes quedaria asi div.font-bold.text-color-blue
        # si el sitio web cambia sus clases y elemento DOM que contiene la informacion
        # es necesario de actualizar dicha variable
        css_classes = 'p.basic-text.fs-2.f-opensans-bold.text-center.c-blue-nb-2'
        # Almacenamos el JSON recibido luego de obtener el texto dentro del elemento
        # este contiene no solo los resultados si no tambien algun tipo de mensaje de error
        # en caso de encontrar alguno
        values = get_elements_inner_text(driver, css_classes)
    except Exception as e:
        # Captura cualquier excepción y proporciona un mensaje de error y el JSON con los errores
        print(f"Ocurrio un error inesperados {e}")
    finally:
        # Cierra el navegador y libera los recursos
        # Imprime los resultados en formato JSON
        print(json.dumps(values, indent=4))
        driver.quit()


# Ejecuta la función principal
if __name__ == "__main__":
    main()
