import sys

if len(sys.argv) < 2:
	print "Supply a log filename as a command line parameter."
	sys.exit(1)

f = open(sys.argv[1], 'r')

for line in f:
	line = line.strip()
	
	if 'QUERY_ISSUED' in line:
		print line.split('\'')[1]

f.close()