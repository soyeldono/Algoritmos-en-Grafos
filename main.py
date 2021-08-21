from pygraph.pygraph import PyGraph,Node
import pygame as pg
from pygame.locals import *
import sys
from win32api import GetSystemMetrics
#from win32con import SWP_NOMOVE, SWP_NOSIZE, HWND_TOP
#from win32gui import FindWindow, SetWindowPos
import time
from copy import copy
import random as rd


conteo = 50

__version__ = "2.0.0"

# ================================
#     VARIABLES FOR KEYWORDS
# ================================

#part visual of 'add_edge'
ADD_EDGE = {
    'follow':False,
    'node_start':None
}

#move node
MOVE_NODE = {
    'follow':False,
    'node':None
}

#show id node and edges values
SHOW_DATA = False

#show extra info:
#*is connected, bool
#*num connected components, int
#*is tree, bool
SHOW_EXTRA_DATA = {
    'show':False,
    'isConnected':None,
    'isTree':None,
    'numConnectedComponents':None
}

#zoom of graph
ZOOM = 1.0

#move graph
MOVE_GRAPH = {
    'prev_mouse_pos':None,
    'detect_mouse_move': [],
    'iterator_mouse': 0
}

#aimation of Prin/Kruskal algorithm
ANIMATE_GRAPH = {
    'animation':False,
    'graph':None,
    'history':None,
    'time_line':0,
    'save':False
}

# ================================
#           FUNCTIONS
#=================================

def actualizate_info():
    SHOW_EXTRA_DATA['isConnected'] = G.is_connected()
    SHOW_EXTRA_DATA['isTree'] = G.is_tree()
    SHOW_EXTRA_DATA['numConnectedComponents'] = G.num_connected_components()

# ================================
#             PYGAME
#=================================
w = GetSystemMetrics(0) - 100
h = GetSystemMetrics(1) - 100

pg.init()
screen = pg.display.set_mode((w,h))
pg.display.set_caption('GraphPy')

#rd.seed(27)
G = PyGraph()
#G = get_graph_example(example=3,show_in_window=True,route='tests/examples_graphs/Prim/graph')#.minimun_spanning_tree(inplace=True)
#G.set_node_attribiutes(G.nodes[0],coordinates=(100,100),color=(255,0,0))

# ================================
#              CODE
# ================================

