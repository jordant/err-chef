#!/usr/bin/env python
from jabberbot import JabberBot, botcmd
from chef import autoconfigure, Node, Search
import chef 
from time import time
import datetime

username = 'YOURUSERNAME@YOURSERVER.COM'
password = 'YOURPASSWORD'
resource = 'chef-xmpp-bot'
chatroom = 'YOURCHATROOM@conference.YOURDOMAIN.COM'
STALE_TIME = 60 * 30 # 30 minutes

class ChefXMPPBot(JabberBot):
        @botcmd
        def stale( self, mess, args):
                list = "Stale nodes for query : %s <br/>" % args
                for row in Search('node', args):
                        if row.object.attributes['ohai_time']:
                                ago = int(time() - row.object.attributes['ohai_time'])
                                pretty_ohai_time = datetime.datetime.fromtimestamp(int(row.object.attributes['ohai_time'])).strftime('%Y-%m-%d %H:%M:%S')
                                if ago >= STALE_TIME:
                                        list += "%s ran %s seconds ago ( %s ) <br/>" % (row.object.name, ago, pretty_ohai_time)
                return(list)

        @botcmd
        def search ( self, mess, args):
                list = "Search results for query : %s <br/>" % args
                list += "Name   Environment<br/>"
                for row in Search('node', args):
                        list += "%s     %s<br/>" % (row.object.name, row.object.chef_environment)
                return(list)



api = autoconfigure()
bot = ChefXMPPBot(username, password, res=resource, debug=True)
bot.muc_join_room(chatroom, "chefbot")
bot.serve_forever()
