# Matilda
Matilda is a telegram bot written in Python 3 to scrape news articles, written in order to allow me to get a better understanding of Python. This bot is purely for educational purposes.

Matilda is currently still in the development stage. Currently, I only have time to work on Matilda on the weekends, so development for this bot might be a little slow.

## Supported Sites
* Straits Times
* ChannelNewsAsia

## Licensing
Matilda is licensed under the [Affero General Public License Version 3](LICENSE).

## Sample
A sample version of this bot is currently running on Telegram, under @matilda_jk_bot. 

<img src="http://i.imgur.com/EhXg6ry.png" width="200"></img>
<img src="http://i.imgur.com/G7KMshH.png" width = "200"></img>
<img src="http://i.imgur.com/fR4WXZ1.png" width = "200"></img>
<img src="http://i.imgur.com/RPiYWbo.png" width = "200"></img>

## Credits
* Thanks to [LFlare](https://github.com/LFlare) for giving me the idea, and letting me take a look at his source code when I was stuck.
* [Python-Telegram-Bot](https://github.com/python-telegram-bot/python-telegram-bot) for making a wonderful wrapper, and having an excellent community who are willing to devote time to assist others.

## Contact
You can open an issue here to contact me regarding bugs.

## Commands
* /cmd (full command list)
* /aboutme (about Matilda)
* /supported (supported sites)
* /cna <article> (scrapes CNA Articles)
* /st <article>  (scrapes straits times article)
* /cna_search <terms> (Searches for CNA Articles)
* /cna_new (Latest five CNA Articles)
* /st_search <terms> (Searches for ST Articles)
* /st_new (Latest five ST Articles)

## Usage
Install the following python libraries
* python-telegram-bot
* Beautiful Soup 4
* Requests
* Python String Utilities
* dateutil
* PyMySQL

Setup a MySQL Database. A schema will be provided shortly.


Update token.py with your bot's api token


Start your bot with 
```bash
python3 matilda.py
```


If you are running Matilda on linux, you may also want to use this command to ensure that Matilda keeps running after you exit the terminal.

```bash
sudo nohup python3 matilda.py > /home/matilda-live/error.log 2>&1 &
```
