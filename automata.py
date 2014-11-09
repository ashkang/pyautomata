import ast, json, pygraphviz
# -*- coding: utf8 -*-

class automata:
    def __init__(self, infile = None):
        if infile is not None:
            self.stream = open(infile)
            self.automaton = json.load(self.stream)
        self.graph = pygraphviz.AGraph(strict=False, directed=True, encoding='UTF-8')


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

    def connecteds(self, state, letter):
        try:
            return self.automaton["defs"][state][letter]
        except:
            return []

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

    def draw(self, outfile):
        for state in self.automaton["defs"]:
            for out in self.automaton["defs"][state]:
                for peer in self.automaton["defs"][state][out]:
                    self.graph.add_edge(state, peer, label=out.replace('-', u'λ'))

        self.graph.draw(outfile, prog='dot')
