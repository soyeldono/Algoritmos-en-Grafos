# PyGraph 2.0

PyGraph allows to works with graph unidirectional. Pygraph was created to use in the class "Algoritmos en Grafos".

![2021-08-21 13-04-17](https://user-images.githubusercontent.com/38016639/130331370-347a4dee-b4ef-4f0e-8288-46583533ab98.gif)

## Instalatrion and Execute

1. Install the requirements:
- python >= 3.7
 - pywin32==300
 - pygame==2.0.1
 - win32gui==221. 6
2.  Clone the repo
```
git clone https://github.com/soyeldono/Algoritmos-en-Grafos.git
``` 
3. Execute **main.py**

## How to use

**Create Node** _LCTRL_ + _LCLICK_ (_LCTRL_: Left Control, _LCLICK_: Left Click)

**Create Edges** _LSHIFT_ + _LCLICK_ on Node (_LSHIFT_:Left Shift)

**Move Nodes** Press _m_ and then _LCLICK_ on Node

**Delete Node|Edge** _Supr_ + _LCLICK_ on Node or Edge

**Show Info** _i_, show ID Node and Edges Values

**Show Extra Info** _LCTRL_ + _i_

## Random Graph

The program have 3 algortihm to create a random graph:

- Probability: Use a 'p' probability to create the graph
- M edges: Use 'm' edges to create the graph
- Connected: Ensure that the graph will be connected

By default the program create a graph with 10 Nodes with 0.5 probability to make an edge. To use it press _1_

## Random Tree

You can choose between a binary random tree or random tree. To use it press _2_

## Minimun Spanning Tree

- Algorithm Prim: Press _p_
- Algotithm Kruskal: Press _k_

Press _space_ to continue the animation.

## Functions

- is_connected
- is_tree
- num_connected_components
