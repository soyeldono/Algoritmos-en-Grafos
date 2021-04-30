from pygraph import PyGraph,Node
import pygame as pg
from pygame.locals import *
import sys
from sys import stdin
from win32api import GetSystemMetrics
import logging
from gui import load_graph,save_graph,info,dialogs,extra_info
import json
from win32con import SWP_NOMOVE, SWP_NOSIZE, HWND_TOP
from win32gui import FindWindow, SetWindowPos
import time

__version__ = "1.5.1"

def recolor_graph(g):
    for i in g.nodes:
        if i is not None:
            i.color =  (255,255,255)
    for i in g.color_edge:
        g.color_edge[i] = (255,0,0)

def command_save(g,logger):
    recolor_graph(g)
    save_graph(g,logger)
    window_name = "Crear Grafos"
    handle = FindWindow(None, window_name)
    SetWindowPos(handle, HWND_TOP, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
    #print("se guarda el arbol")


logging.basicConfig(filename="Pygraph.log",format='%(asctime)s %(message)s',filemode="w")
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)

logger.info("Pygraph version:"+str(__version__))

w = GetSystemMetrics(0)-200
h = GetSystemMetrics(1)-200
#print(w,h)
pg.init()
screen = pg.display.set_mode((w,h))
pg.display.set_caption("Crear Grafos")

G = PyGraph()

prev_mouse_pos = None
detect_mouse_move = []
iterator_mouse_move = 0

a_node = False # agregar nodo
l_alt = False # para reiniciar el arbol
just_s = [False,None] # para mostrar el id de los nodos y los pesos de las aristas

Block = [False,None] #para evitar problemas se bloquean acciones mientras se ejecutan algoritmos de tiempo real
new_graph = None #para el nuevo grafo
save_new_graph = None #pregunta 
output = None #donde se guarda el nuevo grafo en caso de que asi sea

press_1 = False
default_p = ['p',5,0.5]
default_m = ['m',5,6]

press_i = False
is_connected = False
is_tree = False

zoom = 1.0

