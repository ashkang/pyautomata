from automata import automata

class dfa(automata):
    def __init__(self, infile):
        automata.__init__(self, infile)

    def consume_token(self, state, instr):
        if len(instr) <= 0:
            return

        token = instr[0]
        ni = self.automaton["defs"][state][token]
        return ni, instr[1:]

    def has_route(self, state, instr):
        if len(instr) <= 0 and self.is_final(state):
            return True
        elif len(instr) <= 0 and not self.is_final(state):
            return False

        ni, nextstr = self.consume_token(state, instr)
        return self.has_route(ni, nextstr)
