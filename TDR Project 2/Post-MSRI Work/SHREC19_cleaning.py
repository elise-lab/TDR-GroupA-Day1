import argparse

parser = argparse.ArgumentParser()
parser.add_argument("path")
args = parser.parse_args()
f = open(args.path, 'r')
fout = open(args.path.replace('obj','txt'), 'w+')
for line in f:
    if line[0]=='v':
        fout.write(line.replace('v ','').replace(' ',', ').replace('\n','')+', 0.0\n')
f.close()
fout.close()
