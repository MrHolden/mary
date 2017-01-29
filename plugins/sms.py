# Import smtplib for the actual sending function
import smtplib

# Pull cloudbot's hook lib
from cloudbot import hook
from cloudbot.event import EventType

# Import the email modules we'll need
from email.mime.text import MIMEText


@hook.command("sms")
def send_sms(text, conn, nick, notice):
	"""<user> <msg> - send SMS message <msg> to phone number of <user>"""

	# Create a text/plain message
	me = '{}@bluntcave.com'.format(nick)
	msg = text.split(' ', 1)
	person = msg[0].strip()
	body = msg[1].strip()
	if person.lower() == "buddha":
		number = ["5128155940@txt.att.net"]
	elif person.lower() == "laz":
		number = ["2038930077@vtext.com"]
	elif (person.lower() == "alex") or (person.lower() == "cali"):
		number = ["5035392924@txt.att.net"]
	elif (person.lower() == "sag") or (person.lower() == "kenny"):
		number = ["5099411214@vmobl.com"]
	if number:
		s = smtplib.SMTP('localhost')
		s.sendmail(me, [number], body)
		s.quit()
		notice("Text message sent to \x02{}\x02 from {}: {}".format(person, me, body))
	else: 
		notice("User {} not known.".format(person))
