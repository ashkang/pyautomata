from nfa import nfa

infile = raw_input('automata file: ')
instr = raw_input('input string: ')
n0 = nfa(infile)
print "accepts %s: %s" %(instr, n0.consume(instr))
