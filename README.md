# Coin_Taking_and_Snaky_Words
Use of dynamic programming to solve two problems, a coin taking game and a grid based word search algorithm

The first code is a game where there are two piles of coins; with different values underneath each pile.
There are 2 players and each player takes turn to take a coin from the top of the pile:
What we are to optimise for this code is the sequence of turns for one player to achieve their maximum value possible
they can take.

For the Snake words, what we want is given a grid of letters, we will find if the word you want to search for exists in the
grid. The word can be chosen from any square staring from the first letter, and a letter cannot be consequetively be 
chosen twice.


Descriptions

1 – Coin Taking
For our coin taking game, our base cases are; when both piles are empty, and hence we can only get a value of 0. And when only one pile is empty, in that case we can only take coins from that pile.

The subproblem of the coin taking game is that when we take a coin, one pile is left untouched, and we get the value from the pile we took from. 
 A problem arises in that when we take a coin, it is the opponents turn . Hence, what I did for my algorithm is that, since both me and player 2 play optimally. I assumed that both players will at every step; take the coin that will cause the other player to get the minimal, max value of coins they could achieve. Doing so, at every step will lead to the maximum profit for both the players.

Assuming optimal play, the maximum value that a particular cell in my memorize array can take is, the minimum of the row above or the column on the left. If the minimum value  is from the row above, it means we take a value from the second pile. If the values are even, then we have to look at the 2nd previous column, and the 2nd previous row, and see which value is greater. 
This is because it will be our turn after the opponent plays to choose a pile that will give us the maximum later on.


2- Snake Words
For this problem, I will create K (N^2) arrays, this is so that for every kth  letter in my word, I will reference my grid, and increment a count in my memorization table if the letter appears and is linked in the previous kth memo array in my  memo table, taking care of the boundary cases of the four corners, and the 4 edges of the grid. 
At every iteration, I check if I find a word that does link to the current kth letter, if I don’t, I return false, because that word does not exist in my grid.
Once my memo is filled, I loop once again starting from my last letter, and my len(word) array of the table, and I am looking for a number in the array that is equal to the [0..ith] letter in my array. Once it is found, I append the row and column found into a  move list and look back at my previous array for the same thing.
One thing to not is that I make sure that if I already visited a row, column combo, then I cannot append it again to my move 
