import json
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
def get_elements_text(driver, css_selector, array_of_indexes):
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
        # Almacena el nombre de la KEY a la que va a ser asignado el valor que se extraiga
        # es necesesario validar que el nombre que le desea asignar si corresponda con el index
        # del elemento que desea extraer, ejemplo, desea extrar dos P con la
        # misma clase y sus indices y en el sitio web existen 4 elementos P con
        # la misma clase y cada uno seria informacion correspondiente a:
        # Dolar, Peso Colombiano, Peso Chileno y Titulo de una seccion y solo desean
        #  la informacion de Dolar y Peso chileno los indices serian 0 y 2 asi que
        #  las dos keys que debe de ingresar en orden serian Dolar,Peso Chileno
        keys_str = input("""Ingrese nombres de claves separados por comas\nen el mismo orden que el index correspondiente del\nelemento que desea extraer (UF,USD,...): """)
        keys = keys_str.split(',')
        # Validamos que la cantidad de KEYS si corresponda con la cantidad de indexes
        if len(array_of_indexes) != len(keys):
            raise ValueError(f"""\nLa longitud de array_of_indexes ({len(array_of_indexes)}) no coincide con la longitud de keys ({len(keys)}).\n
                             Asegurese de que las keys sean la misma cantidad de elementos que desea extraer""")
        # Validamos si fueron encontrados o no
        if elements:
            # Al ser encontrados son asignados acada propiedad del diccionario
            # Realizamo un ciclo en el que recorremos los elementos encontrados
            # asignamos la Key y el texto que fue encontrado
            # Inicializamos una variable para realizar seguimiento a cada key y recorrerlas ambas en un solo ciclo
            i = 0
            for index in array_of_indexes:
                key = keys[i].strip()  # Limpiar espacios en blanco
                i += 1
                if key:  # Valida que la clave no esté vacía
                    values[key] = elements[index].text.strip().split("\n")[0]
    # Maneja la excepción específica de tiempo de espera agotado cuando no encuentre los elementos
    except TimeoutException:
        print("""No se encontraron los elementos, validar que\nlas clases y el elemento DOM sean correctos""")
        values = {
            "Error": "No se encuentran los elementos"
        }
    except Exception as e:
        # Captura cualquier excepción no esperada y proporciona un mensaje de error por consola
        # y asigna dicha informacion al JSON esperado
        print(
            f"Error al extraer el texto para\n{css_selector}, ExceptionError: {e}")
        values = {
        }
    return values
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
        dom_element_tag = input("""Ingrese el nombre de la etiqueta del elemento\nDOM del que desea extraer los datos, (ejemplos: div, p, span): """)
        classes_of_dom_element_tag = input("""Ingrese las clases sin espacios y cada clase\ncon un punto(.) al inicio de esta,\n(ejemplo:.font-bold.text-blue): """)
        index_of_elements = input("""Ingrese el index separados por un espacio de cada elemento que desea extraer\nya que pueden existir varios elementos con la misma etiqueta de DOM y\nlas mismas clases (los indexes comienzan desde 0 siento este el primero): """)
        # Remueve los espacios y creamos un array con cada uno de los numeros
        index_of_elements = index_of_elements.split()
        # Genera un array nuevamente convirtiendo cada elemento a un entero con cada uno de los numeros
        # en caso de no ser un valor numerico este sera ignorado y arrojara un mensaje en la consola
        array_of_indexes = []
        for num_str in index_of_elements:
            try:
                num = int(num_str)
                array_of_indexes.append(num)
            except ValueError:
                print(f"'{num_str}' no es un número válido y será ignorado.")
        elements_to_scrap = dom_element_tag + classes_of_dom_element_tag
        # Almacenamos el JSON recibido luego de obtener el texto dentro del elemento
        # este contiene no solo los resultados si no tambien algun tipo de mensaje de error
        # en caso de encontrar alguno
        values = get_elements_text(driver, elements_to_scrap, array_of_indexes)
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
