import random
import re
import operator

from time import time
from collections import defaultdict
from sqlalchemy import Table, Column, String, Integer, PrimaryKeyConstraint, desc
from sqlalchemy.sql import select
from cloudbot import hook
from cloudbot.event import EventType
from cloudbot.util import botvars

#declare some constants
ghostbot = "Ghostbot"
bluntcave = "#smoke"
b_re = re.compile(r'^Go, ([\w \d]+) .*Spark it up!!!! Total (.*)', re.UNICODE)

userstats = Table(
    'userstats',
    botvars.metadata,
    Column('name', String),
    Column('bongs', Integer),
    Column('words', Integer),
    Column('lines', Integer),
    Column('actions', Integer),
    Column('upvotes', Integer),
    Column('downvotes', Integer),
    Column('coinswon', Integer),
    PrimaryKeyConstraint('name')
    )

chanstats = Table(
    'chanstats',
    botvars.metadata,
    Column('chan', String),
    Column('smokers', Integer),
    Column('bongs', Integer),
    Column('words', Integer),
    Column('lines', Integer),
    Column('actions', Integer),
    Column('upvotes', Integer),
    Column('downvotes', Integer),
    Column('biggest_b', Integer)
    )

@hook.on_start()
def load_chan_db(db):
    global total_bongs
    total_bongs = 0
    get_bongs(db)

def update_total_b(db, total):
    """update total chan bongs"""
    exists = db.execute(select([chanstats.c.bongs]) \
        .where(chanstats.c.chan == bluntcave)).fetchone()
    query = chanstats.update() \
        .values(bongs = total)
    db.execute(query)
    db.commit()
    global total_bongs
    total_bongs = total

def get_bongs(db):
    """get total bongs and assign to global variable"""
    exists = db.execute(select([chanstats.c.bongs]) \
        .where(chanstats.c.chan == bluntcave)).fetchone()
    global total_bongs
    if exists:
        total_bongs = exists["bongs"]    

def add_user_b(db, user, b):
    """updates a single user's bong count"""
    exists = db.execute(select([userstats.c.name, userstats.c.bongs]) \
        .where(userstats.c.name == user)).fetchone()
    if exists:
        query = userstats.update() \
            .where(userstats.c.name == user) \
            .values(bongs = b)
    else:
        query = userstats.insert().values(
            name = user,
            bongs = b)
    db.execute(query)
    db.commit()

def add_user_line(db, user, line, word, up, down, action):
    """add a user line to userstats db"""
    exists = db.execute(select([userstats.c.name, userstats.c.words, userstats.c.lines, userstats.c.actions, userstats.c.upvotes, userstats.c.downvotes]) \
        .where(userstats.c.name == user)).fetchone()
    if exists:
        query = userstats.update() \
            .where(userstats.c.name == user) \
            .values(words = exists["words"] + word) \
            .values(lines = exists["lines"] + line) \
            .values(upvotes = exists["upvotes"] + up) \
            .values(downvotes = exists["downvotes"] + down) \
            .values(actions = exists["actions"] + action)
    else:
        query = userstats.insert().values(
            name = user,
            words = word,
            lines = line,
            actions = action,
            downvotes = down,
            upvotes = up)
    db.execute(query)
    db.commit()

def add_chan_line(db, line, word, up, down, action):
    """add a line of stats to channel db"""
    exists = db.execute(select([chanstats.c.chan, chanstats.c.words, chanstats.c.lines, chanstats.c.actions, chanstats.c.upvotes, chanstats.c.downvotes]) \
        .where(chanstats.c.chan == bluntcave)).fetchone()
    if exists:
        query = chanstats.update() \
            .where(chanstats.c.chan == bluntcave) \
            .values(words = exists["words"] + word) \
            .values(lines = exists["lines"] + line) \
            .values(actions = exists["actions"] + action) \
            .values(upvotes = exists["upvotes"] + up) \
            .values(downvotes = exists["downvotes"] + down)
    else:
        query = chanstats.insert().values(
            chan = bluntcave,
            words = word,
            lines = line,
            actions = action,
            upvotes = up,
            downvotes = down)
    db.execute(query)
    db.commit()  

