# Made by Gay this Gay earth
# This is kinda PEP8 conform (not really I am too lazy to check everything)
# Also fuck 80 symbols per lime limits
# This bot does tord for healsluts.

import discord
from discord.ext import commands
import asyncio
from random import shuffle, randrange, random, choice
import pickle
import copy
from bottoken import tkn
from pornlist import pornlst

bot = commands.Bot(command_prefix='!',
                   description='what kind of fucking hack made this?')

# Global variables are bad mkay fuck off
qlst = []
shfl = None
started = False
backuplst = [] 
shfllst = []
# Boy you can probably do this list better somehow who cares tho
authlst = ['105784527632220160', '187921806085062657', '195365659985575936',
'110986858812432384', '193859387394097152', '146327419698020352',
'140982805856387072', '139152162071511040', '147189753744195584',
'203087815318306816', '215207500687867908', '197791201791836160',
'151658345705635840', '133644191677808640', '236941748805435397',
'146791841252114432', '134784827361591296']
removedlst = [] # People who leave during a game will be placed behind shuffle

@bot.event
async def on_ready():
    print(bot.user.name +  "/" + bot.user.id)

async def backup():
    global backuplst
    global shfllst

    if (len(backuplst) > 100):
        backuplst.pop(0)

    tmplst = copy.copy(qlst)
    backuplst.append(copy.copy(tmplst))
    shfllst.append(shfl)

async def rest():
    global qlst
    global shfl
    global backuplst
    global shfllst

    if (len(backuplst) == 0):
        await bot.say("No more backups available.")
        return

    tmplst = copy.copy(backuplst[-1])
    qlst = copy.copy(tmplst)
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
                str(i)[:-5] + " :game_die:\n"
            else:
                output = output + '{0}: '.format(pos) + \
                str(i.nick) + " :game_die:\n"
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
    output = output + ":game_die: is shuffle"
    return output

async def move_queue():
    global qlst
    global shfl

    if (len(qlst) == 1):
        await bot.say("This should not happen.")
        return
    elif (len(qlst) == 2):
        tmp = qlst[0]
        qlst.pop(0)
        qlst.append(tmp) 
        return
    else:
        if (qlst[0] == shfl):
            if (len(qlst) == 3):
                qlst[0], qlst[1] = qlst[1], qlst[0]
                shfl = qlst[-1]
            else:
                tmp1 = qlst[0]
                tmp2 = qlst[-1]
                qlst.pop(0)
                qlst.pop()
                for i in range(1, 20):
                    shuffle(qlst)
                qlst.insert(randrange(1, len(qlst)), tmp1)
                qlst.insert(randrange(1, len(qlst)), tmp2)
                shfl = qlst[-1]
        else:
            tmp = qlst[0]
            qlst.pop(0)
            qlst.append(tmp) 


async def is_authed(usr, queue):
    if (queue == True):
        if (usr not in qlst \
            and str(usr.id) not in authlst):
            return False
        else:
            return True
    else:
        if (str(usr.id) not in authlst):
            return False
        else:
            return True

async def remove_user(membr):
    global qlst
    global removedlst
    global shfl
    global started
    reping = False

    if membr in qlst:
        if (len(qlst) == 1):
            await bot.say("Queue is getting too small. Stopping game.")
            qlst = []
            removedlst = []
            backuplst = []
            shfllst = []
            shfl = None
            started = False
        elif (len(qlst) == 2):
            await backup()
            qlst.remove(membr)
            shfl = qlst[-1]
            started = False
            removedlst = []
            await bot.say("Only one user remaining. Stopping game and waiting"
                      " for more.")
            return
        else:
            if (str(membr) == str(qlst[-1])):
                await backup()
                reping = True
                if (str(membr) == str(shfl)):
                    shfl = qlst[-2]
                qlst.remove(membr)
            else:
                if (started == False):
                    await backup()
                    if (str(shfl) == str(membr)):
                        shfl = qlst[int(qlst.index(membr)) - 1]
                    qlst.remove(membr)
                else:
                    if (str(membr) == str(qlst[0]) or
                        str(membr) == str(qlst[-1])):
                        reping = True
                    await backup()
                    if (str(shfl) == str(membr)):
                        shfl = qlst[int(qlst.index(membr)) - 1]
                    qlst.remove(membr)


        if (started == True):
            removedlst.append(membr)
    else:
        await bot.say("User not found in list.")
        return

    if (reping == False or started == False):
        await bot.say("User removed.")
    else:
        await bot.say(await get_queue("Currently asked/asking user removed."
                      " New queue:\n", True))

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
        if (ctx.message.author in removedlst and str(qlst[-1]) != str(shfl)):
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
        await backup()        
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

    if (started == False):
        await bot.say("No game running!")
        return

    await remove_user(qlst[0])

