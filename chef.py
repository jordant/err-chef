#!/usr/bin/env python
import chef
import datetime
from errbot import BotPlugin, botcmd
from time import time

STALE_TIME = 60 * 30 # 30 minutes

class Chef(BotPlugin):
        def pretty_time(self, time):
                return datetime.datetime.fromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S')

        def search_node (self ,args):
                api = chef.autoconfigure()
                if not args:
                        raise Exception("No Search Query")
                return chef.Search('node', args)

        @botcmd
        def search (self, mess, args):
                """ Search and return nodes """
                list = "Search results for query : %s\n" % args
                for row in self.search_node(args):
                       list += "%s\n" % row.object.name
                return(list)

        @botcmd
        def roles (self, mess, args):
                """ Search and return roles """
                api = chef.autoconfigure()
                roles = ''
                for row in chef.Search('role', 'name:*' + args + '*'):
                        roles += "%s\n" % row.object.name
                return(roles)

        @botcmd
        def stale(self, mess, args):
                """ Search for stale nodes """
                list = "Stale nodes for query : %s ( stale time %s seconds )\n" % (args, STALE_TIME)
                for row in self.search_node(args):
                        if row.object.attributes['ohai_time']:
                                ago = int(time() - row.object.attributes['ohai_time'])
                                pretty_ohai_time = self.pretty_time(row.object.attributes['ohai_time'])
                                if ago >= STALE_TIME:
                                        list += "%s ran %s seconds ago ( %s )\n" % (row.object.name, ago, pretty_ohai_time)
                return(list)

        @botcmd
        def dpkg (self, mess, args):
                """ Search installed pacakge versions via Chef API ( requires ohai-dpkg) """

                (search, package) = args.split()
                if not package:
                        raise Exception("No package")

                pacakges = ''
                for row in self.search_node(search):
                        if not row.object.attributes['dpkg']:
                                continue
                        if not row.object.attributes['dpkg'][package]:
                                continue
                        pacakges += "%s\t%s\n" % ( row.object.name , row.object.attributes['dpkg'][package]['version'] )

                return(pacakges)


