# Avery Tan B1
# Alden Tan B2
# Final Project 'Sudoku Problem Solver'



from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from random import randint





puzzle_list=[
"nnn2nn6nnn5n1nn43nnnn6nnn585nnn83nnnn48n9n26nnnn76nnn513nnn6nnnn27nn5n1nnn6nn7nnn",
"nn3n8nnn465nnnnnnnn7n31n5nn326nnn817nnnn7nnnn417nnn953nn1n95n6nnnnnnnn798nnn2n4nn",
"1nnnn7nn4nnnnn6n9nnnn39n75n41n76nn3nnn35n48nnn2nn39n47n47n13nnnn8n9nnnnn3nn6nnnn5",
"2nnn1nn6nnnn6n8n3n8nnn4nn1n7nnnnn25nnn97n41nnn26nnnnn7n5nn6nnn9n9n2n5nnnn7nn9nnn1",
"6nn5n7nn1n79nnnnnn3n5nn94nn7nnnnn8nn82n634n59nn4nnnnn3nn72nn5n8nnnnnn16n1nn7n3nn4",
"98n24n7nnnnn6nn4nnnnnnn9n21n4nn6nnnn12nn5nn69nnnn8nn4n86n1nnnnnnn9nn6nnnnn7n98n34",
"nn7n8n5n2nn1n4nnn925n9n3nnnn1nn2n4n7n6nnnnn8n7n2n5nn1nnnn2n8n548nnn9n7nn4n6n3n8nn",
"nn1nn89n4nnn3n42nn4nnn9n3nnn8nn71nnnn5nnnnn1nnnn98nn3nnn8n5nnn3nn42n6nnn3n28nn4nn",
"nnn6nnnn3n2n4n5nn81n6n7n2nnn6nnn3n29nnnnnnnnn38n2nnn5nnn3n4n5n75nn9n7n1n7nnnn6nnn",
"2n5n63nn7nnnnn4nnn3n8nnnnnn8n16nn3n55nnn9nnn24n9nn87n1nnnnnn8n9nnn1nnnnn7nn32n1n6"
]




# GUI using tkinter
class SudokuMenu:
    def __init__(self,master):
        self.puzzle_no = None #initializing a puzzle number
        self.score = 0 # initializing the puzzle score
        master.configure(background = '#9F48FF') #have pretty background colour
        placement_counter = 0 # a counter to keep track of the entry widgets. We have 81 entry widgets corresponding to the 81 squares in a sudoku puzzle
        self.frame_header = ttk.Frame(master) #define and pack the header frame into the tkinter widget
        self.frame_header.pack()
        ttk.Label(self.frame_header,wraplength = 200, 
            justify= CENTER,text = "Sudoku Problem Solver by Avery & Alden Tan", background = '#9F48FF').grid(row =0, column = 1) #contents of the header frame

        
        ############################################################################################
        self.application_frame = ttk.Frame(master)
        self.application_frame.pack(padx = 20, pady = 20) #defining and packing the application frame which includes our 81 sudoku squares
        self.entries = [] #creating a list to store the entry widgets and allow them to be referenced
        for i in range(81): #defining our 81 entry widgets
            self.entries.append(ttk.Entry(self.application_frame, width = 3))

        #this nested loops place out 81 squares in the correct configuration
        for j in range(9):
            for h in range(9):
                self.entries[placement_counter].grid(row = j+1,column = h)
                placement_counter = placement_counter+1

        #this 'virtual' entry widget serves to keep track of score
        self.extra_e_widget = ttk.Entry(self.application_frame,width=1)
        self.extra_e_widget.config(state = 'disabled')
        ###############################################################################################

        self.button_frame = ttk.Frame(master)#defining the button frame
        self.button_frame.pack(pady=10) #creating buttons
        ttk.Button(self.button_frame, text = 'Hint', command = lambda: self.hint_button(self.puzzle_no)).grid(row = 0,column = 0)
        ttk.Button(self.button_frame, text = 'Solve', command = lambda: self.solve_button(self.puzzle_no)).grid(row = 0,column = 1)
        ttk.Button(self.button_frame, text = 'New Puzzle!', command = lambda: self.new_button()).grid(row = 1,column = 0, columnspan = 2)

        self.style = ttk.Style() #setting background colour
        self.style.configure('TFrame', background = '#9F48FF')
        self.style.configure('TButton', background = '#FF3CF8')
        self.style.configure('Tlabel', background = '#9F48FF')


    
    def hint_button(self,puzzle): 
        """
        givves the answer to the lowest unsolved square in a puzzle.
        """
        list_of_results = solve(puzzle_list[self.puzzle_no])
        counter = 0
        for i in list_of_results:
            if self.entries[counter].get() != i: #if the square doesn't have the correct answer, then change it to the right value
                self.entries[counter].delete(0,END)
                self.entries[counter].insert(0,i)
                self.entries[counter].config(state = 'disabled')
                return
            counter = counter +1 #counter to keep track of the square


    def solve_button(self, puzzle):
        """
        solves the entire puzzle and calculates the score. It also brings our a message box which tells the user their score.
        """
        problem_set = puzzle_list[self.puzzle_no]
        list_of_results = solve(problem_set)
        problem_set_list = list(problem_set)
        counter = 0
        for i in list_of_results: #correcting the problem
            if self.entries[counter].get() != i:
                self.entries[counter].delete(0,END)
                self.entries[counter].insert(0,i)
                self.entries[counter].config(state = 'disabled')
            # print("self.entries[counter].config('state')   ", self.entries[counter].config('state'), "\n\n")
            # print("self.disabled   ", self.extra_e_widget.cget('state'))
            if self.entries[counter].cget('state') != self.extra_e_widget.cget('state'):
                self.score += 1 #if they got the right answer, increase the score
            counter = counter +1
        # print(list_of_results)
        # print(self.score)
        decision = messagebox.showinfo(title = "Score!", message = "Your score is {}.".format(self.score) ) #messagebox pop-up to elt user know the score
        self.score = 0
        if decision == 1: # then click the new button for them to load up a new puzzle
            self.new_button()
        # else:
        #     self.decision_flag = 'exit'


    def new_button(self):
        """
        this function gets a puzzle from our puzzle list.
        """
        for i in range(81): #set all squares to normal and delete anything in them
            self.entries[i].config(state = 'normal')
            self.entries[i].delete(0,END)
        self.puzzle_no = randint(0,(len(puzzle_list)-1))
        puzzle = list(puzzle_list[self.puzzle_no]) #get a random puzzle
        counter = 0
        #load the puzzle into the squares of the board
        for i in puzzle:
            if i != 'n':
                self.entries[counter].insert(0,i)
                self.entries[counter].config(state = 'disabled')
            counter = counter+1



