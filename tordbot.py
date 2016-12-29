# Made by Gay this Gay earth
# This is kinda PEP8 conform (not really I am too lazy to check everything)
# Also fuck 80 symbols per lime limits
# This bot does tord for healsluts.

import discord
from discord.ext import commands
import asyncio
from random import shuffle, randrange
import pickle
import copy
from token.py import token

bot = commands.Bot(command_prefix='!',
                   description='what kind of fucking hack made this?')

# Global variables are bad mkay fuck off
qlst = []
shfl = None
started = False
backuplst = [] 
shfllst = []
# Boy you can probably do this list better somehow who cares tho
authlst = ['Genko#7333', 'becca#9184', 'Monsue#2624', 'Wyvern#6209',
'MKJ#0997', 'Sparks#5180', 'Areii (Julie)#8549', 'Sofroni#7893', 'Carfal#0859',
'Videobunny#7415', 'HealBunny#6430', 'jack0flames#5040', 'Vojjin#9572',
'@Bunny*･ﾟ✧#6395', 'SledgeDensemeat#1640', 'Jac#9484', 'Shinya#1756',
'Dermius#1210', 'Rihn#4199', 'shadowsoze#2615', '¯\_(ツ)_/¯ 유혹#4415',
'Ghost of Slashy Future#1635', 'Aeriko#4284', 'Art#2893', 'CeoJohn#5114',
'Lemons#7768', 'MercyBae#0812', 'Nira#7394', 'Tiara#0161',
'Gay this Gay Earth#6889', 'Tanza#6925', 'Blistering#4912']
removedlst = [] # People who leave during a game will be placed behind shuffle

@bot.event
async def on_ready():
    print(bot.user.name +  "/" + bot.user.id)

async def backup():
    global backuplst
    global shfllst

    print(qlst)
    backuplst.append(qlst)
    print(backuplst)
    shfllst.append(shfl)

async def rest():
    global qlst
    global shfl
    global backuplst
    global shfllst

    if (len(backuplst) == 0):
        await bot.say("No more backups available.")
        return

    qlst = copy.deepcopy(backuplst[-1])
    backuplst.pop()

    shfl = shfllst[-1]
    shfllst.pop()

    await bot.say(await get_queue('Backup restored. Restored queue:\n', True))

async def get_queue(intro, ment):
    output = intro
    output = output + '-----------------------------------------------------\n'
    pos = 1
    for i in qlst:
        if (i == shfl):
            nick = i.nick
            if (i.nick == None):
                output = output + '{0}: '.format(pos) + \
                str(i)[:-5] + ":heart:\n"
            else:
                output = output + '{0}: '.format(pos) + \
                str(i.nick) + ":heart:\n"
        else:
            if (i.nick == None):
                output = output + '{0}: '.format(pos) + str(i)[:-5] + "\n"
            else:
                output = output + '{0}: '.format(pos) + str(i.nick) + "\n"
        pos += 1

    output = output + '-----------------------------------------------------\n'
    if (ment == True):
        output = output + "{0} is asking {1}\n".format(qlst[-1].mention,
                                                       qlst[0].mention)
    output = output + ":heart: is shuffle"
    return output

async def move_queue():
    global qlst
    global shfl

    if (qlst[0] == shfl):
        qlst.pop(0)
        tmp = qlst[-1]
        qlst.pop()
        for i in range(1, 20):
            shuffle(qlst)
        qlst.append(shfl)
        if (len(qlst) == 1):
            qlst.insert(0, tmp)
            await backup()
            return
        qlst.insert(randrange(1, len(qlst)), tmp)
    else:
        tmp = qlst[0]
        qlst.pop(0)
        qlst.append(tmp) 

    await backup()

async def is_authed(usr, queue):

    if (queue == True):
        if (usr not in qlst \
            and str(usr) not in authlst):
            return False
        else:
            return True
    else:
        if (str(usr) not in authlst):
            return False
        else:
            return True

@bot.command(pass_context=True)
async def q(ctx):
    """Places you on the end of the queue.

    If no game is running, you will be 
    placed in the first slot of the queue.
    If a game is running, you will be placed
    in front of the shuffle user.
    """

    global qlst
    global shfl
    global started

    if (ctx.message.author in qlst):
        await bot.say("You are already in the queue!")
    elif (started == False):
        # If the game hasn't been started, people will just be slapped
        # to the bottom of the list
        qlst.append(ctx.message.author)
        shfl = ctx.message.author
        await bot.say('You have been added. Have fun.')
    else:
        # Naughty list? If people leave they will be put after the shuffle
        if (ctx.message.author in removedlst):
            await bot.say("You already were in the list. You will be placed\n"
                          "After the shuffle.")
            qlst.insert(qlst.index(shfl) + 1, ctx.message.author)
        else:
            # Otherwise just before
            if (qlst[0] == shfl):
                qlst.insert(1, ctx.message.author)
            else:
                qlst.insert(qlst.index(shfl), ctx.message.author)
            await bot.say('You have been added. Have fun.')

@bot.command(pass_context=True)
async def n(ctx):
    """Tags the next user in the queue.

    Moves the queue forward once. The person
    that got asked last round will now ask.
    If the queue passes the shuffle user,
    ever user's position in the queue will
    be randomized. You can only move the queue
    forward if you are in the queue or
    authorized to do so.
    """

    global started

    # You will see this all the fucking time I should have made a
    # function for this
    if not await is_authed(ctx.message.author, True):
        await bot.say("You need to be in the queue or authorized to do this.")
        return

    if (len(qlst) < 2):
        await bot.say("Queue too short. Unable to start game.")
        return

    if (started == True):
        await move_queue()
    else:
        started = True

    await bot.say(await get_queue("Thank you for playing Tord. The current"
                  " queue is:\n", True))