while True:
    screen.fill((0,0,0))
    G.draw(screen)
    keys = pg.key.get_pressed()

    #----- ANIMATIONS -----
    if ANIMATE_GRAPH['animation']:
        ANIMATE_GRAPH['graph'].draw(screen)
        pg.font.init()
        font = pg.font.SysFont('arial',20)
        if keys[pg.K_SPACE] and ANIMATE_GRAPH['time_line'] < len(ANIMATE_GRAPH['history']) or ANIMATE_GRAPH['time_line'] == 0:
            if ANIMATE_GRAPH['history'][ANIMATE_GRAPH['time_line']][-2]: #if se agrega un nodo
                for i in ANIMATE_GRAPH['graph'].nodes:
                    if i == ANIMATE_GRAPH['history'][ANIMATE_GRAPH['time_line']][-2]:
                        i.color = (0,0,255)
                        ANIMATE_GRAPH['time_line'] += 1
                        break
                    
            elif ANIMATE_GRAPH['history'][ANIMATE_GRAPH['time_line']][-1]: #if se agrega una arista
                for i in ANIMATE_GRAPH['graph'].edges:
                    if i == ANIMATE_GRAPH['history'][ANIMATE_GRAPH['time_line']][-1] and ANIMATE_GRAPH['history'][ANIMATE_GRAPH['time_line']][2][0] == 'A':
                        i.color = (255,0,0)
                        ANIMATE_GRAPH['time_line'] += 1
                        break
                    elif i == ANIMATE_GRAPH['history'][ANIMATE_GRAPH['time_line']][-1] and ANIMATE_GRAPH['history'][ANIMATE_GRAPH['time_line']][2][0] == 'C':
                        i.color = (57,255,20)
                        ANIMATE_GRAPH['time_line'] += 1
                        break
                    elif i == ANIMATE_GRAPH['history'][ANIMATE_GRAPH['time_line']][-1] and ANIMATE_GRAPH['history'][ANIMATE_GRAPH['time_line']][2][0] == 'D':
                        i.color = (41,49,51)
                        ANIMATE_GRAPH['time_line'] += 1
                        break
            time.sleep(0.1)
        if ANIMATE_GRAPH['time_line'] < len(ANIMATE_GRAPH['history']):
            text = font.render(ANIMATE_GRAPH['history'][ANIMATE_GRAPH['time_line']-1][2],True,(0,255,0))
            screen.blit(text,(100,h-50))
        elif ANIMATE_GRAPH['time_line'] >= len(ANIMATE_GRAPH['history']):
            for i in ANIMATE_GRAPH['graph'].edges:
                if i not in ANIMATE_GRAPH['history'][ANIMATE_GRAPH['time_line']-1][1]:
                    i.color = i.color = (41,49,51)
            ANIMATE_GRAPH['save'] = True
            text = font.render('Save graph press ENTER - Discard graph pres ESC',True,(0,255,0))
            screen.blit(text,(100,h-50))

        if ANIMATE_GRAPH['save']:
            if keys[pg.K_RETURN]:
                G.empty()
                G.add_node(ANIMATE_GRAPH['history'][-1][0])
                for i in ANIMATE_GRAPH['history'][-1][1]:
                    G.add_edge(i.nodes[0].id,i.nodes[1].id,value=i.value)
                for i in G.nodes:
                    i.color = (250,250,250)
                ANIMATE_GRAPH = {
                    'animation':False,
                    'graph':None,
                    'history':None,
                    'time_line':0,
                    'save':False
                }
                for s in G.nodes_connected_to:
                    print(s,':',end='')
                    for l in G.nodes_connected_to[s]:
                        print(l.id,',',end='')
                    print()

            elif keys[pg.K_ESCAPE]:
                for i in G.edges:
                    i.color = (255,0,0)
                for i in G.nodes:
                    i.color = (250,250,250)
                ANIMATE_GRAPH = {
                    'animation':False,
                    'graph':None,
                    'history':None,
                    'time_line':0,
                    'save':False
                }

        time.sleep(0.1)
    
    #----- write graph -----
    #if keys[pg.K_0]:
    #    with open('graph'+str(conteo)+'.txt','w') as f:
            #for i in G.nodes:
            #    f.write(str(i.id)+" ")
    #        f.write('['+str(len(G.nodes))+']')
    #        f.write('\n[')
    #        for i in G.edges:
    #            f.write('('+str(i.nodes[0].id)+','+str(i.nodes[1].id)+'),')
    #        f.write(']')
    #        f.write('\n[')
    #        for i in G.edges:
    #            f.write(str(i.value)+',')
    #        f.write(']')
    #        conteo += 1
    #    time.sleep(0.1)
        

    #----- add node -----
    if keys[pg.K_LCTRL] and pg.mouse.get_pressed()[0]: #LEFT CTRL + CLICK
        node = Node(coordinates=pg.mouse.get_pos())
        G.add_node(node)
        actualizate_info()
        time.sleep(0.1)
    
    #----- add edge -----
    elif keys[pg.K_LSHIFT] and pg.mouse.get_pressed()[0]: #LEFT SHIFT + CLICK
        for i in G.nodes:
            if (pg.mouse.get_pos()[0] - i.coordinates[0])**2 + (pg.mouse.get_pos()[1] - i.coordinates[1])**2 <= 60:
                if ADD_EDGE['follow']: #Cuando se da el click final para terminar de poner la arista
                    G.add_edge(ADD_EDGE['node_start'],i)
                    ADD_EDGE['follow'] = False
                    ADD_EDGE['node_start'] = None
                    time.sleep(0.1)
                elif not ADD_EDGE['follow']: #Cuando se da el primer click para agregar una arista (este debe seguir el cursor)
                    ADD_EDGE['node_start'] = i
                    ADD_EDGE['follow'] = True
                    time.sleep(0.1)
        actualizate_info()
        time.sleep(0.1)
    
    #----- del node or edge -----
    elif keys[pg.K_DELETE] and pg.mouse.get_pressed()[0]: #SUPR + CLICK 
        #delete node
        for i in G.nodes:
            if (pg.mouse.get_pos()[0] - i.coordinates[0])**2 + (pg.mouse.get_pos()[1] - i.coordinates[1])**2 <= 50:
                G.del_node(i)
                #_enter_ = False
        
        #delete edge
        for i in G.edges:
            epsilon = 7 #px error when user clicks on line
            try: # if x2-x1 are almost equal then y2-y1/0 = error 
                m = ((h-i.node_end_coordinates[1]) - (h-i.node_start_coordinates[1])) / ((i.node_end_coordinates[0]) - (i.node_start_coordinates[0])) #m = y2-y1/x2-x1
            except:
                m = 0
            
            mx = min([i.node_start_coordinates[0],i.node_end_coordinates[0]])
            Mx = max([i.node_start_coordinates[0],i.node_end_coordinates[0]])

            if Mx-mx < epsilon: #check if x2-x1 = 0 (aprox), that means the function is a vertical line
                epsilon = 5
                my = min([i.node_start_coordinates[1],i.node_end_coordinates[1]])
                My = max([i.node_start_coordinates[1],i.node_end_coordinates[1]])

                if (my <= pg.mouse.get_pos()[1] <= My and mx-epsilon <= pg.mouse.get_pos()[0] <= Mx + epsilon):
                    G.del_edge(i)
            else: #otherwise means is a normal linear function
                b = (h-i.node_start_coordinates[1]) -m*i.node_start_coordinates[0] #b = y-mx
                fx = lambda x: (m*x + b) - h #y = mx+b
                
                if abs(abs(fx(pg.mouse.get_pos()[0])) - pg.mouse.get_pos()[1]) < epsilon and mx <= pg.mouse.get_pos()[0] <= Mx:
                    G.del_edge(i)
        
        actualizate_info()
        
        time.sleep(0.1)
    
    #----- move node -----
    #to move node first user needs press 'm' keyword
    elif keys[pg.K_m]:
        MOVE_NODE['follow'] = not MOVE_NODE['follow']
        MOVE_NODE['node'] = None
        time.sleep(0.1)


    #while 'm' keyword is True, user can move any node 
    if MOVE_NODE['follow']: 
        if pg.mouse.get_pressed()[0] and MOVE_NODE['node'] is None: #first click on node means that the user wants move this node but no others
            for k,i in enumerate(G.nodes):
                if (pg.mouse.get_pos()[0] - i.coordinates[0])**2 + (pg.mouse.get_pos()[1] - i.coordinates[1])**2 <= 50:
                    MOVE_NODE["node"] = k
                    break
            time.sleep(0.1)
        elif pg.mouse.get_pressed()[0] and MOVE_NODE['node'] is not None: #second click means this is the new node position
            MOVE_NODE['node'] = None
            time.sleep(0.1)

    #----- show data -----
    if keys[pg.K_i] and not keys[pg.K_LCTRL]: # press 'i' to show data 
        SHOW_DATA = not SHOW_DATA
        time.sleep(0.1)
    if SHOW_DATA:
        pg.font.init()
        font = pg.font.SysFont('arial black',20)
        for i in G.edges: #first edges
            text = font.render(str(i.value),True,(0,255,255))
            x = (i.node_start_coordinates[0] + i.node_end_coordinates[0])//2
            y = (i.node_start_coordinates[1] + i.node_end_coordinates[1])//2
            screen.blit(text,(x-15,y-15))
        
        font = pg.font.SysFont('arial',15)
        for i in G.nodes:
            if i.coordinates:
                if ANIMATE_GRAPH['animation']:
                    text = font.render(str(i.id),True,(255,255,255))
                else:    
                    text = font.render(str(i.id),True,(0,0,0))
                if i.id < 10:
                    screen.blit(text,(i.coordinates[0]-5,i.coordinates[1]-10))
                else:
                    screen.blit(text,(i.coordinates[0]-7,i.coordinates[1]-10))
    if keys[pg.K_LCTRL] and keys[pg.K_i]:
        SHOW_EXTRA_DATA['show'] = not SHOW_EXTRA_DATA['show']
        actualizate_info()
        time.sleep(0.2)
    elif SHOW_EXTRA_DATA['show']:
        pg.font.init()
        font = pg.font.SysFont('arial',15)
        text = font.render('Is connected:'+str(SHOW_EXTRA_DATA['isConnected']),True,(0,255,255))
        screen.blit(text,(100,h-50))
        text = font.render('Is tree:'+str(SHOW_EXTRA_DATA['isTree']),True,(0,255,255))
        screen.blit(text,(100,h-65))
        text = font.render('Nums connected components:'+str(SHOW_EXTRA_DATA['numConnectedComponents']),True,(0,255,255))
        screen.blit(text,(100,h-80))
        #print(G.num_connected_components())
        #SHOW_EXTRA_DATA['show'] = not SHOW_EXTRA_DATA['show']


    #----- move graph with left click -----
    if pg.mouse.get_pressed()[0]:
        if MOVE_GRAPH['prev_mouse_pos'] is None:
            MOVE_GRAPH['prev_mouse_pos'] = pg.mouse.get_pos()
        if MOVE_GRAPH['iterator_mouse'] == 0 or MOVE_GRAPH['iterator_mouse'] == 10:
            MOVE_GRAPH['detect_mouse_move'].append(pg.mouse.get_pos())
        if 0 <= MOVE_GRAPH['iterator_mouse'] <= 10:
            MOVE_GRAPH['iterator_mouse'] += 1

        if MOVE_GRAPH['iterator_mouse'] == 11:
            for i in G.nodes:
                #move graph on Y
                if abs(MOVE_GRAPH['detect_mouse_move'][0][1] - MOVE_GRAPH['detect_mouse_move'][1][1]) >= 60:
                    if pg.mouse.get_pos()[1] < MOVE_GRAPH['prev_mouse_pos'][1]:
                        i.coordinates = (i.coordinates[0],i.coordinates[1]-(35/ZOOM))
                    elif pg.mouse.get_pos()[1] > MOVE_GRAPH['prev_mouse_pos'][1]:
                        i.coordinates = (i.coordinates[0],i.coordinates[1]+(35/ZOOM))

                #move graph on X
                if abs(MOVE_GRAPH['detect_mouse_move'][0][0] - MOVE_GRAPH['detect_mouse_move'][1][0]) >= 60:
                    if pg.mouse.get_pos()[0] < MOVE_GRAPH['prev_mouse_pos'][0]:
                        i.coordinates = (i.coordinates[0]-(35/ZOOM),i.coordinates[1])
                    elif pg.mouse.get_pos()[0] > MOVE_GRAPH['prev_mouse_pos'][0]:
                        i.coordinates = (i.coordinates[0]+(35/ZOOM),i.coordinates[1])
                
                for j in G.edges: #actualizate edge coordinates
                    if i.id == j.nodes[0].id:
                        j.node_start_coordinates = i.coordinates
                    elif i.id == j.nodes[1].id:
                        j.node_end_coordinates = i.coordinates
            MOVE_GRAPH['iterator_mouse'] = 0
            MOVE_GRAPH['detect_mouse_move'] = []
    elif not pg.mouse.get_pressed()[0]:
        MOVE_GRAPH['prev_mouse_pos'] = None

    #----- random graph -----
    if keys[pg.K_1]: # Press 1 to make random graph
        #if you want a connected graph use:
        #m_rd = rd.randint(2,10)
        #G.random_graph(method='m',inplace=True,m=rd.randint(((m_rd-2)*(m_rd-1))//2 + 1,(m_rd*(m_rd-1))//2),window_size=(w,h),n=m_rd) #connected graph with m edges
        #G.random_graph(method='m',inplace=True,m=rd.randint(1,(m_rd*(m_rd-1))//2),window_size=(w,h),n=m_rd,dtype=float)
        #G.random_graph(method='connected',inplace=True,window_size=(w,h))
        G.random_graph(inplace=True,window_size=(w,h),p=0.2)
        #print(G.nodes_connected_to.keys())
        actualizate_info()
        time.sleep(0.1)
    elif keys[pg.K_2]:
        #print(G.random_tree().nodes_connected_to)
        G.random_tree(inplace=True,window_size=(w,h),binary=True)
        actualizate_info()
        time.sleep(0.1)


    #----- Minimun Spanning Tree / Arbol Generador de Peso Minimo -----
    # Prim algorithm
    if keys[pg.K_p] or keys[pg.K_k]:
        if keys[pg.K_p]:
            prim_graph,history = G.minimun_spanning_tree(inplace=False,history=True)
            #G.minimun_spanning_tree(inplace=True,history=True)
        else:
            prim_graph,history = G.minimun_spanning_tree(algorithm='kruskal',inplace=False,history=True)
        ANIMATE_GRAPH['animation'] = True

        _animate_graph = copy(G)

        for i in _animate_graph.nodes:
            i.color = (156,156,156)
        for i in _animate_graph.edges:
            i.color = (156,156,156)
        
        ANIMATE_GRAPH['graph'] = _animate_graph
        ANIMATE_GRAPH['history'] = history
        
        actualizate_info()

        time.sleep(0.1)


    #----- end program -----
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
    #----- zoom -----
        elif event.type == pg.MOUSEWHEEL:
            if event.y == -1: #if down mousewheel
                if ZOOM+0.1 <= 1.5: #limit to zoom is 1.5
                    ZOOM = round(ZOOM +0.1,2)
                    if ZOOM != 0:
                        for i in G.nodes:
                            if i.coordinates[0] < pg.mouse.get_pos()[0]:
                                i.coordinates = (i.coordinates[0] + ((pg.mouse.get_pos()[0]-i.coordinates[0])/(10*ZOOM)), i.coordinates[1])
                            elif i.coordinates[0] > pg.mouse.get_pos()[0]:
                                i.coordinates = (i.coordinates[0] - ((pg.mouse.get_pos()[0]-i.coordinates[0])/(10*(-ZOOM))), i.coordinates[1])

                            if i.coordinates[1] < pg.mouse.get_pos()[1]: # si los nodos.y estan a la derecha del mouse
                                i.coordinates = (i.coordinates[0], i.coordinates[1] + ((pg.mouse.get_pos()[1]-i.coordinates[1])/(10*ZOOM)))
                            elif i.coordinates[1] > pg.mouse.get_pos()[1]:
                                i.coordinates = (i.coordinates[0],i.coordinates[1] - ((pg.mouse.get_pos()[1]-i.coordinates[1])/(10*(-ZOOM))))
                            
                            for j in G.edges: #actualizate edge coordinates
                                if i.id == j.nodes[0].id:
                                    j.node_start_coordinates = i.coordinates
                                elif i.id == j.nodes[1].id:
                                    j.node_end_coordinates = i.coordinates
            else:
                if ZOOM-0.1 >= 0.1: #limit to zoom out is 0.1
                    ZOOM = round(ZOOM-0.1,2)
                    if ZOOM != 0:
                        for i in G.nodes:
                            if i.coordinates[0] < pg.mouse.get_pos()[0]:
                                i.coordinates = (i.coordinates[0] - ((pg.mouse.get_pos()[0]-i.coordinates[0])/(10*ZOOM)), i.coordinates[1])
                            elif i.coordinates[0] > pg.mouse.get_pos()[0]:
                                i.coordinates = (i.coordinates[0] + ((pg.mouse.get_pos()[0]-i.coordinates[0])/(10*-ZOOM)), i.coordinates[1])

                            if i.coordinates[1] < pg.mouse.get_pos()[1]:
                                i.coordinates = (i.coordinates[0],i.coordinates[1] - ((pg.mouse.get_pos()[1]-i.coordinates[1])/(10*ZOOM)))
                            elif i.coordinates[1] > pg.mouse.get_pos()[1]:
                                i.coordinates = (i.coordinates[0],i.coordinates[1] + ((pg.mouse.get_pos()[1]-i.coordinates[1])/(10*-ZOOM)))

                            for j in G.edges:#actualizate edge coordinates
                                if i.id == j.nodes[0].id:
                                    j.node_start_coordinates = i.coordinates
                                elif i.id == j.nodes[1].id:
                                    j.node_end_coordinates = i.coordinates


    #----- FOLLOWS -----
    #edge follow mouse while user add it
    if ADD_EDGE['follow']: 
        pg.draw.line(screen,(250,0,0),ADD_EDGE['node_start'].coordinates,pg.mouse.get_pos(),3)

    #node and edges follows mouse while user moves node
    elif MOVE_NODE['follow'] and MOVE_NODE['node'] is not None:
        G.nodes[MOVE_NODE['node']].coordinates = pg.mouse.get_pos()
        for k,e in enumerate(G.edges):
            if e.nodes[0].id == G.nodes[MOVE_NODE['node']].id:
                G.edges[k].node_start_coordinates = pg.mouse.get_pos()
            elif e.nodes[1].id == G.nodes[MOVE_NODE['node']].id:
                G.edges[k].node_end_coordinates = pg.mouse.get_pos()


    pg.display.update()