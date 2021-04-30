# PyGraph

PyGraph es una aplicación creada para el curso de Algoritmos en Grafos la cual tiene como objetivo, el poder trabajar con grafos unidireccionales. 

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

## Algoritmos y Funciones

