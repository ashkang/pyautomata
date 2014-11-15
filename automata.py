import ast, json, pygraphviz
# -*- coding: utf8 -*-
from collections import defaultdict

class automata:
    def __init__(self, infile = None, bsimplify = True):
        if infile is not None:
            self.stream = open(infile)
            self.automaton = json.load(self.stream)
        self.graph = pygraphviz.AGraph(strict=False, directed=True, encoding='UTF-8', rankdir='LR' )
        self.bsimplify = bsimplify

    def set(self, automaton):
        self.automaton = automaton

    def is_initial(self, state):
        try:
            if self.automaton["states"][state][0] == 1:
                return True
        except:
            return False

    def is_final(self, state):
        try:
            if self.automaton["states"][state][1] == 1:
                return True
        except:
            return False

    def find_initial(self):
        try:
            for state in self.automaton["states"]:
                if self.automaton["states"][state][0] == 1:
                    return state
        except:
            pass

        return ("error: no initial state defined")

    def consume(self, instr):
        return self.has_route(self.find_initial(), instr)

    def alphabet(self):
        return self.automaton["alphabet"]

    def path(self, state, letter):
        if letter in self.automaton["defs"][state]:
            nodes = self.automaton["defs"][state][letter]
            post = []
            for node in nodes:
                ni = self.path(node, letter)
                if len(ni) > 0:
                    post.extend(ni)

            if len(post) > 0:
                nodes.extend(post)

            return list(set(nodes))
        else:
            return []

    def simplify(self):
        edges = defaultdict()

        for edge in self.graph.edges():
            mlabel = edge.attr["label"]
            if edge not in edges:
                # print "adding edge (%s -> %s) with label %s" %(edge[0], edge[1], mlabel)
                edges[edge] = mlabel
            else:
                target = self.graph.get_edge(edge[0], edge[1], edges[edge])
                # print "updating edge (%s -> %s) with key %s" %(edge[0], edge[1], edges[edge])
                target.attr["label"] += ("," + mlabel)
                # print "removing edge (%s -> %s) with label %s" %(edge[0], edge[1], mlabel)
                self.graph.remove_edge(edge, key=mlabel)

    def draw(self, outfile):
        self.graph.add_node("__init__", style="invis")

        for state in self.automaton["defs"]:
            shapeatr = "circle"
            if self.is_initial(state):
                self.graph.add_edge("__init__", state, key="__init__", arrowhead="open")

            if self.is_final(state):
                shapeatr = "doublecircle"

            self.graph.add_node(state, shape=shapeatr)

        for state in self.automaton["defs"]:
            for out in self.automaton["defs"][state]:
                for peer in self.automaton["defs"][state][out]:
                    mk = out.replace('-', u'λ')
                    self.graph.add_edge(state, peer, label=mk, key=mk)

        if self.bsimplify == True:
            self.simplify()
        self.graph.draw(outfile, prog='dot')
