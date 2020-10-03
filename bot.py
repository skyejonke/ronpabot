import asyncio
import discord
import shelve
import config
import random
import copy
import datetime
import re
import yaml
import evidence
from fuzzywuzzy import fuzz

client = discord.Client()

global active
active = []
global activeLocal
activeLocal = ""
global locations
locations = {}

# def activationList(active):
#     names = []
#     for i in active:
#         names.append(i.name)
#     return names

def getActive(active, local):
    for i in active:
        if i[0] == local:
            return i[1]
    return None

def loadDescription(evi) :
    return evi.text

@client.event
async def on_ready():
    global locations
    global active
    print('Logged in as')
    print(client.user.name)
    print('---------')

    locations = evidence.loadFile(config.source)

    itr = 0
    for i in locations.keys():
        print(i)
        print(locations[i])
        active.append([])
        active[itr].append(i)
        active[itr].append(locations[i])

        itr += 1

def here(active):
    out = "\n**Things in the room include:"
    for x in active:
        out += "\n- " + x.name
    out+="**"
    return out


@client.event
async def on_message(message):
    global active
    global locations
    global activeLocal
    out = ""
    messageContent = message.content
    messageContent = re.sub(r'\s+',' ',messageContent)
    splitMessage = messageContent.split(" ")
    if (message.author.id != client.user.id):
        print(activeLocal)

        if (config.goto == None or fuzz.partial_ratio(splitMessage[0], config.goto) > 50):
            for i in locations.keys():
                if fuzz.token_set_ratio(messageContent, i) > 50:
                        out += "Switching to " + i + "!"
                        activeLocal = getActive(active, i)
                        out += here(activeLocal)

        elif (config.investigate == None or
                fuzz.partial_ratio(splitMessage[0], config.investigate) > 50):
            found = False
            for i in activeLocal:
                # print("DAMMIT")
                # print(i)
                # print(i.name)
                if fuzz.token_set_ratio(messageContent, i.name) > 50:
                    activeLocal = evidence.loadEvidence(
                            activeLocal, i)
                    out += "\n" + i.name  + ": " + loadDescription(i)
                    found = True

            if (found):
                out += here(activeLocal)

        if (out != ""):
            await message.channel.send(out)

client.run(config.token)
