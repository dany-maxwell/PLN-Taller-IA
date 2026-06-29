#Conclusiones

-La tokenización es lo más sencillo ya que se puede realizar hasta con lo mas básico de Python
ejemplo. split().
-La normalización requiere mas pasos amenos que se usen librerías como “spacy” o “nltk”, sin
embargo, utilizamos un diccionario para las abreviaturas, tal vez podría utilizarse una librería que
contenga más.
-La lematización fue lo mas complicado ya que cuando se utilizaba una palabra con la primera letra
en mayúscula, la librería spacy lo confundía con un sustantivo
-Por último el standing no fue tan difícil ya que la librería se encargaba de hacerlo, eso si algunas
palabras se confundían por estar en español, aunque eso pasa tanto con la lematización como con
las abreviaciones en la normalización.

#Recomendaciones
-A la hora de normalizar utilizar un diccionario con almenos unas mil palabras abreviadas o una base de datos en Español
-Utilizar librerias como "spacy" o "nltk" es bastante mas rapido que hacer la tokenizacion y normalizacion a mano
