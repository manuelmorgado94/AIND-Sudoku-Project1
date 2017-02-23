assignments = []

rows = 'ABCDEFGHI' # Each row is represented by the letters A to I, there are 9 rows
cols = '123456789' # Each column is represented by the numbers 1 to 9, there are 9 columns

def cross(a, b):
    "Cross product of elements in A and elements in B."
    return[s+t for s in a for t in b]
    pass
# Start creating sudoku grid/design

boxes = cross(rows, cols) # each box (little square) is represented by the combination of row and column

row_units = [cross(r, cols) for r in rows] # each row is composed by 9 boxes, each row is a unit
column_units = [cross(rows, c) for c in cols] # each column is composed of 9 boxes, each column is a unit

square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')] # Create squares, each square is composed of 9 boxes and is a unit


diagonal_unit1 = [[rows[i] + cols[i] for i in range(len(rows))]]    # in diagonal sudoku,  the diagonal is again a combination of 9 squares so is a unit
diagonal_unit2 = [[rows[i] + cols[::-1][i] for i in range(len(rows))]] # there are 2 diagonal units in sudoku


# If sudoku is diagonal we need to add 2 units to unitlist this conditional uses a flag to iterate between a diagonal and non diagonal sudoku
is_diagonal = 1
if is_diagonal == 1:
    unitlist = row_units + column_units + square_units + diagonal_unit1 + diagonal_unit2
else:
    unitlist = row_units + column_units + square_units

# dictionary with units for each box
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
# dictionary with the peers of each box
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)





def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    # Identify all boxes with 2 elements
    possible_naked_twins = [box for box in values.keys() if len(values[box]) == 2]

    # From all boxes with 2 digits Identify boxes that share peers and have the same digits
    naked_twins = [[box1, box2] for box1 in possible_naked_twins \
                   for box2 in peers[box1] if set(values[box1]) == set(values[box2])]

    # Iterate through those boxes and remove the digits from it's peers
    for i in range(len(naked_twins)):
        box1 = naked_twins[i][0]
        box2 = naked_twins[i][1]
        peers1 = set(set(peers[box1]) - set([box2]))
        peers2 = set(set(peers[box2]) - set([box1]))
        all_peers = peers1 & peers2
        for peer_box in all_peers:
            for value in values[box1]:
                values = assign_value(values, peer_box, values[peer_box].replace(value, ''))
    return values

def cross(a, b):
    "Cross product of elements in A and elements in B."
    return[s+t for s in a for t in b]
    pass

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))
    pass

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return
    pass

def eliminate(values):
    """
    If there are boxes with only one digits than that box is solved and it's peers can't have that digit as possibility
    Remove that digit from the peers
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            #values[peer] = values[peer].replace(digit,'')
            values = assign_value(values, peer, values[peer].replace(digit,''))
    return values
    pass

def only_choice(values):
    """
    if a digit only appears in one box  within a unit then that digit must be in that box, find those cases and assign that number.

    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                #values[dplaces[0]] = digit
                values = assign_value(values, dplaces[0], digit)
    return values
    pass

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        #use naked twins strategy
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values
    pass

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    " First, reduce the puzzle using the previous function"
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt
    pass

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)
    return values

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    values = grid_values(diag_sudoku_grid)
    display(values)
    display(solve(diag_sudoku_grid))

    try:
        from visualize import 	visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
