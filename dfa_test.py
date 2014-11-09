from dfa import dfa

infile = raw_input('automata file: ')
instr = raw_input('input string: ')
d0 = dfa(infile)
print "accepts %s: %s" %(instr, d0.consume(instr))
d0.draw('dfa.png')
