import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import json

Client = discord.Client() #Initialise Client
client = commands.Bot(command_prefix = "") #Initialise client bot, we have two prefixes, so yeah, no need to use

token = "NDU1MzY0MTI1MDUzMTU3Mzg2.Df66mw.2XyafD2HUkRb6ly-Np4UH2UM2SE"

# statics
ban = "BANANO"
nano = "NANO"
naneroo = 1000000.0 # for calculation

pb = "." # prefix for banano commands
pn = "?" # prefix for nano commands

command = {ban: ".ban", nano: "?tip"}
prefix = {ban: pb, nano: pn}
color = {ban: 0xffd800, nano: 0x6da5ff}

# team turd channels
#bananoChannel = "441603518659559424"
#nanoChannel = "443962819428220929"
#winChannel = "445788486188924938"

# la jungla channels
bananoChannel = "451848512754417664"
nanoChannel = "451848537718652928"
winChannel = "449308348815376385"

testingChannel = "448502533242224640"

testingChannel = ["448230365803446273", "448502533242224640"]

channel = {
            ban: bananoChannel,
            nano: nanoChannel,
            "win": winChannel,
            "test": testingChannel
            }

# names
teamName = "Team Example"

# emojis
x = '\U0000274C'
save = '\U0001F4BE'
#tick = ':tick:448243202592473088'
tick = u"\U0001F346"
scissors = "\u2702"
cup = "\U0001F3C6"
zap = "\u26A1"
star = u"\u2605"
#star = '?'
letter = "\u2709"

class User:

   def __init__(self, discordID, name):
        self.id = discordID
        self.name = name

   def getID(self):
       return self.id

   def getName(self):
       return self.name

class customError:

    def __init__(self, active, name, message):
        self.active = active
        self.name = name
        self.message = message

    def getActive(self):
        return self.active

    def getName(self):
        return self.name

    def getMessage(self):
        return self.message

# hardcoded user for testing only
#b1 = User(11111, "Banano1")
#b2 = User(22222, "Banano2")

#n1 = User(11111, "Nano1")
#n2 = User(22222, "Nano2")

userList = {ban: [], nano: []}
#userList = {ban: [b1,b2], nano: [n1,n2]} # hardcoded list for testing only

async def add_to_list(message, currency):
    if channelPerm(message, currency):
        user = User(message.author.id, message.author.name)
        cList = userList[currency]
        if not userInList(user, cList):
            cList.insert(len(cList), user)
            await client.add_reaction(message, tick) # reaction: tick
        else:
            await client.add_reaction(message, x) # reaction: x

async def show_list(message, currency):
    if channelPerm(message, currency):
        cList = userList[currency]
        strList  = getlist(cList)

        settings = {
            "Title": currency,
            "Desc": "**Current list - " + str(len(cList)) + " member(s)**\n" + "```" + strList +  "```",
            "Color": color[currency] # yellow or blue
        }
        fields = {}
        #footer = {
        #    "text":"Type " +  prefix[currency] + "help for all commands."
        #}
        footer = {}

        embed = newEmbed(settings, fields, footer)
        await client.send_message(message.channel, embed=embed)

async def start_new_giveaway(message, currency):
    if channelPerm(message, currency):
        cList = userList[currency]
        args = message.content.split(" ")
        verify = verifyUserInput(args, {"mode": "start"})
        if not verify.getActive():
            cList.clear()
            fee = args[1]

            settings = {
                "Title": currency,
                "Desc": "**New giveaway started!**",
                "Color": color[currency]
            }
            fields = {
                1: {
                    "name": "Fee",
                    "value": "" + fee + "", # not sure if `` looks good tho
                    "inline": True
                },
                2: {
                    "name": "Command",
                    "value": "" + "Type " + prefix[currency] + "in if you entered." + "",
                    "inline": True
                }
            }
            footer = {}

            embed = newEmbed(settings, fields, footer)
            if verify.getName() == "e":
                await client.send_message(message.channel, verify.getMessage())

            await client.send_message(message.channel, embed=embed)

        else:
            settings = {
                "Title": currency,
                "Desc": "**Error " + verify.getName() + "**",
                "Color": 0xe82c2c
            }
            fields = {
                1: {
                    "name" : "Reason",
                    "value":  verify.getMessage(),
                    "inline": True
                }
            }
            footer = {
                "text": "Type " +  prefix[currency] + "help for all commands."
            }
            embed = newEmbed(settings, fields, footer)
            await client.add_reaction(message, x) # reaction: x
            await client.send_message(message.channel, embed=embed)

