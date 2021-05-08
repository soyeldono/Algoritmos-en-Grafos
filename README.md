# PyGraph

PyGraph es una aplicación creada para el curso de Algoritmos en Grafos la cual tiene como objetivo, el poder trabajar con grafos unidireccionales. 

![intro](https://user-images.githubusercontent.com/38016639/117523676-43e94300-af7f-11eb-8c63-6e3a39ea33f2.gif)

## Instalación y Ejecución

1. Revisa que tienes las librerias necesarias:
 - pywin32==300
 - pygame==2.0.1
 - win32gui==221. 6
2.  Clona/Descarga el repositorio
```
git clone https://github.com/soyeldono/Algoritmos-en-Grafos
``` 
3. Ejecuta el archivo **main.py** en la misma carpeta de **gui.py pygraph.py**

## Manual de Uso

PyGraph funciona a base de presionado de teclas específicas. Sin importar la tecla especial que se presione, abajo a la izquierda de la ventana saldrá un mensaje con la tecla que actualmente esta activa.

**Crear Nodos**
Presiona _LCTRL_ una sola vez y ahora solo da click en donde quieras y las veces que quieras para crear un Nodo por cada click. Para desactivar esta función vuelve a presionar _LCTRL_. (_LCTRL_ = Left CTRL)

**Crear Aristas**
Presiona _LSHIFT_ una sola vez y ahora haz click encima de los nodos que quieras crear una Arista. Para desactivar esta función vuelve a presionar _LSHIFT_. (_LSHIFT_ = Left SHIFT)

**Mover Nodos**
Presiona _m_ una sola vez y ahora haz click encima de los nodos que quieras mover de lugar. Para desactivar esta función vuelve a presionar _m_. (_m_= tecla m minúscula)

**Borrar Nodos/Aristas**
Presiona _Supr_ una sola vez y ahora haz click encima del nodo o arista para borrarlo. Para desactivar esta función vuelve a presionar _Supr_.

**Inicializar Valores de las Aritas Aleatoriamente**
Presiona _LCTRL_ + _LSHIFT_ + _r_ 

**Reiniciar Proyecto**
Presiona _LALT_ una sola vez y después _r_. (Borrará el grafo que actualmente estes trabajando)(_LALT_ = Left ALT)

**ZOOM y Mover el Grafo Entero (en desarrollo)** 
En caso de tener proyectos muy grandes se puede hacer zoom con solo hacer girar la rueda del mouse (scroll mouse), el zoom se hará en torno a la posición del mouse. Para mover el grafo entero manten presionado el click derecho del mouse y mueve a la dirección donde quiere que se mueva. (Esta función aun sigue en desarrollo por lo que si llegas a encontrar un bug agradecería que lo comentaras para poder solucionarlo)

**Guardar Proyecto**
Presiona _LCTRL_ y después _s_. (Se guardara en formato *.pg)

**Abrir Proyecto**
Presiona _LCTRL_ y después _o_. 

**Reiniciar Varibales**
Si ya habías presionado una tecla especial pero te equivocaste puesde nuevamente presionar la misma tecla para cancelarla o también puedes presionar _ESC_, la diferencia es que _ESC_ reinicia todas las variables de las teclas ya presionadas.

**Visualizar Valores de Aristas**
No debes tener activados ninguna tecla especial (ejemplo: _LSHIFT_,_LCTRL_,etc...), solo presiona la tecla _a_. Para dejar de ver los valores nuevamente presiona _a_ sin tener telcas especiales activadas.

## Algoritmos y Funciones

**Árbol Generador**

Para usar Prim debe estar activa la tecla _CTRL_ y después presionar _p_. Al actvar este método se bloquean TODAS las demas funcionalidades hasta que termine.

Para usar Kruskal debe estar activa la tecla _CTRL_ y después presionar _k_. Al actvar este método se bloquean TODAS las demas funcionalidades hasta que termine.

**Grafos Aleatorios**

Presionar la tecla _1_ hace que entres a un submenu donde permite crear grafos de manera aleatoria, para ello hay 2 formas. La primera es usando probabilidades y la segunda es por cantidad de aristas. Para aumentar|disminuir la cantidad de nodos presiona _flecha arriba_|_flecha abajo_, para aumentar|disminuir la probabilidad|cantidad de aritas presiona _flecha izq_|_flecha der_. Y para cambiar de modo entre probabilidad y cantidad de aristas es necesario hacer click en el circulo que esta a la izquierda del modo al cual se quiere acceder.

**Saber si el grafo es Árbol,Conexo**

Presiona la tecla _i_, en la esquina inferior derecha saldrá dos textos los cuales te dirán que propiades cumple tu grafo.