def generate_crossproduct(iter_a, iter_b):
    """
    Returns a list with iter_a + iter_b for every element in iter_a and iter_b
    """
    grids = []
    for i in iter_a:
        for j in iter_b:
            grids.append(i+j)
    return grids



permitted_values = '123456789' #a square is only alowwed to have these values
rows = 'abcdefghi' #rows of the board
cols = '123456789' #columns of the board


square= generate_crossproduct(rows,cols) #get all the squares 


#get a list of the board coordinates that form the columns 
vertical_units = []
for c in cols:
    vertical_units.append(generate_crossproduct(rows,c)) 

#get a list of the board coordinates that form the rows
horizontal_units = []
for r in rows:
    horizontal_units.append(generate_crossproduct(r,cols))

#get a list of the board coordinates that form each individual 9 by 9 unit
threebythree_units = []
for r in ('ABC', 'DEF', 'GHI'):
    for c in ('123', '456', '789'):
        threebythree_units.append(generate_crossproduct(r,c))



#a list of lists of all the units(vert_units, horiz_unis and 9x9units). This contains a list of 27 lists
unitlist = vertical_units+horizontal_units+threebythree_units 

units = dict()
#this will forma dictcalled 'units' with the key being a square referenceing a list containint 3 lists, which
#are the 3 collections of units.
for s in square:
    for u in unitlist:
        if s in u:
            units.setdefault(s,[]).append(u)

#this will take our units above and combine them together for each square and removeduplicates
peers = dict()
for s in square:
    y = set(sum(units[s], []))-set([s]) #this concatenates the three lists of units to make a single lists containing all the peers of a square minus the square itself
    peers[s]= y #the key is a square referencing all of its peers, that is every sqaure that lies in its unit



def propagate(puzzle, board_with_all_possible_values,square):
    '''
    Update the board and remove known values
    '''
    puzzle_list = list(puzzle)
    puzzle_dict = dict(zip(square, puzzle_list)) #assign each square to its partially solved state
    for s, val in puzzle_dict.items():
        if (val in permitted_values) and not (assign(board_with_all_possible_values,s,val)):
            #FAILED
            return False
    return board_with_all_possible_values


def assign(board, square, val):
    """
    delete values that are not referenced by board[square] and propagate to delete this
    value from board[square]'s units
    """
    unneeded_vals= board[square].replace(val,'')
    if not all(remove(board,square,val)for val in unneeded_vals):
        return False #problem removing unneeded values from board
    else:
        return board #succcess! Our board now does not contain the unneeded vals referenced by the square

def remove(board,square,unneeded_vals):
    """
    deletes unneeded vals from board which is referenced by a particular square
    """
    if unneeded_vals not in board[square]: #the value is already gone
        return board
    board[square] =  board[square].replace(unneeded_vals, '')#remove the value!

    # if the square only has 1 val, then remove the val from its peers
    if len(board[square]) == 0:#the square has no values, so there is an error and the puzzle cannot be solved this way
        return False 
    elif len(board[square])==1:
        final = board[square]
        if not all(remove(board,peer,final)for peer in peers[square]): #recursively remove values
            return False #if all not removeable, return False


    #sets a square to a particular value if it is the only square in that unit that can be set
    #to that value
    for u in units[square]:
        s_unit = [s for s in u if unneeded_vals in board[s]]#contains unneeded val
        if len(s_unit) == 0: #square fcontains no value, error. Puzzle can't be solved
            return False
        elif len(s_unit) ==1: #we will assign the unneeded value here since it can only be in one square per unit
            if not assign(board,s_unit[0], unneeded_vals):
                return False
    return board


def dfs(board):
    """
    find square with fewest remaining values and propagate them
    """
    if board is False: #puzzle not passed!
        return False

    if all(len(board[s])==1 for s in square): #board is solved!
        return board

    m_value,m_square = min((len(board[s]),s)for s in square if len(board[s])>1) #find square with fewest remaining possible values
    return sol(dfs(assign(board.copy(), m_square,val))for val in board[m_square]) #recursively try to propagate constraints


def sol(solution):
    """
    return the solution
    """
    for result in solution:
        if result:
            return result
    return False #no solution found



def solve(problem_set):
    """
    solves our sudoku puzzle and returns them as a list of values
    """
    board_with_all_possible_values = dict((s,permitted_values)for s in square) #setting each square to '123456789'
    solution = dfs(propagate(problem_set, board_with_all_possible_values, square))
    result_list = list()
    for s in square: #sets our solution into a list in the correct order.
        result_list.append(solution[s])
    return result_list




def main():
    """
    initialize the GUI
    """
    root = Tk()
    GUI = SudokuMenu(root)
    root.mainloop()


if __name__ == "__main__":
    main()
