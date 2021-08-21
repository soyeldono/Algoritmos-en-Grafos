import pygame as pg
from pygame.locals import *
import random as rd
import time
from copy import Error, copy
import random as rd
import sys

class PyGraph:

    def __init__(self,n=None):
        """
        Create a Graph

        Parameters
        ----------
        n: int, optional default None
            Create the graph with n empty nodes
        """
        self.nodes = []
        self.edges = []
        self.nodes_connected_to= {}
        self.nodes_edges = {}
        if n:
            self.add_node(n)
        
    
    def draw(self,screen,esc=0):
        """
        Draw a graph using Pygame

        Parameters
        ----------
        screen: pg.display
            The window that will show the graph
        """

        #primero se dibujan las aristas para que no queden por encima de los nodos
        for i in self.edges:
            pg.draw.line(screen,i.color,i.node_start_coordinates,i.node_end_coordinates,i.width)

        for i in self.nodes:
            if i.coordinates:
                pg.draw.circle(screen,i.color,i.coordinates,10-(10*esc))
                 

    def add_node(self,n=1,**kwargs):
        """
        Add one o more nodes to graph

        Parameters
        ----------
        n: {int, Node, list}, optional default 1
            Numbers of nodes to add depending on the type that is given
            * int: Add n empty nodes
            * class Node: Add given Node
            * list: Add all Nodes in the list (Each element must be class Node)
        
        See Also
        --------
        Node: See the params of each node 
        
        """

        if isinstance(n,int):
            for i in range(n):
                _node = Node(**kwargs)
                self.nodes_connected_to[_node.id] = []
                self.nodes_edges[_node.id] = []
                self.nodes.append(_node)

        elif n.__class__ == Node:
            self.nodes.append(n)
            if kwargs != {}:
                self.set_node_attribiutes(n,**kwargs)
            self.nodes_connected_to[n.id] = []
            self.nodes_edges[n.id] = []
        elif isinstance(n,list):
            for i in n:
                if i.__class__ == Node:
                    self.nodes.append(i)
                    if kwargs != {}:
                        self.set_node_attribiutes(i,**kwargs)
                    self.nodes_connected_to[i.id] = []
                    self.nodes_edges[i.id] = []
                else:
                    raise ValueError('The object %s is not compatible' %(i))
        else:
            raise ValueError('The object %s is not compatible' %(n))


    def add_edge(self,u,v,value=None,color=(255,0,0),name=None,width=3):
        """
        Add an edge between two nodes

        Parameters
        ----------
        u: {int, class Node} 
            Nodo start
        v: {int, class Node}
            Nodo end
        value: {int, float}, optional default None
            Value that will have this edge
        color: tuple (R,G,B), optional default (255,0,0)
            The color that will have this edge
        name: str, optional default None
            Name of edge
        width: int, optional default None
            The width of this node
        
        Notes
        -----
        *u and v must be same type, {int, Node}

        *if u and v are int, node.id will be searched*

        See Also
        --------
        Edge: See the params of each edge 
        """
        
        if isinstance(u,int) and isinstance(v,int):
            for i in self.nodes:
                if i.id == u:
                    u = i
                elif i.id == v:
                    v = i    
        if type(u) != Node and type(v) != Node:
            raise ValueError('type(u) %s or type(v) %s is not comtabile' %(type(u),type(v)))
        _edge = Edge(u,v,u.coordinates,v.coordinates,value=value,color=color,name=name,width=width)
        self.edges.append(_edge)
        self.nodes_connected_to[u.id].append(v)
        self.nodes_connected_to[v.id].append(u)
        self.nodes_edges[u.id].append(_edge)
        self.nodes_edges[v.id].append(_edge)
        del _edge
    

    def del_node(self,node):
        """
        Delete the given node

        Parameters
        ----------
        node: Node
            The node to delete
        """
        self.nodes.remove(node)
        for i in copy(self.edges):
            if node in i.nodes:
                self.del_edge(i)
        del self.nodes_edges[node.id]
        del self.nodes_connected_to[node.id]
        

    def del_edge(self,edge):
        """
        Delete the given edge

        Parameters
        ----------
        edge: Edge
            The edge to delete
        """
        self.nodes_connected_to[edge.nodes[0].id].remove(edge.nodes[1])
        self.nodes_connected_to[edge.nodes[1].id].remove(edge.nodes[0])
        self.nodes_edges[edge.nodes[0].id].remove(edge)
        self.nodes_edges[edge.nodes[1].id].remove(edge)
        self.edges.remove(edge)


    def set_node_attribiutes(self,node,**kwargs):
        """
        Set attributes on node

        Parameters
        ----------
        node: Node
            Node to change attributes
        """

        for k,i in enumerate(self.nodes):
            if i == node:
                self.nodes[k] = Node(**kwargs)
                self.nodes[k].id = node.id
                Node.set_id(Node,Node.idNode -1)
                break
    

    def empty(self):
        """
        Empty the graph
        """
        for i in copy(self.nodes):
            self.del_node(i)
        Node.set_id(Node,-1)
    

    def random_graph(self,method='p',n=10,inplace=False,dtype=int,window_size=None,**kwargs):
        """
        Generate a random graph

        Parameters
        ----------
        mehtod: {'p', 'm', 'connected'}, optional defualt p. 
            The method to create graph
            * 'p': Erdos Renyi whit p probability
            * 'm': Erdos Renyi with m edges
            * 'connected': Ensure that the graph will be connected
        n: int, optional default 10. 
            Nums of nodes with random coordinates
        inplace: bool, optional default False. 
            * If True overwrite the random graph on the actual graph
            * If False return the random graph
        dtype: {int,float}, optional default int.
            Data type of edges values
        window_size: {tuple, None}, optional default None.
            Size of Pygame window, (width,height)

        kwargs
        ------
        * p: float [0,1] required if algorithm = 'p'. 
        * m: int, required if algorithm = 'm'. 

        Return
        ------
        random_graph: PyGraph 
        
        Notes
        -----
        Return random_graph only if inplace is False, otherwise None
        """
        
        if method == 'p' and 'p' not in list(kwargs.keys()):
            raise TypeError('method = p but not found p (probability) parameter')
        if method == 'm' and 'm' not in list(kwargs.keys()):
            raise TypeError('method == m but not found m (nums edges) parameter')
        

        if not inplace:
            _random_graph_ = PyGraph(n)
            if window_size:
                for i in _random_graph_.nodes:
                    i.coordinates = (rd.randint(10,window_size[0]), rd.randint(10,window_size[1]))
        else:
            self.empty()
            self.add_node(n)
            if window_size:
                for i in self.nodes:
                    i.coordinates = (rd.randint(10,window_size[0]), rd.randint(10,window_size[1]))

        if method == 'm':
            E = [] 
            assert (len(self.nodes)*(len(self.nodes)-1))//2 >= kwargs['m'], 'Maximun number of edges with %s nodes is %s, but get %s' %(n,(len(self.nodes)*(len(self.nodes)-1))//2,kwargs['m'])
        elif method == 'connected':
            E = []
            assert n > 0, 'Error n=%s' %(n)

        for v in range(1,n):
            for u in range(v):
                if method == 'p':
                    if rd.random() < kwargs['p']:
                        if not inplace:
                            _random_graph_.add_edge(u,v,value=round(dtype(rd.randint(0,500) + rd.random()),2))
                        else:
                            self.add_edge(u,v,value=round(dtype(rd.randint(0,500) + rd.random()),2))
                elif method == 'm' or method == 'connected':
                    E.append((u,v))
                else:
                    raise ValueError('Unknown algortihm %s' %(method))

        if method == 'm' or method == 'connected':
            if method == 'm':
                E = rd.sample(E,kwargs['m'])
            else:
                E = rd.sample(E,rd.randint(((n-2)*(n-1))//2 + 1,(n*(n-1))//2))
            for i in E:
                if not inplace:
                    _random_graph_.add_edge(i[0],i[1],value=round(dtype(rd.randint(0,500) + rd.random()),2))
                else:
                    self.add_edge(i[0],i[1],value=round(dtype(rd.randint(0,500) + rd.random()),2))
            
        if not inplace:
            return _random_graph_
    

    def random_tree(self,n=10,depth=4,binary=False,dtype=int,inplace=False,window_size=None):
        """
        Generate a random tree

        Parameters
        ----------
        n: int, optional default 10
            Numbers of nodes in the tree
        depth: int, optional default 3
            Depth of tree
        binary: bool, optional default False
            Whether the tree will be binary or not
        inplace: bool, optional default False
            * If True overwrite the random tree on the actual graph
            * If False return the random tree
        dtype: {int, float}, optional default int
            Data type of edges value
        window_size: {tuple, None}, optional default None
            Size of Pygame window, (width,height)

        Returns
        -------
        Return random_tree only if inplace is False 

        Notes
        -----
        If binary is True, please be sure that number of nodes (n) and
        depth of tree (depth) are compatibles. Remeber that 2^{depth+1}-1
        is the maximun number of nodes in binary tree (considering root
        as depth=0).
        """

        if binary:
            assert n < (2**(depth+1))-1, '2^%s - 1 > %s' %(depth,n)
        assert depth <= n-1, 'Minimun nodes requiered to create a graph with depth=%s is %s, but get %s' %(depth,depth+1,n)
        
        _random_tree_ = PyGraph(n=n)
        all_nodes = copy(_random_tree_.nodes)
        added_node = [[rd.choice(all_nodes)]]
        all_nodes.remove(added_node[-1][-1])

        for i in range(1,depth+1):
            if not binary:
                if depth-i > 0:
                    random_nodes = rd.sample(all_nodes,rd.randint(1,len(all_nodes)-(depth-i)))
                else:
                    random_nodes = rd.sample(all_nodes,len(all_nodes))
            else:
                shuffle = []
                if len(all_nodes)-(depth-i) > 2**i:
                    random_nodes = rd.sample(all_nodes,2**i)
                else:
                    random_nodes = rd.sample(all_nodes,len(all_nodes))

                for nd in added_node[-1]:
                    for _ in range(2):
                        shuffle.append(nd)
            
            for r_e in random_nodes:
                if not binary:
                    _random_tree_.add_edge(rd.choice(added_node[-1]),r_e,value=round(dtype(rd.randint(0,100) + rd.random()),2))
                else:
                    rd_c = rd.choice(shuffle)
                    _random_tree_.add_edge(rd_c,r_e,round(dtype(rd.randint(0,100) + rd.random()),2))
                    shuffle.remove(rd_c)

            for r_n in random_nodes:
                all_nodes.remove(r_n)
                
            added_node.append(random_nodes)

        if window_size:
            for i in _random_tree_.nodes:
                i.coordinates = (rd.randint(10,window_size[0]),rd.randint(10,window_size[1]))

        if not inplace:
            return _random_tree_
        else:
            self.empty()
            self.add_node(_random_tree_.nodes)
            for i in _random_tree_.edges:
                self.add_edge(i.nodes[0],i.nodes[1],value=i.value)

    def __Prim(self,history):
        _history_ = []
        _added_node_ = []
        _added_edge_ = []
        _descarted_edge_ = []
        _iterator_ = 0
        
        #check if each edge.value is int or float
        for i in self.edges:
            if not isinstance(i.value,int) and not isinstance(i.value,float):
                raise TypeError('Prim algortihm just accepted int or float type value but edge [%s-%s].value is type %s' %(i.nodes[0].id,i.nodes[1].id,type(i.value)))
        
        if not self.is_connected():
            raise TypeError('The graph is not connected')

        #random node
        rd_n = rd.choice(self.nodes)
        _added_node_.append(rd_n)

        if history:
            _history_.append((copy(_added_node_),copy(_added_edge_),'Node ' + str(rd_n.id) + ' has been randomly selected',rd_n,None))
        
        while len(_added_edge_) < len(self.nodes) - 1:
            min_edge = {'value':None,'edge':None,'node':None}
            for i in _added_node_:
                for k,j in enumerate(self.nodes_edges[i.id]):
                    if min_edge['edge'] is None and j not in _added_edge_ and j not in _descarted_edge_:
                        min_edge['value'] = j.value
                        min_edge['edge'] = j
                        min_edge['node'] = i
                    if min_edge['value']:
                        if j.value < min_edge['value'] and j not in _added_edge_ and j not in _descarted_edge_:
                            min_edge['value'] = j.value
                            min_edge['edge'] = j
                            min_edge['node'] = i
                
            if history:
                _history_.append((copy(_added_node_),copy(_added_edge_),'Considering edge ' + str(min_edge['edge'].value) + ': [' + str(min_edge['edge'].nodes[0].id) + '-' + str(min_edge['edge'].nodes[1].id) + ']',None,min_edge['edge']))
            

            if min_edge['edge'].nodes[0] not in _added_node_ or min_edge['edge'].nodes[1] not in _added_node_:
                _added_edge_.append(min_edge['edge'])
                if history:
                    _history_.append((copy(_added_node_),copy(_added_edge_),'Adding edge ' + str(min_edge['edge'].value) + ': [' + str(min_edge['edge'].nodes[0].id) + '-' + str(min_edge['edge'].nodes[1].id) + ']',None,min_edge['edge']))

                if min_edge['edge'].nodes[0] == min_edge['node']:
                    min_edge['node'] = min_edge['edge'].nodes[1]
                else:
                    min_edge['node'] = min_edge['edge'].nodes[0]

                _added_node_.append(min_edge['node'])
                if history:
                    _history_.append((copy(_added_node_),copy(_added_edge_),'Adding node ' + str(min_edge['node'].id),min_edge['node'],None))
                
            else: 
                _descarted_edge_.append(min_edge['edge'])
                if history:
                    _history_.append((copy(_added_node_),copy(_added_edge_),'Descarting edge ' + str(min_edge['edge'].value) + ': [' + str(min_edge['edge'].nodes[0].id) + '-' + str(min_edge['edge'].nodes[1].id) + ']',None,min_edge['edge']))

            _iterator_ += 1

            if _iterator_ > (len(self.nodes)*(len(self.nodes)-1))//2:
                for i in _history_:
                    print(i[2])
                raise TypeError('Bug detected, please pull request with your graph')

        return _added_node_,_added_edge_,_history_
    

    def __find(self,parent,u):
        if parent[u] == -1:
            return u
        return self.__find(parent,parent[u])
    

    def __Kruskal(self,history):
        _history_ = []
        _added_node_ = []
        _added_edge_ = []
        _descarted_edge_ = []
        _iterator_ = 0

        for i in self.edges:
            if not isinstance(i.value,int) and not isinstance(i.value,float):
                raise TypeError('Kruskal algortihm just accepted int or float type value but edge [%s-%s].value is type %s' %(i.nodes[0].id,i.nodes[1].id,type(i.value)))
        
        if not self.is_connected():
            raise TypeError('The graph is not connected')

        sort_edges = {i:i.value for i in self.edges}
        sort_edges = {k: v for k, v in sorted(sort_edges.items(), key=lambda item: item[1])}
        parents = {k.id: -1 for k in self.nodes}
        
        for i in sort_edges:
            if len(_added_edge_) == len(self.nodes)-1:
                break

            if history:
                _history_.append((copy(_added_node_),copy(_added_edge_),'Considering edge ' + str(i.value) + ': [' + str(i.nodes[0].id) + '-' + str(i.nodes[1].id) + ']',None,i))
            
            p1 = self.__find(parents,i.nodes[0].id)
            p2 = self.__find(parents,i.nodes[1].id)

            if p1 == -1 and p2 == -1 or p1 != p2:
                parents[p1] = i.nodes[1].id
                _added_edge_.append(i)

                if i.nodes[0] not in _added_node_:
                    _added_node_.append(i.nodes[0])
                if i.nodes[1] not in _added_node_:
                    _added_node_.append(i.nodes[1])

                if history:
                    _history_.append((copy(_added_node_),copy(_added_edge_),'Adding edge ' + str(i.value) + ': [' + str(i.nodes[0].id) + '-' + str(i.nodes[1].id) + ']',None,i))
            elif p1 == p2:
                _descarted_edge_.append(i)

                if history:
                    _history_.append((copy(_added_node_),copy(_added_edge_),'Descarting edge ' + str(i.value) + ': [' + str(i.nodes[0].id) + '-' + str(i.nodes[1].id) + ']',None,i))

        return _added_node_,_added_edge_,_history_


    def minimun_spanning_tree(self,algorithm='prim',inplace=False,history=False):
        """
        Return a Minimun Spanning Tree.

        Parameters
        ----------
        algorithm: {'prim', 'kruskal'}, optional default prim
            The algorithm that will use to create Minimun Spanning Tree
        
        inplace: bool, default False 
            * If True overwrite the Prim result on the actual graph
            * If False return the algorithm result

        history: bool, default False
            Return all procedures that algorithm did

        Return
        ------
        if inplace = False
            copy(Actual Grapgh) with Prim algorithm done
        if history = True
            list of tuples of size 5 [(added Nodes,added Edges,'Actual Procedure',node considered,edge considered)]
        if inplace = False and history = True
            Grapgh with Prim algorithm done, algorithm history

        """

        if not inplace:
            _prim_graph_ = PyGraph()
        
        if history:
            _history_ = []

        if algorithm.lower() == 'prim':
            _added_node_,_added_edge_,_history_ = self.__Prim(history)
        elif algorithm.lower() == 'kruskal':
            _added_node_,_added_edge_,_history_ = self.__Kruskal(history)
        else:
            raise ValueError('Unkwon algorithm %s' %(algorithm))
        
        
        if not inplace:
            _prim_graph_.add_node(_added_node_)
            for i in _added_edge_:
                _prim_graph_.add_edge(i.nodes[0],i.nodes[1],value=i.value)
        else:
            self.empty()
            self.add_node(_added_node_)
            for i in _added_edge_:
                self.add_edge(i.nodes[0],i.nodes[1],value=i.value)
        
        if not inplace and history:
            return _prim_graph_,_history_
        elif not inplace:
            return _prim_graph_
        elif history:
            return _history_


    def __isConnected(self,ac_node,list_nodes,return_nodes=False):
        for i in self.nodes_connected_to[ac_node]:
            if i.id not in list_nodes:
                list_nodes.append(i.id)
                if len(list_nodes) == len(self.nodes):
                    if not return_nodes:
                        return True
                    else:
                        return list_nodes
                else:
                    res = self.__isConnected(i.id,list_nodes,return_nodes=return_nodes)
                    if isinstance(res,bool) and res:
                        return res
                    elif res == list(self.nodes_connected_to.keys())[-1]:
                        return res
        if return_nodes:
            return list_nodes
        else:
            return None

    def is_connected(self):
        """
        Check if actual graph is connected

        Return
        ------
        bool 
        """
        if len(list(self.nodes_connected_to.keys())) > 0:
            ac_node = list(self.nodes_connected_to.keys())[0]
            list_nodes = [ac_node]
            res = self.__isConnected(ac_node,list_nodes)
            if res is None:
                return False
            elif res:
                return True
        else:
            return False
    
    def is_tree(self):
        """
        Check if actual graph is tree

        Return
        ------
        bool
        """
        return self.is_connected() and len(self.edges) == len(self.nodes)-1
    
    def num_connected_components(self):
        """
        Get the num of connected components in graph

        Return
        ------
        int >= 0
        """
        if len(list(self.nodes_connected_to.keys())) > 0:
            all_nodes = list(self.nodes_connected_to.keys())
            num_comp = 0
            while len(all_nodes) > 0:
                ac_node = all_nodes[0]
                list_nodes = [ac_node]
                res = self.__isConnected(ac_node,list_nodes,return_nodes=True)
                for i in res:
                    if i in all_nodes:
                        all_nodes.remove(i)
                num_comp += 1
                if num_comp == 50:
                    raise TypeError('crash')
            return num_comp
        else:
            return 0
        
            


        

class Node:
    idNode = -1
    
    def set_id(self,value):
        self.idNode = value
    
    def __init__(self,coordinates=None,value=None,color=(250,250,250),name=None):
        type(self).idNode += 1
        self.coordinates = coordinates
        self.value = value
        self.color = color
        self.name = name
        self.id = self.idNode
    
    

class Edge:

    def __init__(self,node_start,node_end,node_start_coordinates,node_end_coordinates,value=None,color=(255,0,0),name=None,width=3):
        self.nodes = [node_start,node_end]
        self.node_start_coordinates = node_start_coordinates
        self.node_end_coordinates = node_end_coordinates
        self.value = value
        self.color = color
        self.name = name
        self.width = width
        
if __name__ == '__main__':
    #test Pygraph
    PG = PyGraph(2)
    print(PG.nodes)