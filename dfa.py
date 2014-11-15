from automata import automata

class dfa(automata):
    def __init__(self, infile = None, bsimplify = True):
        automata.__init__(self, infile, bsimplify)

    def consume_token(self, state, instr):
        if len(instr) <= 0:
            return

        token = instr[0]
        ni = self.automaton["defs"][state][token][0]
        return ni, instr[1:]

    def has_route(self, state, instr):
        if len(instr) <= 0 and self.is_final(state):
            return True
        elif len(instr) <= 0 and not self.is_final(state):
            return False

        ni, nextstr = self.consume_token(state, instr)
        return self.has_route(ni, nextstr)

    def connecteds(self, state, letter):
        try:
            return self.automaton["defs"][state][letter]
        except:
            return []
