# Prueba tecnica UNBC de Scraping con Selenium en python
## Problema:
El objetivo de este ejercicio es desarrollador un script en Python utilizando Selenium para automatizar la extracción de datos desde la página web del Banco Central de Chile.
Específicamente, el script debe extraer tanto el valor de la Unidad de Fomento (UF) como el valor del Dólar (USD) del día, desde la página principal del sitio web.
### Tareas a realizar:
- Iniciar un navegador web con Selenium.
- Navegar a la página principal del Banco Central de Chile (https://www.bcentral.cl/inicio).
- Extraer el valores diarios de la UF y del USD.
- Imprimir los resultados en formato JSON en la consola.
### Anotaciones:
- Se agregan 3 soluciones con diferentes cambios:
### Solucion 1:
- La solucion 1 entrega los resultados siendo estos un string y el simbolo monetario
### Solucion 2:
- La solucion 2 entrega los resultados con el texto extraido convertido en un numero decimal
### Solucion 3:
- La solucion 3 pregunta por consola en una secuencia la etiqueta del elemento, luego sus clases para buscar todos los elementos que encajen.
- Luego pregunta por los index de dichos elementos en caso de que existan multiples etiquetas con la misma clases en este ejercicio en particular serian los index 0 y 2
- Luego pregunta por el nombre de las keys a las que se van a asignar dichos valores encontrados para asignarlos, las keys deben de ser nombradas en el mismo orden en el que se ingreso cada index en el caso de este ejercicio seria UF,USD.
- La solucion 3 funciona de manera dinamica ya que en el momento de la prueba la informacion que se desea extraer esta dentro de una etiqueta de parrafo y con ciertas clases, si en cuyo caso cambian las clases solo se ejecutaria de nuevo el script y se agregarian las clases nuevas, sin mencionar que podria funcionar para otras paginas web(cambiando en el codigo el sitio web) especificando el elemento DOM y sus clases
>Se anexan los JSON esperados al dia de hoy 30 de julio
