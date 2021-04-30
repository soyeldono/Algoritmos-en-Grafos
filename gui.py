import pygame as pg
from pygame.locals import *
import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox as MessageBox
from pygraph import PyGraph,Node
import json
import os

def load_graph(initialdir,logger):
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(initialdir = initialdir, title="Selecciona el archivo",filetype=(("pg files","*.pg"),("all files","*.*")))

    try:
        f = open(file_path,"r")

        logger.info("se cargó el grafo guardado en " + str(file_path))

        c = f.read()
        f.close()
        js = json.loads(c)

        g = PyGraph()

        #primero cargamos los nodos
        for i in js["node"]:
            if i.split("_")[0] != "None":
                n = Node(Graph=g,coordinates=js["node"][i]["coordinates"],name=js["node"][i]["name"],color=js["node"][i]["color"])
                n.id = int(js["node"][i]["id"])
                n.node_grade = int(js["node"][i]["node_grade"])
                g.add_node(node=n)
            else:
                g.nodes.append(None)
        
        #ahora las aristas
        aux = {} 
        for i in js["nodes_connected_to"]:
            aux[int(i)] = js["nodes_connected_to"][i]
        g.nodes_connected_to = aux

        aux = {} 
        for i in js["edges_values"]:
            aux[i] = int(js["edges_values"][i])
        g.edges_values = aux

        aux = {} 
        for i in js["color_edge"]:
            aux[i] = (int(js["color_edge"][i][0]),js["color_edge"][i][1],js["color_edge"][i][2])
        g.color_edge = aux

        return g
    except:
        if file_path == '':
            logger.exception("no se escogio un archivo")
        else:
            logger.exception("no se pudo abrir el archivo en la ruta "+str(file_path))
        return None

def save_graph(graph,logger):
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.asksaveasfilename(initialdir = "./", title="Selecciona el archivo",filetype=(("pg files","*.pg"),("all files","*.*")))
    #print(file_path)
    if file_path == "":
        logger.info("no se guardo el archivo")
        print("no se guardo el archivo")
        return None
        
    gp = {}

    #primero se guardan los nodos
    gp["node"] = {}

    for k,i in enumerate(graph.nodes):
        if i is not None:
            gp["node"][int(i.id)] = {"node_grade":i.node_grade,"id":i.id,"name":i.name,"coordinates":i.coordinates,"color":i.color}
        else:
            gp["node"]["None_"+str(k)] = {}
    
    #se guardan las aristas
    gp["nodes_connected_to"] = {}

    for i in graph.nodes_connected_to:
        gp["nodes_connected_to"][int(i)] = graph.nodes_connected_to[i]

    #se guarda el valor de las aristas
    gp["edges_values"] = {}

    for i in graph.edges_values:
        gp["edges_values"][i] = graph.edges_values[i]

    #se guarda el color de las aristas
    gp["color_edge"] ={}

    for i in graph.color_edge:
        gp["color_edge"][i] = graph.color_edge[i]

    s = json.dumps(gp,indent=4)
    if str(file_path.split("/")[-1]) in os.listdir("./"):
        f = open(str(file_path.split("/")[-1]),"w")
    else:
        f = open(str(file_path.split("/")[-1])+".pg","w")
    f.write(s)
    f.close()
    logger.info("se ha guardado exitosamente el archivo en " + str(file_path))


