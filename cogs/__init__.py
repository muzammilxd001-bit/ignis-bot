from __future__ import annotations
from core import Ignis




#____________ Commands ___________

from .commands.emoji import emojis
from .commands.embed import Embed
from .commands.invites import invites
from .commands.j2c import J2C
# from .commands.nsfw import nsfw
from .commands.Leveling import Leveling
# from .commands.encryption import encryption
from .commands.stats import Stats
from .commands.starboard import Starboard 
from .commands.mod import mod
from .commands.zestar import Zestar
from .commands.Autorole import AutoRole
from .commands.Giveaways import giveaway
from .commands.gwtask import gwtask
# from .commands.youtube import Youtube
from .commands.help import Help
from .commands.general import General
from .commands.music import Music
from .commands.moderation import Moderation
from .commands.vcroles import Voice
from .commands.anti import Antinuke
from .commands.extraown import Extraowner
from .commands.anti_wl import Whitelist
from .commands.anti_unwl import Unwhitelist
from .commands.emergency import Emergency
from .commands.nightmode import Nightmode
from .commands.automod import Automod
from .commands.welcome import Welcomer
from .commands.fun import Fun
from .commands.games import Games
from .commands.extra import Utility
from .commands.owner import Owner
from .commands.role import Server
from .commands.ignore import Ignore
from .commands.List import list
from .commands.serverinfo import Info
from .commands.GAfk import gafk
from .commands.afk import afk
from .commands.Verification import Verification
from .commands.Media import Media
from .commands.Logging import Logging
from .commands.owner1 import owner1
from .commands.Reminder import Reminder
from .commands.pfps import pfps
from .commands.joindm import joindm
from .commands.uptime import Uptime
from .commands.filter import MusicFilters
from .commands.nitro import Nitro
from .commands.boost import boost
from .commands.ticket import TicketCog
# from .commands.calc import calculator
from .commands.report import report
from .commands.profile import Profile
from .commands.vanityroles import Vanityroles
from .commands.notify import NotifCommands
# from .commands.marrige import Marriage
# from .commands.Birthday import Birthdays
from .commands.Blacklist import Blacklist
from .commands.MuteAll import MuteAll
from .commands.panic import PanicMode

#____________ Events _____________


from .events.join import Join
from .events.antiban import antiban
from .events.antichannel import antichannel
from .events.antiguild import antiguild
from .events.antirole import antirole
from .events.antibot import antibot
from .events.antikick import antikick
from .events.antiprune import antiprune
from .events.antiwebhook import antiwebhook
from .events.antiping import antipinginv
from .events.antiemostick import antiemostick
from .events.antintegration import antintegration
from .events.antispam import AntiSpam
from .events.autoblacklist import AutoBlacklist
from .events.antiemojid import antiemojid
from .events.antiemojiu import antiemojiu
from .events.Errors import Errors
from .events.on_guild import Guild
from .events.greet2 import greet
from .events.voiceupdate import Vcroles2
from .events.boost2 import bst
from .events.boost3 import Boost3
from .events.autoreact import AutoReactListener



##############select menu + button#############

from .help.all import all
from .help.anti1 import anti1
from .help.invites1 import invites1
from .help.VoiceChannelManager1 import VoiceChannelManager1
from .help.general1 import general1
from .help.extra1 import extra1
from .help.gw1 import gw1
from .help.pfps1 import pfps1
from .help.nsfw1 import nsfw1
from .help.Leveling1 import Leveling1
from .help.mod1 import mod1
from .help.music1 import music1
from .help.boost1 import boost1
from .help.automod1 import automod1
from .help.media1 import media1
from .help.welcome1 import welcome1
from .help.fun1 import fun1
from .help.logging1 import logging1
from .help.role1 import role1
from .help.voice1 import voice1
from .help.vcrole1 import vcrole1
from .help.verification1 import ver1
from .help.games1 import games1
from .help.encryption1 import encryption1
from .help.ticket1 import ticket1
from .help.joindm1 import joindm1
from .help.owner2 import owner2
from .help.vanity1 import vanity1
from .help.marrige1 import marrige1
from .commands.autoreact import AutoReaction



###############cmnd add################


