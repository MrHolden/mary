import re
import time

# Pull cloudbot's hook lib
from cloudbot import hook
from cloudbot.event import EventType
from random import randint

b_re = re.compile(r'.*b\?|.*rdy\?|.*nother\?|.*ready for a b\?')
bluntcave = "#smoke"
smile = ":)"
op = "!op"

@hook.on_start()
def toke_start():
    global opped_now
    opped_now = "no"

@hook.command("toke", autohelp=False)
def op_if_not_opped(message, chan):
    """command to force Mary to op"""
    global opped_now
    if (chan == bluntcave) and (opped_now == "no"):
        msg_chan_op(message)

def msg_chan_op(message):
    """messages chan saying '!op'"""
    time.sleep(5)
    message(op)

@hook.regex(b_re)
def join_the_b(match, message):
    """if regex matches, join the b"""
    global opped_now
    if (opped_now == "no"):
        b = randint(0,9)
        if (b < 3):
            msg_chan_op(message)

@hook.irc_raw("MODE", singlethread=True)
def check_op_mode(irc_raw, chan, message, conn):
    """follow chanmodes and update opped_now"""
    global opped_now
    result = irc_raw.split()
    me = conn.nick
    channel = result[2]
    mode = result[3]
    name = result[4]
    if (name == me) and (channel == bluntcave):
        if ("+o" in mode):
            opped_now = "yes"
        elif ("-o" in mode):
            opped_now = "no"
    
@hook.event(EventType.message, singlethread=True)
def its_my_turn(event, nick, message, conn):
    """if it's Mary's turn, start the b"""
    me = conn.nick
    global opped_now
    if (nick == "Ghostbot") and (opped_now == "yes"):
        if ("Mary's" in event.content):
            time.sleep(5)
            message("!smoke")
        elif ("Spark it up!!!!" in event.content):
            time.sleep(5)
            message(smile)
