# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: By using constraint propagation we are applaying a restriction as many times as possible to simplify and eventually solve a problem.
    In Sudoku it's all about reducing the number of possible digits in each square so we can get to a solved puzzle with 1 digit per square and each digit appears once in each unit.
    The naked twins strategy is to identify boxes with the same 2 digits as only possibilities belonging to the same set of peers and eliminate those 2 numbers from those peers.
    I implemented it by using bits and pieces of both the eliminate and only choice function presented in class



# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: The Diagonal sudoku is a much simpler problem.
    A unit is defined as a set of 9 boxes, and in the implemented solution we already account for the fact that each unit can only have each digit once.
    well, the diagonal is just another set of 9 boxes so we just need to add it as a unit when the sudoku is diagonal.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.