@hook.command("stats", "s", autohelp=False, singlethread=True)
def get_userstats(text, nick, db, notice):
    """return user stats"""
    name = nick
    words, lines, upvotes, downvotes, bongs, actions = 0, 0, 0, 0, 0, 0
    if text:
        name = text.split()[0]
    exists = db.execute(select([userstats.c.name, userstats.c.bongs, userstats.c.words, userstats.c.lines, userstats.c.actions, userstats.c.upvotes, userstats.c.downvotes]) \
        .where(userstats.c.name == name)).fetchone()
    if exists:
        words = exists["words"]
        lines = exists["lines"]
        upvotes = exists["upvotes"]
        downvotes = exists["downvotes"]
        actions = exists["actions"]
        bongs = exists["bongs"]
        wordsperline = "{:.2f}".format(words/lines)
        out = "User Stats for \x02{}: Words:\x02 {}, \x02Lines:\x02 {}, \x02Words Per Line:\x02 {}".format(name, words, lines, wordsperline)
        if actions:
            out += ", \x02Actions:\x02 {}".format(actions)
        if upvotes:
            out += ", \x02Upvotes:\x02 {}".format(upvotes)
        if downvotes:
            out += ", \x02Downvotes:\x02 {}".format(downvotes)
        if bongs:
            out += ", \x02Bongs:\x02 {}".format(bongs)
        get_bongs(db)
        if (total_bongs > 0):
            bongparticipation = "{:.1f}%".format((bongs/total_bongs)*100)
            out += ", \x02Bong Participation:\x02 {}".format(bongparticipation)
        notice(out)
    else:
        notice("Cannot find stats for \x02{}\x02.".format(name))

@hook.command("cstats", "cs", autohelp=False, singlethread=True)
def get_chanstats(db, notice):
    """return channel stats"""
    words, lines, upvotes, downvotes, bongs, actions, smokers = 0, 0, 0, 0, 0, 0, 0
    exists = db.execute(select([chanstats.c.chan, chanstats.c.bongs, chanstats.c.words, chanstats.c.lines, chanstats.c.actions, chanstats.c.upvotes, chanstats.c.downvotes]) \
        .where(chanstats.c.chan == bluntcave)).fetchone()
    if exists:
        words = exists["words"]
        lines = exists["lines"]
        upvotes = exists["upvotes"]
        downvotes = exists["downvotes"]
        actions = exists["actions"]
        bongs = exists["bongs"]
        wordsperline = "{:.2f}".format(words/lines)
        out = "Channel Stats for \x02{}: Words\x02 {}, \x02Lines:\x02 {}, \x02Words Per Line:\x02 {}".format(bluntcave, words, lines, wordsperline)
        if actions:
            out += ", \x02Actions:\x02 {}".format(actions)
        if upvotes:
            out += ", \x02Upvotes:\x02 {}".format(upvotes)
        if downvotes:
            out += ", \x02Downvotes:\x02 {}".format(downvotes)
        if bongs:
            out += ", \x02Bongs:\x02 {}".format(bongs)
    else:
        out = "Cannot find stats for {}.".format(bluntcave)
    notice(out)


@hook.regex(b_re)
def parse_smokers(match, nick, notice, db, message):
    """parses b text for statkeeping"""
    users = match.group(1).split()
    result = match.group(2).split()
    total = result[2].replace('\\x02','').replace('\\x03','')
    i = 0
    c = ""
    while i < len(users):
        user = users[i]
        b_s = users[i+1]
        if ((int(b_s) % 100) == 0):
            c += "{} has {} b's! ".format(user,b_s)
        add_user_b(db, user, b_s)
        i += 2
    # update_total_b(db, total)
    if (len(c) >= 1):
        c = "\x02Yay!\x02 {}".format(c)
        message(c)

@hook.event([EventType.message, EventType.action], singlethread=True)
def parse_chatline(event, chan, nick, notice, db):
    """parse user chat into words, lines, etc"""
    downvotes, upvotes, words, lines, actions = 0, 0, 0, 0, 0
    text = event.content
    if "++" in text:
        upvotes += 1
    elif "--" in text:
        downvotes += 1
    words += len(text.split())
    lines += 1
    if event.type is EventType.action:
        actions += 1
    add_user_line(db, nick, lines, words, upvotes, downvotes, actions)
    add_chan_line(db, lines, words, upvotes, downvotes, actions)


@hook.command("addbongs", singlethread=True)
def add_bongs_manually(text, db, notice):
    """manually add total bong count to channel db"""
    total = text.split()[0]
    update_total_b(db, total)
    notice("Updated total bong count to {}".format(total))


@hook.command("saybongs", autohelp=False)
def say_bongs_manually(db, notice):
    """manually say total_bongs value"""
    notice(str(total_bongs))
