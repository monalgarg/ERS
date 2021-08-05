# ERS (Egyptian Rat Screw) card game 

I really enjoy ERS and wanted to create a way to play this with friends. Currently, this game just runs locally on your computer so you can 
play it with a friend granted they are in the same room as you. You can learn the basic ERS rules [here](https://bicyclecards.com/how-to-play/egyptian-rat-screw/).

## How to run this game in terminal

Clone the repo and run ```python3 ERS.py```. This will start running the game and you should see ```Player 0 starts``` in your terminal. 
From here, the ERS game begins.

## Playing inside terminal

First, decide who will be player 0 and player 1. Player 1 will be able to flip a new card using the key 'a' and slap using the key 's'. Player 2 will 
be able to flip a card using the key 'f' and slip using the key 'g'.

When a player flips a card (by pressing either 'a' or 'f'), the card that they have flipped will appear. Keep in mind that although the game prompts 
Player 0 to play first, it will not indicate whose turn it is. The players must track this themselves (similar to the original ERS game). The suit of 
the card will appear as ```♢ ♡ ♣ ♠``` and will be followed by the number of the card.

If a player plays out of turn, the terminal will note this error by printing something like this 

```
Player 0 played out of turn. Burn a card! 
Burned ♣ 8 
```

In order to slap, press the key associated with slapping depending on what player you are. If you slap correctly according to one of the rules listed
below, you will see a message similar to this where it tells the players who won the slap, what rule applied to the pile, and prompt the next person
to draw another card.

```
Player 1 slapped!
Adding rule! 

Player 1 will now play a card.
```

If someone slaps incorrectly, they will see a message similar to this where it tells what player slapped incorrect and what card they now have to burn.

```
Player 0 slapped!
Player 0 slapped incorrectly. Burn a card!
Burned ♢ Q
```

Once a player wins all 52 cards, the terminal will print out the winner with a message like...

```
Player 0 is the winner!
```

## ERS Slap Rules

Currently the game supports the following slapping rules...

### Classic ERS Rules

- Doubles: Two of the same number cards appear consecutively. Example: ```♡ 7, ♠ 7```.
- Sandwiches: Two of the same number cards are separated by another card. Example: ```♡ 7, ♡ K, ♠ 7```.
- Marriage: A queen and king appear consecutively. Example: ```♢ Q, ♣ K```.

 ### Lesser known rules
 
- Top & Bottom: The top and bottom card of the pile are the same number. Note that when cards are burned, the burned card becomes the bottom most card.
Example: ```♣ 8, ♡ 7, ...., ♡ K, ♡ 8```. 
- Add to Ten: The numerical sum of the top two cards add up to 10. Note that an ace counts as 1. Example: ```♡ 7, ♠ 3``` or ```♡ A, ♠ 9```.
- Adding Rule: Any permutation of the top three cards creates a valid adding equation. Example ```♡ 6, ♠ 3, ♢ 9``` since 6 + 3 = 9. ```♢ 9, ♠ 3, ♡ 6``` 
is also valid.

