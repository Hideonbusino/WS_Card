This code takes images of WS cards, identifies its name, then searches and deduces a market price for the card. It is for my own use only but I still uploaded it to github just in case.

First, users should save their cards inside img directory. The filenames should be ddd_L.jpg, where ddd are digets starting from 001 to 999. L is a letter from A-E that corresponds to the quality of the card. 

The functions in getid.py does the image processing and uses selinium to obtain the serial number of the card

The functions in price.py then searches for market price from Mercari JP

run.py integrates the above functions. You can run the final functions in this file, or use the UI in ui.py. 

The outpput will be in the data directory, which saves down relevant information. Raw.csv contains all the search instaces and price.csv gives the final database for the cards.

imports.py contains the dependencies and the paths, where the users should define them accordingly before using the code

Other files are only for development/testing purposes and are not needed for this program to work