def info(screen,size,keyboard,show_values,method=None,zoom=None):
    """
    info muestra la informacion esencial y que el usuario debe saber en todo momento


    keyboard es una lista que tiene informacion sobre que tecla esta activa de la siguiente forma

    [0]: CTRL
    [1]: SHIFT
    [2]: DEL
    [3]: ALT
    """

    if isinstance(method,str):
        pg.font.init()
        font = pg.font.SysFont('arial', 30)
        if method == "Prim" or method == "Kruskal":
            text = font.render("Metodo " + method, True, (255,0,0))
            screen.blit(text,(0,size[1]-30))
        elif method == "¿":
            text = font.render("[ENTER] Guardar, [ESC] Descartar", True, (255,0,0))
            screen.blit(text,(0,size[1]-30))
    else:
        pg.font.init()
        font = pg.font.SysFont('arial', 30)
        if isinstance(method,list):
            # method[0]: tipo de aleatoridad, 'p' por probabilidad, 'm' por aristas
            # method[1]: numero de nodos
            # method[2]: la probabilidad o la cantidad de aristas

            text = font.render("Aumentar/Disminuir Nodos[Up/Down]", True, (255,0,0))
            screen.blit(text,(5,size[-1]*0.025))

            text = font.render("Aumentar/Disminuir Prob/M aristas[Rigth/Left]", True, (255,0,0))
            screen.blit(text,(5,size[-1]*0.09))

            text = font.render("Nodos: " +str(method[1]), True, (255,0,0))
            screen.blit(text,(5,size[-1]*0.15))


            if method[0] == "p":
                pg.draw.circle(screen,(255,255,255),(12,size[-1]*0.25),8)
                pg.draw.circle(screen,(255,255,255),(12,size[-1]*0.35),8)
                pg.draw.circle(screen,(0,0,0),(12,size[-1]*0.35),6)

                text = font.render("Probabilidad: " +str(method[2]), True, (255,0,0))
                screen.blit(text,(25,size[-1]*0.25 - 17))

                text = font.render("Aristas: ", True, (71,75,78))
                screen.blit(text,(25,size[-1]*0.35 - 17))
            elif method[0] == "m":
                pg.draw.circle(screen,(255,255,255),(12,size[-1]*0.25),8)
                pg.draw.circle(screen,(255,255,255),(12,size[-1]*0.35),8)
                pg.draw.circle(screen,(0,0,0),(12,size[-1]*0.25),6)

                text = font.render("Probabilidad: ", True, (71,75,78))
                screen.blit(text,(25,size[-1]*0.25 - 17))

                text = font.render("Aristas: " +str(method[2]), True, (255,0,0))
                screen.blit(text,(25,size[-1]*0.35 - 17))



        # Primero se muestra la informacion de cual tecla clave esta activa
        kb = ["CTRL","SHIFT","DEL","ALT","m"]
        it = -1
        for i,k in enumerate(keyboard):
            if k:
                it = i 
        
        if it != -1:
            text = font.render(kb[it]+" esta activo", True, (255,0,0))
        else:
            text = font.render("", True, (255,0,0))
        screen.blit(text,(0,size[1]-30))

        text = font.render("Zoom: " + str(2-zoom), True, (255,0,0))
        screen.blit(text,(size[0]-125,size[-1]*0.010))

    # se muestra los valores de las aristas
    if isinstance(show_values,tuple):
        pg.font.init()
        font = pg.font.SysFont('arial', 15)
        for i in show_values[0]:
            if i is not None:
                text = font.render(str(i.id), True, (0,0,0))
                if i.id < 10:
                    screen.blit(text,(i.coordinates[0]-5,i.coordinates[1]-10))
                else:
                    screen.blit(text,(i.coordinates[0]-7,i.coordinates[1]-10))
        
        font = pg.font.SysFont('arial black', 20)
        for i in show_values[1]:
            text = font.render(str(show_values[1][i]), True, (0,255,255))
            x = (show_values[0][int(i.split("_")[0])].coordinates[0] + show_values[0][int(i.split("_")[1])].coordinates[0])/2
            y = (show_values[0][int(i.split("_")[0])].coordinates[1] + show_values[0][int(i.split("_")[1])].coordinates[1])/2
            
            screen.blit(text,(x-15,y-15))

    
def extra_info(screen,size,is_connected,is_tree):
    """
    extra_info muestra informacion que es opcional y si el usuario quiere saber
    """
    
    pg.font.init()
    font = pg.font.SysFont('arial', 30)
    text = font.render("Conexo: ", True, (255,0,0))
    screen.blit(text,(size[0]-170,size[1]-30))

    if is_connected:
        text = font.render("True", True, (0,255,0))
        screen.blit(text,(size[0]-70,size[1]-30))
    elif not is_connected:
        text = font.render("False", True, (255,0,0))
        screen.blit(text,(size[0]-70,size[1]-30))

    text = font.render("Árbol: ", True, (255,0,0))
    screen.blit(text,(size[0]-170,size[1]-60))

    if is_tree:
        text = font.render("True", True, (0,255,0))
        screen.blit(text,(size[0]-70,size[1]-60))
    elif not is_tree:
        text = font.render("False", True, (255,0,0))
        screen.blit(text,(size[0]-70,size[1]-60))


def dialogs(screen,type_q):
    root = tk.Tk()
    root.withdraw()
    if type_q == "ask":
        resultado = MessageBox.askquestion("Reiniciar", "Se va a borrar el grafo actual ¿Quiere guardar?")
        root.destroy()
        return resultado


