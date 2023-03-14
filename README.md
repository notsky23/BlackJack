# BlackJack
Game: BlackJack<br>
A practice with object oriented programming<br>
w Pygame<br><br>

How to play?<br>
1. Rules:<br>
    - Win condition: player and dealer sums the total of the value of the cards in their hand, and whoever is higher wins:<br>
        - One caveat: if either player or dealer goes over 21, they bust and lost the game.<br>
    - At the start of the game:<br>
        - You(Player) and Dealer are given 2 cards each face up<br>
        - The dealer's 1st card is face down<br>
    - Player:<br>
        - Can keep hitting while his card total is less than or equal to 21<br>
        - When you feel like your hand is high enough and dealer won't be able to beat it, stand<br>
    - Dealer:<br>
        - After Player ends turn by choosing stand:<br>
          - While the sum of dealer's hand is less than 17, keep drawing cards<br>
          - If dealer's hand goes past 21, dealer busts and player wins<br>
          
2. Legal moves/Button controls:<br>
    - Deal - new round (similar ro folding and starting a new round)<br>
    - Hit - gives player another card<br>
    - Stand - keep current cards and compare with dealer's hand<br>
    - Quit - exits game<br><br>
    
  
![image](https://user-images.githubusercontent.com/98131995/210928293-96b418be-0669-434d-ba6c-15770412aef2.png)<br><br>