@bot.command(pass_context=True)
async def r(ctx, todelete=None):
    """Removes yourself or other user.

    Removes yourself or others (if you are authorized)
    from the current queue.

    :Usage:
    !r
    !r 4
    """

    # Only authed people can remove others
    if (todelete == None):
        membr = ctx.message.author
    else:
        try:
            if not await is_authed(ctx.message.author, False):
                await bot.say("You need to be authorized to do this.")
                return
            else:
                if(len(qlst) < int(todelete)):
                    await bot.say("Please enter valid number.")
                else:
                    membr = qlst[int(todelete) - 1]
        except TypeError:
            await bot.say("Please only use numbers.")
            return

    await remove_user(membr)

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
async def purgequeue(ctx):
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

    await backup()
    for i in range(1,20):
        shuffle(qlst)

    shfl=qlst[-1]
    started = False

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
async def setshuffle(ctx, toshuffle : int):
    """Set a new user as shuffle.

    The first user that is mentioned
    will be the new shuffle. You need
    to be authorized to do this.

    :Usage:
    !setshuffle 2
    """

    global shfl

    if not await is_authed(ctx.message.author, False):
        await bot.say("You need to be authorized to do this.")
        return

    try:
        shfl = qlst[int(toshuffle) - 1]
        await backup()
        await bot.say(await get_queue('Shuffle changed. Current queue:\n', True))
    except TypeError:
        await bot.say("Please enter a number.")


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
@bot.command(pass_context=True, hidden=True)
async def supermad(ctx):
    em = discord.Embed()
    em.set_image(url='http://i.imgur.com/VCDHNnn.png')
    await bot.send_message(ctx.message.channel, embed=em)

@bot.command(hidden=True)
async def ripandtear():
    await bot.say('https://www.youtube.com/watch?v=zZMg9ryeWOw')

@bot.command(pass_context=True, hidden=True)
async def imgay(ctx):
    em = discord.Embed()
    em.set_image(url='https://cdn.discordapp.com/attachments/254665648012001280/2'
                  '64083658275684353/ugh.png')
    await bot.send_message(ctx.message.channel, embed=em)

@bot.command(hidden=True)
async def soldierpotg():
    await bot.say('https://www.youtube.com/v/9aqopEQr7wI?start=0&end=38&versio'
                  'n=3')

@bot.command(pass_context=True, hidden=True)
async def porn(ctx):
    em = discord.Embed()
    em.set_image(url=str(choice(pornlst)))
    await bot.send_message(ctx.message.channel, embed=em)

@bot.command(hidden=True)
async def whatthefuck():
    await bot.say('https://youtu.be/F9UKNwlhhpo?t=111')

@bot.command(pass_context=True, hidden=True)
async def rip(ctx):
    em = discord.Embed()
    em.set_image(url='http://i.imgur.com/4I9ycgj.png')
    await bot.send_message(ctx.message.channel, embed=em)

@bot.command(hidden=True)
async def sofro():
    await bot.say("fucking sofro fucking SLUT")
    
@bot.command(hidden=True)
async def cowbell():
    await bot.say("https://www.youtube.com/watch?v=TklM2-lSby4")

@bot.command(hidden=True)
async def mistake():
    await bot.say("https://youtu.be/O0_wpzt8CY4")

@bot.command(pass_context=True, hidden=True)
async def flat(ctx):
    em = discord.Embed()
    em.set_image(url='http://i.imgur.com/HXtXDiL.jpg')
    await bot.send_message(ctx.message.channel, embed=em)

@bot.command(hidden=True)
async def riddick():
    await bot.say('EVERY MORNING I WAKE UP AND OPEN PALM SLAM A VHS INTO THE '
                  'SLOT. ITS CHRONICLES OF RIDDICK AND RIGHT THEN AND THERE I '
                  'START DOING THE MOVES ALONGSIDE WITH THE MAIN CHARACTER, '
                  'RIDDICK. I DO EVERY MOVE AND I DO EVERY MOVE HARD. MAKIN '
                  'WHOOSHING SOUNDS WHEN I SLAM DOWN SOME NECRO BASTARDS OR '
                  'EVEN WHEN I MESS UP TECHNIQUE. NOT MANY CAN SAY THEY '
                  'ESCAPED THE GALAXYS MOST DANGEROUS PRISON. I CAN. I SAY IT '
                  'AND I SAY IT OUTLOUD EVERYDAY TO PEOPLE IN MY COLLEGE CLASS '
                  'AND ALL THEY DO IS PROVE PEOPLE IN COLLEGE CLASS CAN STILL '
                  'BE IMMATURE JEKRS. AND IVE LEARNED ALL THE LINES AND '
                  'IVE LEARNED HOW TO MAKE MYSELF AND MY APARTMENT LESS '
                  'LONELY BY SHOUTING EM ALL. 2 HOURS INCLUDING WIND DOWN '
                  'EVERY MORNIng')

# bot crash bot get up again. bot strong you weak
while True:
    bot.run(tkn)
