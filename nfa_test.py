from nfa import nfa
from dfa import dfa

infile = raw_input('automata file: ')
instr = raw_input('input string: ')
n0 = nfa(infile)
n0.draw('nfa.png')
d0 = dfa()
d0.set(n0.to_dfa())
d0.draw('cdfa.png')

print "accepts %s: %s" %(instr, n0.consume(instr))
