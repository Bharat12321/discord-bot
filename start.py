import os
import bot
import settings
from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from threading import Thread

thread = Thread(target=bot.run)
thread.start()

app = Flask(__name__)

@app.route('/')
def hello_world():
	DISCORD_SERVER = settings.DISCORD_SERVER
	return '<b>Bot is running in the background <b> <br>\
		you can play with it from discord app by joining my server <br>\
		<a href="'+str(DISCORD_SERVER)+'">'+str(DISCORD_SERVER)+'</a> <br> \
		below are some commands you can actually use <br> \
		hi, <br>\
		!google games: for searching links, <br>\
		!recent games: for searching recent matched searches <br>\
		Hope you enjoy the bot.<b>'

if __name__ == '__main__': 
	app.run() 