while True:
    screen.fill((0,0,0))    
    keys = pg.key.get_pressed()

    if keys[pg.K_LCTRL] and keys[pg.K_LSHIFT] and keys[pg.K_r]: # inicializar valores de aristas de forma aleatoria
        time.sleep(0.1)
        G.init_random_edge_values()

    if pg.mouse.get_pressed()[2]:
        if prev_mouse_pos is None:
            prev_mouse_pos = pg.mouse.get_pos()
        if iterator_mouse_move == 0 or iterator_mouse_move == 10:
            detect_mouse_move.append(pg.mouse.get_pos())
        if 0 <= iterator_mouse_move <= 10:
            iterator_mouse_move += 1

        if iterator_mouse_move == 11:
            for i in G.nodes:
                # mover en Y
                if abs(detect_mouse_move[0][1]-detect_mouse_move[1][1]) >= 60:
                    if pg.mouse.get_pos()[1] < prev_mouse_pos[1]:
                        i.coordinates = (i.coordinates[0], i.coordinates[1]-(25/zoom))
                    elif pg.mouse.get_pos()[1] > prev_mouse_pos[1]:
                        i.coordinates = (i.coordinates[0], i.coordinates[1]+(25/zoom))

                # mover en X
                if abs(detect_mouse_move[0][0]-detect_mouse_move[1][0]) >= 60:
                    if pg.mouse.get_pos()[0] < prev_mouse_pos[0]:
                        i.coordinates = (i.coordinates[0]-(25/zoom), i.coordinates[1])
                    elif pg.mouse.get_pos()[0] > prev_mouse_pos[0]:
                        i.coordinates = (i.coordinates[0]+(25/zoom), i.coordinates[1])
            iterator_mouse_move = 0
            detect_mouse_move = []

    elif not pg.mouse.get_pressed()[2]:
        prev_mouse_pos = None
    
    if G.a_edge[0] and press_1 and save_new_graph[2] != len(G.edges_values):
        default_m[2] = len(G.edges_values)
        save_new_graph[2] = len(G.edges_values)
        if just_s[1] is not None:
            just_s[1] = (G.nodes,G.edges_values)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            logger.info("se cierra la aplicación")
            sys.exit()
        elif event.type == pg.KEYDOWN: 
            if event.key == pg.K_LCTRL and not Block[0]: # Press Left CTRL, create node
                logger.info("se presionó CTRL")
                a_node = not a_node
                G.a_edge = [False,False]
                G.del_ = False
                G.m_node = False
                G.m_node_f = None
                G.follow = None
                l_alt = False
                just_s[0] = False
            elif event.key == pg.K_LSHIFT and not Block[0]: # Press Left Shift, create edge
                logger.info("se presionó SHIFT para crear una arista")
                G.a_edge[0] = not G.a_edge[0]
                a_node = False
                G.del_ = False
                G.m_node = False
                G.m_node_f = None
                l_alt = False
                just_s[0] = False
            elif event.key == pg.K_DELETE and not Block[0]: # Press Del, del node or edge
                logger.info("se presionó Supr/Delete para borrar un nodo o arista")
                G.del_ = not G.del_
                a_node = False
                G.a_edge = [False,False]
                G.m_node = False
                G.m_node_f = None
                G.follow = None
                l_alt = False
                just_s[0] = False
            elif event.key == pg.K_LALT and not Block[0]: # Press ALT, condition for restar graph
                l_alt = True
                G.del_ = False
                a_node = False
                G.a_edge = [False,False]
                G.m_node = False
                G.m_node_f = None
                G.follow = None
                just_s[0] = False
            elif event.key == pg.K_m and not Block[0]: # Press m, move node
                logger.info("se presionó m para mover un nodo")
                G.m_node = not G.m_node
                G.del_ = False
                a_node = False
                G.a_edge = [False,False]
                G.follow = None
                l_alt = False
                just_s[0] = False
            elif event.key == pg.K_a: # Press a, show all nodes and edges
                logger.info("se presionó a")
                just_s[0] = not just_s[0]
                if just_s[0]:
                    just_s[1] = (G.nodes,G.edges_values)
                else:
                    just_s[1] = None
                G.m_node = False
                G.del_ = False
                a_node = False
                G.a_edge = [False,False]
                G.follow = None
                l_alt = False
            elif event.key == pg.K_r and l_alt and not Block[0]: # restar graph
                G.nodes[0].set_()
                del G
                G = PyGraph()
                l_alt = False
                just_s = [False,None]
                is_connected = G.isConnected()
                logger.info("se ha borrado el grafo")
            elif event.key == pg.K_i:
                press_i = not press_i
                is_connected = G.isConnected()
                is_tree = G.isTree()

            elif event.key == pg.K_1: # presionar 1, crear grafos aleatorios
                press_1 = not press_1
                if len(G.nodes) > 0 and press_1:
                    if dialogs(screen,'ask') == "yes":
                        command_save(G,logger)
                    else:
                        window_name = "Crear Grafos"
                        handle = FindWindow(None, window_name)
                        SetWindowPos(handle, HWND_TOP, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
                    G.nodes[0].set_()
                    del G
                    G = PyGraph()
                a_node = False
                G.a_edge = [False,False]
                G.del_ = False
                G.m_node = False
                G.m_node_f = None
                G.follow = None
                l_alt = False
                just_s[0] = False
                save_new_graph = default_p
                if press_1:
                    G.Erdos_Reny(save_new_graph[0],save_new_graph[1],save_new_graph[2],(w,h))
                    if just_s[1] is not None:
                        just_s[1] = (G.nodes,G.edges_values)
                is_connected = G.isConnected()
                is_tree = G.isTree()
            elif event.key == pg.K_UP and press_1: # presionar la flecha a arriba, aumentar los nodos en los grafos aleatorios
                G.nodes[0].set_()
                del G
                G = PyGraph()
                save_new_graph[1] += 1
                default_p[1] = save_new_graph[1]
                default_m[1] = save_new_graph[1]
                G.Erdos_Reny(save_new_graph[0],save_new_graph[1],save_new_graph[2],(w,h))
                if just_s[1] is not None:
                    just_s[1] = (G.nodes,G.edges_values)
                is_connected = G.isConnected()
                is_tree = G.isTree()
            elif event.key == pg.K_DOWN and press_1: # presionar la flecha a la abajo
                if save_new_graph[0] == 'm':
                    if ((len(G.nodes)-2)*(len(G.nodes)-1)/2) >= save_new_graph[2]:
                        if save_new_graph[1] != 1:
                            G.nodes[0].set_()
                            del G
                            G = PyGraph()
                            save_new_graph[1] -= 1 
                            default_p[1] = save_new_graph[1]
                            default_m[1] = save_new_graph[1]
                            G.Erdos_Reny(save_new_graph[0],save_new_graph[1],save_new_graph[2],(w,h))
                            if just_s[1] is not None:
                                just_s[1] = (G.nodes,G.edges_values)
                else:
                    if save_new_graph[1] != 1:
                        G.nodes[0].set_()
                        del G
                        G = PyGraph()
                        save_new_graph[1] -= 1 
                        default_p[1] = save_new_graph[1]
                        default_m[1] = save_new_graph[1]
                        G.Erdos_Reny(save_new_graph[0],save_new_graph[1],save_new_graph[2],(w,h))
                        if just_s[1] is not None:
                            just_s[1] = (G.nodes,G.edges_values)
                is_connected = G.isConnected()
                is_tree = G.isTree()
            elif event.key == pg.K_LEFT and press_1: # presionar la flecha a la izquierda
                if save_new_graph[0] == 'p':
                    if save_new_graph[2] != 0:
                        G.nodes[0].set_()
                        del G
                        G = PyGraph()
                        save_new_graph[2] = round(save_new_graph[2]-0.1,ndigits=1)
                        default_p[2] = save_new_graph[2]
                        G.Erdos_Reny(save_new_graph[0],save_new_graph[1],save_new_graph[2],(w,h))
                        if just_s[1] is not None:
                            just_s[1] = (G.nodes,G.edges_values)
                if save_new_graph[0] == 'm':
                    if save_new_graph[2] != 0:
                        G.nodes[0].set_()
                        del G
                        G = PyGraph()
                        save_new_graph[2] -= 1
                        default_m[2] = save_new_graph[2]
                        G.Erdos_Reny(save_new_graph[0],save_new_graph[1],save_new_graph[2],(w,h))
                        if just_s[1] is not None:
                            just_s[1] = (G.nodes,G.edges_values)
                is_connected = G.isConnected()
                is_tree = G.isTree()
            elif event.key == pg.K_RIGHT and press_1: # presionar la flecha a la derecha
                if save_new_graph[0] == 'p':
                    if save_new_graph[2] != 1.0:
                        G.nodes[0].set_()
                        del G
                        G = PyGraph()
                        save_new_graph[2] = round(save_new_graph[2]+0.1,ndigits=1)
                        default_p[2] = save_new_graph[2]
                        G.Erdos_Reny(save_new_graph[0],save_new_graph[1],save_new_graph[2],(w,h))
                        if just_s[1] is not None:
                            just_s[1] = (G.nodes,G.edges_values)
                if save_new_graph[0] == 'm':
                    if ((len(G.nodes)-1)*(len(G.nodes))/2) > save_new_graph[2]:
                        G.nodes[0].set_()
                        del G
                        G = PyGraph()
                        save_new_graph[2] += 1
                        default_m[2] = save_new_graph[2]
                        G.Erdos_Reny(save_new_graph[0],save_new_graph[1],save_new_graph[2],(w,h))
                        if just_s[1] is not None:
                            just_s[1] = (G.nodes,G.edges_values)
                is_connected = G.isConnected()
                is_tree = G.isTree()
            elif event.key == pg.K_p and a_node and not Block[0]: # Prim algorithm
                logger.info("Metodo Prim iniciado")
                Block[0] = True
                Block[1] = "Prim"
                l_alt = False
                G.del_ = False
                a_node = False
                G.a_edge = [False,False]
                G.m_node = False
                G.m_node_f = None
                G.follow = None
                just_s[0] = False
                new_graph = PyGraph()
            elif event.key == pg.K_k and a_node and not Block[0]: # Kruskal algorithm
                logger.info("Metodo Kruskal iniciado")
                Block[0] = True
                Block[1] = "Kruskal"
                l_alt = False
                G.del_ = False
                a_node = False
                G.a_edge = [False,False]
                G.m_node = False
                G.m_node_f = None
                G.follow = None
                just_s[0] = False
                new_graph = PyGraph()
            elif event.key == pg.K_RETURN and not Block[0] and save_new_graph == "¿": # Confirm save graph by algorithm
                del G
                G = output
                recolor_graph(G)
                save_new_graph = None
                output = None
                just_s[1] = (G.nodes,G.edges_values)
                logger.info("se ha guardado el nuevo grafo hehco por el metodo: " + Block[1])
                Block = [False,None]
                is_connected = G.isConnected()
                is_tree = G.isTree()
            elif event.key == pg.K_ESCAPE: # restart variables
                press_1 = False
                l_alt = False
                G.del_ = False
                a_node = False
                G.a_edge = [False,False]
                G.m_node = False
                G.m_node_f = None
                G.follow = None
                just_s[0] = False
                Block = [False,None]
                if save_new_graph == "¿":
                    recolor_graph(G)
                    logger.info("se ha descartado el nuevo grafo")
                    output = None
                save_new_graph = None
                logger.info("se presionó ESCAPE y se reinciarion las variables")
            elif event.key == pg.K_s and a_node and not Block[0]: # Press s, save graph
                a_node = False
                command_save(G,logger)
            elif event.key == pg.K_o and a_node and not Block[0]: # Press o, open graph
                new_graph = load_graph("./",logger)
                a_node = False
                if new_graph is not None:
                    #del G
                    G = new_graph
                    window_name = "Crear Grafos"
                    handle = FindWindow(None, window_name)
                    SetWindowPos(handle, HWND_TOP, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
                else:
                    logger.info("error al cargar el archivo seleccionado")
                    print("error al cargar el archivo seleccionado")
                

        if event.type == pg.MOUSEBUTTONDOWN and not Block[0] and pg.mouse.get_pressed()[0]:
            G.mouse_clicked = True
            if a_node: # Crear Nodo
                node = Node(Graph=G,coordinates=pg.mouse.get_pos())
                G.add_node(node=node)
                logger.info("se ha creado el nodo " + str(node.id))
                del node
                is_connected = G.isConnected()
                is_tree = G.isTree()
            elif press_1: # si se abre el sub menu de los algoritmos prim y kruskal
                if (pg.mouse.get_pos()[0] - 12)**2 + (pg.mouse.get_pos()[1] - h*0.25)**2 <= 32:
                    if save_new_graph[0] != 'p':
                        G.nodes[0].set_()
                        del G
                        G = PyGraph()
                        save_new_graph = default_p
                        G.Erdos_Reny(save_new_graph[0],save_new_graph[1],save_new_graph[2],(w,h))
                        
                elif (pg.mouse.get_pos()[0] - 12)**2 + (pg.mouse.get_pos()[1] - h*0.35)**2 <= 32:
                    if save_new_graph[0] != 'm':
                        save_new_graph = default_m
                        if ((len(G.nodes)-1)*(len(G.nodes))/2) >= save_new_graph[2]:
                            G.nodes[0].set_()
                            del G
                            G = PyGraph()
                            G.Erdos_Reny(save_new_graph[0],save_new_graph[1],save_new_graph[2],(w,h))
                            
                        else:
                            save_new_graph[2] = int((len(G.nodes)-1)*(len(G.nodes))/2)
                            default_m[2] = int((len(G.nodes)-1)*(len(G.nodes))/2)
                            G.nodes[0].set_()
                            del G
                            G = PyGraph()
                            G.Erdos_Reny(save_new_graph[0],save_new_graph[1],save_new_graph[2],(w,h))
                            
                if just_s[1] is not None:
                    just_s[1] = (G.nodes,G.edges_values)

        #hacer zoom con la rueda del mouse
        elif event.type == pg.MOUSEWHEEL: 
            if event.y == -1: #si la ruda es girada hacia abajo
                if zoom+0.1 <= 1.5:
                    zoom = round(zoom + 0.1, 2)
                    if zoom != 0:
                        for i in G.nodes:
                            if i.coordinates[0] < pg.mouse.get_pos()[0]: # si los nodos.x estan a la izquierda del mouse
                                i.coordinates = (i.coordinates[0] + ((pg.mouse.get_pos()[0]-i.coordinates[0])/(10*zoom)), i.coordinates[1])
                            elif i.coordinates[0] > pg.mouse.get_pos()[0]:
                                i.coordinates = (i.coordinates[0] - ((pg.mouse.get_pos()[0]-i.coordinates[0])/(10*(-zoom))), i.coordinates[1])

                            if i.coordinates[1] < pg.mouse.get_pos()[1]: # si los nodos.y estan a la derecha del mouse
                                i.coordinates = (i.coordinates[0], i.coordinates[1] + ((pg.mouse.get_pos()[1]-i.coordinates[1])/(10*zoom)))
                            elif i.coordinates[1] > pg.mouse.get_pos()[1]:
                                i.coordinates = (i.coordinates[0],i.coordinates[1] - ((pg.mouse.get_pos()[1]-i.coordinates[1])/(10*(-zoom))))
                else: 0
            else:
                if zoom-0.1 >= 0.1:
                    zoom = round(zoom - 0.1, 2)
                    if zoom != 0:
                        for i in G.nodes:
                            if i.coordinates[0] < pg.mouse.get_pos()[0]:
                                i.coordinates = (i.coordinates[0] - ((pg.mouse.get_pos()[0]-i.coordinates[0])/(10*zoom)), i.coordinates[1])
                            elif i.coordinates[0] > pg.mouse.get_pos()[0]:
                                i.coordinates = (i.coordinates[0] + ((pg.mouse.get_pos()[0]-i.coordinates[0])/(10*-zoom)), i.coordinates[1])

                            if i.coordinates[1] < pg.mouse.get_pos()[1]:
                                i.coordinates = (i.coordinates[0],i.coordinates[1] - ((pg.mouse.get_pos()[1]-i.coordinates[1])/(10*zoom)))
                            elif i.coordinates[1] > pg.mouse.get_pos()[1]:
                                i.coordinates = (i.coordinates[0],i.coordinates[1] + ((pg.mouse.get_pos()[1]-i.coordinates[1])/(10*-zoom)))
                else: 0
        

    if len(G.nodes_connected_to) > 0:
        G.draw(screen=screen,logger=logger,esc=zoom-1)
        if G.mouse_clicked:
            is_connected = G.isConnected()
            is_tree = G.isTree()
    
    if press_i:
        extra_info(screen,(w,h),is_connected,is_tree)
    
    if Block[0]: # si esta bloqueado es que se esta ejecutando un algoritmo de tiempo real
        if Block[1] == "Prim":
            output = G.Prim(screen,logger,new_graph,info,(screen,(w,h),[a_node,G.a_edge[0],G.del_,l_alt,G.m_node],just_s[1]),G)
            Block[0] = False
            save_new_graph = "¿"
        elif Block[1] == "Kruskal":
            output = G.Kruskal(screen,logger,new_graph,info,(screen,(w,h),[a_node,G.a_edge[0],G.del_,l_alt,G.m_node],just_s[1]),G)
            Block[0] = False
            save_new_graph = "¿"
    
    elif not press_1 and isinstance(save_new_graph,list):
        save_new_graph = None

    #print(event)
    info(screen,(w,h),[a_node,G.a_edge[0],G.del_,l_alt,G.m_node],just_s[1],method=save_new_graph,zoom=zoom)
    pg.display.update()

    G.mouse_clicked = False