# zarkmid
This is a PHP wrapper for frotz games which interfaces with dogecoin game sharing.  Infocom games included a pretend currency known as zorkmid, so I decided to use that as the name of this project since it involves coding game saves into dogecoin transactions.  I pick dogecoin because it is quite inexpensive at this point and the save and share method is accomplished by creating weak hashes of text files and referencing them in the least significant digits of a transaction.
<br>
In order to use this, you will need a linux machine with PHP and a web server, install dfrotz and get a game module.  Dfrotz is available here:
<br>
https://gitlab.com/DavidGriffith/frotz
<br>
You can also try to install it on Ubuntu with:
sudo apt-get install frotz
<br>
There is a working online example of Zork I at this site if you just want to play the game online.  It seems to even let you save and load
by perhaps using cookies.  This project is more ambitious in that it devises an entire ecosystem of data sharing (selling) and presents zorkmid as a proof-of-concept:
https://classicreload.com/zork-i.html
<br>
I found the three zork games on this site:
<br>
https://infocom-if.org/downloads/downloads.html
https://infocom-if.org/downloads/zork1.zip
https://infocom-if.org/downloads/zork2.zip
https://infocom-if.org/downloads/zork3.zip
