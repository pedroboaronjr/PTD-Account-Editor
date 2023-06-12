# PTD CLI Account Editor
#### Video Demo: https://www.youtube.com/watch?v=tScAp4Qwd0I
# Installation:
- Download python3
- Run "pip install -r requirements.txt" on the ptdcli.py folder
- That's it, now you can run the program via "python ptdcly.py --help"
#### Description:
This is a Command Line Interface account editor for Pokemon Tower Defense 1.

  It works via HTTP requests, the program send the user info via Post and the response
  parameters are passed as a key-value pair inside user_data, if not modified, the
  data is sent back to the server.

  The sqlite3 database poke_data.db contains some info that the program fetches.
  All the moves and their ids and all the pokemon with their ids and default moveset.
  If the user doesn't pass in the CLI a specific move to the pokemon, the move from
  the default moveset will be select.

# Usage:

***First be sure to set your Username and Password inside the "ptdcli.py" file.***
***Also be sure to click in "new game" on the saveslot you want to modify and save the game at least 1 time.***


  -h, --help            show this help message and exit.

  -a  [ ...], --add  [ ...]
   **Adds a pokemon to your account. You can either use the**
    **pokemon ID (1 to 151) or the pokemon name.**

  -l , --level          Defines the level of your pokemon.
  **If not set, the default is 100.**
  ***(Max 255 or you will end up with a corrupted pokemon.)***

  -s, --shiny           Set your pokemon as a shiny.

  -ss, --shadow         Set your pokemon as a shadow.

  -m , --money          Defines the amount of money.

  -m1 , --move1         Defines pokemon first move.
  **Here you can also use the id of the move or the move name (without spaces)**

  -m2 , --move2         Defines pokemon second move.

  -m3 , --move3         Defines pokemon third move.

  -m4 , --move4         Defines pokemon fourth move.


  -v {Blue,Red}, --version {Blue,Red}
                        Changes game version (Red/Blue).

  -n , --nickname       Changes nickname of the current save.

  -b , --badges         Change the number of badges.

  --unlockchallenges    Unlocks all challenges.

  --unlockdex           Unlocks all entrys in pokedex.

  --unlocklevels        Unlocks all levels.

  # Examples:

  python ptdcly.py --help

  python ptdcly.py --add Pikachu
  
  python ptdcly.py --add 1,2,3,4,Pikachu

  python ptdcly.py --add 151 --shiny

  python ptdcly.py --add VOLTORB --shadow --level 5

  python ptdcly.py -a Magikarp -m1 100

  python ptdcly.py -a Magikarp -m1 SolarBeam -m2 IceBeam

  python ptdcly.py --money 10000000

  python ptdcly.py -n MyNickname

  python ptdcly.py --unlocklevels

  # Todo

  I plan on adding some kind of --addrange which will allow you to, as the name says, add
  a range of pokemon. Ex: --addrange 1, 10 would add all pokemon from id 1 to 10.

  Also maybe some argument to pass multiple of the same pokemon, ex: --addtimes 30 Lapras
  would add 30 lapras to your account