@bot.command(pass_context=True)
async def s(ctx):
    """Skips the current users.

    The current user will be skipped
    if you are authorized to do so.
    """

    if not await is_authed(ctx.message.author, True):
        await bot.say("You need to be in the queue or authorized to do this.")
        return

    if (started == True):
        await move_queue()
    else:
        await bot.say("No game running!")
        return

    await bot.say(await get_queue("Player got skipped. The current queue is:"
                  "\n", True))

@bot.command(pass_context=True)
async def r(ctx):
    """Removes yourself or mentioned user.

    Removes yourself or others (if you are authorized)
    from the current queue.

    :Usage:
    !r
    !r @User#0001
    """

    global qlst
    global removedlst
    global shfl
    global started
    reping = False

    # Only authed people can remove others
    if (len(ctx.message.mentions) < 1):
        membr = ctx.message.author
    else:
        if not await is_authed(ctx.message.author, False):
            await bot.say("You need to be authorized to do this.")
            return
        else:
            membr = ctx.message.mentions[0]

    # this could have been done better
    if (len(qlst) < 2):
        await bot.say("Queue is getting too small. Stopping game.")
        qlst = []
        removedlst = []
        shfl = None 
        started = False
        return

    if membr in qlst:
        if (qlst[0] == membr or qlst[-1] == membr):
            reping = True
        qlst.remove(membr)
        if (started == True):
            removedlst.append(membr)
    else:
        await bot.say("User not found in list.")
        return

    if (str(shfl) == str(membr)):
        shfl = qlst[-1]

    await backup()
    if (reping == False):
        await bot.say("User removed.")
    else:
        await bot.say(await get_queue("Currently asked user removed. New"
                      " queue:\n", True))

@bot.command()
async def d():
    """Display current queue.

    Displays the current queue. However,
    if only one user is in the current queue,
    it will not be displayed.
    """

    if (len(qlst) == 0):
        await bot.say("Nobody currently in queue.")
    elif (len(qlst) < 2):
        await bot.say("Currently only one user in queue: {0}.\n"
                      "Add more users to display proper"
                      " queue.".format(qlst[0]))
    else:
        if (started == False):
            await bot.say(await get_queue("This did not start the game. "
                          "To start it, please use !n. Queue:\n", False))
        else:
            await bot.say(await get_queue("The current queue is:\n", False))

# I started changing the naming convetion here because the alphabet only
# has so many letters and these functions are only for important twats
@bot.command(pass_context=True)
async def purge(ctx):
    """Purges the queue and stops the game.

    Removes every user from the queue.
    Only authorized people can do this.
    """

    if not await is_authed(ctx.message.author, False):
        await bot.say("You need to be authorized to do this.")
        return

    global qlst
    global removedlst
    global started
    global backuplst
    global shfllst
    global shfl

    qlst = []
    removedlst = []
    backuplst = []
    shfllst = []
    shfl = None
    started = False
    await bot.say("List purged.")

@bot.command(pass_context=True)
async def shufflequeue(ctx):
    """Shuffles the queue and stops the game.

    Shuffles the queue a few times in
    case the queue is not neatly randomized.
    This also randomizes the shuffle person.
    Only authorized people can do this.
    """

    global qlst
    global started
    global shfl

    if not await is_authed(ctx.message.author, False):
        await bot.say("You need to be authorized to do this.")
        return

    for i in range(1,20):
        shuffle(qlst)

    shfl=qlst[-1]
    started = False

    await backup()
    await bot.say(await get_queue("Queue has been shuffled. Start game again with"
                  " !n. New queue:\n", False))

@bot.command(pass_context=True)
async def restore(ctx):
    """Restores the last turn.

    The last turn will be loaded again.
    This can be run multiple times.
    Only authorized people can do this.
    """

    if not await is_authed(ctx.message.author, False):
        await bot.say("You need to be authorized to do this.")
        return

    await rest()

@bot.command(pass_context=True)
async def setshuffle(ctx):
    """Set a new user as shuffle.

    The first user that is mentioned
    will be the new shuffle. You need
    to be authorized to do this.

    :Usage:
    !setshuffle @User#0001
    """

    global shfl

    if not await is_authed(ctx.message.author, False):
        await bot.say("You need to be authorized to do this.")
        return

    shfl = ctx.message.mentions[0]
    await backup()
    await bot.say(await get_queue('Shuffle changed. Current queue:\n', True))


@bot.command(pass_context=True)
async def moveuser(ctx, first : int, second : int):
    """Move a user in the queue.

    Move the first position
    to the second. Only authorized
    users can do this.

    :Usage:
    !moveuser <move> <to>
    """

    global shfl
    global qlst

    if not await is_authed(ctx.message.author, False):
        await bot.say("You need to be authorized to do this.")
        return

    try:
        if (first > len(qlst) or second > len(qlst)):
            await bot.say("One or more invalid numbers given.")
            return

        if (first == second):
            await bot.say("Numbers can't be the same.")
            return
        elif (first > second):
            tmp = qlst[int(first - 1)] 
            del qlst[int(first - 1)]
            qlst.insert(int(second - 1), tmp)
        elif (first < second):
            tmp = qlst[int(first - 1)] 
            del qlst[int(first - 1)]
            qlst.insert(int(second - 1), tmp)
    except TypeError:
        await bot.say("Please only enter numbers.")
        return
 
    await backup()
    await bot.say(await get_queue('Positions changed. Current queue:\n', True))

# dont touch me REEEEEEEEEEEEEEEEEEEE
@bot.command()
async def supermad():
    """:MadBlini:"""
    await bot.say('http://i.imgur.com/VCDHNnn.png')

# bot crash bot get up again. bot strong you weak
while True:
    bot.run(token)
