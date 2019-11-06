"""
Name: Teng Ian Khoo
Created: 30th August 2019
Last Modified: 9th September 2019
"""
import math


def best_score(pile_1, pile_2):
    """
    This function will , given two piles of coins, find the maximum possible value for the first player and the
    decisions both players took to get to their respective values. this assumes both players are playing optimally
    :param pile_1: A coin pile with n number of coins
    :param pile_2: Another coin stack with a m number of coins
    :return: a Tuple, containing the max score achieved by player 1 and the decisions made by both players
    :complexity: O(nm), where n and m are the number of coins in pile 1 and 2 respectively.
    """
    p1_len = len(pile_1)
    p2_len = len(pile_2)

    # don't go into calculations if both arrays are empty
    if p1_len == 0 and p2_len == 0:
        return 0, ()

    # create our memoization table of size, m x n and set initial values to infinity
    memo = [[math.inf] * (p1_len + 1)]
    # appending to that they don't point to the same array reference
    for _ in range(p2_len):
        memo.append([math.inf] * (p1_len + 1))

    # Now to set the base cases of our memo array
    memo[0][0] = 0  # if both piles are empty. you cannot take any coins
    # setting up our values for the first row and columns, i.e when only one pile has coins
    if p1_len > 0:
        memo[0][1] = pile_1[0]
    if p2_len > 0:
        memo[1][0] = pile_2[0]
    # case for when pile 2 is empty
    for i in range(2, p1_len + 1):
        memo[0][i] = memo[0][i - 2] + pile_1[i - 1]
    # another case for when pile 1 is empty
    for j in range(2, p2_len + 1):
        memo[j][0] = memo[j - 2][0] + pile_2[j - 1]
    # we have already populated our array for if on pile is empty
    # The following population of the memo array only works if the len of both array is greater than 0
    if p1_len > 0 and p2_len > 0:
        # 2nd row and 2nd column has a different population pattern to the rest of the table columns
        for column in range(1, p1_len + 1):
            if memo[1][column - 1] > memo[0][column]:
                memo[1][column] = pile_2[0] + memo[0][column - 1]
            else:
                memo[1][column] = pile_1[column - 1] + min(memo[0][column - 1], memo[1][column - 2])

        for row in range(2, p2_len + 1):
            if memo[row][0] > memo[row - 1][1]:
                memo[row][1] = pile_2[row - 1] + min(memo[row - 1][0], memo[row - 2][1])
            else:
                memo[row][1] = pile_1[0] + memo[row - 1][0]

        # now to traverse my memo array, and populate it with the maximum coin value i can get
        for row in range(2, p2_len + 1):
            for column in range(2, p1_len + 1):
                # check which value will lead to a smaller max sum for the opponent
                if memo[row][column - 1] == memo[row - 1][column]:
                    # if the values are even, we want to choose the route that will give us the better max value further
                    # down along the line in our game
                    if memo[row][column - 2] >= memo[row - 2][column]:
                        memo[row][column] = pile_2[row - 1] + min(memo[row - 1][column - 1], memo[row - 2][column])
                    else:
                        memo[row][column] = pile_1[column - 1] + min(memo[row - 1][column - 1], memo[row][column - 2])
                elif memo[row][column - 1] > memo[row - 1][column]:
                    memo[row][column] = pile_2[row - 1] + min(memo[row - 1][column - 1], memo[row - 2][column])
                else:
                    memo[row][column] = pile_1[column - 1] + min(memo[row - 1][column - 1], memo[row][column - 2])

    # Now my memoization array is populated, my answer is at memo[-1][-1], we have to back track for out decision
    max_value = memo[-1][-1]
    # store it as a list first, then change to a tuple at the end
    decisions = []
    current_value = memo[-1][-1]
    # loop through my decision array, ending at my absolute base case
    current_row = p2_len
    current_column = p1_len
    # we iterate back till our base case
    while current_value != 0:
        # if values are the same, we need to check which route will give us a better optimal further down along the line
        if memo[current_row][current_column - 1] == memo[current_row - 1][current_column]:
            if memo[current_row][current_column - 2] >= memo[current_row - 2][current_column]:
                decisions.append(1)
                current_column -= 1
            else:
                decisions.append(2)
                current_row -= 1
        elif memo[current_row][current_column - 1] > memo[current_row - 1][current_column]:
            decisions.append(2)
            current_row -= 1
        else:
            decisions.append(1)
            current_column -= 1
        current_value = memo[current_row][current_column]

    return max_value, tuple(decisions)


