# Caso de estudio

## Empresa de transporte de cargas

Situación (dominio del problema):

Una empresa de transporte de cargas necesita un software que la ayude a organizarse con la carga de las camiones. La empresa puede recibir requerimiento para transportar packings, cajas sueltas y bidones que transportan líquido.

* Un packing es una estructura de madera que arriba tiene un montón de cajas, se envuelve todo con plástico para que no se desbanden las cajas. Todas las cajas tiene el mismo peso.
* return self.peso
* Para cada packing se informa qué llevan las cajas, p.ej. Material de construcción.
* De cada caja suelta se informa el peso individualmente, son todas distintas.
* El peso de un bidón es su capacidad en litros por la densidad (o sea, cuántos kg pesa un litro) del líquido que se le carga. Los bidones van siempre llenos hasta el tope.

Cada camión puede llevar hasta una carga máxima medida en kg. Además, cada camión puede tener el siguiente estado:

* disponible para la carga (en cuyo caso ya puede tener cosas cargadas).
* estar en reparación.
* estar de viaje al destino.
* esta de regreso.

Requerimientos:

* Se pide al menos el formulario de gestión de camiones, no obstante, se pueden crear todos los formularios que se deseen.
* Considerar que no se puede saturar un camión con más peso de lo que su carga máxima permite (75%).
* Bajar una carga (siempre que el camión se encuentre disponible y la carga presente dentro de él)
* Permitir modificar el estado de un camión

Saber:

* Obtener el listado de cargas contenidas en un camion.
* Estado de los camiones.

Se adjunta un diagrama de clases que podrá ser usado como referencia.
Se adjunta un archivo con cada tipo de carga (cajas, packing y bidones) y sus atributos correspondientes que podran ser utilizados para cargar las tablas.

Objetivos a evaluar:

* manejo de clases (si las hubiere).
* creación de formulario/s.
* lógica de solución al problema planteado (libre elección) y de las dudas que pudiesen existir. No se responden preguntas.
* manejo de DB (Postgres o MySql).
* interpretación del objetivo del challenge.

Premisa:

* se pueden aplicar criterios propios para resolver el probema especialmente en aquillos casos donde hubiera mas de una interpretación.

Archivos CSV:

* se adjuntan archivos con la naturaleza o tipo de datos en cada caso. Pueden usar esto archivos para volcarlos a la DB.

Entrega:

* Armar un readme expliando la forma de ejecucion del projecto y consideraciones si las hubiere.
