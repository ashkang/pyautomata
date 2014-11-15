from automata import automata
from collections import defaultdict
from pprint import pprint
from dfa import dfa
import json

class nfa(automata):
    def __init__(self, infile = None):
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
            if self.is_final(node) and len(nextstr) == 0:
                return True
            else:
                dec = dec or self.has_route(node, nextstr)

        return dec

    def to_dfa(self):
        initial = self.find_initial()
        dfa_dict = defaultdict()
        dfa_dict_new = defaultdict()
        dfa_dict_new["defs"] = defaultdict()
        dfa_dict_new["alphabet"] = self.alphabet()
        dfa_dict_new["states"] = defaultdict()

        state_mapping = defaultdict()

        allstates = []
        initial_set = frozenset([initial])
        allstates.append(initial_set)

        for states in allstates:
            for letter in self.alphabet():
                # print "now processing %s with key %s" %(states, letter)
                unioned = set()
                for state in states:
                    # print "\t --> %s with key %s" %(state, letter)
                    connecteds = self.connecteds(state, letter)
                    connecteds.extend(self.path(state, "-"))

                    possibles = frozenset(connecteds)
                    unioned = unioned.union(possibles)

                key = states, letter
                value = frozenset(unioned)
                # print "adding (%s) with value %s to dict" %(key, value)
                dfa_dict[key] = value

                if unioned not in allstates:
                    # print "adding %s to allstates" %unioned
                    allstates.append(frozenset(unioned))

        print dfa_dict
        marker = 0
        for state, letter in dfa_dict:
            # print "%s with %s goes to %s" %(state, letter, dfa_dict[state, letter])
            if state not in state_mapping:
                new_name = "Q%s" %marker
                state_mapping[state] = new_name
                marker = marker + 1
                is_initial = 0
                is_final = 0
                if state == initial_set:
                    is_initial = 1
                for orig_state in state:
                    if self.is_final(orig_state):
                        is_final = 1

                dfa_dict_new["states"][new_name] = [ is_initial, is_final ]
            else:
                new_name = state_mapping[state]

        for state, letter in dfa_dict:
            mapped = state_mapping[state]
            if mapped not in dfa_dict_new["defs"]:
                dfa_dict_new["defs"][mapped] = defaultdict()

            if letter not in dfa_dict_new["defs"][mapped]:
                dfa_dict_new["defs"][mapped][letter] = []

            dfa_dict_new["defs"][mapped][letter].append(state_mapping[dfa_dict[state, letter]])

        # for state in dfa_dict_new["defs"]:
        #     for letter in dfa_dict_new["defs"][state]:
                # print "%s with %s goes to %s" %(state, letter, dfa_dict_new["defs"][state][letter])

        result = json.dumps(dfa_dict_new)
        # pprint(result)
        return dfa_dict_new