async def remove_user(message, currency):
    if channelPerm(message, currency):
        cList = userList[currency]
        args = message.content.split(" ")
        verify = verifyUserInput(args, {"mode": "remove", "list": cList})
        if not verify.getActive():
            index = int(args[1]) - 1
            removedUser = cList[index]
            cList.pop(index)
            strList  = getlist(cList)
            await client.add_reaction(message, zap)

            settings = {
                "Title": currency,
                "Desc": "**Successfully removed " + removedUser.getName() + " from the List!**",
                "Color": color[currency]
            }
            fields = {
                1: {
                    "name": "Updated List",
                    "value": "```" + strList +  "```",
                    "inline": False
                }
            }
            footer = {}
            embed = newEmbed(settings, fields, footer)
            await client.add_reaction(message, zap) # reaction: zap
            await client.send_message(message.channel, embed=embed)

        else:
            settings = {
                "Title": currency,
                "Desc": "**Error " + verify.getName() + "**",
                "Color": 0xe82c2c
            }
            fields = {
                1: {
                    "name" : "Reason",
                    "value":  verify.getMessage(),
                    "inline": True
                }
            }
            footer = {
                "text": "Type " +  prefix[currency] + "help for all commands."
            }
            embed = newEmbed(settings, fields, footer)
            await client.add_reaction(message, x) # reaction: x
            await client.send_message(message.channel, embed=embed)

async def clear(message, currency):
    if channelPerm(message, currency):
        cList = userList[currency]
        cList.clear()

        settings = {
            "Title": currency,
            "Desc": "**List was cleared**",
            "Color": color[currency]
        }
        fields = {}
        footer = {}
        embed = newEmbed(settings, fields, footer)
        await client.add_reaction(message, scissors) # scissors
        await client.send_message(message.channel, embed=embed)

async def addcustom_to_list(message, currency):
    if channelPerm(message, currency):
        args = message.content.split(" ")
        verify = verifyUserInput(args, {"mode": "add"})

        if not verify.getActive():
            user = User(args[1], args[2])
            cList = userList[currency]
            if not userInList(user, cList):
                cList.insert(len(cList), user)
                await client.add_reaction(message, tick) # reaction: tick
            else:
                await client.add_reaction(message, x) # reaction: x
        else:
            settings = {
                "Title": currency,
                "Desc": "**Error " + verify.getName() + "**",
                "Color": 0xe82c2c
            }
            fields = {
                1: {
                    "name" : "Reason",
                    "value":  verify.getMessage(),
                    "inline": True
                }
            }
            footer = {
                "text": "Type " +  prefix[currency] + "help for all commands."
            }
            embed = newEmbed(settings, fields, footer)
            await client.add_reaction(message, x) # reaction: x
            await client.send_message(message.channel, embed=embed)

