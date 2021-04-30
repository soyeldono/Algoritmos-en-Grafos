import pygame as pg
from pygame.locals import *
import random as rd
import time
from copy import copy

class PyGraph:

    def __init__(self):
        self.nodes = []
        self.nodes_connected_to = {}
        self.edges_values = {}
        self.follow = None
        self.a_edge = [False,False]
        self.m_node = False
        self.m_node_f = None
        self.del_ = False
        self.mouse_clicked = False
        self.color_edge = {}


    def draw(self,screen,logger,esc=0):
        if True:
            #draw edges
            acept_del = (False,None)
            for i in self.nodes_connected_to:
                if len(self.nodes_connected_to[i]) > 0:
                    for j in range(len(self.nodes_connected_to[i])):
                        if self.mouse_clicked and self.del_: # si se quiere borrar una arista
                            try:
                                acept_del = self.__del_edge(acept_del,i,j)
                            except:
                                logger.exception("Error al intentar borrar la arista " + str(i) + " a " + str(j)) 
                        else:
                            #print(self.color_edge)
                            aux = str(i)+"_"+str(self.nodes_connected_to[i][j]) 
                            if aux not in self.color_edge:
                                aux = str(self.nodes_connected_to[i][j])+"_"+str(i)
                            try:
                                pg.draw.line(screen,self.color_edge[aux],self.nodes[i].coordinates,self.nodes[self.nodes_connected_to[i][j]].coordinates,3)
                            except:
                                print("colores:",self.color_edge)
                                print("color:",self.color_edge[aux])
                                print("i:",i,"j:",j,self.nodes)
                                print("coordinates1:",self.nodes[i].coordinates)
                                print("i:",i,"j:",j)
                                print("coordinates2:",self.nodes[self.nodes_connected_to[i][j]].coordinates)

            #draw nodes
            for i in self.nodes:
                if i is not None:
                    acept_del = self.__do_to_node(acept_del,i,logger)
                    pg.draw.circle(screen,i.color,i.coordinates,10-(10*esc))        
            
            #condiciones
            if acept_del[0]: # si se quiere borrar una arista
                self.del_edge(acept_del[1],acept_del[2])
                logger.info("se ha borrado exitosamente la arista " + str(acept_del[1]) + " a " + str(acept_del[2]))

            if self.follow is not None: # sirve para poder ver como la arista sigue al mouse
                pg.draw.line(screen,(255,0,0),self.follow,pg.mouse.get_pos(),5)
            
            if self.m_node_f is not None: # si quiere mover un nodo
                self.m_node_f.coordinates = pg.mouse.get_pos()
    
    def add_node(self,node):
        """
        Agrega uno o varios nodos al arbol

        Parametros:

            node: class, lista de classes
                el o los nodos a agragar al arbol
        
        Regresa:
            None
        """
        if isinstance(node,list) == False:
            node = [node]
        
        for i in node:
            if i.id not in self.nodes_connected_to:
                self.nodes_connected_to[i.id] = []
            if len(self.nodes) - 1 > i.id:
                self.nodes[i.id] = i
            else:
                self.nodes.insert(i.id,i)
    
    def add_edge(self,u,v,weight=0):
        if v not in self.nodes_connected_to[u]:
            self.nodes_connected_to[u].append(v)
            self.nodes_connected_to[v].append(u)
            self.edges_values[str(u)+"_"+str(v)] = weight
            self.color_edge[str(u)+"_"+str(v)] = (255,0,0)
        else:
            #logger.warning("WARNING - El nodo " + str(u) + " ya estaba conectado con " + str(v))
            print("WARNING - El nodo " + str(u) + " ya estaba conectado con " + str(v))
    
    def del_node(self,node):
        self.nodes[node.id] = None
        for i in self.nodes_connected_to[node.id]:
            self.nodes_connected_to[i].remove(node.id)
        del self.nodes_connected_to[node.id]
        for i in list(self.edges_values.keys()):
            if i.split("_")[0] == str(node.id) or i.split("_")[1] == str(node.id):
                del self.edges_values[i]
        node.dcr()
        return self.nodes,self.nodes_connected_to
    
    def del_edge(self,u,v):
        self.nodes_connected_to[u].remove(v)
        self.nodes_connected_to[v].remove(u)
        for i in list(self.edges_values.keys()):
            if str(u) in i.split("_") and str(v) in i.split("_"):
                self.edges_values.pop(i)
    
    def init_random_edge_values(self,min_max=(0,100),dtype="int"):
        if len(self.edges_values) > 0:
            for i in self.edges_values:
                if dtype == "int":
                    self.edges_values[i] = rd.randint(min_max[0],min_max[1])
                elif dtype == "float":
                    self.edges_values[i] = rd.randint(min_max[0],min_max[1]) + rd.random()
    
    def Prim(self,screen,logger,new_graph,info,data,G):
        for i in self.nodes:
            i.color =  (120,120,120)
        for i in self.color_edge:
            self.color_edge[i] = (205,205,205)


        for iterator in range(len(self.nodes)-1):
            if iterator == 0: #primero se escoge un nodo aleatoriamente
                node = self.nodes[rd.randint(0,len(self.nodes)-1)]
                node.color = (255,0,0)
                new_graph.nodes_connected_to[node.id] = []
            else:
                node.color = (0,255,0)
            if len(new_graph.nodes)-1 < node.id:
                for _ in range(node.id-(len(new_graph.nodes)-1)):
                    new_graph.nodes.append(None)

            #agregar al nuevo grafo
            new_graph.nodes[node.id] = node
            
            #volver a dibujar las cosas
            G.draw(screen,logger)
            new_graph.draw(screen,logger)
            info(data[0],data[1],data[2],data[3],method="Prim")
            pg.display.update()
            time.sleep(0.5)


            min_ed = [None,None,None] #0: edge_v, 1: nodo.id inicio, 2: nodo.id final
            for i in new_graph.nodes:
                if i is not None:
                    k = 0
                    for j in self.nodes_connected_to[i.id]:
                        if self.nodes[j] not in new_graph.nodes:
                            if k == 0:
                                k += 1
                                min_ed[0] = str(i.id) + "_" + str(j)
                                try:
                                    self.edges_values[min_ed[0]]
                                    min_ed[1] = i.id
                                    min_ed[2] = j
                                except:
                                    min_ed[0] = str(self.nodes[j].id) + "_" + str(i.id)
                                    min_ed[1] = j
                                    min_ed[2] = i.id
                            aux = str(i.id) + "_" + str(j)
                            try:
                                self.edges_values[aux]
                            except:
                                aux = str(j) + "_" + str(i.id)
                            if self.edges_values[aux] < self.edges_values[min_ed[0]] and self.nodes[j] not in new_graph.nodes:
                                min_ed[0] = aux
                                min_ed[1] = int(aux.split("_")[0])
                                min_ed[2] = int(aux.split("_")[1])

            if self.nodes[min_ed[2]] not in new_graph.nodes:
                if len(new_graph.nodes)-1 < min_ed[2]:
                    for _ in range(min_ed[2]-(len(new_graph.nodes)-1)):
                        new_graph.nodes.append(None)
                new_graph.nodes[min_ed[2]] = self.nodes[min_ed[2]]
                new_graph.nodes_connected_to[min_ed[2]] = []
                node = self.nodes[min_ed[2]]
            else:
                if len(new_graph.nodes)-1 < min_ed[1]:
                    for _ in range(min_ed[1]-(len(new_graph.nodes)-1)):
                        new_graph.nodes.append(None)
                new_graph.nodes[min_ed[1]] = self.nodes[min_ed[1]]
                new_graph.nodes_connected_to[min_ed[1]] = [] 
                node = self.nodes[min_ed[1]]
            if len(new_graph.nodes_connected_to[min_ed[1]]) == 0:
                new_graph.nodes_connected_to[min_ed[1]] = [min_ed[2]]
            else:
                new_graph.nodes_connected_to[min_ed[1]].append(min_ed[2])
            if len(new_graph.nodes_connected_to[min_ed[2]]) == 0:
                new_graph.nodes_connected_to[min_ed[2]] = [min_ed[1]]
            else:
                new_graph.nodes_connected_to[min_ed[2]].append(min_ed[1])

            new_graph.edges_values[min_ed[0]] = self.edges_values[min_ed[0]]
            self.color_edge[min_ed[0]] = (255,0,255)
            new_graph.color_edge[min_ed[0]] = self.color_edge[min_ed[0]]

        return new_graph

    def Kruskal(self,screen=None,logger=None,new_graph=None,info=None,data=None,G=None,return_=False):
        if new_graph is None:
            new_graph = PyGraph()
        else:
            for i in self.nodes:
                i.color =  (120,120,120)
            for i in self.color_edge:
                self.color_edge[i] = (205,205,205)
        

        sort_edges = {k: v for k, v in sorted(self.edges_values.items(), key=lambda item: item[1])}
        parents = {k: -1 for k in range(len(self.nodes))}

        for i in sort_edges:
            if len(new_graph.edges_values) == len(self.nodes) -1:
                if logger is not None:
                    logger.info("metodo Kruskal terminado")
                return new_graph

            if G is not None and info is not None:
                G.draw(screen,logger)
                info(data[0],data[1],data[2],data[3],method="Kruskal")
                pg.display.update()
                time.sleep(0.5)
            
            p1 = self.__find(parents,int(i.split("_")[0]))
            p2 = self.__find(parents,int(i.split("_")[1]))

            if p1 == -1 and p2 == -1:
                if logger is not None:
                    logger.info("se ha agregado la arista " + str(i.split("_")[0]) + " - " + i.split("_")[1] + ", w: " +str(sort_edges[i]))
                parents[int(i.split("_")[0])] = int(i.split("_")[1])
                if len(new_graph.nodes)-1 < int(i.split("_")[0]):
                    for _ in range(int(i.split("_")[0])-(len(new_graph.nodes))):
                        new_graph.nodes.append(None)

                new_graph.add_node([self.nodes[int(i.split("_")[0])],self.nodes[int(i.split("_")[1])]])
                new_graph.add_edge(int(i.split("_")[0]),int(i.split("_")[1]))
                if G is not None and info is not None:
                    self.color_edge[i] = (255,0,255)    
                new_graph.edges_values[i] = self.edges_values[i]
            elif p1 != p2:
                if logger is not None:
                    logger.info("se ha agregado la arista " + str(i.split("_")[0]) + " - " + i.split("_")[1] + ", w: " +str(sort_edges[i]))
                parents[p1] = p2
                if len(new_graph.nodes)-1 < int(i.split("_")[0]):
                    for _ in range(int(i.split("_")[0])-(len(new_graph.nodes))):
                        new_graph.nodes.append(None)

                new_graph.add_node([self.nodes[int(i.split("_")[0])],self.nodes[int(i.split("_")[1])]])
                new_graph.add_edge(int(i.split("_")[0]),int(i.split("_")[1]))
                if G is not None and info is not None:
                    self.color_edge[i] = (255,0,255)
                new_graph.edges_values[i] = self.edges_values[i]
            else:
                if logger is not None:
                    logger.info("se ha descartado la arista " + str(i.split("_")[0]) + " - " + i.split("_")[1] + ", w: " +str(sort_edges[i]))
                #print("Descartado")
    
        if return_:
            return new_graph
        
    def Erdos_Reny(self,type_m,n,p_m,size):
        for _ in range(n):
            node = Node(Graph=self,coordinates=(rd.randint(300,size[0]-40),rd.randint(100,size[1]-40)))
            self.add_node(node=node)
            del node
        
        E = []

        for u in self.nodes:
            for v in self.nodes[1:]:
                if type_m == 'p':
                    if rd.random() < p_m and u.id != v.id:
                        self.add_edge(u.id, v.id)
                else:
                    if (v.id,u.id) not in E and u.id != v.id:
                        E.append((u.id,v.id))
        if type_m == 'm':
            E = rd.sample(E,p_m)
            for i in E:
                self.add_edge(i[0],i[1])
    
    def isConnected(self,):
        if len(list(self.nodes_connected_to.keys())) > 0:
            ac_node = list(self.nodes_connected_to.keys())[0]
            list_nodes = [ac_node]
            res = self.__isConnected(ac_node,list_nodes)
            if res is None:
                return False
            elif res == True:
                return True
        else:
            return False
    
    def isTree(self,):
        copy_graph = copy(self)

        if copy_graph.Kruskal(return_=True).nodes_connected_to == self.nodes_connected_to and self.isConnected():
            return True
        else:
            return False
        

    
    def __isConnected(self,ac_node,list_nodes):
        for i in self.nodes_connected_to[ac_node]:
            if i not in list_nodes:
                list_nodes.append(i)
                if len(list_nodes) == len(self.nodes_connected_to):
                    return True
                else:
                    res = self.__isConnected(i,list_nodes)
                    if res == True:
                        return res
                    

    def __find(self,parents,v):
        if parents[v] == -1:
            return v
        return self.__find(parents,parents[v])

    
    def __del_edge(self,acept_del,i,j):
        epsilon = 30 # error aceptable
        try: #si x2 - x1 = 0 entonces será x/0 lo cual significa linea perpendicaluar al eje x
            m = (self.nodes[self.nodes_connected_to[i][j]].coordinates[1] - self.nodes[i].coordinates[1]) / (self.nodes[self.nodes_connected_to[i][j]].coordinates[0] - self.nodes[i].coordinates[0]) # m = y2 - y1 / x2 - x2
        except:
            m = 0
        # calculamos la difernecia horizontal entre los 2 puntos de la arista
        mx = min([self.nodes[i].coordinates[0],self.nodes[self.nodes_connected_to[i][j]].coordinates[0]])
        Mx = max([self.nodes[i].coordinates[0],self.nodes[self.nodes_connected_to[i][j]].coordinates[0]])
        if Mx - mx < epsilon: # si la linea es demasiado vertical entonces ya no se tomara la funcion y = mx + b, y solo se comprobara si el mouse esta dentro de un rango
            epsilon = 5
            my = min([self.nodes[i].coordinates[1],self.nodes[self.nodes_connected_to[i][j]].coordinates[1]])
            My = max([self.nodes[i].coordinates[1],self.nodes[self.nodes_connected_to[i][j]].coordinates[1]])
            if (my <= pg.mouse.get_pos()[1] <= My and mx-epsilon <= pg.mouse.get_pos()[0] <= Mx + epsilon):
                acept_del = (True,self.nodes[i].id,self.nodes[self.nodes_connected_to[i][j]].id)
        else:
            fx = lambda x: m*(x - self.nodes[i].coordinates[0]) + self.nodes[i].coordinates[1] # y = mx + b
            if abs(fx(pg.mouse.get_pos()[0]) - pg.mouse.get_pos()[1]) < epsilon and mx <= pg.mouse.get_pos()[0] <= Mx:
                acept_del = (True,self.nodes[i].id,self.nodes[self.nodes_connected_to[i][j]].id)
        return acept_del
    
    def __do_to_node(self,acept_del,i,logger):
        global us
        if (pg.mouse.get_pos()[0] - (i.coordinates[0]))**2 + (pg.mouse.get_pos()[1] - (i.coordinates[1]))**2 <= 40 and self.follow != i.coordinates and self.mouse_clicked: #si el moouse esta en el nodo y se hizo click
            if self.m_node: #si se quiere mover un nodo 
                self.m_node_f = i
                self.m_node = False
                logger.info("se ha movido de lugar el nodo " + str(i.id) + " con posicion inicial:" + str(i.coordinates))
            else:
                if self.m_node_f is not None:
                    self.m_node = True
                    logger.info("se ha fijado el nuevo lugar del nodo " + str(i.id) + " con posicion final:" + str(i.coordinates))
                self.m_node_f = None

            if self.del_: #si se quiere borrar un nodo
                self.nodes,self.nodes_connected_to = self.del_node(i)
                logger.info("se ha borrado el nodo " + str(i.id))
                acept_del = (False,None)
            else:
                if self.a_edge[0]:
                    us = i.id
                    self.follow = i.coordinates
                    self.a_edge[0] = not self.a_edge[0]
                else:
                    if self.follow is not None:
                        self.add_edge(us,i.id)
                        self.a_edge[0] = not self.a_edge[0]
                    self.follow = None
        return acept_del
        
    
class Node(object):
    idNode = -1

    @classmethod
    def incr(self,Graph):
        if self.idNode+1 in Graph.nodes_connected_to:
            for i in range(self.idNode+1):
                if i not in Graph.nodes_connected_to:
                    self.idNode += 1
                    return i
        else:
            self.idNode += 1
            return self.idNode
    
    @classmethod
    def dcr(self):
        self.idNode -= 1
        return self.idNode
    
    @classmethod
    def set_(self,new_id_set=-1):
        self.idNode = new_id_set

    def __init__(self,Graph,coordinates=None,name="",color=(250,250,250)):
        self.node_grade = 0
        self.id = self.incr(Graph)
        self.name = name
        self.coordinates = coordinates
        self.color = color


