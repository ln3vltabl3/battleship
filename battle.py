from csp import Constraint, Variable, CSP
from constraints import *
from backtracking import bt_search
import sys
import argparse
import time

start_time =time.time()


#parse board and ships info
#file = open(sys.argv[1], 'r')
#b = file.read()
parser = argparse.ArgumentParser()
parser.add_argument(
  "--inputfile",
  type=str,
  required=True,
  help="The input file that contains the puzzles."
)
parser.add_argument(
  "--outputfile",
  type=str,
  required=True,
  help="The output file that contains the solution."
)
args = parser.parse_args()
file = open(args.inputfile, 'r')
b = file.read()

#INITIALIZE BOARD
board = Board(b.split())

#INITIALIZE VARIABLES

varlist = []
conslist = []

for i in range(5):
    v = None
    dom = []
    ship_names = ['Sub', 'Des', 'Cru', 'Bat', 'Car']
    for j in range(board.get_size()**2):
        if j % board.get_size() + i < board.get_size():
            dom.append((j, j+i))
        if (j + (i * board.get_size())) < (board.get_size() ** 2) and i:
            dom.append((j, j + (i * board.get_size())))
    for k in range(board.get_shipC()[i]):
        v = Variable(ship_names[i] + str(k), dom)
        varlist.append(v)

varlist.reverse()

#INITIALIZE CONSTRAINTS
for i in range(len(varlist)):
    conslist.append(ShipBoardConstraint(varlist[i].name(), [varlist[i]], board))

#find all solutions and check which one has right ship #'s

csp = CSP('battleship', varlist, conslist)
solutions, num_nodes = bt_search('FC', csp, 'fixed', False, False, board)
sys.stdout = open(args.outputfile, 'w')
board.print_board()
"''''''''''''''''''''''''''''\n"
print("--- %s seconds ---" % (time.time() - start_time))