async def setup(bot: Ignis):
  await bot.add_cog(Help(bot))
  await bot.add_cog(Stats(bot))
  await bot.add_cog(Profile(bot))
  await bot.add_cog(Starboard(bot))
  await bot.add_cog(AutoRole(bot))
  await bot.add_cog(General(bot))
  await bot.add_cog(Music(bot))
  await bot.add_cog(Moderation(bot))
  await bot.add_cog(Antinuke(bot))
  await bot.add_cog(Whitelist(bot))
  await bot.add_cog(Unwhitelist(bot))
  await bot.add_cog(Emergency(bot))
  await bot.add_cog(Nightmode(bot))
  await bot.add_cog(Extraowner(bot))
  await bot.add_cog(Automod(bot))
  await bot.add_cog(Welcomer(bot))
  await bot.add_cog(boost(bot))    
  await bot.add_cog(Fun(bot))
  await bot.add_cog(Games(bot))
  # await bot.add_cog(nsfw(bot))
  await bot.add_cog(Leveling(bot))
  await bot.add_cog(J2C(bot))
  await bot.add_cog(Utility(bot))
  await bot.add_cog(Voice(bot))
  await bot.add_cog(Owner(bot))
  await bot.add_cog(Server(bot))
  await bot.add_cog(Ignore(bot))
  await bot.add_cog(Verification(bot))
  await bot.add_cog(Media(bot))
  await bot.add_cog(Info(bot))
  await bot.add_cog(list(bot))
  await bot.add_cog(gafk(bot))
  await bot.add_cog(afk(bot))
  await bot.add_cog(Logging(bot))
  await bot.add_cog(owner1(bot))
  # await bot.add_cog(Youtube(bot))
  await bot.add_cog(Reminder(bot))
  await bot.add_cog(giveaway(bot))
  await bot.add_cog(gwtask(bot))
  await bot.add_cog(pfps(bot))
  await bot.add_cog(joindm(bot))
  await bot.add_cog(Zestar(bot))
  await bot.add_cog(Uptime(bot))
  await bot.add_cog(mod(bot)) 
  await bot.add_cog(MusicFilters(bot))
  await bot.add_cog(TicketCog(bot))
  await bot.add_cog(Nitro(bot))
  await bot.add_cog(bst(bot))
  # await bot.add_cog(calculator(bot))
  await bot.add_cog(report(bot))
  await bot.add_cog(Vanityroles(bot))
  await bot.add_cog(emojis(bot)) 
  # await bot.add_cog(encryption(bot))
  await bot.add_cog(invites(bot))
  await bot.add_cog(NotifCommands(bot))
  # await bot.add_cog(Marriage(bot))
  # await bot.add_cog(Birthdays(bot))
  await bot.add_cog(Blacklist(bot))
  await bot.add_cog(MuteAll(bot))
  await bot.add_cog(Embed(bot))
  await bot.add_cog(AutoReaction(bot))
  await bot.add_cog(PanicMode(bot))

############select menu + button###############
  await bot.add_cog(anti1(bot))
  await bot.add_cog(automod1(bot))
  await bot.add_cog(general1(bot))
  await bot.add_cog(extra1(bot))
  await bot.add_cog(gw1(bot))
  await bot.add_cog(pfps1(bot))
  await bot.add_cog(mod1(bot))
  await bot.add_cog(music1(bot))
  await bot.add_cog(boost1(bot))  
  await bot.add_cog(media1(bot)) 
  await bot.add_cog(welcome1(bot))
  # await bot.add_cog(fun1(bot))
  await bot.add_cog(Leveling1(bot))
  # await bot.add_cog(VoiceChannelManager1(bot))
  await bot.add_cog(invites1(bot))
  await bot.add_cog(logging1(bot))
  await bot.add_cog(role1(bot))
  await bot.add_cog(games1(bot))
  # await bot.add_cog(encryption1(bot)) 
  await bot.add_cog(voice1(bot)) 
  # await bot.add_cog(vcrole1(bot))
  await bot.add_cog(ver1(bot))
  await bot.add_cog(ticket1(bot))
  # await bot.add_cog(all(bot))
  await bot.add_cog(joindm1(bot))
  await bot.add_cog(vanity1(bot))
  await bot.add_cog(marrige1(bot))
  # await bot.add_cog(ai1(bot))
  await bot.add_cog(nsfw1(bot))


    
###########################events################3
  
  await bot.add_cog(antiban(bot))
  await bot.add_cog(antichannel(bot))
  await bot.add_cog(antiguild(bot))
  await bot.add_cog(antirole(bot))
  await bot.add_cog(antibot(bot))
  await bot.add_cog(antikick(bot))
  await bot.add_cog(antiprune(bot))
  await bot.add_cog(antiwebhook(bot))
  await bot.add_cog(antipinginv(bot))
  await bot.add_cog(antiemostick(bot))
  await bot.add_cog(antintegration(bot))  
  await bot.add_cog(AntiSpam(bot))
  await bot.add_cog(AutoBlacklist(bot))
  await bot.add_cog(antiemojid(bot))
  await bot.add_cog(antiemojiu(bot))
  await bot.add_cog(Guild(bot))
  await bot.add_cog(Errors(bot))
  await bot.add_cog(greet(bot))
  await bot.add_cog(Join(bot))
  await bot.add_cog(Vcroles2(bot))
  await bot.add_cog(Boost3(bot))
  await bot.add_cog(AutoReactListener(bot))



 
