# palabros

Esto no es más que un CLI inspirado en [Wordle ES](https://wordle.danielfrg.com/), que a su vez es una adaptación de [Wordle](https://www.powerlanguage.co.uk/wordle/). No hay mucho de original con **palabros**, más allá de lo _sexy friki_ de jugar a través de la terminal.

![palabros screenshot](https://rawcdn.githack.com/vermicida/palabros/4ab0e73a58113195ca8c4e71698ceb832388f01d/assets/screenshot.png)

Puedes leer el artículo [Creando un Wordle para consola](https://medium.com/@vermicida/creando-un-wordle-para-consola-b284a6ad10a0) de Medium para conocer con algo más de detalle cómo planteé el desarrollo de **palabros**.

## Cómo jugar

**palabros** está publicado en [PyPI](https://pypi.org/), por lo que su instalación es tan sencilla como:

```bash
pip install palabros
```

Se muestra la instalación con [pip](https://pip.pypa.io/en/stable/cli/pip_install/), pero se puede usar cualquier otro gestor de paquetes, como [Poetry](https://python-poetry.org/docs/cli/#add), por ejemplo.

Una vez instalado, tendremos disponible el comando `palabros play`, que podremos usar para jugar con una palabra de nuestra conveniencia:

```bash
palabros play coche
```

Al ejecutar el comando pueden darse las siguientes opciones:

- Si es la primera ejecución del día, cuenta como primer intento de adivinar la palabra semilla
- Si no es la primera ejecución del día, cuenta como un intento sucesivo de adivinar la palabra semilla -hasta un total de 6 intentos-
- Si la palabra semilla se adivinó, o bien no se adivinó pero se consumió el número de intentos, se mostrará una cuenta atrás a cumplir para que se genere una nueva palabra semilla y, por tanto, se pueda volver a jugar

Como resumen: puedes ejecutar `palabros play` cuantas veces quieras, pero solo las 6 primeras del día cuentan como intentos de adivinar la palabra semilla.

Si le das al coco lo suficiente y lo combinas con un poco de suerte, darás con la palabra semilla :-)

## Cómo trabajar

Si quieres trastear con el código, hacer añadidos o cambios, necesitas saber que **palabros** está desarrollado con [Python 3.8](https://www.python.org/downloads/) y utiliza [Poetry](https://python-poetry.org/) como gestor de paquetes. Una vez tengas ambos instalados y, también, el repositorio clonado, debes hacer lo siguiente:

```bash
poetry install
```

Esto creará un nuevo entorno virtual para el proyecto e instalará en él todas las dependencias necesarias. Con esto ya podrás ejecutar **palabros** localmente y desarrollar a tu antojo.

¡Ah, importante! Se hace uso de [pre-commit](https://pre-commit.com/) para validar automáticamente la calidad del código que se _commitea_, ejecutando por nosotros los checks de [pyupgrade](https://github.com/asottile/pyupgrade), [isort](https://github.com/PyCQA/isort), [black](https://github.com/psf/black) y [flake8](https://github.com/PyCQA/flake8). Antes de hacer tu primer commit no olvides configurar el hook:

```bash
poetry run pre-commit install
```

Esto es necesario hacerlo una sola vez tras clonar el repositorio e instalar las dependencias. Ahora, con cada `git commit`, tendremos una validación de calidad del código _by the face_ sin tener que intervenir manualmente.

## Por hacer

Aunque **palabros** sea fruto de un par de tardes ociosas y no tenga pretensión alguna, sí que tiene cosas que son mejorables y, conforme el tiempo me lo vaya permitiendo, las iré atendiendo. Tengo fichadas las siguientes:

- ~~El diccionario de palabras que usa quizá no sea el mejor. Muchas de ellas no son de uso común y, a su vez, no contiene otras que sí lo son; me gustaría encontrar un dataset o corpus de sustantivos que tenga información de frecuencia de uso. No me culpes mucho si te salen palabras que desconoces -a mí también me pasa-.~~ He reconstruido el diccionario desde cero usando 3.750 palabras del [Corpus de Referencia del Español Actual (CREA) - Listado de frecuencias](https://corpus.rae.es/lfrecuencias.html) que ofrece gratuitamente la RAE. Ha sido tedioso, ya que la fuente es un _.txt_ sin formato alguno y con el encoding incorrecto, pero ya está hecho. Gracias [@iknite](https://github.com/iknite) por la ayuda.
- A nivel arquitectura hay una separación de capas evidente, pero no es perfecta. Sería genial marcar bien los límites y que cada módulo, clase y método asuma solo y exclusivamente las responsabilidades que son de su competencia.
- Muchos pequeños detalles no están contemplados. Por ejemplo, la limpieza de las palabras que indica el usuario se limita a tildes y diéresis, pero se pueden colar otros gazapos.
- La gestión de errores es algo -muy- parca.
- Los tests unitarios. La ausencia de ellos, vamos.

## Créditos

Aquí quiero mencionar a varias personas.

Por un lado, la idea de **palabros** surje de [Wordle ES](https://wordle.danielfrg.com/), y ésta a su vez de [Wordle](https://www.powerlanguage.co.uk/wordle/). Mi trabajo se resume en poner un par de neuronas a codificar una versión CLI que nada tiene que ver oficialmente con los servicios mencionados. Si os mola **palabros**, dad las gracias a [Daniel Rodriguez](https://twitter.com/danielfrg) y a [Josh Wardle](https://twitter.com/powerlanguish), que son, respectivamente, los responsables de Wordle ES y Wordle.

Por otro lado, agradecer a [Carlos Fenollosa](https://twitter.com/cfenollosa) el trabajo realizado para crear el [Diccionario libre en español](https://cfenollosa.com/blog/diccionario-libre-en-espanol---free-spanish-dictionary.html) que he utilizado para generar el diccionario de **palabros**. Todas las palabras están debidamente tipificadas en el diccionario: yo las he filtrado para quedarme exclusivamente con nombres (comunes, compuestos, femeninos, masculinos y ambiguos) de 5 letras. Suman más de 3600 palabras: nos da para jugar diaramiente a **palabros** los próximos 10 años.

## Licencia

La licencia que he contemplado es [MIT](./LICENSE), que si no me equivoco, permite hacer con este código cualquier modificación, publicación y explotación posible. Dicho de otro modo, más directo: haced con este código lo que más os mole. Eso sí, si os hacéis millonarios con él, que lo dudo, por favor, invitadme a un café; es lo único que pido.
