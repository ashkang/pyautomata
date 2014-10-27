from automata import automata

class nfa(automata):
    def __init__(self, infile):
        automata.__init__(self, infile)

    def consume_token(self, state, instr):
        if len(instr) <= 0:
            return

        token = instr[0]
        ptokens = self.automaton["defs"][state]
        connecteds = []

        for ptoken in ptokens:
            connected = None
            for pstate in self.automaton["defs"][state][ptoken]:
                if ptoken == token:
                    connected = pstate, instr[1:]
                    connecteds.append(connected)
                    # print "adding %s to list of connected node for %s" %(automata["defs"][state][ptoken], state)
                elif ptoken == "-":
                    connected = pstate, instr
                    connecteds.append(connected)
                    # print "adding %s to list of connected node for %s" %(automata["defs"][state][ptoken], state)

        return connecteds

    def has_route(self, state, instr):
        # print "> has_route(automata, %s, %s)" %(state, instr)

        if len(instr) <= 0:
            return False

        connected = self.consume_token(state, instr)
        # print connected
        dec = False

        for node, nextstr in connected:
            # print "state: %s, nextstr: %s" %(node, nextstr)
            if self.is_final(node) and (len(nextstr) == 0):
                return True
            else:
                dec = dec or self.has_route(node, nextstr)

        return dec