async def save_win(message, currency):
    if channelPerm(message, currency):
        args = message.content.split(" ")
        cList = userList[currency]
        verify = verifyUserInput(args, {"mode": "win", "list": cList})
        if not verify.getActive():
            cList.clear()
            winningAmount = int(args[1])
            winner = cList[int(args[2]) - 1]
            splitAmount = round(winningAmount / len(cList)) # INTENSE MATH
            if currency == nano:
                # 1 nano = 1.000.000 naneroo
                winningAmount = round(winningAmount / naneroo, 6)
            strList  = getlist(cList)
            settings = {
                "Title": (star) + " Congratulations " + teamName + ", we just won " +  str(winningAmount) + " " + currency + "! " + (star),
                "Desc": "**Winners**" +"\n"  + "```" + strList +  "```" ,
                "Color": color[currency]
            }
            fields = {
                1: {
                    "name": "Winner",
                    "value": winner.getName(),
                    "inline": True
                },
                2: {
                    "name": "Splitamount",
                    "value": splitAmount,
                    "inline": True
                }
            }
            footer = {}

            embed = newEmbed(settings, fields, footer)
            await client.add_reaction(message, cup)
            await client.send_message(discord.Object(id=channel["win"]), "@everyone")
            await client.send_message(discord.Object(id=channel["win"]), embed=embed)
        else:
            settings = {
                "Title": currency,
                "Desc": "**Error " + verify.getName() + "**",
                "Color": 0xe82c2c
            }
            fields = {
                "field1": {
                    "name" : "Reason",
                    "value":  verify.getMessage(),
                    "inline": True
                }
            }
            footer = {
                "text": "Type " +  prefix[currency] + "help for all commands."
            }
            embed = newEmbed(settings, fields, footer)
            await client.add_reaction(message, x) # reaction: x
            await client.send_message(message.channel, embed=embed)

async def help(message, currency):
    p = prefix[currency]
    settings = {
        "Title": "Giveaway Managament Bot for Banano and Nano",
        "Desc": "Command Overview",
        "Color": color[currency]
    }
    fields = {
        1: {
            "name": "Prefixes",
            "value": "Banano: " + "**" + pb + "**" + " | " + "Nano: " + "**" + pn + "**" + "\n" + "Your selected prefix: " + "**" + p + "**",
            "inline": False
        },
        2: {
            "name": p + "in",
            "value": "Register into the list",
            "inline": False
        },
        3: {
            "name": p + "start <amount> optional: 'e'",
            "value": "Starts new giveaway with fee: <amount>, pass a optional 'e' to tag everyone, also clears list",
            "inline": False
        },
        4: {
            "name": p + "add <discordID> <name>",
            "value": "Adds Non-member into the list",
            "inline": False
        },
        5: {
            "name": p + "remove <index>",
            "value": "Removes member from the list at position <index>",
            "inline": False
        },
        6: {
            "name": p + "list",
            "value": "Shows current list",
            "inline": False
        },
        7: {
            "name": p + "clear",
            "value": "Clears complete list",
            "inline": False
        },
        8: {
            "name": p + "win <amount> <index>",
            "value": "Saves current list in the win channel. Displays winning list, the winner at <index>, the winning <amount>, and the correct splitting amount, also clears list",
            "inline": False
        },
        9: {
            "name": p + "help",
            "value": "Sends command overview as private message",
            "inline": False
        }
    }

    footer = {
        "text": "Contact not_idol#3950 if you have any questions/problems"
    }

    embed = newEmbed(settings, fields, footer)
    await client.add_reaction(message, letter)
    await client.send_message(message.author, embed=embed)

def channelPerm(message, currency):
    channelID = message.channel.id
    if channelID == channel[currency] or channelID in channel["test"]: # checks if current channel is testing/currency channel
        return True
    else:
        return False

def userInList(user, list):
    for u in list:
        if user.getID() == u.getID():
            return True

    return False

def getlist(list):
    if len(list) <= 0:
        return "List is empty"
    output = ""
    pos = 1
    for user in list:
        output = output + "\n" + str(pos) + ". " + user.getName()
        pos += 1
    return output