def is_in(grid, word):
    """
    This function calculates weather a word can be found in a grid
    :param grid: A NxN grid of [a-z] letters
    :param word: The word to search for in the grid
    :return: False, if not found, a tuple of one of the possible indexes that make up that word from the grid
    : complexity: best case = O(1) will return false if the word is never encountered in the grid, Worst = O(KN^2), as
    we make K N^2 arrays for our dynamic programming approach
    """
    #  variables so we don't constantly need to calculate them
    grid_len = len(grid)
    grid_edge = grid_len - 1

    # create a memo array of size kN^2
    memo = []
    for i in range(len(word)):
        new_grid = []
        for j in range(grid_len):
            new_row = [math.inf] * grid_len
            new_grid.append(new_row)
        memo.append(new_grid)

    # base case to try and find the first letter
    letter_found = False
    for i in range(grid_len):
        for j in range(grid_len):
            if grid[i][j] == word[0]:
                memo[0][i][j] = 1
                letter_found = True

    # if for any iteration, we cannot find a letter that belongs to our string, we can straight away return False
    if not letter_found:
        return False

    # For each  kth array, other than the first, we will look at the kth letter of our word and check all possible
    # routes we could have took from the previous array that will make the word[0..k]

    # now to loop through all the rest of my characters to see if they appear in my grid
    for k in range(1, len(word)):
        letter_found = False
        for row in range(grid_len):
            for column in range(grid_len):
                # special cases for the 4 edges of the grid, less cases to deal with as we go down,
                # as we deal with them above
                # top row
                if row == 0:
                    # top -left corner, 3 directions, down, right, right-diagonal down
                    if column == 0:
                        if grid[row][column] == word[k]:
                            memo[k][row][column] = 1 + min(memo[k - 1][row][column + 1],
                                                           memo[k - 1][row + 1][column],
                                                           memo[k - 1][row + 1][column + 1])
                            letter_found = True
                    # top-right corner, 3 directions, left, down, diagonal - left down
                    elif column == grid_edge:
                        if grid[row][column] == word[k]:
                            memo[k][row][column] = 1 + min(memo[k - 1][row + 1][column],
                                                           memo[k - 1][row][column - 1],
                                                           memo[k - 1][row + 1][column - 1])
                            letter_found = True
                    # not in the top left or top right, 5 directions, left, right. down, left diagonal down,
                    # right diagonal down
                    else:
                        if grid[row][column] == word[k]:
                            memo[k][row][column] = 1 + min(memo[k - 1][row][column - 1],
                                                           memo[k - 1][row][column + 1],
                                                           memo[k - 1][row + 1][column],
                                                           memo[k - 1][row + 1][column - 1],
                                                           memo[k - 1][row + 1][column + 1])
                            letter_found = True
                # leftmost column
                elif column == 0:
                    # bottom left square, 3 directions, up, right, right diagonal up
                    if row == grid_edge:
                        if grid[row][column] == word[k]:
                            memo[k][row][column] = 1 + min(memo[k - 1][row - 1][column],
                                                           memo[k - 1][row][column + 1],
                                                           memo[k - 1][row - 1][column + 1])
                            letter_found = True
                    # not in top left or right, 5 directions, up,down, right, up/down diagonal right
                    elif row != 0:
                        if grid[row][column] == word[k]:
                            memo[k][row][column] = 1 + min(memo[k - 1][row + 1][column],
                                                           memo[k - 1][row - 1][column],
                                                           memo[k - 1][row][column + 1],
                                                           memo[k - 1][row + 1][column + 1],
                                                           memo[k - 1][row - 1][column + 1])
                            letter_found = True
                # bottom most row
                elif row == grid_edge:
                    # bottom right most  corner, 3 directions left, up, up diagonal left
                    if column == grid_edge:
                        if grid[row][column] == word[k]:
                            memo[k][row][column] = 1 + min(memo[k - 1][row][column - 1],
                                                           memo[k - 1][row - 1][column],
                                                           memo[k - 1][row - 1][column - 1])
                            letter_found = True
                    # not bottom left or right, 5 directions, left, right, up, left/right up diagonal
                    elif column != 0:
                        if grid[row][column] == word[k]:
                            memo[k][row][column] = 1 + min(memo[k - 1][row][column - 1],
                                                           memo[k - 1][row][column + 1],
                                                           memo[k - 1][row - 1][column],
                                                           memo[k - 1][row - 1][column - 1],
                                                           memo[k - 1][row - 1][column + 1])
                            letter_found = True
                # right most corner, need
                elif column == grid_edge:
                    # not top right, or bottom right corner, 5 directions, left, up, down, up/down left diagonal
                    if row != 0 and row != grid_edge:
                        if grid[row][column] == word[k]:
                            memo[k][row][column] = 1 + min(memo[k - 1][row][column - 1],
                                                           memo[k - 1][row - 1][column],
                                                           memo[k - 1][row + 1][column],
                                                           memo[k - 1][row - 1][column - 1],
                                                           memo[k - 1][row + 1][column - 1])
                            letter_found = True
                # now all is left is the rows and columns that can move in all 8 directions
                else:
                    if grid[row][column] == word[k]:
                        memo[k][row][column] = 1 + min(memo[k - 1][row][column - 1],  # left
                                                       memo[k - 1][row][column + 1],  # right
                                                       memo[k - 1][row - 1][column],  # up
                                                       memo[k - 1][row + 1][column],  # down
                                                       memo[k - 1][row - 1][column - 1],  # L diag up
                                                       memo[k - 1][row + 1][column - 1],
                                                       # L diag down
                                                       memo[k - 1][row - 1][column + 1],  # R diag up
                                                       memo[k - 1][row + 1][column + 1],
                                                       # R diag down
                                                       )
                        letter_found = True
        # if for any iteration, we cannot find a letter that belongs to our string, we can straight away return False
        if not letter_found:
            return False

    # now my memo is populated, the answer will be found in  my final table, i need to back track to get all my moves
    # starting from when the word is finished
    number_to_find = len(word)
    moves = []

    # starting from the last letter, will ensure that i manage to find the word
    for i in range(len(word) - 1, -1, -1):
        for row in range(grid_len):
            found = False
            for column in range(grid_len):
                if not found:
                    # after my first move has been inputted
                    if len(moves) > 0:
                        # we are checking that we are not choosing the same index again, and that the index is connected
                        # to our next letter
                        if memo[i][row][column] == number_to_find and abs(row - moves[0][0]) <= 1 and abs(
                                column - moves[0][1]) <= 1 and (row != moves[0][0] or column != moves[0][1]):
                            moves.insert(0, (row, column))
                            found = True
                            number_to_find -= 1  # we are now looking for a
                    # looking at the last table, we try and find the end of our word
                    else:
                        if memo[i][row][column] == number_to_find:
                            moves.insert(0, (row, column))
                            found = True
                            number_to_find -= 1

    return moves


