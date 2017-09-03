from telegram.ext import Updater
from telegram.error import(TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError)
import requests
import string
from bs4 import BeautifulSoup
from commands import Commands
from tokens import bottoken

t = bottoken
updater = Updater(token=t.token("staging"))
dispatcher = updater.dispatcher
commands = Commands

from telegram.ext import CommandHandler, CallbackQueryHandler
start_handler = CommandHandler('aboutme', commands.aboutme)
dispatcher.add_handler(start_handler)
cmd_handler = CommandHandler('cmd', commands.commands)
dispatcher.add_handler(cmd_handler)
cmd_handler = CommandHandler('supported', commands.supported)
dispatcher.add_handler(cmd_handler)
cmd_handler = CommandHandler('st', commands.straitstimes)
dispatcher.add_handler(cmd_handler)
cmd_handler = CommandHandler('mega',commands.megaphone)
dispatcher.add_handler(cmd_handler)
cmd_handler = CommandHandler('cna', commands.cna)
dispatcher.add_handler(cmd_handler)
cmd_handler = CommandHandler('st_search', commands.stsearch)
dispatcher.add_handler(cmd_handler)
cmd_handler = CommandHandler('st_new', commands.stnew)
dispatcher.add_handler(cmd_handler)
cmd_handler = CommandHandler('cna_search', commands.cnasearch)
dispatcher.add_handler(cmd_handler)
cmd_handler = CommandHandler('cna_new', commands.cnanew)
dispatcher.add_handler(cmd_handler)
updater.dispatcher.add_handler(CallbackQueryHandler(commands.search))

updater.start_polling()
