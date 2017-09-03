from telegram.ext import Updater
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import requests
import string
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import parser
from telegram.utils.helpers import escape_html, escape_markdown
import html2text
import html
import pymysql
from contextlib import closing
from tokens import SQL
from tokens import admins
import traceback

class Commands():
	def megaphone(bot,update):
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					userid = update.message.from_user.id
					print(userid)
					if admins.adminlist(userid) == "admin":
						megamessage = update.message.text[6:]
						cur.execute("""SELECT chatid FROM Userdb""")
						if cur.rowcount > 0:
							data = cur.fetchall()
							for each in data:
								print(round(float(each[0])))
								bot.sendMessage(chat_id=round(float(each[0])), text=megamessage,parse_mode='HTML')
						else:
							bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. Please report this so our trained monkeys can fix it!""",parse_mode='Markdown')
					else:
						traceback.print_exc()
						bot.sendMessage(chat_id=update.message.chat_id, text="""HTTP 418: I'm a teapot""",parse_mode='Markdown')
		except:
			traceback.print_exc()
			bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. Please report this so our trained monkeys can fix it!""",parse_mode='Markdown')
	def supported (bot,update):
		supportsites = "Hi, these are the sites currently supported by Matilda \n"
		supportsites += "Please type /cmd for more information! \n"
		supportsites += "- Straits Times \n"
		supportsites += "- TodayOnline \n"
		supportsites += "- CNA \n"
		supportsites += "- Mothership"
		#"""Hi, these are the sites currently supported by Matilda \nPlease type /cmd for more information! \n- Straits Times \n- TodayOnline \n- CNA \n- Mothership"""
		bot.sendMessage(chat_id=update.message.chat_id, text=supportsites, parse_mode='Markdown')
	def commands (bot,update):
		commandstring = "Hi, this are the commands that I currently support \n"
		commandstring += "- /aboutme (about the bot) \n"
		commandstring += "- /cmd (command list) \n"
		commandstring += "- /st <article> (Straits Times Scraper) \n"
		commandstring += "- /today <article> (TodayOnline Scraper) \n"
		commandstring += "- /cna <article> (Channel News Asia Scraper) \n"
		commandstring += "- /laobu <article> (Mothership.sg Scraper) \n"
		commandstring += "- /laobu\_new (Returns Mothership's newest 5 articles) \n"
		commandstring += "- /laobu\_search <searchtext> (Searches for mothership articles)"

		bot.sendMessage(chat_id=update.message.chat_id, text=commandstring, parse_mode='Markdown')
	def aboutme(bot,update):
		bot.sendMessage(chat_id=update.message.chat_id, text="Hi, I was created by my user, @fatalityx to learn more about Python, as well as scrape news articles from websites")

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
								if (result.status_code >= 400):
									bot.sendMessage(chat_id=update.message.chat_id, text="""This story does not exist!""",parse_mode='Markdown')
								else:
									chatid = update.message.chat.id
									chattype = update.message.chat.type
									cur.execute("""SELECT * FROM Userdb WHERE chatid = %s""",(chatid,))
									if cur.rowcount == 0:
										cur.execute("""INSERT INTO Userdb VALUES(%s,%s)""",(chatid,chattype,))
									cur.execute("""SELECT * FROM Retrievedmsg WHERE retrievedurl = %s""",(sturl,))
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
											bodyobject.append("*")
											bodyobject.append(title.text)
											bodyobject.append("*")
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
										bodyobject.append("_")
										bodyobject.extend(publishedobject)
										bodyobject.append("_")
										bodyobject.append("\n")
										bodyobject.append("_")
										bodyobject.extend(modifiedobject)
										bodyobject.append("_")
										bodyobject.append("\n")
										bodyobject.append("\n")
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
													parastring = escape_markdown(para.text)
													bodyobject.append(parastring)
													bodyobject.append("\n")
													bodyobject.append("\n")
										str1 = ''.join(bodyobject)
										result = 0
										for char in str1:
											result +=1
										try:
											if (result) > 4096:
												n = 4000
												checklist=["false"]
												while "false" in checklist:
													del checklist[:]
													n = n-1
													msglist = [str1[i:i+n] for i in range(0, len(str1), n)]
													for msg in msglist:
														lastchar = (msg.strip()[-1])
														if msg[-1] not in string.whitespace:
															checklist.append("false")
														else:
															checklist.append("true")
												msglist = [str1[i:i+n] for i in range(0, len(str1), n)]
												for msg in msglist:
													cur.execute("""INSERT INTO Retrievedmsg VALUES(NULL,%s,%s)""",(sturl,msg,))
											else:
												cur.execute("""INSERT INTO Retrievedmsg VALUES(NULL,%s,%s)""",(sturl,str1,))
										except:
											traceback.print_exc()
											bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. Please report this so our trained monkeys can fix it!""",parse_mode='Markdown')
										cur.execute("""SELECT retrievedtext,retrievedid FROM Retrievedmsg WHERE retrievedurl=%s limit 1""",(sturl,))
										if cur.rowcount > 0:
											data = cur.fetchone()
											retrievedmsg = data[0]
											spliceretrievedmsg = retrievedmsg[:500]
											dbid = "db-"+str(data[1])
											keyboard = []
											keyboard.append([InlineKeyboardButton("Read more", callback_data=dbid)])
											reply_markup = InlineKeyboardMarkup(keyboard)
											update.message.reply_text(spliceretrievedmsg, reply_markup=reply_markup,parse_mode='Markdown')
									else:
										cur.execute("""SELECT retrievedtext,retrievedid FROM Retrievedmsg WHERE retrievedurl=%s limit 1""",(sturl,))
										if cur.rowcount > 0:
											data = cur.fetchone()
											retrievedmsg = data[0]
											spliceretrievedmsg = retrievedmsg[:500]
											dbid = "db-"+str(data[1])
											keyboard = []
											keyboard.append([InlineKeyboardButton("Read more", callback_data=dbid)])
											reply_markup = InlineKeyboardMarkup(keyboard)
											update.message.reply_text(spliceretrievedmsg, reply_markup=reply_markup,parse_mode='Markdown')
							except:
								traceback.print_exc()
								bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. Please report this so our trained monkeys can fix it!""",parse_mode='Markdown')
		
					except:
						traceback.print_exc()
						bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. Please report this so our trained monkeys can fix it!""",parse_mode='Markdown')
		except:
			traceback.print_exc()
			bot.sendMessage(chat_id=update.message.chat_id, text="""Something has gone wrong. Please report this so our trained monkeys can fix it!""",parse_mode='Markdown')

	'''
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
									cur.execute("""SELECT * FROM Userdb WHERE chatid = %s""",(chatid,))
									if cur.rowcount == 0:
										cur.execute("""INSERT INTO Userdb VALUES(%s)""",(chatid,))
									cur.execute("""SELECT * FROM Retrievedmsg WHERE retrievedurl = %s""",(todayurl,))
									if cur.rowcount == 0:
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
										if len(dateval) > 0:
											for date in dateval:
												dt = parser.parse(date.text)
												dateobj.append(dt)
										if not dateobj:
											pubdate = "No published date avaliable"
										else:
											if len(dateobj) > 1:
												pubdate = min(dateobj)
												moddate = max(dateobj)
											else:
												pubdate = min(dateobj)
										for title in titlediv:
											articletitle = title['content']
											bodyobject.append("*")
											bodyobject.append(articletitle)
											bodyobject.append("*")
											bodyobject.append("\n")
											bodyobject.append("\n")
										for postdate in publishdiv:
											datelbl = postdate.findAll("span", {"class" : "date-label"})
											for lbl in datelbl:
												print(lbl.text)
												if "Published:" in lbl.text:
													publishedobject.append('Published at: ')
													publishedobject.append(pubdate.strftime("%B %d, %Y %H:%M"))
												else:
													modifiedobject.append('Updated at: ')
													modifiedobject.append(moddate.strftime("%B %d, %Y %H:%M"))
										bodyobject.append("_")
										bodyobject.extend(publishedobject)
										bodyobject.append("_")
										bodyobject.append("\n")
										bodyobject.append("_")
										bodyobject.extend(modifiedobject)
										bodyobject.append("_")
										bodyobject.append("\n")
										bodyobject.append("\n")
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
											if (result) > 4096:
												n = 4000
												checklist=["false"]
												while "false" in checklist:
													del checklist[:]
													n = n-1
													msglist = [str1[i:i+n] for i in range(0, len(str1), n)]
													for msg in msglist:
														lastchar = (msg.strip()[-1])
														if msg[-1] not in string.whitespace:
															checklist.append("false")
														else:
															checklist.append("true")
												msglist = [str1[i:i+n] for i in range(0, len(str1), n)]
												for msg in msglist:
													cur.execute("""INSERT INTO Retrievedmsg VALUES(NULL,%s,%s)""",(todayurl,msg,))
											else:
												cur.execute("""INSERT INTO Retrievedmsg VALUES(NULL,%s,%s)""",(todayurl,str1,))
										except Exception as e: print(e)
										cur.execute("""SELECT retrievedtext,retrievedid FROM Retrievedmsg WHERE retrievedurl=%s limit 1""",(todayurl,))
										if cur.rowcount > 0:
											data = cur.fetchone()
											retrievedmsg = data[0]
											spliceretrievedmsg = retrievedmsg[:500]
											dbid = "db-"+str(data[1])
											keyboard = []
											keyboard.append([InlineKeyboardButton("Read more", callback_data=dbid)])
											reply_markup = InlineKeyboardMarkup(keyboard)
											update.message.reply_text(spliceretrievedmsg, reply_markup=reply_markup,parse_mode='Markdown')
									else:
										cur.execute("""SELECT retrievedtext,retrievedid FROM Retrievedmsg WHERE retrievedurl=%s limit 1""",(todayurl,))
										if cur.rowcount > 0:
											data = cur.fetchone()
											retrievedmsg = data[0]
											spliceretrievedmsg = retrievedmsg[:500]
											dbid = "db-"+str(data[1])
											keyboard = []
											keyboard.append([InlineKeyboardButton("Read more", callback_data=dbid)])
											reply_markup = InlineKeyboardMarkup(keyboard)
											update.message.reply_text(spliceretrievedmsg, reply_markup=reply_markup,parse_mode='Markdown')
							except Exception as e: print(e)
					except Exception as e: print(e)
		except Exception as e: print(e)
	'''
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
										cur.execute("""INSERT INTO Userdb VALUES(%s,%s)""",(chatid,chattype,))
									cur.execute("""SELECT * FROM Retrievedmsg WHERE retrievedurl = %s""",(cnaurl,))
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
											bodyobject.append("*")
											bodyobject.append(title.text)
											bodyobject.append("*")
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
										bodyobject.append("_")
										bodyobject.extend(publishedobject)
										bodyobject.append("_")
										bodyobject.append("\n")
										bodyobject.append("_")
										bodyobject.extend(modifiedobject)
										bodyobject.append("_")
										bodyobject.append("\n")
										bodyobject.append("\n")
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
													if para.text.strip() is not "":
														parastring = escape_markdown(para.text)
														#strip1 = parastring.replace("*","")
														#strip2 = strip1.replace("_","")
														#strip3 = strip2.replace("`","")
														bodyobject.append(parastring)
														bodyobject.append("\n")
														bodyobject.append("\n")
										str1 = ''.join(bodyobject)
										result = 0
										for char in str1:
											result +=1
										try:
											if (result) > 4096:
												n = 4000
												checklist=["false"]
												while "false" in checklist:
													del checklist[:]
													n = n-1
													msglist = [str1[i:i+n] for i in range(0, len(str1), n)]
													for msg in msglist:
														lastchar = (msg.strip()[-1])
														if msg[-1] not in string.whitespace:
															checklist.append("false")
														else:
															checklist.append("true")	
												msglist = [str1[i:i+n] for i in range(0, len(str1), n)]
												for msg in msglist:
													cur.execute("""INSERT INTO Retrievedmsg VALUES(NULL,%s,%s)""",(cnaurl,msg,))
											else:
												cur.execute("""INSERT INTO Retrievedmsg VALUES(NULL,%s,%s)""",(cnaurl,str1,))
										except Exception as e: print(e)
										cur.execute("""SELECT retrievedtext,retrievedid FROM Retrievedmsg WHERE retrievedurl=%s limit 1""",(cnaurl,))
										if cur.rowcount > 0:
											data = cur.fetchone()
											retrievedmsg = data[0]
											spliceretrievedmsg = retrievedmsg[:500]
											dbid = "db-"+str(data[1])
											keyboard = []
											keyboard.append([InlineKeyboardButton("Read more", callback_data=dbid)])
											reply_markup = InlineKeyboardMarkup(keyboard)
											update.message.reply_text(spliceretrievedmsg, reply_markup=reply_markup,parse_mode='Markdown')
									else:
										cur.execute("""SELECT retrievedtext,retrievedid FROM Retrievedmsg WHERE retrievedurl=%s limit 1""",(cnaurl,))
										if cur.rowcount > 0:
											data = cur.fetchone()
											retrievedmsg = data[0]
											spliceretrievedmsg = retrievedmsg[:500]
											dbid = "db-"+str(data[1])
											keyboard = []
											keyboard.append([InlineKeyboardButton("Read more", callback_data=dbid)])
											reply_markup = InlineKeyboardMarkup(keyboard)
											update.message.reply_text(spliceretrievedmsg, reply_markup=reply_markup,parse_mode='Markdown')
							except Exception as e: print(e)
					except Exception as e: print(e)
		except Exception as e: print(e)
	'''def laobu(bot, update):

		try:

			url=update.message.text
			msurl = url[7:]
			checkmsurl = msurl[:22]
			if checkmsurl != "https://mothership.sg/":
				bot.sendMessage(chat_id=update.message.chat_id, text="""Please enter a valid url. For example, https://mothership.sg/<article>""",parse_mode='Markdown')

			else:
				try:
					headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
					result = requests.get(msurl,headers=headers)
					print(result.status_code)
					if (result.status_code >= 400):
						bot.sendMessage(chat_id=update.message.chat_id, text="""This story does not exist!""",parse_mode='Markdown')
					else:
						headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
						r = requests.get(msurl, headers=headers)
						c = r.content
						soup = BeautifulSoup(c,"html.parser")
						mydivs = soup.findAll("div", { "class" : "content-article-wrap" })
						subtitlediv = soup.findAll("div", { "class" : "article original" })
						titlediv = soup.findAll("meta", {"property" : "og:title"})
						bodyobject = []
						publishedobject = []
						modifiedobject = []
						for title in titlediv:
							bodyobject.append("*")
							bodyobject.append(title['content'])
							bodyobject.append("*")
							bodyobject.append("\n")
						for sub in subtitlediv:
							header = sub.findAll('div',{"class":"header"})
							bar= sub.findAll('div',{"class":"side-bar"})
							for side in bar:
								side.decompose()
							adv = sub.findAll('div',{"class":"related-stories"})
							for ad in adv:
								ad.decompose()
							rel = sub.findAll('div',{"class":"related-articles"})
							for re in rel:
								re.decompose()
							for p in header:
								pclass = p.findAll('p',{"class":"subtitle"})
								for pc in pclass:
									bodyobject.append(pc.text)
									bodyobject.append("\n")
									bodyobject.append("\n")
							for date in header:
								dclass = date.findAll('span',{"class":"publish-date"})
								for d in dclass:
									publishedobject.append("Published: ")
									publishedobject.append(d.text)
						bodyobject.append("_")
						bodyobject.extend(publishedobject)
						bodyobject.append("_")
						bodyobject.append("\n")
						bodyobject.append("\n")
						for div in mydivs:
							adv = div.findAll('div')
							for ad in adv:
								ad.decompose()
							fig = div.findAll('figure')
							for f in fig:
								f.decompose()
							h3 = div.findAll('h3')
							if len(h3) > 0:
								for each in h3:
									text = each.text
									replacement = "*"+text+"*"
									div.h3.replace_with(replacement)
							h4 = div.findAll('h4')
							if len(h4) > 0:
								for each in h4:
									text = each.text
									replacement = "*"+text+"*"
									div.h4.replace_with(replacement)
							h5 = div.findAll('h5')
							if len(h5) > 0:
								for each in h5:
									text = each.text
									replacement = "*"+text+"*"
									div.h5.replace_with(replacement)
							h1 = div.findAll('h1')
							if len(h1) > 0:
								for each in h1:
									text = each.text
									replacement = "*"+text+"*"
									div.h1.replace_with(replacement)
							h2 = div.findAll('h2')
							if len(h2) > 0:
								for each in h2:
									text = each.text
									replacement = "*"+text+"*"
									div.h2.replace_with(replacement)
							text = div.text
							striptext = text.strip()
							if striptext != "":
								bodyobject.append(div.text)
								bodyobject.append("\n")
								bodyobject.append("\n")
						str1 = ''.join(bodyobject)
						result = 0
						for char in str1:
							result +=1
						
						if (result) > 4096:
							n = 4000
							checklist=["false"]
							while "false" in checklist:
								del checklist[:]
								n = n-1
								msglist = [str1[i:i+n] for i in range(0, len(str1), n)]
								for msg in msglist:
									lastchar = (msg.strip()[-1])
									if msg[-1] not in string.whitespace:
										checklist.append("false")
									else:
										checklist.append("true")
							msglist = [str1[i:i+n] for i in range(0, len(str1), n)]
							for msg in msglist:
								bot.sendMessage(chat_id=update.message.chat_id, text=msg, parse_mode='Markdown')
						else:
							bot.sendMessage(chat_id=update.message.chat_id, text=str1, parse_mode= 'Markdown')
				except:
					headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
					result = requests.get(msurl,headers=headers)
					print(result.status_code)
					if (result.status_code >= 400):
						bot.sendMessage(chat_id=update.message.chat_id, text="""This story does not exist!""",parse_mode='Markdown')
					else:
						headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
						r = requests.get(msurl, headers=headers)
						c = r.content
						soup = BeautifulSoup(c,"html.parser")
						mydivs = soup.findAll("div", { "class" : "content-article-wrap" })
						subtitlediv = soup.findAll("div", { "class" : "article original" })
						titlediv = soup.findAll("meta", {"property" : "og:title"})
						bodyobject = []
						publishedobject = []
						modifiedobject = []
						for title in titlediv:
							bodyobject.append("*")
							bodyobject.append(title['content'])
							bodyobject.append("*")
							bodyobject.append("\n")
						for sub in subtitlediv:
							header = sub.findAll('div',{"class":"header"})
							bar= sub.findAll('div',{"class":"side-bar"})
							for side in bar:
								side.decompose()
							adv = sub.findAll('div',{"class":"related-stories"})
							for ad in adv:
								ad.decompose()
							rel = sub.findAll('div',{"class":"related-articles"})
							for re in rel:
								re.decompose()
							for p in header:
								pclass = p.findAll('p',{"class":"subtitle"})
								for pc in pclass:
									bodyobject.append(pc.text)
									bodyobject.append("\n")
									bodyobject.append("\n")
							for date in header:
								dclass = date.findAll('span',{"class":"publish-date"})
								for d in dclass:
									publishedobject.append("Published: ")
									publishedobject.append(d.text)
						bodyobject.append("_")
						bodyobject.extend(publishedobject)
						bodyobject.append("_")
						bodyobject.append("\n")
						bodyobject.append("\n")
						for div in mydivs:
							adv = div.findAll('div')
							for ad in adv:
								ad.decompose()
							fig = div.findAll('figure')
							for f in fig:
								f.decompose()
							htmltext = str(div)
							newhtmltext = htmltext[33:]
							h = html2text.HTML2Text()
							h.ignore_links = True
							handledtext = h.handle(newhtmltext)
							h3 = div.findAll('h3')
							if len(h3) > 0:
								for each in h3:
									text = each.text
									replacement = "*"+text+"*"
									print(replacement)
									div.h3.replace_with(replacement)
							h4 = div.findAll('h4')
							if len(h4) > 0:
								for each in h4:
									text = each.text
									replacement = "*"+text+"*"
									print(replacement)
									div.h4.replace_with(replacement)
							h5 = div.findAll('h5')
							if len(h5) > 0:
								for each in h5:
									text = each.text
									replacement = "*"+text+"*"
									print(replacement)
									div.h5.replace_with(replacement)
							h1 = div.findAll('h1')
							if len(h1) > 0:
								for each in h1:
									text = each.text
									replacement = "*"+text+"*"
									print(replacement)
									div.h1.replace_with(replacement)
							h2 = div.findAll('h2')
							if len(h2) > 0:
								for each in h2:
									text = each.text
									replacement = "*"+text+"*"
									print(replacement)
									div.h2.replace_with(replacement)
							bodyobject.append(escape_markdown(div.text))
							bodyobject.append("\n")
							bodyobject.append("\n")
						str1 = ''.join(bodyobject)
						result = 0
						for char in str1:
							result +=1
						
						if (result) > 4096:
							n = 4000
							checklist=["false"]
							while "false" in checklist:
								del checklist[:]
								n = n-1
								msglist = [str1[i:i+n] for i in range(0, len(str1), n)]
								for msg in msglist:
									lastchar = (msg.strip()[-1])
									if msg[-1] not in string.whitespace:
										checklist.append("false")
									else:
										checklist.append("true")
							msglist = [str1[i:i+n] for i in range(0, len(str1), n)]
							for msg in msglist:
								bot.sendMessage(chat_id=update.message.chat_id, text=msg, parse_mode='Markdown')
						else:
							bot.sendMessage(chat_id=update.message.chat_id, text=str1, parse_mode= 'Markdown')
		except Exception as e: print(e)

	def laobusearch(bot,update):
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					try:
						searchtext = update.message.text
						if len(searchtext[14:]) < 5:
							bot.sendMessage(chat_id=update.message.chat_id, text="""Please enter a longer search query!""",parse_mode='Markdown')
						else:
							newsearch = searchtext[14:]
							qsearch = "%"+newsearch+"%"
							cur.execute("""SELECT * 
											FROM `Mothership` 
											WHERE LOWER(ms_title) LIKE LOWER(%s)
											ORDER BY ms_time 
											DESC LIMIT 5""",(qsearch,))
							data = cur.fetchall()
							if cur.rowcount > 0:
								counter = 1
								keyboard = []
								replystring = "These are the latest 5 stories based on your search terms\n For more stories, please refine your search terms\n"
								for row in data:
									ms_id = "ms-"+str(row[0])
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
					except Exception as e: print(e)
		except Exception as e: print(e)
	def laobunew(bot,update):
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					try:
						cur.execute("""SELECT * FROM `Mothership` 
										ORDER BY `ms_time` 
										DESC LIMIT 5""")
						data = cur.fetchall()
						if cur.rowcount > 0:
							counter = 1
							keyboard = []
							replystring = "These are the latest 5 stories\n"
							for row in data:
								ms_id = "ms-"+str(row[0])
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
					except Exception as e: print(e)
		except Exception as e: print(e)
	'''
	def stnew(bot,update):
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					try:
						cur.execute("""SELECT * FROM `StraitsTimes` 
						ORDER BY `st_time` 
						DESC LIMIT 5""")
						data = cur.fetchall()
						if cur.rowcount > 0:
							counter = 1
							keyboard = []
							replystring = "These are the latest 5 stories\n"
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
					except Exception as e: print(e)
		except Exception as e: print(e)
	def stsearch(bot,update):
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					try:
						searchtext = update.message.text
						if len(searchtext[14:]) < 5:
							bot.sendMessage(chat_id=update.message.chat_id, text="""Please enter a longer search query!""",parse_mode='Markdown')
						else:
							newsearch = searchtext[14:]
							qsearch = "%"+newsearch+"%"
							cur.execute("""SELECT * 
											FROM `StraitsTimes` 
											WHERE LOWER(st_title) LIKE LOWER(%s)
											ORDER BY st_time 
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
					except Exception as e: print(e)
		except Exception as e: print(e)
	def cnanew(bot,update):
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					try:
						cur.execute("""SELECT * FROM `ChannelNewsAsia` 
						ORDER BY `cna_dt` 
						DESC LIMIT 5""")
						data = cur.fetchall()
						if cur.rowcount > 0:
							counter = 1
							keyboard = []
							replystring = "These are the latest 5 stories\n"
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
					except Exception as e: print(e)
		except Exception as e: print(e)
	def cnasearch(bot,update):
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					try:
						searchtext = update.message.text
						if len(searchtext[14:]) < 5:
							bot.sendMessage(chat_id=update.message.chat_id, text="""Please enter a longer search query!""",parse_mode='Markdown')
						else:
							newsearch = searchtext[14:]
							qsearch = "%"+newsearch+"%"
							cur.execute("""SELECT * 
											FROM `ChannelNewsAsia` 
											WHERE LOWER(cna_title) LIKE LOWER(%s)
											ORDER BY cna_dt 
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
					except Exception as e: print(e)
		except Exception as e: print(e)
	def search(bot,update):
		try:
			with closing(pymysql.connect(SQL.sqlinfo('host'),SQL.sqlinfo('usn'),SQL.sqlinfo('pw'),SQL.sqlinfo('db'),charset='utf8')) as conn:
				conn.autocommit(True)
				with closing(conn.cursor()) as cur:
					query = update.callback_query
					dbtype = query.data[:2]
					if dbtype == "ms":
						artid = query.data[3:]
						cur.execute("""SELECT ms_url
									FROM `Mothership`
									WHERE ms_id = %s""",(artid))
						data = cur.fetchone()
						if cur.rowcount > 0:
							arturl = data[0]
							fullurl = "/laobu "+arturl
							query.message.text = fullurl
							Commands.laobu(bot,query)
						else:
							bot.sendMessage(chat_id=query.message.chat_id, text="""Oops, something went wrong :(""",parse_mode='Markdown')
					elif dbtype == "st":
						artid = query.data[3:]
						cur.execute("""SELECT st_link
									FROM `StraitsTimes`
									WHERE st_id = %s""",(artid))
						data = cur.fetchone()
						if cur.rowcount > 0:
							arturl = data[0]
							print(arturl)
							fullurl = "/st "+arturl
							query.message.text = fullurl
							Commands.straitstimes(bot,query)
						else:
							bot.sendMessage(chat_id=query.message.chat_id, text="""Oops, something went wrong :(""",parse_mode='Markdown')
					elif dbtype == "cn":
						artid = query.data[3:]
						cur.execute("""SELECT cna_link
									FROM `ChannelNewsAsia`
									WHERE cna_id = %s""",(artid))
						data = cur.fetchone()
						if cur.rowcount > 0:
							arturl = data[0]
							print(arturl)
							fullurl = "/cna "+arturl
							query.message.text = fullurl
							Commands.cna(bot,query)
						else:
							bot.sendMessage(chat_id=query.message.chat_id, text="""Oops, something went wrong :(""",parse_mode='Markdown')
					elif dbtype == "db": #named db because you're pulling out of db
						multiid = query.message.message_id
						chatid = query.message.chat.id
						cur.execute("""SELECT multiid FROM multiplemsg WHERE multiid = %s AND chatid = %s""",(multiid,chatid,))
						if cur.rowcount == 0:
							artid = query.data[3:]
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
									keyboard.append([InlineKeyboardButton('Show less ↑', callback_data=hideid)])
									reply_markup = InlineKeyboardMarkup(keyboard)
									bot.edit_message_text(text=text,chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=reply_markup,parse_mode='Markdown')
								else:
									data = cur.fetchall()
									counter = 0
									for each in data:
										if counter == 0:
											hideid = 'hd-'+ str(each[0])
											text = each[2]
											keyboard = []
											keyboard.append([InlineKeyboardButton('Show less ↑', callback_data=hideid)])
											reply_markup = InlineKeyboardMarkup(keyboard)
											bot.edit_message_text(text=text,chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=reply_markup,parse_mode='Markdown')
											cur.execute("""INSERT INTO multiplemsg VALUES(%s,%s,%s)""",(multiid,each[0],chatid))
											counter+=1
										else:
											hideid = 'hd-'+ str(each[0])
											text = each[2]
											keyboard = []
											keyboard.append([InlineKeyboardButton('Show less ↑', callback_data=hideid)])
											reply_markup = InlineKeyboardMarkup(keyboard)
											sent = bot.sendMessage(chat_id=query.message.chat_id, text=text,reply_markup=reply_markup,parse_mode='Markdown')
											cur.execute("""INSERT INTO multiplemsg VALUES(%s,%s,%s)""",(sent.message_id,each[0],chatid))
						else:
							cur.execute("""SELECT b.retrievedtext FROM multiplemsg a left join Retrievedmsg b on a.retrievedid = b.retrievedid where a.multiid =  %s""",(multiid,))
							data = cur.fetchone()
							text = data[0]
							artid = query.data[3:]
							hideid = 'hd-'+artid
							keyboard = []
							keyboard.append([InlineKeyboardButton('Show less ↑', callback_data=hideid)])
							reply_markup = InlineKeyboardMarkup(keyboard)
							bot.edit_message_text(text=text,chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=reply_markup,parse_mode='Markdown')
					elif dbtype == "hd": #named hd because you're hiding msg
						artid = query.data[3:]
						cur.execute("""SELECT retrievedtext FROM Retrievedmsg WHERE retrievedid = %s""",(artid,))
						if cur.rowcount > 0:
							data = cur.fetchone()
							text = data[0]
							hiddentext = text[:500]
							showid = 'db-'+artid
							keyboard = []
							keyboard.append([InlineKeyboardButton('Show more ↓', callback_data=showid)])
							reply_markup = InlineKeyboardMarkup(keyboard)
							bot.edit_message_text(text=hiddentext,chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=reply_markup,parse_mode='Markdown')

		except Exception as e: print(e)