def newEmbed(settings, fields, footer):
    embed = discord.Embed(title=settings["Title"], description=settings["Desc"], color=settings["Color"], type="rich")

    for key, value in fields.items():
        embed.add_field(name=value["name"], value=value["value"], inline=value["inline"])

    for key, value in footer.items():
        embed.set_footer(text=value)

    return embed

def verifyUserInput(args, mode):
    if mode["mode"] == "start":
        if len(args) >= 2:
            if args[1].isdigit():
                if len(args) >= 3:
                    if args[2] == "e":
                        return customError(False, "e", "@everyone")
                    else:
                        return customError(False, "", "")
                else:
                    return customError(False, "", "")
            else:
                return customError(True, "InvalidArgument", "First argument <amount> needs to be valid digit")
        else:
            return customError(True, "MissingArgument", "Missing parameter <amount>")

    if mode["mode"] == "remove":
        if not len(args) <= 1:
            if args[1].isdigit():
                arg = int(args[1])
                if arg > 0:
                    if arg <= len(mode["list"]):
                        return customError(False, "", "")
                    else:
                        return customError(True, "ArgumentOutOfList", "<index> is not in current list")
                else:
                    return customError(True, "InvalidArgument", "<index> needs to be a number higher than 0")
            else:
                return customError(True, "InvalidArgument", "<index> must be a valid digit")
        else:
            return customError(True, "MissingArgument", "Missing parameter <index>")

    if mode["mode"] == "add":
        if not len(args) <=2:
            if args[1].isdigit():
                return customError(False, "", "")
            else:
                return customError(True, "InvalidArgument", "<id> must be a valid digit")
        else:
            return customError(True, "MissingArgument", "Missing parameter <id> and <name>")

    if mode["mode"] == "win":
        if not len(args) <=2:
            if args[1].isdigit() and args[2].isdigit():
                if int(args[1]) > 0:
                    if int(args[2]) - 1 < len(mode["list"]) and int(args[2]) > 0:
                        return customError(False, "", "")
                    else:
                        return customError(True, "InvalidArgument", "User not found on position " + args[2])
                else:
                    return customError(True, "InvalidArgument", "<amount> needs to be a number higher than 0")
            else:
                return customError(True, "InvalidArgument", "<amount> and <index> must be valid digits")
        else:
            return customError(True, "MissingArgument", "Missing parameter <amount> and <index>")

# initialise bot
@client.event
async def on_ready():
    print("Bot is online and connected to Discord") # print to console that bot works fine

@client.event
async def on_message(message):

    if message.content.upper().startswith(pb + "IN"):
        await add_to_list(message, ban)

    if message.content.upper().startswith(pb + "LIST"):
        await show_list(message, ban)

    if message.content.upper().startswith(pb + "START"):
        await start_new_giveaway(message, ban)

    if message.content.upper().startswith(pb + "REMOVE"):
        await remove_user(message, ban)

    if message.content.upper().startswith(pb + "CLEAR"):
        await clear(message, ban)

    if message.content.upper().startswith(pb + "ADD"):
        await addcustom_to_list(message, ban)

    if message.content.upper().startswith(pb + "WIN"):
        await save_win(message, ban)

    if message.content.upper().startswith(pb + "HELP"):
        await help(message, ban)

########################################################################

    if message.content.upper().startswith(pn + "IN"):
        await add_to_list(message, nano)

    if message.content.upper().startswith(pn + "LIST"):
        await show_list(message, nano)

    if message.content.upper().startswith(pn + "START"):
        await start_new_giveaway(message, nano)

    if message.content.upper().startswith(pn + "REMOVE"):
        await remove_user(message, nano)

    if message.content.upper().startswith(pn + "CLEAR"):
        await clear(message, nano)

    if message.content.upper().startswith(pn + "ADD"):
        await addcustom_to_list(message, nano)

    if message.content.upper().startswith(pn + "WIN"):
        await save_win(message, nano)

    if message.content.upper().startswith(pn + "HELP"):
        await help(message, nano)

client.run(token)
