#  Scripts estaciones LISN

En este repositorio se encuentras los scripts utilizados para enviar data almacenada en el servidor de los instrumentos de Magnetómetro, GNSS, Ionosondas y Receptores de Ecos Oblicuos.

### MAGNETÓMETROS

Actualmente (Marzo 2026) se encuentran en funcionamiento las siguientes estaciones: 

* Jicamarca, Piura, Huancayo, Ancón, Arequipa, Nazca, Leoncito, Cuiaba, Puerto Maldonado, Leticia, Sao Luis, Tarapoto, Alta Floresta, Huancayo Magdas, Ica Magdas, Tingo María Magdas y Ancón Magdas

Para el envío de datos desde el servidor a la Web de LISN se usaron dos scripts:

`magneto_ITD.py`

Este script lo ejecutamos con python3. Además, este script reconoce 5 parámetros al momento de su ejecución: year_inferior, year_superior, mes_inferior, mes_superior, estacion y datatype. 
<br>
Ejemplo: python3 magneto_ITD.py 2026 2026 3 3 huam minute
<br>
<br>
Cómo se observa, este código puede enviar datos desde periodos de tiempo hasta solo un día. Utiliza la librería externa creada en Jicamarca que tiene como nombrer: jrodb. Con ello, se crean datasets utilizando un token, tomando en consideración el tipo de dato y caracterizando a través de paramétros entre los cuales se encuentran nombre o título.

Después de la creación de los datasets se ubican en el servidor los datos que se almacenan por cada estación y dependiendo de su tipo, para luego incluirlos a cada dataset como recursos y visualizarlo en formato TXT o PNG.

`magneto_ITD.sh`

Este bash llama al script magneto_ITD.py para que pueda ejecutarse de forma automatizada en un crontab, tomando en consideración todas las estaciones, los tipos de datos y la fecha actual.
