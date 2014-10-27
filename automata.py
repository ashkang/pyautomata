import ast, json

class automata:
    def __init__(self, infile):
        self.stream = open(infile)
        self.automaton = json.load(self.stream)

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
