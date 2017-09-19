#! /usr/bin/env python3
##
# Matilda's init and commands
# Written by xlanor
##
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
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

start_handler = CommandHandler('aboutme', commands.aboutme)
dispatcher.add_handler(start_handler)
start_handler = CommandHandler('subscribe', commands.sub)
dispatcher.add_handler(start_handler)
start_handler = CommandHandler('unsub', commands.unsub)
dispatcher.add_handler(start_handler)
cmd_handler = CommandHandler('mode', commands.mode)
dispatcher.add_handler(cmd_handler)
cmd_handler = CommandHandler('cmd', commands.commands)
dispatcher.add_handler(cmd_handler)
cmd_handler = CommandHandler('supported', commands.supported)
dispatcher.add_handler(cmd_handler)
cmd_handler = CommandHandler('today', commands.todayonline)
dispatcher.add_handler(cmd_handler)
cmd_handler = CommandHandler('st', commands.straitstimes)
dispatcher.add_handler(cmd_handler)
cmd_handler = CommandHandler('mega',commands.megaphone)
dispatcher.add_handler(cmd_handler)
cmd_handler = CommandHandler('cna', commands.cna)
dispatcher.add_handler(cmd_handler)
cmd_handler = CommandHandler('new', commands.allnew)
dispatcher.add_handler(cmd_handler)
cmd_handler = CommandHandler('search', commands.allsearch)
dispatcher.add_handler(cmd_handler)
cmd_handler = CommandHandler('rand', commands.allrand)
dispatcher.add_handler(cmd_handler)
cmd_handler = CommandHandler('st_search', commands.stsearch)
dispatcher.add_handler(cmd_handler)
cmd_handler = CommandHandler('st_rand', commands.strand)
dispatcher.add_handler(cmd_handler)
cmd_handler = CommandHandler('st_new', commands.stnew)
dispatcher.add_handler(cmd_handler)
cmd_handler = CommandHandler('cna_search', commands.cnasearch)
dispatcher.add_handler(cmd_handler)
cmd_handler = CommandHandler('cna_new', commands.cnanew)
dispatcher.add_handler(cmd_handler)
cmd_handler = CommandHandler('cna_rand', commands.cnarand)
dispatcher.add_handler(cmd_handler)
updater.dispatcher.add_handler(CallbackQueryHandler(commands.search))

updater.start_polling()
