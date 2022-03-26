# Diagnostic
Repository for initial Git diagnostic

# Importante:
El dataset necesita estar en el mismo directorio que el archivo *main.ipynb* y los módulos *.py*. El nombre está colocado por defecto como *tweets.json*, pero
este puede ser cambiado ya que es pasado como parámetro cuando se llama a cada una de las funciones auxiliares.

Debido al gran tamaño del dataset (1,3G), para responder cada una de las tareas que se nos pidían se ocupó solo 50.000 tweets del total. Esto fue para disminuir de forma considerable el tiempo de cómputo y facilitar el trabajo. Para realizar esto se hizo uso de *read_json* de la librería pandas, la que permite leer el archivo por chunks de cierto tamaño, determinado por el parámetro *chunksize* y de esa forma iterar sobre cada chunk y no tener en memoria todo el dataset cargado al mismo tiempo. Si se desea aumentar la cantidad de tweets leídos basta con cambiar los parámetros de cada función auxiliar importada en el archivo principal.
