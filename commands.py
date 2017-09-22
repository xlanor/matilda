#! /usr/bin/env python3
# -*- coding: utf-8 -*-
##
# This makes up the core of Matilda
# Written by xlanor
##

from telegram.ext import Updater
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_html, escape_markdown
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from nltk.tokenize import word_tokenize
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import parser
import html2text, html, pymysql, traceback, random, time, requests, string
from contextlib import closing
from tokens import SQL, admins, errorchannel
from lxml import html 
from selenium import webdriver
from emoji import emojize




class Commands():
	def sub(bot,update):
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					chatid = update.message.chat_id
					cur.execute("""SELECT mode FROM Userdb WHERE chatid = %s""",(chatid,))
					if cur.rowcount == 0:
						registermsg = "Sorry, you are not registered!"
						registermsg += "\n"
						registermsg += "In order to register, please call an article with Matilda."
						bot.sendMessage(chat_id=update.message.chat_id, text=registermsg,parse_mode='Markdown')
					else:
						cur.execute("""UPDATE Userdb SET sub = 'Subscribe' WHERE chatid = %s""",(int(chatid),))
						sucessmsg = "You are now subscribed to updates from Matilda!"
						bot.sendMessage(chat_id=update.message.chat_id, text=sucessmsg,parse_mode='Markdown')
		except:
			catcherror = traceback.format_exc()
			info = update.message.from_user
			bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
			bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
	def unsub(bot,update):
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					chatid = update.message.chat_id
					cur.execute("""SELECT mode FROM Userdb WHERE chatid = %s""",(chatid,))
					if cur.rowcount == 0:
						registermsg = "Sorry, you are not registered!"
						registermsg += "\n"
						registermsg += "In order to register, please call an article with Matilda."
						bot.sendMessage(chat_id=update.message.chat_id, text=registermsg,parse_mode='Markdown')
					else:
						cur.execute("""UPDATE Userdb SET sub = 'Unsub' WHERE chatid = %s""",(int(chatid),))
						sucessmsg = "You are no longer subscribed to updates from Matilda!"
						bot.sendMessage(chat_id=update.message.chat_id, text=sucessmsg,parse_mode='Markdown')
		except:
			catcherror = traceback.format_exc()
			info = update.message.from_user
			bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
			bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
	def mode(bot,update):
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					chatid = update.message.chat_id
					cur.execute("""SELECT mode FROM Userdb WHERE chatid = %s""",(chatid,))
					if cur.rowcount == 0:
						registermsg = "Sorry, you are not registered!"
						registermsg += "\n"
						registermsg += "In order to register, please call an article with Matilda."
						bot.sendMessage(chat_id=update.message.chat_id, text=registermsg,parse_mode='Markdown')
					else:
						modetype = update.message.text[6:]
						if modetype == "Full":
							cur.execute("""UPDATE Userdb SET mode = 'Full' WHERE chatid = %s""",(int(chatid),))
							sucessmsg = "Sucessfully updated your preferred mode to Full"
							bot.sendMessage(chat_id=update.message.chat_id, text=sucessmsg,parse_mode='Markdown')
						elif modetype == "Trunc":
							cur.execute("""UPDATE Userdb SET mode = 'Trunc' WHERE chatid = %s""",(int(chatid),))
							sucessmsg = "Sucessfully updated your preferred mode to Truncated"
							bot.sendMessage(chat_id=update.message.chat_id, text=sucessmsg,parse_mode='Markdown')
						else:
							errormsg = "Sorry, I don't recognize the mode that you have entered!"
							errormsg += "\n"
							errormsg += "I only accept either \'Full\' or \'Trunc\' as valid modes"
							errormsg += "\n"
							errormsg += "If you think this is a bug, please report it for our trained chinchillas to work on it."
							bot.sendMessage(chat_id=update.message.chat_id, text=errormsg,parse_mode='Markdown')
		except:	
			catcherror = traceback.format_exc()
			info = update.message.from_user
			bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
			bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
	def megaphone(bot,update):
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					userid = update.message.from_user.id
					print(userid)
					if admins.adminlist(userid) == "admin":
						megamessage = update.message.text[6:]
						cur.execute("""SELECT chatid FROM Userdb WHERE sub ='Subscribe'""")
						if cur.rowcount > 0:
							data = cur.fetchall()
							for each in data:
								try:
									bot.sendMessage(chat_id=each[0], text=megamessage,parse_mode='HTML')
									time.sleep(0.5)
								except:
									catcherror = traceback.format_exc()
									info = update.message.from_user
									bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
									pass
						else:
							bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
					else:
						bot.sendMessage(chat_id=update.message.chat_id, text="""HTTP 418: I'm a teapot""",parse_mode='Markdown')
		except:	
			catcherror = traceback.format_exc()
			info = update.message.from_user
			bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
			bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
	def supported (bot,update):
		supportsites = "Hi, these are the sites currently supported by Matilda \n"
		supportsites += "Please type /cmd for more information! \n"
		supportsites += "- Straits Times \n"
		supportsites += "- CNA \n"
		bot.sendMessage(chat_id=update.message.chat_id, text=supportsites, parse_mode='Markdown')
	def commands (bot,update):
		commandstring = "Hi, this are the commands that I currently support \n"
		commandstring += "- /aboutme (about the bot) \n"
		commandstring += "- /cmd (command list) \n"
		commandstring += "- /mode <Full/Trunc> (Switches between Truncated and Full Article) \n"
		commandstring += "- /new (New articles from all sources)\n"
		commandstring += "- /search <search terms> (Searches all sources)\n"
		commandstring += "- /rand (Random 5 articles from all sources)\n"
		commandstring += "- /today <article url> (Today Articles) \n"
		commandstring += "- /st <article url> (Straits Times Scraper) \n"
		commandstring += "- /cna <article url> (Channel News Asia Scraper) \n"
		commandstring += "- /cna\_search <search terms> (Channel News Asia search) \n"
		commandstring += "- /cna\_new (Channel News Asia latest 5) \n"
		commandstring += "- /cna\_rand (Channel News Asia random 5 articles) \n"
		commandstring += "- /st\_search <search terms> (Straits Times search) \n"
		commandstring += "- /st\_new (StraitsTimes latest 5) \n"
		commandstring += "- /st\_rand (StraitsTimes random 5 articles) \n"
		commandstring += "- /unsub (Unsubscribe from Matilda updates) \n"
		commandstring += "- /sub (Subscribe from Matilda updates) \n"
		bot.sendMessage(chat_id=update.message.chat_id, text=commandstring, parse_mode='Markdown')
	def aboutme(bot,update):
		bot.sendMessage(chat_id=update.message.chat_id, text="My name is Matilda, and I love to read. If you're using me, so do you! Check me out on github (https://github.com/xlanor/matilda)")
	def straitstimes(bot, update):
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					try:
						url=update.message.text
						sturl = url[4:]
						checksturl = sturl[:28]
						if checksturl != "http://www.straitstimes.com/":
							bot.sendMessage(chat_id=update.message.chat_id, text="""Please enter a valid url. For example, http://www.straitstimes.com/<article>""",parse_mode='Markdown')

						else:
							try:
								headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
								result = requests.get(sturl,headers=headers)
								print(result.status_code)
								print(sturl)
								
								if (result.status_code >= 400):
									bot.sendMessage(chat_id=update.message.chat_id, text="""This story does not exist!""",parse_mode='Markdown')
								else:
									chatid = update.message.chat.id
									chattype = update.message.chat.type
									cur.execute("""SELECT * FROM Userdb WHERE chatid = %s""",(chatid,))
									if cur.rowcount == 0:
										cur.execute("""INSERT INTO Userdb VALUES(%s,%s,%s,%s)""",(chatid,chattype,'Full','Subscribe'))
										mode = "Full"
									else:
										data = cur.fetchone()
										mode = data[2]
									if mode == "Full":
										cur.execute("""SELECT * FROM Retrievedmsg WHERE retrievedurl = %s""",(sturl,))
									else:
										cur.execute("""SELECT * FROM Truncmsg WHERE retrievedurl = %s""",(sturl,))
									if cur.rowcount == 0:
										headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
										r = requests.get(sturl, headers=headers)
										c = r.content
										soup = BeautifulSoup(c,"html.parser")
										mydivs = soup.findAll("div", { "class" : "odd field-item" })
										titlediv = soup.findAll("h1", {"class" : "headline node-title"})
										publishdiv = soup.findAll("meta", {"property" : "article:published_time"})
										updatediv = soup.findAll("meta", {"property" : "article:modified_time"})
										bodyobject = []
										publishedobject = []
										modifiedobject = []
										for title in titlediv:
											bodyobject.append("<b>")
											bodyobject.append(title.text)
											bodyobject.append("</b>")
											bodyobject.append("\n")
											bodyobject.append("\n")
										for postdate in publishdiv:
											publishedobject.append('Published at: ')
											pubdate = parser.parse(postdate['content'])
											publishedobject.append(pubdate.strftime("%B %d, %Y %H:%M"))
										for modidate in updatediv:
											modifiedobject.append('Updated at: ')
											moddate = parser.parse(modidate['content'])
											modifiedobject.append(moddate.strftime("%B %d, %Y %H:%M"))
										bodyobject.append("<i>")
										bodyobject.extend(publishedobject)
										bodyobject.append("</i>")
										bodyobject.append("\n")
										bodyobject.append("<i>")
										bodyobject.extend(modifiedobject)
										bodyobject.append("</i>")
										bodyobject.append("\n")
										bodyobject.append("\n")
										if mode == "Full":
											for div in mydivs:
												blockquote = div.findAll('blockquote')
												for b in blockquote:
													b.decompose()
												a = div.findAll('span')
												for link in a:
													link.decompose()
												p = div.findAll('p',{"class": None})
												for para in p:
													if para.text is not "":
														parastring = para.text
														if not parastring.isspace():
															bodyobject.append(parastring)
															bodyobject.append("\n")
															bodyobject.append("\n")
											str1 = ''.join(bodyobject)
											result = 0
											for char in str1:
												result +=1
											try:
												if (result) > 4000:
													n = 4000
													checklist=["false"]
													while "false" in checklist:
														try:
															del checklist[:]
															n = n-1
															msglist = [str1[i:i+n] for i in range(0, len(str1), n)]
															for msg in msglist:
																if msg[-1] not in string.whitespace:
																	checklist.append("false")
																else:
																	checklist.append("true")
														except:
															del checklist[:]
															checklist = ["true"]
															n = 4000
															msglist = [str1[i:i+n] for i in range(0, len(str1), n)]
													for msg in msglist:
														cur.execute("""INSERT INTO Retrievedmsg VALUES(NULL,%s,%s)""",(sturl,msg,))
												else:
													cur.execute("""INSERT INTO Retrievedmsg VALUES(NULL,%s,%s)""",(sturl,str1,))
											except:
												catcherror = traceback.format_exc()
												info = update.message.from_user
												bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
												bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
											cur.execute("""SELECT retrievedtext,retrievedid FROM Retrievedmsg WHERE retrievedurl=%s limit 1""",(sturl,))
											if cur.rowcount > 0:
												data = cur.fetchone()
												retrievedmsg = data[0]
												spliceretrievedmsg = retrievedmsg[:500]
												dbid = "db-"+str(data[1])
												keyboard = []
												keyboard.append([InlineKeyboardButton("Read more 📰", callback_data=dbid),InlineKeyboardButton("Delete 🗑️",callback_data="dl")])
												reply_markup = InlineKeyboardMarkup(keyboard)
												update.message.reply_text(spliceretrievedmsg, reply_markup=reply_markup,parse_mode='HTML')
										else:
											summarystring = ""
											for div in mydivs:
												blockquote = div.findAll('blockquote')
												for b in blockquote:
													b.decompose()
												a = div.findAll('span')
												for link in a:
													link.decompose()
												p = div.findAll('p',{"class": None})
												for para in p:
													if para.text is not "":
														parastring = para.text
														if not parastring.isspace():
															summarystring += parastring
															summarystring += " "
											plaintext = PlaintextParser.from_string(summarystring,Tokenizer("english"))
											stemmer = Stemmer("english")
											summarizer = Summarizer(stemmer)
											summarizer.stop_words = get_stop_words("english")
											for sentence in summarizer(plaintext.document, 3):			
												bodyobject.append(str(sentence))
												bodyobject.append("\n")
												bodyobject.append("\n")
											bodyobject.append("This is a truncated version of the article. For the full version, please switch the bot using /mode Full")
											str1 = ''.join(bodyobject)
											cur.execute("""INSERT INTO Truncmsg VALUES(NULL,%s,%s)""",(sturl,str1,))
											keyboard = []
											keyboard.append([InlineKeyboardButton("Delete 🗑️",callback_data="dl")])
											reply_markup=InlineKeyboardMarkup(keyboard)
											bot.sendMessage(chat_id=update.message.chat_id,reply_markup = reply_markup, text=str1,parse_mode='HTML')
									else:
										if mode == "Full":
											cur.execute("""SELECT retrievedtext,retrievedid FROM Retrievedmsg WHERE retrievedurl = %s limit 1""",(sturl,))
											if cur.rowcount > 0:
												data = cur.fetchone()
												retrievedmsg = data[0]
												spliceretrievedmsg = retrievedmsg[:500]
												dbid = "db-"+str(data[1])
												keyboard = []
												keyboard.append([InlineKeyboardButton("Read more 📰", callback_data=dbid),InlineKeyboardButton("Delete 🗑️",callback_data="dl")])
												reply_markup = InlineKeyboardMarkup(keyboard)
												update.message.reply_text(spliceretrievedmsg, reply_markup=reply_markup,parse_mode='HTML')
										else:
											cur.execute("""SELECT retrievedtext,retrievedid FROM Truncmsg WHERE retrievedurl = %s limit 1""",(sturl,))
											if cur.rowcount > 0:
												data = cur.fetchone()
												keyboard = []
												keyboard.append([InlineKeyboardButton("Delete 🗑️",callback_data="dl")])
												reply_markup=InlineKeyboardMarkup(keyboard)
												bot.sendMessage(chat_id=update.message.chat_id, reply_markup = reply_markup, text=data[0],parse_mode='HTML')
							except:
								catcherror = traceback.format_exc()
								info = update.message.from_user
								bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
								bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
		
					except:						
						catcherror = traceback.format_exc()
						info = update.message.from_user
						bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
						bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
		except:
			catcherror = traceback.format_exc()
			info = update.message.from_user
			bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
			bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
	def cna(bot, update):
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					try:
						url=update.message.text
						cnaurl = url[5:]
						checkcnaurl = cnaurl[:31]
						if checkcnaurl != "http://www.channelnewsasia.com/":
							bot.sendMessage(chat_id=update.message.chat_id, text="""Please enter a valid url. For example, http://www.channelnewsasia.com/<article>""",parse_mode='Markdown')
						else:
							try:
								headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
								result = requests.get(cnaurl,headers=headers)
								print(result.status_code)
								if (result.status_code >= 400):
									bot.sendMessage(chat_id=update.message.chat_id, text="""This story does not exist!""",parse_mode='Markdown')
								else:
									chatid = update.message.chat.id
									chattype = update.message.chat.type
									cur.execute("""SELECT * FROM Userdb WHERE chatid = %s""",(chatid,))
									if cur.rowcount == 0:
										cur.execute("""INSERT INTO Userdb VALUES(%s,%s,%s,%s)""",(chatid,chattype,'Full','Subscribe'))
										mode = "Full"
									else:
										data = cur.fetchone()
										mode = data[2]										
									if mode == "Full":
										cur.execute("""SELECT * FROM Retrievedmsg WHERE retrievedurl = %s""",(cnaurl,))
									else:
										cur.execute("""SELECT * FROM Truncmsg WHERE retrievedurl = %s""",(cnaurl,))
									if cur.rowcount == 0:
										headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
										r = requests.get(cnaurl, headers=headers)
										c = r.content
										soup = BeautifulSoup(c,"html.parser")
										mydivs = soup.findAll("div", { "class" : "c-rte--article" })
										titlediv = soup.findAll("h1", {"class" : "article__title"})
										publishdiv = soup.findAll("meta", {"name" : "cXenseParse:recs:publishtime"})
										updatediv = soup.findAll("time")
										bodyobject = []
										publishedobject = []
										modifiedobject = []
										for title in titlediv:
											bodyobject.append("<b>")
											bodyobject.append(title.text)
											bodyobject.append("</b>")
											bodyobject.append("\n")
											bodyobject.append("\n")
										for postdate in publishdiv:
											publishedobject.append('Published at: ')
											pubdate = parser.parse(postdate['content'])
											publishedobject.append(pubdate.strftime("%B %d, %Y %H:%M"))
										for modidate in updatediv:
											if modidate['datetime'] is not '':
												modifiedobject.append('Updated at: ')
												modifdate = parser.parse(modidate['datetime'])
												modifiedobject.append(modifdate.strftime("%B %d, %Y %H:%M"))
										bodyobject.append("<i>")
										bodyobject.extend(publishedobject)
										bodyobject.append("</i>")
										bodyobject.append("\n")
										bodyobject.append("<i>")
										bodyobject.extend(modifiedobject)
										bodyobject.append("</i>")
										bodyobject.append("\n")
										bodyobject.append("\n")
										if mode == "Full":
											for div in mydivs:
												blockquote = div.findAll('blockquote')
												for b in blockquote:
													b.decompose()
												br = div.findAll('br/')
												for b in br:
													b.decompose()
												innerdiv = div.findAll('div')
												for inn in innerdiv:
													inn.decompose()	
												strong = div.findAll('strong')
												for s in strong:
													s.decompose()	
												a = div.findAll('span')
												for link in a:
													link.decompose()
												f = div.findAll('figure')
												for figure in f:
													figure.decompose()
												pic = div.findAll('div',{"data-css":"c-picture"})
												for picture in pic:
													picture.decompose()
												p = div.findAll('p',{"class": None})
												for para in p:
													if para.text is not "":
														parastring = para.text
														if not parastring.isspace():
															bodyobject.append(parastring)
															bodyobject.append("\n")
															bodyobject.append("\n")
											str1 = ''.join(bodyobject)
											result = 0
											for char in str1:
												result +=1
											try:
												if (result) > 4000:
													n = 4000
													checklist=["false"]
													while "false" in checklist:
														try:
															del checklist[:]
															n = n-1
															print(n)
															msglist = [str1[i:i+n] for i in range(0, len(str1), n)]
															for msg in msglist:
																if msg[-1] not in string.whitespace:
																	checklist.append("false")
																else:
																	checklist.append("true")
														except:
															del checklist[:]
															checklist = ["true"]
															n = 4000
															msglist = [str1[i:i+n] for i in range(0, len(str1), n)]
													for msg in msglist:
														cur.execute("""INSERT INTO Retrievedmsg VALUES(NULL,%s,%s)""",(cnaurl,msg,))
												else:
													cur.execute("""INSERT INTO Retrievedmsg VALUES(NULL,%s,%s)""",(cnaurl,str1,))
											except:
												catcherror = traceback.format_exc()
												info = update.message.from_user
												bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
												bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
											cur.execute("""SELECT retrievedtext,retrievedid FROM Retrievedmsg WHERE retrievedurl=%s limit 1""",(cnaurl,))
											if cur.rowcount > 0:
												data = cur.fetchone()
												retrievedmsg = data[0]
												spliceretrievedmsg = retrievedmsg[:500]
												dbid = "db-"+str(data[1])
												keyboard = []
												keyboard.append([InlineKeyboardButton("Read more 📰", callback_data=dbid),InlineKeyboardButton("Delete 🗑️",callback_data="dl")])
												reply_markup = InlineKeyboardMarkup(keyboard)
												update.message.reply_text(spliceretrievedmsg, reply_markup=reply_markup,parse_mode='HTML')
										else:
											summarystring = ""
											for div in mydivs:
												blockquote = div.findAll('blockquote')
												for b in blockquote:
													b.decompose()
												br = div.findAll('br/')
												for b in br:
													b.decompose()
												innerdiv = div.findAll('div')
												for inn in innerdiv:
													inn.decompose()	
												strong = div.findAll('strong')
												for s in strong:
													s.decompose()	
												a = div.findAll('span')
												for link in a:
													link.decompose()
												f = div.findAll('figure')
												for figure in f:
													figure.decompose()
												pic = div.findAll('div',{"data-css":"c-picture"})
												for picture in pic:
													picture.decompose()
												p = div.findAll('p',{"class": None})
												for para in p:
													if para.text is not "":
														parastring = para.text
														if not parastring.isspace():
															summarystring += parastring
															summarystring += " "
											plaintext = PlaintextParser.from_string(summarystring,Tokenizer("english"))
											stemmer = Stemmer("english")
											summarizer = Summarizer(stemmer)
											summarizer.stop_words = get_stop_words("english")
											for sentence in summarizer(plaintext.document, 3):			
												bodyobject.append(str(sentence))
												bodyobject.append("\n")
												bodyobject.append("\n")
											bodyobject.append("This is a truncated version of the article. For the full version, please switch the bot using /mode Full")
											str1 = ''.join(bodyobject)
											keyboard = []
											keyboard.append([InlineKeyboardButton("Delete 🗑️",callback_data="dl")])
											reply_markup=InlineKeyboardMarkup(keyboard)
											cur.execute("""INSERT INTO Truncmsg VALUES(NULL,%s,%s)""",(cnaurl,str1,))
											bot.sendMessage(chat_id=update.message.chat_id,reply_markup=reply_markup, text=str1,parse_mode='HTML')
									else:
										if mode == "Full":
											cur.execute("""SELECT retrievedtext,retrievedid FROM Retrievedmsg WHERE retrievedurl=%s limit 1""",(cnaurl,))
											if cur.rowcount > 0:
												data = cur.fetchone()
												retrievedmsg = data[0]
												spliceretrievedmsg = retrievedmsg[:500]
												dbid = "db-"+str(data[1])
												keyboard = []
												keyboard.append([InlineKeyboardButton("Read more 📰", callback_data=dbid),InlineKeyboardButton("Delete 🗑️",callback_data="dl")])
												reply_markup = InlineKeyboardMarkup(keyboard)
												update.message.reply_text(spliceretrievedmsg, reply_markup=reply_markup,parse_mode='HTML')
										else:
											cur.execute("""SELECT retrievedtext,retrievedid FROM Truncmsg WHERE retrievedurl = %s limit 1""",(cnaurl,))
											if cur.rowcount > 0:
												data = cur.fetchone()
												keyboard = []
												keyboard.append([InlineKeyboardButton("Delete 🗑️",callback_data="dl")])
												reply_markup=InlineKeyboardMarkup(keyboard)
												bot.sendMessage(chat_id=update.message.chat_id,reply_markup=reply_markup, text=data[0],parse_mode='HTML')
							except:
								catcherror = traceback.format_exc()
								info = update.message.from_user
								bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
								bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
					except:
						catcherror = traceback.format_exc()
						info = update.message.from_user
						bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
						bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')

		except:
			catcherror = traceback.format_exc()
			info = update.message.from_user
			bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
			bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
	def todayonline(bot, update):
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					try:
						url=update.message.text
						todayurl = url[7:]
						checktodayurl = todayurl[:27]
						if checktodayurl != "http://www.todayonline.com/":
							bot.sendMessage(chat_id=update.message.chat_id, text="""Please enter a valid url. For example, http://www.todayonline.com/<article>""",parse_mode='Markdown')

						else:
							try:
								headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
								result = requests.get(todayurl,headers=headers)
								print(result.status_code)
								if (result.status_code >= 400):
									bot.sendMessage(chat_id=update.message.chat_id, text="""This story does not exist!""",parse_mode='Markdown')
								else:
									chatid = update.message.chat.id
									chattype = update.message.chat.type
									cur.execute("""SELECT * FROM Userdb WHERE chatid = %s""",(chatid,))
									if cur.rowcount == 0:
										cur.execute("""INSERT INTO Userdb VALUES(%s,%s,%s,%s)""",(chatid,chattype,'Full','Subscribe'))
										mode = "Full"
									else:
										data = cur.fetchone()
										mode = data[2]										
									if mode == "Full":
										cur.execute("""SELECT * FROM Retrievedmsg WHERE retrievedurl = %s""",(todayurl,))
									else:
										cur.execute("""SELECT * FROM Truncmsg WHERE retrievedurl = %s""",(todayurl,))
									if cur.rowcount == 0:
										if (datetime.today().weekday() <= 4): #if weekday (0-4 = Monday to Fri, 5-6 = Sat,Sun)
											headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
											r = requests.get(todayurl, headers=headers)
											c = r.content
											soup = BeautifulSoup(c,"html.parser")
											mydivs = soup.findAll("div", { "class" : "content" })
											titlediv = soup.findAll("meta", {"property" : "og:title"})
											publishdiv = soup.findAll("div", {"class" : "authoring full-date"})
											updatediv = soup.findAll("meta", {"property" : "article:modified_time"})
											bodyobject = []
											publishedobject = []
											modifiedobject = []
											dateval = soup.findAll("span", {"class" : "date-value"})
											dateobj = []
											for date in dateval:
												dt = parser.parse(date.text)
												dateobj.append(dt)
											if len(dateobj) > 1:
												pubdate = min(dateobj)
												moddate = max(dateobj)
											else:
												pubdate = min(dateobj)
											for title in titlediv:
												articletitle = title['content']
												bodyobject.append("<b>")
												bodyobject.append(articletitle)
												bodyobject.append("</b>")
												bodyobject.append("\n")
												bodyobject.append("\n")
											for postdate in publishdiv:
												datelbl = postdate.findAll("span", {"class" : "date-label"})
												for lbl in datelbl:
													if "Published:" in lbl.text:
														publishedobject.append('Published at: ')
														publishedobject.append(pubdate.strftime("%B %d, %Y %H:%M"))
													else:
														modifiedobject.append('Updated at: ')
														modifiedobject.append(moddate.strftime("%B %d, %Y %H:%M"))
											bodyobject.append("<i>")
											bodyobject.extend(publishedobject)
											bodyobject.append("</i>")
											bodyobject.append("\n")
											bodyobject.append("<i>")
											bodyobject.extend(modifiedobject)
											bodyobject.append("</i>")
											bodyobject.append("\n")
											bodyobject.append("\n")
											if mode == "Full":
												for div in mydivs:
													blockquote = div.findAll('blockquote')
													for b in blockquote:
														b.decompose()
													a = div.findAll('span')
													for link in a:
														link.decompose()
													s = div.findAll('sup')
													for sup in s:
														sup.decompose()
													p = div.findAll('p',{"class": None})
													for para in p:
														if para.text is not "":
															parastring = escape_markdown(para.text)
															bodyobject.append(parastring)
															bodyobject.append("\n")
															bodyobject.append("\n")
												str1 = ''.join(bodyobject)
												result = 0
												for char in str1:
													result +=1
												try:
													if (result) > 4000:
														n = 4000
														checklist=["false"]
														while "false" in checklist:
															try:
																del checklist[:]
																n = n-1
																msglist = [str1[i:i+n] for i in range(0, len(str1), n)]
																for msg in msglist:
																	if msg[-1] not in string.whitespace:
																		checklist.append("false")
																	else:
																		checklist.append("true")
															except:
																del checklist[:]
																checklist = ["true"]
																n = 4000
																msglist = [str1[i:i+n] for i in range(0, len(str1), n)]
														for msg in msglist:
															cur.execute("""INSERT INTO Retrievedmsg VALUES(NULL,%s,%s)""",(todayurl,msg,))
													else:
														cur.execute("""INSERT INTO Retrievedmsg VALUES(NULL,%s,%s)""",(todayurl,str1,))
												except:
													catcherror = traceback.format_exc()
													info = update.message.from_user
													bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
													bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
												cur.execute("""SELECT retrievedtext,retrievedid FROM Retrievedmsg WHERE retrievedurl=%s limit 1""",(todayurl,))
												if cur.rowcount > 0:
													data = cur.fetchone()
													retrievedmsg = data[0]
													spliceretrievedmsg = retrievedmsg[:500]
													dbid = "db-"+str(data[1])
													keyboard = []
													keyboard.append([InlineKeyboardButton("Read more 📰", callback_data=dbid),InlineKeyboardButton("Delete 🗑️",callback_data="dl")])
													reply_markup = InlineKeyboardMarkup(keyboard)
													update.message.reply_text(spliceretrievedmsg, reply_markup=reply_markup,parse_mode='HTML')
											else: #if mode = trunc
												summarystring = ""
												for div in mydivs:
													blockquote = div.findAll('blockquote')
													for b in blockquote:
														b.decompose()
													a = div.findAll('span')
													for link in a:
														link.decompose()
													s = div.findAll('sup')
													for sup in s:
														sup.decompose()
													p = div.findAll('p',{"class": None})
													for para in p:
														if para.text is not "":
															parastring = escape_markdown(para.text)
															summarystring += parastring
															summarystring += " "
												plaintext = PlaintextParser.from_string(summarystring,Tokenizer("english"))
												stemmer = Stemmer("english")
												summarizer = Summarizer(stemmer)
												summarizer.stop_words = get_stop_words("english")
												for sentence in summarizer(plaintext.document, 3):			
													bodyobject.append(str(sentence))
													bodyobject.append("\n")
													bodyobject.append("\n")
												bodyobject.append("This is a truncated version of the article. For the full version, please switch the bot using /mode Full")
												str1 = ''.join(bodyobject)
												cur.execute("""INSERT INTO Truncmsg VALUES(NULL,%s,%s)""",(todayurl,str1,))
												keyboard = []
												keyboard.append([InlineKeyboardButton("Delete 🗑️",callback_data="dl")])
												reply_markup=InlineKeyboardMarkup(keyboard)
												bot.sendMessage(chat_id=update.message.chat_id,reply_markup=reply_markup, text=str1,parse_mode='HTML')
										else:
											url = todayurl  
											#This does the magic.Loads everything
											browser = webdriver.PhantomJS('./phantomjs')
											browser.get(todayurl)
											formatted_result = browser.page_source
											#Next build lxml tree from formatted_result
											tree = html.fromstring(formatted_result)
											headline = tree.xpath('//div[@class="post-title"]/h2/text()[1]')
											pubdate = tree.xpath('//div[@class="post-byline_item"]/span/text()[1]')
											updatedate = tree.xpath('//div[@class="post-timestamp-update"]/text()[1]')
											contentbody = tree.xpath('//div[@class="post-content _3BQOkQI9IqOVz5LCwpdk2f_1"]/p/text()[1]')
											bodyobject = []
											modifiedobject = []
											bodyobject.append("<b>")
											bodyobject.append(headline[0])
											bodyobject.append("</b> \n \n")
											bodyobject.append("<i>")
											for each in pubdate:
												bodyobject.append(each)
											bodyobject.append("</i> \n \n")
											if updatedate:
												bodyobject.append("<i>")
												bodyobject.append(updatedate[0])
												bodyobject.append("</i> \n \n")
											if mode == "Full":
												for para in contentbody:
													if para.strip() != "":
														bodyobject.append(para)
														bodyobject.append("\n \n")
												str1 = ' '.join(bodyobject)
												result = 0
												for char in str1:
													result +=1
												try:
													if (result) > 4000:
														n = 4000
														checklist=["false"]
														while "false" in checklist:
															try:
																del checklist[:]
																n = n-1
																msglist = [str1[i:i+n] for i in range(0, len(str1), n)]
																for msg in msglist:
																	if msg[-1] not in string.whitespace:
																		checklist.append("false")
																	else:
																		checklist.append("true")
															except:
																del checklist[:]
																checklist = ["true"]
																n = 4000
																msglist = [str1[i:i+n] for i in range(0, len(str1), n)]
														for msg in msglist:
															cur.execute("""INSERT INTO Retrievedmsg VALUES(NULL,%s,%s)""",(todayurl,msg,))
													else:
														cur.execute("""INSERT INTO Retrievedmsg VALUES(NULL,%s,%s)""",(todayurl,str1,))
												except:
													catcherror = traceback.format_exc()
													info = update.message.from_user
													bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
													bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
												cur.execute("""SELECT retrievedtext,retrievedid FROM Retrievedmsg WHERE retrievedurl=%s limit 1""",(todayurl,))
												if cur.rowcount > 0:
													data = cur.fetchone()
													retrievedmsg = data[0]
													spliceretrievedmsg = retrievedmsg[:500]
													dbid = "db-"+str(data[1])
													keyboard = []
													keyboard.append([InlineKeyboardButton("Read more 📰", callback_data=dbid),InlineKeyboardButton("Delete 🗑️",callback_data="dl")])
													reply_markup = InlineKeyboardMarkup(keyboard)
													update.message.reply_text(spliceretrievedmsg, reply_markup=reply_markup,parse_mode='HTML')
											else:
												summarystring = ""
												for para in contentbody:
													summarystring += para
													summarystring += " "
												plaintext = PlaintextParser.from_string(summarystring,Tokenizer("english"))
												stemmer = Stemmer("english")
												summarizer = Summarizer(stemmer)
												summarizer.stop_words = get_stop_words("english")
												for sentence in summarizer(plaintext.document, 3):			
													bodyobject.append(str(sentence))
													bodyobject.append("\n")
													bodyobject.append("\n")
												bodyobject.append("This is a truncated version of the article. For the full version, please switch the bot using /mode Full")
												str1 = ''.join(bodyobject)
												cur.execute("""INSERT INTO Truncmsg VALUES(NULL,%s,%s)""",(todayurl,str1,))
												keyboard = []
												keyboard.append([InlineKeyboardButton("Delete 🗑️",callback_data="dl")])
												reply_markup=InlineKeyboardMarkup(keyboard)
												bot.sendMessage(chat_id=update.message.chat_id,reply_markup=reply_markup, text=str1,parse_mode='HTML')
									else:
										if mode == "Full":
											cur.execute("""SELECT retrievedtext,retrievedid FROM Retrievedmsg WHERE retrievedurl=%s limit 1""",(todayurl,))
											if cur.rowcount > 0:
												data = cur.fetchone()
												retrievedmsg = data[0]
												spliceretrievedmsg = retrievedmsg[:500]
												dbid = "db-"+str(data[1])
												keyboard = []
												keyboard.append([InlineKeyboardButton("Read more 📰", callback_data=dbid),InlineKeyboardButton("Delete 🗑️",callback_data="dl")])
												reply_markup = InlineKeyboardMarkup(keyboard)
												update.message.reply_text(spliceretrievedmsg, reply_markup=reply_markup,parse_mode='HTML')
										else:
											cur.execute("""SELECT retrievedtext,retrievedid FROM Truncmsg WHERE retrievedurl = %s limit 1""",(todayurl,))
											if cur.rowcount > 0:
												data = cur.fetchone()
												keyboard = []
												keyboard.append([InlineKeyboardButton("Delete 🗑️",callback_data="dl")])
												reply_markup=InlineKeyboardMarkup(keyboard)
												bot.sendMessage(chat_id=update.message.chat_id,reply_markup=reply_markup,text=data[0],parse_mode='HTML') #if its a weekend
							except:
								catcherror = traceback.format_exc()
								info = update.message.from_user
								bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
								bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
					except:
						catcherror = traceback.format_exc()
						info = update.message.from_user
						bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
						bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')

		except:
			catcherror = traceback.format_exc()
			info = update.message.from_user
			bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
			bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')

	def allnew(bot,update):
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					try:
						cur.execute("""SELECT * 
							FROM `combinedarticle` 
							WHERE(url_site = 1 OR url_site = 2 OR url_site = 3) 
							ORDER BY `url_dt` 
							DESC LIMIT 5 OFFSET 0""")
						data = cur.fetchall()
						if cur.rowcount > 0:
							counter = 1
							keyboard = []
							replystring = "These are the latest 5 stories from all supported news sources\n"
							for row in data:
								if row[5] == 2:
									all_id = "cn-"+str(row[0])
									source = "CNA"
								elif row[5] == 3:
									all_id = "td-"+str(row[0])
									source = "Today"
								elif row[5] == 1:
									all_id = "st-"+str(row[0]) 
									source = "ST"
								label= "Story "+ str(counter) +" : ("+source+") "
								keyboard.append([InlineKeyboardButton(label, callback_data=all_id)])
								replystring += str(counter) + ". "+"("+source+")"
								replystring += row[1]
								replystring += "\n"						
								counter +=1
							next5 = "nx-"+"alsearch-"+"5"
							keyboard.append([InlineKeyboardButton("Next Five →",callback_data=next5)])
							replystring += "Please select an option below."
							reply_markup = InlineKeyboardMarkup(keyboard)
							update.message.reply_text(replystring, reply_markup=reply_markup)
						else:
							bot.sendMessage(chat_id=update.message.chat_id, text="""Unable to find any results =( =(""",parse_mode='Markdown')
					except:						
						catcherror = traceback.format_exc()
						info = update.message.from_user
						bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
						bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
		except:						
			catcherror = traceback.format_exc()
			info = update.message.from_user
			bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
			bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
	def allnext(bot,update,offset,hidebtn):
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					try:
						cur.execute("""SELECT * 
							FROM `combinedarticle` 
							WHERE(url_site = 1 OR url_site = 2 OR url_site = 3) 
							ORDER BY `url_dt` DESC 
							LIMIT 5 OFFSET %s""",(int(offset),))
						data = cur.fetchall()
						if cur.rowcount > 0:
							counter = 1
							keyboard = []
							replystring = "These are the latest 5 stories from all supported news sources\n"
							for row in data:
								if row[5] == 2:
									all_id = "cn-"+str(row[0])
									source = "CNA"
								elif row[5] == 3:
									all_id = "td-"+str(row[0])
									source = "Today"
								elif row[5] == 1:
									all_id = "st-"+str(row[0]) 
									source = "ST"
								label= "Story "+ str(counter) +" : ("+source+") "
								keyboard.append([InlineKeyboardButton(label, callback_data=all_id)])
								replystring += str(counter) + ". "+"("+source+") "
								replystring += row[1]
								replystring += "\n"						
								counter +=1
							nextoffset = int(offset)+5
							prevoffset = int(offset)-5
							next5 = "nx-"+"alsearch-"+str(nextoffset)
							prev5 = "pr-"+"alsearch-"+str(prevoffset)
							if hidebtn == "true":
								keyboard.append([InlineKeyboardButton("Next Five →",callback_data=next5)])
							else:
								keyboard.append([InlineKeyboardButton("← Previous Five",callback_data=prev5),InlineKeyboardButton("Next Five →",callback_data=next5)])
							replystring += "Please select an option below."
							reply_markup = InlineKeyboardMarkup(keyboard)
							bot.edit_message_text(text=replystring,chat_id=update.message.chat_id,message_id=update.message.message_id,reply_markup=reply_markup,parse_mode='HTML')
						else:
							bot.sendMessage(chat_id=update.message.chat_id, text="""Unable to find any results =( =(""",parse_mode='Markdown')
					except:						
						catcherror = traceback.format_exc()
						info = update.message.from_user
						bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
						bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
		except:						
			catcherror = traceback.format_exc()
			info = update.message.from_user
			bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
			bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
	def allsearch(bot,update):
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					try:
						searchtext = update.message.text
						if len(searchtext[8:]) < 5:
							bot.sendMessage(chat_id=update.message.chat_id, text="""Please enter a longer search query!""",parse_mode='Markdown')
						else:
							newsearch = searchtext[8:]
							print(newsearch)
							qsearch = "%"+newsearch+"%"
							cur.execute("""SELECT * 
											FROM combinedarticle 
											WHERE LOWER(url_title) LIKE LOWER(%s)
											AND (url_site = 1 OR url_site = 2 OR url_site = 3) 
											ORDER BY url_dt 
											DESC LIMIT 5""",(qsearch,))
							data = cur.fetchall()
							if cur.rowcount > 0:
								counter = 1
								keyboard = []
								replystring = "These are the latest 5 stories based on your search terms\n For more stories, please refine your search terms\n"
								for row in data:
									if row[5] == 2:
										all_id = "cn-"+str(row[0])
										source = "CNA"
									elif row[5] == 3:
										all_id = "td-"+str(row[0])
										source = "Today"
									elif row[5] == 1:
										all_id = "st-"+str(row[0]) 
										source = "ST"
									label= "Story "+ str(counter) +" : ("+source+") "
									keyboard.append([InlineKeyboardButton(label, callback_data=all_id)])
									replystring += str(counter) + ". "+"("+source+") "
									replystring += row[1]
									replystring += "\n"					
									counter +=1
								replystring += "Please select an option below."
								reply_markup = InlineKeyboardMarkup(keyboard)
								update.message.reply_text(replystring, reply_markup=reply_markup)
							else:
								bot.sendMessage(chat_id=update.message.chat_id, text="""Unable to find any results =( =(""",parse_mode='Markdown')
					except:
						catcherror = traceback.format_exc()
						info = update.message.from_user
						bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
						bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
		except:
			catcherror = traceback.format_exc()
			info = update.message.from_user
			bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
			bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
	def allrand(bot,update):
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					try:
						cur.execute("""SELECT MAX(url_id) FROM combinedarticle WHERE (url_site = 1 OR url_site = 2 OR url_site = 3)""")
						if cur.rowcount > 0:
							data = cur.fetchone()
							maxval = int(data[0])
							randomidlist = []
							confirmedidlist = []
							checkrandom = ["false"]
							try:
								while "false" in checkrandom:
									del checkrandom[:]
									del randomidlist[:]
									randomidlist = random.sample(range(1,maxval),1)
									cur.execute("""SELECT url_id FROM combinedarticle WHERE url_id = %s AND (url_site = 1 OR url_site = 2 OR url_site = 3) """,(int(randomidlist[0]),))
									if cur.rowcount > 0:
										data = cur.fetchone()
										urlid = data[0]
										newstring = "'" + str(urlid) + "'"
										confirmedidlist.append(urlid)
										if len(confirmedidlist) < 5:
											checkrandom.append("false")
										else:
											checkrandom.append("true")
									else:
										checkrandom.append("false")
							except:		
								catcherror = traceback.format_exc()
								info = update.message.from_user
								bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
								bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')

							try:
								checkidlist = ["false"] #here, we force a while loop to start. we'll clear it later, so if the results work, it stops
								keyboard = []
								while "false" in checkidlist:
									del checkidlist[:]
									del keyboard[:]
									del randomidlist[:] 
									#for each loop, if it doesnt match, you're gonna want to clear your lists and start all over again.
									randomidlist = random.sample(range(1,maxval),5)
									print(randomidlist)
									counter = 1
									replystring = "These are 5 random stories from all supported news sources.\n\n"
									for each in confirmedidlist:
										try:
											cur.execute("""SELECT * FROM combinedarticle WHERE url_id = %s AND (url_site = 1 OR url_site = 2 OR url_site = 3) """,(each,))
											if cur.rowcount > 0:
												row = cur.fetchone()
												if row[5] == 2:
													all_id = "cn-"+str(row[0])
													source = "CNA"
												elif row[5] == 3:
													all_id = "td-"+str(row[0])
													source = "Today"
												elif row[5] == 1:
													all_id = "st-"+str(row[0]) 
													source = "ST"
												label= "Story "+ str(counter) +" : ("+source+") "
												keyboard.append([InlineKeyboardButton(label, callback_data=all_id)])
												replystring += str(counter) + ". "+"("+source+") "
												replystring += row[1]
												replystring += "\n"									
												counter +=1
												checkidlist.append("true")
											else:
												checkidlist.append("false")
										except:						
											catcherror = traceback.format_exc()
											info = update.message.from_user
											bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
											bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
								replystring += "\n"	
								replystring += "Please select an option below."
								reply_markup = InlineKeyboardMarkup(keyboard)
								update.message.reply_text(replystring, reply_markup=reply_markup)
							except:						
								catcherror = traceback.format_exc()
								info = update.message.from_user
								bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
								bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
					except:
						catcherror = traceback.format_exc()
						info = update.message.from_user
						bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
						bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
		except:						
			catcherror = traceback.format_exc()
			info = update.message.from_user
			bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
			bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
	def stnew(bot,update):
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					try:
						cur.execute("""SELECT * 
							FROM `combinedarticle` 
							WHERE url_site = 1 
							ORDER BY `url_dt` 
							DESC LIMIT 5 
							OFFSET 0""")
						data = cur.fetchall()
						if cur.rowcount > 0:
							counter = 1
							keyboard = []
							replystring = "These are the latest 5 stories from StraitsTimes\n"
							for row in data:
								ms_id = "st-"+str(row[0])
								print(ms_id)
								label= "Story "+ str(counter)
								keyboard.append([InlineKeyboardButton(label, callback_data=ms_id)])
								replystring += str(counter) + ". "
								replystring += row[1]
								replystring += "\n"						
								counter +=1
							next5 = "nx-"+"stsearch-"+"5"
							keyboard.append([InlineKeyboardButton("Next Five →",callback_data=next5)])
							replystring += "Please select an option below."
							reply_markup = InlineKeyboardMarkup(keyboard)
							update.message.reply_text(replystring, reply_markup=reply_markup)
						else:
							bot.sendMessage(chat_id=update.message.chat_id, text="""Unable to find any results =( =(""",parse_mode='Markdown')
					except:						
						catcherror = traceback.format_exc()
						info = update.message.from_user
						bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
						bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
		except:						
			catcherror = traceback.format_exc()
			info = update.message.from_user
			bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
			bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
	def stnext(bot,update,offset,hidebtn):
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					try:
						cur.execute("""SELECT * 
							FROM `combinedarticle` 
							WHERE url_site = 1 
							ORDER BY `url_dt` 
							DESC LIMIT 5 
							OFFSET %s""",(int(offset),))
						data = cur.fetchall()
						if cur.rowcount > 0:
							counter = 1
							keyboard = []
							replystring = "These are the next 5 stories from Straits Times\n"
							for row in data:
								ms_id = "st-"+str(row[0])
								label= "Story "+ str(counter)
								keyboard.append([InlineKeyboardButton(label, callback_data=ms_id)])
								replystring += str(counter) + ". "
								replystring += row[1]
								replystring += "\n"
								counter += 1
							nextoffset = int(offset)+5
							prevoffset = int(offset)-5
							next5 = "nx-"+"stsearch-"+str(nextoffset)
							prev5 = "pr-"+"stsearch-"+str(prevoffset)
							if hidebtn == "true":
								keyboard.append([InlineKeyboardButton("Next Five →",callback_data=next5)])
							else:
								keyboard.append([InlineKeyboardButton("← Previous Five",callback_data=prev5),InlineKeyboardButton("Next Five →",callback_data=next5)])
							replystring += "Please select an option below."
							reply_markup = InlineKeyboardMarkup(keyboard)
							bot.edit_message_text(text=replystring,chat_id=update.message.chat_id,message_id=update.message.message_id,reply_markup=reply_markup,parse_mode='HTML')
						else:
							bot.sendMessage(chat_id=update.message.chat_id, text="""Unable to find any results =( =(""",parse_mode='Markdown')
					except:						
						catcherror = traceback.format_exc()
						info = update.message.from_user
						bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
						bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
		except:						
			catcherror = traceback.format_exc()
			info = update.message.from_user
			bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
			bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
	def stsearch(bot,update):
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					try:
						searchtext = update.message.text
						if len(searchtext[11:]) < 5:
							bot.sendMessage(chat_id=update.message.chat_id, text="""Please enter a longer search query!""",parse_mode='Markdown')
						else:
							newsearch = searchtext[11:]
							qsearch = "%"+newsearch+"%"
							cur.execute("""SELECT * 
											FROM combinedarticle 
											WHERE LOWER(url_title) LIKE LOWER(%s)
											AND url_site = 1
											ORDER BY url_dt 
											DESC LIMIT 5""",(qsearch,))
							data = cur.fetchall()
							if cur.rowcount > 0:
								counter = 1
								keyboard = []
								replystring = "These are the latest 5 stories based on your search terms\n For more stories, please refine your search terms\n"
								for row in data:
									ms_id = "st-"+str(row[0])
									label= "Story "+ str(counter)
									keyboard.append([InlineKeyboardButton(label, callback_data=ms_id)])
									replystring += str(counter) + ". "
									replystring += row[1]
									replystring += "\n"									
									counter +=1
								replystring += "Please select an option below."
								reply_markup = InlineKeyboardMarkup(keyboard)
								update.message.reply_text(replystring, reply_markup=reply_markup)
							else:
								bot.sendMessage(chat_id=update.message.chat_id, text="""Unable to find any results =( =(""",parse_mode='Markdown')
					except:
						catcherror = traceback.format_exc()
						info = update.message.from_user
						bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
						bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
		except:
			catcherror = traceback.format_exc()
			info = update.message.from_user
			bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
			bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
	def strand(bot,update):
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					try:
						cur.execute("""SELECT MAX(url_id) FROM combinedarticle WHERE url_site = 1""")
						if cur.rowcount > 0:
							data = cur.fetchone()
							maxval = int(data[0])
							randomidlist = []
							confirmedidlist = []
							checkrandom = ["false"]
							try:
								while "false" in checkrandom:
									del checkrandom[:]
									del randomidlist[:]
									randomidlist = random.sample(range(1,maxval),1)
									cur.execute("""SELECT url_id FROM combinedarticle WHERE url_id = %s AND url_site = 1""",(int(randomidlist[0]),))
									if cur.rowcount > 0:
										data = cur.fetchone()
										urlid = data[0]
										newstring = "'" + str(urlid) + "'"
										confirmedidlist.append(urlid)
										if len(confirmedidlist) < 5:
											checkrandom.append("false")
										else:
											checkrandom.append("true")
									else:
										checkrandom.append("false")
							except:		
								catcherror = traceback.format_exc()
								info = update.message.from_user
								bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
								bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')

							try:
								checkidlist = ["false"] #here, we force a while loop to start. we'll clear it later, so if the results work, it stops
								keyboard = []
								while "false" in checkidlist:
									del checkidlist[:]
									del keyboard[:]
									del randomidlist[:] 
									#for each loop, if it doesnt match, you're gonna want to clear your lists and start all over again.
									randomidlist = random.sample(range(1,maxval),5)
									counter = 1
									replystring = "These are 5 random stories from StraitsTimes.\n\n"
									for each in confirmedidlist:
										try:
											cur.execute("""SELECT * FROM combinedarticle WHERE url_id = %s AND url_site = 1""",(each,))
											if cur.rowcount > 0:
												row = cur.fetchone()
												ms_id = "st-"+str(row[0])
												label= "Story "+ str(counter)
												keyboard.append([InlineKeyboardButton(label, callback_data=ms_id)])
												replystring += str(counter) + ". "
												replystring += row[1]
												replystring += "\n"									
												counter +=1
												checkidlist.append("true")
											else:
												checkidlist.append("false")
										except:						
											catcherror = traceback.format_exc()
											info = update.message.from_user
											bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
											bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
								replystring += "\n"	
								replystring += "Please select an option below."
								reply_markup = InlineKeyboardMarkup(keyboard)
								update.message.reply_text(replystring, reply_markup=reply_markup)
							except:						
								catcherror = traceback.format_exc()
								info = update.message.from_user
								bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
								bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
					except:
						catcherror = traceback.format_exc()
						info = update.message.from_user
						bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
						bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
		except:						
			catcherror = traceback.format_exc()
			info = update.message.from_user
			bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
			bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
	def cnarand(bot,update):
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					try:
						cur.execute("""SELECT MAX(url_id) FROM combinedarticle WHERE url_site = 2""")
						if cur.rowcount > 0:
							data = cur.fetchone()
							maxval = int(data[0])
							randomidlist = []
							confirmedidlist = []
							checkrandom = ["false"]
							try:
								while "false" in checkrandom:
									del checkrandom[:]
									del randomidlist[:]
									randomidlist = random.sample(range(1,maxval),1)
									cur.execute("""SELECT url_id FROM combinedarticle WHERE url_id = %s AND url_site = 2""",(int(randomidlist[0]),))
									if cur.rowcount > 0:
										data = cur.fetchone()
										urlid = data[0]
										newstring = "'" + str(urlid) + "'"
										confirmedidlist.append(urlid)
										if len(confirmedidlist) < 5:
											checkrandom.append("false")
										else:
											checkrandom.append("true")
									else:
										checkrandom.append("false")
							except:		
								catcherror = traceback.format_exc()
								info = update.message.from_user
								bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
								bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')

							try:
								checkidlist = ["false"]
								keyboard = []
								while "false" in checkidlist:
									del checkidlist[:]
									del keyboard[:]
									counter = 1
									replystring = "These are 5 random stories from Channel News Asia.\n\n"
									for each in confirmedidlist:
										try:
											cur.execute("""SELECT * FROM combinedarticle WHERE url_id = %s AND url_site = 2""",(each,))
											if cur.rowcount > 0:
												row = cur.fetchone()
												ms_id = "cn-"+str(row[0])
												label= "Story "+ str(counter)
												keyboard.append([InlineKeyboardButton(label, callback_data=ms_id)])
												replystring += str(counter) + ". "
												replystring += row[1]
												replystring += "\n"									
												counter +=1
												checkidlist.append("true")
											else:
												checkidlist.append("false")
										except:						
											catcherror = traceback.format_exc()
											info = update.message.from_user
											bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
											bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
								replystring += "\n"	
								replystring += "Please select an option below."
								reply_markup = InlineKeyboardMarkup(keyboard)
								update.message.reply_text(replystring, reply_markup=reply_markup)
							except:		
								catcherror = traceback.format_exc()
								info = update.message.from_user
								bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
								bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
					except:						
						catcherror = traceback.format_exc()
						info = update.message.from_user
						bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
						bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
		except:
			catcherror = traceback.format_exc()
			info = update.message.from_user
			bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
			bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')	
	def cnanew(bot,update):
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					try:
						cur.execute("""SELECT * 
							FROM `combinedarticle` 
							WHERE url_site = 2 
							ORDER BY `url_dt` 
							DESC LIMIT 5 
							OFFSET 0""")
						data = cur.fetchall()
						if cur.rowcount > 0:
							counter = 1
							keyboard = []
							replystring = "These are the latest 5 stories from ChannelNewsAsia\n"
							for row in data:
								cna_id = "cn-"+str(row[0])
								label= "Story "+ str(counter)
								keyboard.append([InlineKeyboardButton(label, callback_data=cna_id)])
								replystring += str(counter) + ". "
								replystring += row[1]
								replystring += "\n"								
								counter +=1
							next5 = "nx-"+"cnsearch-"+"5"
							keyboard.append([InlineKeyboardButton("Next Five →",callback_data=next5)])
							replystring += "Please select an option below."
							reply_markup = InlineKeyboardMarkup(keyboard)
							update.message.reply_text(replystring, reply_markup=reply_markup)
						else:
							bot.sendMessage(chat_id=update.message.chat_id, text="""Unable to find any results =( =(""",parse_mode='Markdown')
					except:						
						catcherror = traceback.format_exc()
						info = update.message.from_user
						bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
						bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
	
		except:						
			catcherror = traceback.format_exc()
			info = update.message.from_user
			bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
			bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')	
	def cnanext(bot,update,offset,hidebtn):
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					try:
						cur.execute("""SELECT * 
							FROM `combinedarticle` 
							WHERE url_site = 2 
							ORDER BY `url_dt` 
							DESC LIMIT 5 
							OFFSET %s""",(int(offset),))
						data = cur.fetchall()
						if cur.rowcount > 0:
							counter = 1
							keyboard = []
							replystring = "These are the latest 5 stories from ChannelNewsAsia\n"
							cnlist = []
							for row in data:
								cna_id = "cn-"+str(row[0])
								label= "Story "+ str(counter)
								keyboard.append([InlineKeyboardButton(label, callback_data=cna_id)])
								replystring += str(counter) + ". "
								replystring += row[1]
								replystring += "\n"
								cnlist.append(row[0])									
								counter +=1
							nextoffset = int(offset)+5
							prevoffset = int(offset)-5
							next5 = "nx-"+"cnsearch-"+str(nextoffset)
							prev5 = "pr-"+"cnsearch-"+str(prevoffset)
							if hidebtn == "true":
								keyboard.append([InlineKeyboardButton("Next Five →",callback_data=next5)])
							else:
								keyboard.append([InlineKeyboardButton("← Previous Five",callback_data=prev5),InlineKeyboardButton("Next Five →",callback_data=next5)])
							replystring += "Please select an option below."
							reply_markup = InlineKeyboardMarkup(keyboard)
							bot.edit_message_text(text=replystring,chat_id=update.message.chat_id,message_id=update.message.message_id,reply_markup=reply_markup,parse_mode='HTML')
						else:
							bot.sendMessage(chat_id=update.message.chat_id, text="""Unable to find any results =( =(""",parse_mode='Markdown')
					except:						
						catcherror = traceback.format_exc()
						info = update.message.from_user
						bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
						bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
	
		except:						
			catcherror = traceback.format_exc()
			info = update.message.from_user
			bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
			bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')	
	def cnasearch(bot,update):
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					try:
						searchtext = update.message.text
						if len(searchtext[12:]) < 5:
							bot.sendMessage(chat_id=update.message.chat_id, text="""Please enter a longer search query!""",parse_mode='Markdown')
						else:
							newsearch = searchtext[12:]
							qsearch = "%"+newsearch+"%"
							cur.execute("""SELECT * 
											FROM combinedarticle 
											WHERE LOWER(url_title) LIKE LOWER(%s)
											AND url_site = 2
											ORDER BY url_dt 
											DESC LIMIT 5""",(qsearch,))
							data = cur.fetchall()
							if cur.rowcount > 0:
								counter = 1
								keyboard = []
								replystring = "These are the latest 5 stories based on your search terms\n For more stories, please refine your search terms\n"
								for row in data:
									cna_id = "cn-"+str(row[0])
									label= "Story "+ str(counter)
									keyboard.append([InlineKeyboardButton(label, callback_data=cna_id)])
									replystring += str(counter) + ". "
									replystring += row[1]
									replystring += "\n"									
									counter +=1
								replystring += "Please select an option below."
								reply_markup = InlineKeyboardMarkup(keyboard)
								update.message.reply_text(replystring, reply_markup=reply_markup)
							else:
								bot.sendMessage(chat_id=update.message.chat_id, text="""Unable to find any results =( =(""",parse_mode='Markdown')
					except:
						catcherror = traceback.format_exc()
						info = update.message.from_user
						bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
						bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
		except:						
			catcherror = traceback.format_exc()
			info = update.message.from_user
			bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
			bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
	def search(bot,update):
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					query = update.callback_query
					dbtype = query.data[:2]
					if dbtype in ['ms','st','cn', 'td']:
						artid = query.data[3:]
						cur.execute("""SELECT url_link FROM combinedarticle WHERE url_id = %s""",(int(artid),))
						if cur.rowcount > 0:
							data = cur.fetchone()
							arturl = data[0]
							if dbtype == "ms":
								fullurl = "/laobu "+arturl
								query.message.text = fullurl
								Commands.laobu(bot,query)
							elif dbtype == "st":
								fullurl = "/st "+arturl
								query.message.text = fullurl
								Commands.straitstimes(bot,query)
							elif dbtype == "cn":
								fullurl = "/cna "+arturl
								query.message.text = fullurl
								Commands.cna(bot,query)
							elif dbtype == "td":
								fullurl = "/today "+arturl
								query.message.text = fullurl
								Commands.todayonline(bot,query)
						else:
							bot.sendMessage(chat_id=query.message.chat_id, text="""Oops, something went wrong :(""",parse_mode='Markdown')
					elif dbtype == "db": #named db because you're pulling out of db
						multiid = query.message.message_id
						chatid = query.message.chat.id
						cur.execute("""SELECT multiid FROM multiplemsg WHERE multiid = %s AND chatid = %s""",(multiid,chatid,))
						if cur.rowcount == 0:
							artid = query.data[3:]
							print(query.data)
							cur.execute("""SELECT retrievedurl FROM Retrievedmsg WHERE retrievedid = %s""",(artid,))
							if cur.rowcount > 0:
								data = cur.fetchone()
								url = data[0]
								cur.execute("""SELECT * FROM Retrievedmsg WHERE retrievedurl = %s""",(url,))
								if cur.rowcount == 1:
									data = cur.fetchone()
									text = data[2]
									hideid = 'hd-'+artid
									keyboard = []
									keyboard.append([InlineKeyboardButton('Hide text 📕', callback_data=hideid),InlineKeyboardButton("Delete 🗑️",callback_data="dl")])
									reply_markup = InlineKeyboardMarkup(keyboard)
									bot.edit_message_text(text=text,chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=reply_markup,parse_mode='HTML')
								else:
									data = cur.fetchall()
									counter = 0
									for each in data:
										if counter == 0:
											hideid = 'hd-'+ str(each[0])
											text = each[2]
											keyboard = []
											keyboard.append([InlineKeyboardButton('Hide text 📕', callback_data=hideid),InlineKeyboardButton("Delete 🗑️",callback_data="dl")])
											reply_markup = InlineKeyboardMarkup(keyboard)
											bot.edit_message_text(text=text,chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=reply_markup,parse_mode='HTML')
											cur.execute("""INSERT INTO multiplemsg VALUES(%s,%s,%s)""",(multiid,each[0],chatid))
											counter+=1
										else:
											hideid = 'hd-'+ str(each[0])
											text = each[2]
											keyboard = []
											keyboard.append([InlineKeyboardButton('Hide text 📕', callback_data=hideid),InlineKeyboardButton("Delete 🗑️",callback_data="dl")])
											reply_markup = InlineKeyboardMarkup(keyboard)
											sent = bot.sendMessage(chat_id=query.message.chat_id, text=text,reply_markup=reply_markup,parse_mode='HTML')
											cur.execute("""INSERT INTO multiplemsg VALUES(%s,%s,%s)""",(sent.message_id,each[0],chatid))
						else:
							cur.execute("""SELECT b.retrievedtext FROM multiplemsg a left join Retrievedmsg b on a.retrievedid = b.retrievedid where a.multiid =  %s""",(multiid,))
							data = cur.fetchone()
							text = data[0]
							artid = query.data[3:]
							hideid = 'hd-'+artid
							keyboard = []
							keyboard.append([InlineKeyboardButton('Hide text 📕', callback_data=hideid),InlineKeyboardButton("Delete 🗑️",callback_data="dl")])
							reply_markup = InlineKeyboardMarkup(keyboard)
							bot.edit_message_text(text=text,chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=reply_markup,parse_mode='HTML')
					elif dbtype == "hd": #named hd because you're hiding msg
						artid = query.data[3:]
						cur.execute("""SELECT retrievedtext FROM Retrievedmsg WHERE retrievedid = %s""",(artid,))
						if cur.rowcount > 0:
							data = cur.fetchone()
							text = data[0]
							hiddentext = text[:500]
							showid = 'db-'+artid
							keyboard = []
							keyboard.append([InlineKeyboardButton('Read More 📖', callback_data=showid),InlineKeyboardButton("Delete 🗑️",callback_data="dl")])
							reply_markup = InlineKeyboardMarkup(keyboard)
							bot.edit_message_text(text=hiddentext,chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=reply_markup,parse_mode='HTML')
					elif dbtype == "nx": #next 5
						removenx = query.data[3:]
						searchtype = removenx[:8]
						removesearch = removenx[9:]
						bot.edit_message_text(chat_id=query.message.chat_id,message_id=query.message.message_id,text=query.message.text,parse_mode='HTML')
						if searchtype == "stsearch":
							try:
								Commands.stnext(bot,query,removesearch,"false")
							except:
								catcherror = traceback.format_exc()
								info = update.message.from_user
								bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
								bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
						elif searchtype == "cnsearch":
							try:
								Commands.cnanext(bot,query,removesearch,"false")
							except:
								catcherror = traceback.format_exc()
								info = update.message.from_user
								bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
								bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
						elif searchtype == "alsearch":
							try:
								Commands.allnext(bot,query,removesearch,"false")
							except:
								catcherror = traceback.format_exc()
								info = update.message.from_user
								bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
								bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')
					
					elif dbtype == "pr": #previous 5
						removepr = query.data[3:]
						searchtype = removepr[:8]
						removesearch = removepr[9:]
						bot.edit_message_text(chat_id=query.message.chat_id,message_id=query.message.message_id,text=query.message.text,parse_mode='HTML')
						if searchtype == "stsearch":
							try:
								if (int(removesearch) < 5):
									Commands.stnext(bot,query,0,"true")
								else:
									Commands.stnext(bot,query,removesearch,"false")
								
							except:						
								catcherror = traceback.format_exc()
								info = update.message.from_user
								bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
								bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')

						elif searchtype == "cnsearch":
							try:
								if (int(removesearch) < 5):
									Commands.cnanext(bot,query,0,"true")
								else:
									Commands.cnanext(bot,query,removesearch,"false")
							except:						
								catcherror = traceback.format_exc()
								info = update.message.from_user
								bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
								bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')

						elif searchtype == "alsearch":
							if (int(removesearch) < 5):
								Commands.allnext(bot,query,0,"true")
							else:
								Commands.allnext(bot,query,removesearch,"false")
					elif dbtype == "dl":
						try:
							bot.delete_message(chat_id = query.message.chat_id, message_id = query.message.message_id)
						except:						
							catcherror = traceback.format_exc()
							info = update.message.from_user
							bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
							bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')

		except:						
			catcherror = traceback.format_exc()
			info = update.message.from_user
			bot.sendMessage(chat_id=errorchannel.errorchannel('error'), text=str(catcherror)+str(info),parse_mode='HTML')
			bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. An error log has been generated for our trained chinchillas to work on it. We're sorry! =(""",parse_mode='Markdown')

