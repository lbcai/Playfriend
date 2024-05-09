import os
import random
import datetime
import sys
import asyncio
import time

import discord
import emojis
import re

import pymongo
from discord import Intents
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from dotenv import load_dotenv

from urllib.request import urlopen, Request
from selenium import webdriver
from selenium.webdriver.common.by import By

if len(sys.argv) > 1:
    prod = sys.argv[1]
else:
    prod = None

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = Intents.default()
intents.message_content = True
bot = Bot(command_prefix='>', intents=intents)
hm_game_dictionary = {}
ttt_game_dictionary = {}
settings = {
    'sky': {
        'grandma': True,
        'geyser': True,
        'sky': False,
        'channel': None
    }
}
guild = None

options = webdriver.ChromeOptions()
if prod:
    # for headless chrome selenium web scraping
    options.add_argument('--headless=new')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
else:
    options.add_argument("--start-maximized")

MONGODB_URI = os.getenv('MONGODB_URI')
# Connect to database
client = pymongo.MongoClient(MONGODB_URI)
mongo_db = client.db
mongo_db.launches.drop()


def time_until_end_of_day(dt=None):
    """
    Get timedelta until end of day on the datetime passed, or current time.
    https://stackoverflow.com/questions/45986035/seconds-until-end-of-day-in-python
    """
    if dt is None:
        dt = datetime.datetime.now()
    tomorrow = dt + datetime.timedelta(days=1)
    return int((datetime.datetime.combine(tomorrow, datetime.time.min) - dt).total_seconds())


class Dungeon(commands.Cog):
    """Docs here"""

    # class Mage:
    #    def __init__(self):
    #        self.armorType = cloth

    # class Priest:

    # class Warrior:

    # class Archer:

    # class Thief:

    # @commands.command(name='dsetup', help='Start a new Dungeon session.')
    # async def dungeon_setup(self, ctx):
    #    bot.add_cog(Dungeon(), guild=ctx.guild)


class Tictactoe(commands.Cog):
    """Allows users to play tic tac toe. Use function ttt_start to create game instances.
    Can play 1p mode against bot AI or 2p mode with another user. Function ttt_mark_square is how a player adds their
    marker to the board. The bot turn is attached at the end so the bot can respond to user moves in a 1p game.

    Function ttt_setup allows a user to change their marker. Updates both in the game dictionary (to save markers across
    games) and in the Tictactoe object for that channel (where the marker is actually processed and used). This function
    can also be used to update the bot marker in 1p games.

    Function ttt_ai_move handles bot AI using an evaluate function so the bot knows which results are good and a minimax
    function so the bot can recursively predict outcomes and choose the best move (when combined with evaluate). There
    is also some logic at the end for actually submitting the move.

    Function ttt_output is used to display the game board (which is stored in a list) in a grid format with user markers.

    Function ttt_check_win is used after every turn to see if the game is over.

    Function ttt_quit ends the game and allows another game to be started in the same channel."""

    def __init__(self, ctx):
        self.tt_board_list = [0 for _ in range(0, 9)]
        self.tt_p1_symbol = ttt_game_dictionary[ctx.channel][3]
        self.tt_p2_symbol = ttt_game_dictionary[ctx.channel][4]
        self.ttt_first_player = 0

        if ttt_game_dictionary[ctx.channel][2] is not f'{bot.user.name}':
            player_2 = ttt_game_dictionary[ctx.channel][2].name
        else:
            player_2 = f'{bot.user.name}'
        today_date = datetime.date.today()
        self.game_doc = {'player1': ttt_game_dictionary[ctx.channel][1].name,
                         'player2': player_2, 'game': 'Tic-Tac-Toe',
                         'date': '%s/%s/%s' % (today_date.month, today_date.day,
                                               today_date.year)}

    async def ttt_ai_move(self, ctx):
        tt_list = self.tt_board_list
        rng_limiter = random.choice([5, 5, 5, 5, 6])

        def ttt_evaluate(tt_list):
            for row in range(0, 3):
                offset = row * 3
                if tt_list[offset] == tt_list[offset + 1] and tt_list[offset + 1] == tt_list[offset + 2]:
                    if tt_list[offset] == 1:
                        return -10
                    elif tt_list[offset] == 2:
                        return 10
            for column in range(0, 3):
                if tt_list[column] == tt_list[column + 3] and tt_list[column + 3] == tt_list[column + 6]:
                    if tt_list[column] == 1:
                        return -10
                    elif tt_list[column] == 2:
                        return 10
            if (tt_list[0] == tt_list[4] and tt_list[4] == tt_list[8]) or (
                    tt_list[2] == tt_list[4] and tt_list[4] == tt_list[6]):
                if tt_list[4] == 1:
                    return -10
                elif tt_list[4] == 2:
                    return 10
            return 0

        def ttt_minimax(tt_list, bot_turn, depth):
            score = ttt_evaluate(tt_list)
            if score == 10:
                return score
            if score == -10:
                return score
            if 0 not in tt_list:
                return 0

            if bot_turn:
                best_score = -11
                for square in range(0, 9):
                    if tt_list[square] == 0:
                        tt_list[square] = 2
                        if depth < rng_limiter:
                            best_score = max(best_score, ttt_minimax(tt_list, False, depth + 1))
                        tt_list[square] = 0
                return best_score - depth
            if not bot_turn:
                not_best_score = 11
                for square in range(0, 9):
                    if tt_list[square] == 0:
                        tt_list[square] = 1
                        if depth < rng_limiter:
                            not_best_score = min(not_best_score, ttt_minimax(tt_list, True, depth + 1))
                        tt_list[square] = 0
                return not_best_score + depth

        if self.tt_board_list.count(0) >= 8:
            self.tt_board_list[random.choice(range(0, 9))] = 2
            return

        tt_list_copy = self.tt_board_list * 1
        best_value = -11
        best_move = -1
        for square in range(0, 9):
            if tt_list_copy[square] == 0:
                tt_list_copy[square] = 2
                minimax_value = ttt_minimax(tt_list_copy, False, 0)
                tt_list_copy[square] = 0
                if minimax_value > best_value:
                    best_value = minimax_value
                    best_move = square
        if best_move != -1:
            tt_list[best_move] = 2
        else:
            await ctx.channel.send('Something went wrong. Restart the game!')

    async def ttt_output(self, ctx):
        def ttt_replacer(tt_list):
            tt_num_list = [':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:']
            tt_symbol_list = []
            for i in range(len(tt_list)):
                if tt_list[i] == 0:
                    tt_symbol_list.append(tt_num_list[i])
                elif tt_list[i] == 1:
                    tt_symbol_list.append(self.tt_p1_symbol)
                else:
                    tt_symbol_list.append(self.tt_p2_symbol)
            return tt_symbol_list

        tt_board = '{0}{1}{2} \n{3}{4}{5} \n{6}{7}{8}'.format(*ttt_replacer(self.tt_board_list))
        await ctx.channel.send(tt_board)
        await Tictactoe.ttt_check_win(self, ctx)

    async def ttt_check_win(self, ctx):
        tt_list = self.tt_board_list
        for row in range(0, 3):
            offset = row * 3
            if tt_list[offset] == tt_list[offset + 1] and tt_list[offset + 1] == tt_list[offset + 2]:
                if tt_list[offset] == 0:
                    return
                elif tt_list[offset] == 1:
                    await ctx.channel.send(f'{ttt_game_dictionary[ctx.channel][1].mention} has won the game!')
                    # Winner is player 1
                    self.game_doc['winner'] = self.game_doc['player1']

                elif tt_list[offset] == 2:
                    if ttt_game_dictionary[ctx.channel][2] is not f'{bot.user.name}':
                        await ctx.channel.send(f'{ttt_game_dictionary[ctx.channel][2].mention} has won the game!')
                    else:
                        await ctx.channel.send('Better luck next time!')
                    # Winner is player 2
                    self.game_doc['winner'] = self.game_doc['player2']
                await Tictactoe.ttt_quit(ttt_game_dictionary[ctx.channel], ctx)
                return mongo_db.games.insert_one(self.game_doc)
        for column in range(0, 3):
            if tt_list[column] == tt_list[column + 3] and tt_list[column + 3] == tt_list[column + 6]:
                if tt_list[column] == 0:
                    return
                elif tt_list[column] == 1:
                    await ctx.channel.send(f'{ttt_game_dictionary[ctx.channel][1].mention} has won the game!')
                    # Winner is player 1
                    self.game_doc['winner'] = self.game_doc['player1']
                elif tt_list[column] == 2:
                    if ttt_game_dictionary[ctx.channel][2] is not f'{bot.user.name}':
                        await ctx.channel.send(f'{ttt_game_dictionary[ctx.channel][2].mention} has won the game!')
                    else:
                        await ctx.channel.send('Better luck next time!')
                    # Winner is player 2
                    self.game_doc['winner'] = self.game_doc['player2']
                await Tictactoe.ttt_quit(ttt_game_dictionary[ctx.channel], ctx)
                return mongo_db.games.insert_one(self.game_doc)
        if (tt_list[0] == tt_list[4] and tt_list[4] == tt_list[8]) or (
                tt_list[2] == tt_list[4] and tt_list[4] == tt_list[6]):
            if tt_list[4] == 0:
                return
            elif tt_list[4] == 1:
                await ctx.channel.send(f'{ttt_game_dictionary[ctx.channel][1].mention} has won the game!')
                # Winner is player 1
                self.game_doc['winner'] = self.game_doc['player1']
            elif tt_list[4] == 2:
                if ttt_game_dictionary[ctx.channel][2] is not f'{bot.user.name}':
                    await ctx.channel.send(f'{ttt_game_dictionary[ctx.channel][2].mention} has won the game!')
                else:
                    await ctx.channel.send('Better luck next time!')
                # Winner is player 2
                self.game_doc['winner'] = self.game_doc['player2']
            await Tictactoe.ttt_quit(ttt_game_dictionary[ctx.channel], ctx)
            return mongo_db.games.insert_one(self.game_doc)
        if 0 not in tt_list:
            await ctx.channel.send('It\'s a tie!')
            await Tictactoe.ttt_quit(ttt_game_dictionary[ctx.channel], ctx)
            self.game_doc['winner'] = 'Tie!'
            return mongo_db.games.insert_one(self.game_doc)

    @commands.command(name='ttsetup',
                      help='Customize the marker you place on the board. Type bot after to randomize the bot marker.')
    async def ttt_game_setup(self, ctx, message='not bot'):

        def ttt_get_emoji(emoji_response):
            return ctx.channel == emoji_response.channel and ctx.message.author == emoji_response.author and \
                emojis.count(emoji_response.content) > 0

        if ctx.message.author in ttt_game_dictionary[ctx.channel][1:3]:
            if message.strip().lower() == 'bot' and ttt_game_dictionary[ctx.channel][2] is f'{bot.user.name}':
                await ctx.channel.send('Put a default emoji into the chat. The marker I use on the board will change.')
                symbol = await bot.wait_for('message', check=ttt_get_emoji)
                symbol = emojis.decode(random.choice(list(emojis.get(symbol.content))))
                ttt_game_dictionary[ctx.channel][4] = symbol
                ttt_game_dictionary[ctx.channel][0].tt_p2_symbol = ttt_game_dictionary[ctx.channel][4]
                await ctx.channel.send('My marker has been changed.')
                return

            await ctx.channel.send('Put a default emoji into the chat. The marker you use on the board will change.')

            symbol = await bot.wait_for('message', check=ttt_get_emoji)
            symbol = emojis.decode(random.choice(list(emojis.get(symbol.content))))
            if ctx.message.author == ttt_game_dictionary[ctx.channel][1]:
                ttt_game_dictionary[ctx.channel][3] = symbol
                ttt_game_dictionary[ctx.channel][0].tt_p1_symbol = ttt_game_dictionary[ctx.channel][3]
            elif ctx.message.author == ttt_game_dictionary[ctx.channel][2]:
                ttt_game_dictionary[ctx.channel][4] = symbol
                ttt_game_dictionary[ctx.channel][0].tt_p2_symbol = ttt_game_dictionary[ctx.channel][4]
            await ctx.channel.send('Your marker has been changed.')

    @commands.command(name='ttquit', help='Quit the current tic tac toe game.')
    async def ttt_quit(self, ctx):
        ttt_game_dictionary[ctx.channel][0] = None
        await ctx.channel.send('The tic tac toe game has ended.')
        await bot.remove_cog('Tictactoe', guild=ctx.guild)

    @commands.command(name='tt', help="To mark a square, type >tt # according to the grid.")
    async def ttt_mark_square(self, ctx, message):
        if ctx.message.author == ttt_game_dictionary[ctx.channel][1] or ctx.message.author == \
                ttt_game_dictionary[ctx.channel][2]:
            if int(message.strip()) in range(1, 10):
                if ttt_game_dictionary[ctx.channel][0].tt_board_list[int(message.strip()) - 1] == 0:
                    if (ctx.message.author == ttt_game_dictionary[ctx.channel][1] and
                            ttt_game_dictionary[ctx.channel][0].ttt_first_player == 1):
                        ttt_game_dictionary[ctx.channel][0].tt_board_list[int(message.strip()) - 1] = 1
                        ttt_game_dictionary[ctx.channel][0].ttt_first_player = 2
                    elif ctx.message.author == ttt_game_dictionary[ctx.channel][2] and ttt_game_dictionary[ctx.channel][
                        0].ttt_first_player == 2:
                        ttt_game_dictionary[ctx.channel][0].tt_board_list[int(message.strip()) - 1] = 2
                        ttt_game_dictionary[ctx.channel][0].ttt_first_player = 1
                    # prevent unnecessary board in single player games.
                    if ttt_game_dictionary[ctx.channel][2] is not f'{bot.user.name}':
                        await Tictactoe.ttt_output(ttt_game_dictionary[ctx.channel][0], ctx)
                    else:
                        await Tictactoe.ttt_check_win(ttt_game_dictionary[ctx.channel][0], ctx)
                else:
                    await ctx.channel.send('That square is already marked.')
            else:
                await ctx.channel.send('Send a number between 1 and 9 to mark a square!')
        if ttt_game_dictionary[ctx.channel][0] is not None:
            if (ttt_game_dictionary[ctx.channel][2] is f'{bot.user.name}' and 0 in
                    ttt_game_dictionary[ctx.channel][0].tt_board_list and
                    ttt_game_dictionary[ctx.channel][0].ttt_first_player == 2):
                await Tictactoe.ttt_ai_move(ttt_game_dictionary[ctx.channel][0], ctx)
                ttt_game_dictionary[ctx.channel][0].ttt_first_player = 1
                await Tictactoe.ttt_output(ttt_game_dictionary[ctx.channel][0], ctx)


@bot.command(name='ttstart', help='Starts a game of tic tac toe.')
async def ttt_start(ctx):
    def ttt_get_players(num_response):
        # Check to make sure the game starter is answering the question.
        return ctx.message.author == num_response.author and ctx.channel == num_response.channel and \
            num_response.content.lower().strip() in ['1', '2', 'one', 'two', '1p', '2p', '>tt 1', '>tt 2']

    def ttt_get_second_player(me_response):
        return ctx.channel == me_response.channel and ttt_player_one != me_response.author and \
            me_response.content.lower().strip() in ['me', 'i']

    if ctx.channel not in ttt_game_dictionary or ttt_game_dictionary[ctx.channel][0] is None:
        ttt_players = 0
        ttt_player_one = 0
        ttt_player_two = 0
        await ctx.channel.send('1p and 2p games are allowed. How many players are there?')
        while ttt_players == 0:
            response = await bot.wait_for('message', check=ttt_get_players)
            if response.content.lower().strip() in ['1', 'one', '1p', '>tt 1']:
                ttt_player_one = response.author
                ttt_player_two = f'{bot.user.name}'
                ttt_players = 1
            elif response.content.lower().strip() in ['2', 'two', '2p', '>tt 2']:
                ttt_player_one = response.author
                await ctx.channel.send('Who is the second player? Type "me".')
                ttt_player_two = 0
                while ttt_player_two == 0:
                    second_response = await bot.wait_for('message', check=ttt_get_second_player)
                    ttt_player_two = second_response.author
                ttt_players = 2
            else:
                await ctx.channel.send('Please specify whether there are one or two players.')

            if ctx.channel not in ttt_game_dictionary:
                ttt_game_dictionary[ctx.channel] = [None, ttt_player_one, ttt_player_two, ':x:', ':o:']
                ttt_game_dictionary[ctx.channel][0] = Tictactoe(ctx)
            else:
                ttt_game_dictionary[ctx.channel][0:3] = [Tictactoe(ctx), ttt_player_one, ttt_player_two]
            await ctx.channel.send('Type >help to see a list of commands available for tic tac toe.')
            if random.choice([0, 1]) == 1:
                ttt_game_dictionary[ctx.channel][0].ttt_first_player = 2
                if ttt_game_dictionary[ctx.channel][2] is not f'{bot.user.name}':
                    await ctx.channel.send(f'{ttt_game_dictionary[ctx.channel][2].mention} is going first.')
                else:
                    await ctx.channel.send('I am going first.')
                    await Tictactoe.ttt_ai_move(ttt_game_dictionary[ctx.channel][0], ctx)
                    ttt_game_dictionary[ctx.channel][0].ttt_first_player = 1
            else:
                ttt_game_dictionary[ctx.channel][0].ttt_first_player = 1
                await ctx.channel.send(f'{ttt_game_dictionary[ctx.channel][1].mention} is going first.')

            await Tictactoe.ttt_output(ttt_game_dictionary[ctx.channel][0], ctx)
    else:
        await ctx.channel.send('There is already a tic tac toe game in this channel!')
    await bot.add_cog(Tictactoe(ctx), guild=ctx.guild)


class Hangman(commands.Cog):
    """Allows users to play hangman. Use function hangman_start to create game instances.

    Function hangman_custom allows a user to submit their own word and restarts the game with that word as self.word[0].

    Function hangman_check is used to check if the user's guess of a single letter or a full word matches self.word[0].

    Function hangman_wrong is used when a guess is incorrect. It adds a hangman body part to the gallows, and when
    the man is complete, it causes the user to lose the game.

    Function hangman_win is used when the user has successfully guessed the entire word and won the game.

    Function hangman_output uses hangman_guess_filler to display the current state of the word and the man in chat."""

    from module_vars import hangman_vocab, hangman_list

    def __init__(self, ctx):
        self.hangman_image_counter = 0
        self.word = random.choice(self.hangman_vocab)
        self.used_word_list = []
        Hangman.hangman_guess_list(self)

        today_date = datetime.date.today()
        self.game_doc = {'Server': ctx.guild.name,
                         'game': 'Hangman',
                         'guesses': 0, 'date': '%s/%s/%s' % (today_date.month,
                                                             today_date.day,
                                                             today_date.year)}

    # The list that will be used to display the current state of the guessed word is self.guess_list. _ for blanks,
    # letters for correct guesses, and any non-letter characters will already be displayed. self.guess is for
    # actually displaying the state to the user in the chat.
    def hangman_guess_list(self):
        self.guess_list = []
        for item in self.word[0]:
            if item.isalpha():
                self.guess_list.append('_')
            else:
                self.guess_list.append(item)
        Hangman.hangman_guess_filler(self)

    def hangman_guess_filler(self):
        self.guess = '```'
        for item in self.guess_list:
            self.guess += item
            if item != " ":
                self.guess += " "
        self.guess += '```'

    @commands.command(name='hmword',
                      help='Submit a custom word in spoiler tags, ex. ||word||. This will restart the game.')
    async def hangman_custom(self, ctx, *, message):
        hangman_custom_word = ''
        if re.search("[a-zA-Z]", message) is not None:
            if '||' in message.strip():
                for item in message.strip():
                    if item == '|':
                        pass
                    else:
                        hangman_custom_word += item
                await ctx.message.delete()
                if ctx.channel in hm_game_dictionary:
                    hm_game_dictionary[ctx.channel].hangman_image_counter = 0
                    hm_game_dictionary[ctx.channel].word = (hangman_custom_word, '...google it')
                    Hangman.hangman_guess_list(hm_game_dictionary[ctx.channel])
                await ctx.channel.send(f'A new game with {ctx.message.author.mention}\'s custom word is starting.')
                await Hangman.hangman_output(hm_game_dictionary[ctx.channel], ctx.message)
            else:
                await ctx.channel.send("Put your word in spoiler tags next time.")
                pass
        else:
            await ctx.channel.send("There has to be at least one letter to guess in your word.")
            pass

    async def hangman_output(self, message):
        Hangman.hangman_guess_filler(self)
        await message.channel.send(self.hangman_list[self.hangman_image_counter])
        await message.channel.send(self.guess)

    async def hangman_wrong(self, ctx):
        hm_game_dictionary[ctx.channel].hangman_image_counter += 1
        self.game_doc['guesses'] = hm_game_dictionary[ctx.channel].hangman_image_counter
        await Hangman.hangman_output(hm_game_dictionary[ctx.channel], ctx.message)
        if hm_game_dictionary[ctx.channel].hangman_image_counter == 6:
            bot_message = f'Your man is hung. RIP. The word was {hm_game_dictionary[ctx.channel].word[0].lower()}, ' \
                          f'which means {hm_game_dictionary[ctx.channel].word[1]}.'
            await ctx.channel.send(bot_message)
            self.game_doc['status'] = 'Hung'
            self.game_doc['lastplayer'] = ctx.message.author.name
            mongo_db.games.insert_one(self.game_doc)
            await self.hangman_quit_helper(ctx)

    async def hangman_win(self, ctx):
        bot_message = f'Congratulations! You won. The word was {hm_game_dictionary[ctx.channel].word[0].lower()}, ' \
                      f'which means {hm_game_dictionary[ctx.channel].word[1]}.'
        await ctx.channel.send(bot_message)
        self.game_doc['status'] = 'Survived'
        self.game_doc['lastplayer'] = ctx.message.author.name
        mongo_db.games.insert_one(self.game_doc)
        await self.hangman_quit_helper(ctx)

    @commands.command(name='hm',
                      help='Make a guess. Use single letters unless you are confident you know the entire word!')
    async def hangman_check(self, ctx, message):
        if message.strip().isalpha() is False:
            await ctx.channel.send('Use a letter.')
        else:
            if (len(message.strip()) == 1 and message.strip().lower() not in
                    hm_game_dictionary[ctx.channel].used_word_list):
                hm_game_dictionary[ctx.channel].used_word_list.append(message.strip().lower())
                hm_letter_counter = 0
                for letter in range(0, len(hm_game_dictionary[ctx.channel].word[0])):
                    if message[-1].strip().lower() == hm_game_dictionary[ctx.channel].word[0][letter].lower():
                        hm_letter_counter += 1
                        hm_game_dictionary[ctx.channel].guess_list[letter] = hm_game_dictionary[ctx.channel].word[0][
                            letter].upper()
                    else:
                        pass
                if hm_letter_counter == 0:
                    await Hangman.hangman_wrong(hm_game_dictionary[ctx.channel], ctx)
                else:
                    await Hangman.hangman_output(hm_game_dictionary[ctx.channel], ctx.message)
            else:
                if message.strip().lower() in hm_game_dictionary[ctx.channel].used_word_list:
                    await ctx.channel.send('That guess has already been used.')
                    return
                if hm_game_dictionary[ctx.channel].word[0].lower() == message.strip().lower():
                    for letter in range(0, len(hm_game_dictionary[ctx.channel].word[0])):
                        hm_game_dictionary[ctx.channel].guess_list[letter] = hm_game_dictionary[ctx.channel].word[0][
                            letter].upper()
                    await Hangman.hangman_output(hm_game_dictionary[ctx.channel], ctx.message)
                    await Hangman.hangman_win(hm_game_dictionary[ctx.channel], ctx)
                else:
                    hm_game_dictionary[ctx.channel].used_word_list.append(message.strip().lower())
                    await Hangman.hangman_wrong(hm_game_dictionary[ctx.channel], ctx)
            if '_' not in hm_game_dictionary[ctx.channel].guess_list:
                await Hangman.hangman_win(hm_game_dictionary[ctx.channel], ctx)

    @commands.command(name='hmquit', help='Quit the current hangman game.')
    async def hangman_quit(self, ctx):
        await self.hangman_quit_helper(ctx)

    async def hangman_quit_helper(self, ctx):
        if ctx.channel in hm_game_dictionary:
            hm_game_dictionary.pop(ctx.channel, None)
            await ctx.channel.send('The hangman game has ended.')
        else:
            await ctx.channel.send('There is currently no hangman game in this channel.')
        await bot.remove_cog('Hangman', guild=ctx.guild)


@bot.command(name='hmstart', help='Starts a game of hangman.')
async def hangman_start(ctx):
    if ctx.channel not in hm_game_dictionary:
        hm_game_dictionary[ctx.channel] = Hangman(ctx)
        await ctx.channel.send('Type >help to see a list of commands available for hangman.')
        await Hangman.hangman_output(hm_game_dictionary[ctx.channel], ctx.message)
    else:
        await ctx.channel.send('There is already a hangman game in this channel!')
    await bot.add_cog(Hangman(ctx), guild=ctx.guild)


@bot.event
async def on_ready():
    global settings
    global guild
    ready_message = f'{bot.user.name} just woke up! Type ">help" for a basic command list.'
    channel = discord.utils.get(bot.get_all_channels(), name='playfriend')
    guild = channel.guild
    old_settings = mongo_db.settings.find_one({"guild": guild.id})
    if old_settings:
        settings = old_settings['settings']
    else:
        mongo_db.settings.insert_one({"guild": guild.id, "settings": settings})
    if settings['sky']['sky']:
        channel = bot.get_channel(settings['sky']['channel'])
        await bot.add_cog(SkyTracker(bot, channel), guild=channel.guild)
    await channel.send(ready_message)


geyser_times = [
    datetime.time(hour=6, minute=55),
    datetime.time(hour=8, minute=55),
    datetime.time(hour=10, minute=55),
    datetime.time(hour=12, minute=55),
    datetime.time(hour=14, minute=55),
    datetime.time(hour=16, minute=55),
    datetime.time(hour=18, minute=55),
    datetime.time(hour=20, minute=55),
    datetime.time(hour=22, minute=55),
    datetime.time(hour=0, minute=55),
    datetime.time(hour=2, minute=55),
    datetime.time(hour=4, minute=55)
]

grandma_times = [
    datetime.time(hour=7, minute=25),
    datetime.time(hour=9, minute=25),
    datetime.time(hour=11, minute=25),
    datetime.time(hour=13, minute=25),
    datetime.time(hour=15, minute=25),
    datetime.time(hour=17, minute=25),
    datetime.time(hour=19, minute=25),
    datetime.time(hour=21, minute=25),
    datetime.time(hour=23, minute=25),
    datetime.time(hour=1, minute=25),
    datetime.time(hour=3, minute=25),
    datetime.time(hour=5, minute=25)
]

reset_time = datetime.time(hour=7, minute=1)


@bot.command(name='skytrack', help='Starts Sky: Children of Light event tracking.')
async def sky_start(ctx):
    message = f'Starting Sky tracking.'
    channel = discord.utils.get(bot.get_all_channels(), name=ctx.channel.name)
    await channel.send(message)
    settings["sky"]["sky"] = True
    settings["sky"]["channel"] = channel.id
    mongo_db.settings.find_one_and_update({"guild": guild.id}, {'$set': {"settings": settings}})
    await bot.add_cog(SkyTracker(bot, ctx), guild=ctx.guild)


class SkyTracker(commands.Cog, name="Sky: Children of Light"):
    def __init__(self, self_bot, ctx):
        self.bot = self_bot
        if settings['sky']['geyser']:
            self.geyser_time_tracking.start()
        if settings['sky']['grandma']:
            self.grandma_time_tracking.start()
        if settings['sky']['channel'] is None:
            self.sky_channel = ctx.channel
            settings['channel'] = ctx.channel.id
        else:
            self.sky_channel = self.bot.get_channel(settings['sky']['channel'])
        # setting the URL you want to monitor
        self.url_shard = 'https://sky-shards.pages.dev/en'
        self.url = Request('https://sky-children-of-the-light.fandom.com/wiki/Seasonal_Events',
                           headers={'User-Agent': 'Mozilla/5.0'})
        self.url_ts = Request('https://sky-children-of-the-light.fandom.com/wiki/Spirit_Visits',
                              headers={'User-Agent': 'Mozilla/5.0'})
        self.month_mapper = {
            1: 'January',
            2: 'February',
            3: 'March',
            4: 'April',
            5: 'May',
            6: 'June',
            7: 'July',
            8: 'August',
            9: 'September',
            10: 'October',
            11: 'November',
            12: 'December'
        }
        self.base_url = "https://sky-children-of-the-light.fandom.com"
        self.driver = webdriver.Chrome(options=options)
        self.converted_times = []
        self.shard_message = ""
        self.jobs = []

        self.check_daily.start()
        self.check_shard.start()
        self.check_ts.start()

    @commands.command(name='skygeyser', help='Enables/disables Geyser monitoring.')
    async def sky_geyser(self, ctx):
        if self.geyser_time_tracking.is_running:
            self.geyser_time_tracking.stop()
            settings["sky"]["geyser"] = False
        else:
            self.geyser_time_tracking.start()
            settings["sky"]["geyser"] = True
        mongo_db.settings.find_one_and_update({"guild": guild.id}, {'$set': {"settings": settings}})

    @commands.command(name='skygrandma', help='Enables/disables Grandma monitoring.')
    async def sky_grandma(self, ctx):
        if self.grandma_time_tracking.is_running:
            self.grandma_time_tracking.stop()
            settings["sky"]["grandma"] = False
        else:
            self.grandma_time_tracking.start()
            settings["sky"]["grandma"] = True
        mongo_db.settings.find_one_and_update({"guild": guild.id}, {'$set': {"settings": settings}})

    @commands.command(name='skych', help='Controls what channel Sky messages will be sent to.')
    async def sky_channel(self, ctx):
        ready_message = f'Sky messages will only be sent to this channel.'
        self.sky_channel = ctx.channel
        mongo_db.settings.find_one_and_update({"guild": guild.id}, {'$set': {"settings": settings}})
        await self.sky_channel.send(ready_message)

    @commands.command(name='daily', help="Check today's seasonal candle locations.")
    async def check_daily_triggered(self, ctx):
        await self.check_daily()

    @commands.command(name='shard', help="Check today's shards.")
    async def check_shard_triggered(self, ctx):
        await self.send_shard_msg(datetime.datetime.now())

    @commands.command(name='ts', help="Check if there is news about the next traveling spirit.")
    async def check_ts_triggered(self, ctx):
        await self.check_ts()

    @commands.command(name='skyquit', help='Stop Sky tracking.')
    async def sky_quit(self, ctx):
        settings["sky"]["sky"] = False
        mongo_db.settings.find_one_and_update({"guild": guild.id}, {'$set': {"settings": settings}})
        message = f'Turning off Sky notifications.'
        await self.sky_channel.send(message)
        await bot.remove_cog("SkyTracker", guild=ctx.guild)

    def cog_unload(self):
        self.geyser_time_tracking.cancel()
        self.grandma_time_tracking.cancel()
        self.check_daily.cancel()
        self.check_shard.cancel()
        self.clear_jobs()

    @tasks.loop(time=geyser_times)
    async def geyser_time_tracking(self):
        message = f'Geyser is in 10 minutes. Head to Sanctuary Islands in Daylight Prairie!'
        await self.sky_channel.send(message, delete_after=600)

    @tasks.loop(time=grandma_times)
    async def grandma_time_tracking(self):
        message = f'Grandma is in 10 minutes. Head to the Elevated Clearing in Hidden Forest!'
        await self.sky_channel.send(message, delete_after=600)

    @tasks.loop(time=reset_time)
    async def check_daily(self):
        response = urlopen(self.url).read().decode('utf-8')
        index = response.index('<a href="/wiki/Season_of_')
        if index != -1:
            quote_index = response[index + 9:].index('"')
            response = urlopen(self.base_url + response[index + 9:index + 9 + quote_index]).read().decode('utf-8')
            month = self.month_mapper[datetime.datetime.now().month]
            day = datetime.datetime.now().day
            today = month + " " + str(day)
            match = re.search(r"<b>(.*" + today + ".*)</b>", response, re.IGNORECASE)
            if not match:
                match = re.search(r"<b>(.*andle rotation .*)</b>", response, re.IGNORECASE)
            if not match:
                match = re.search(r"<b>(.*Today's .*)</b>", response, re.IGNORECASE)
            if match:
                message = match.group(1)
                location = re.search(r"otation . in (.*)\.", message).group(1)
                if not location:
                    location = re.search(r"in (.*).", message).group(1)
                if location:
                    words = location.split(" ")
                    img_url = str(
                        re.search(r'(https://static\.wikia\.nocookie\.net/sky-children-of-the-light/images/./../' +
                                  words[0] + '.*/)revision/.*=\d{14}.*\" title=\"' + words[0],
                                  response[match.end():],
                                  re.IGNORECASE).groups(1))
                    if img_url:
                        message = message + "\n" + img_url[2:-3]
                print(f"[{datetime.datetime.now()}] [INFO    ] ", "time until message deletion: ",
                      time_until_end_of_day(), file=sys.stderr)
                await self.sky_channel.send(message, delete_after=time_until_end_of_day())
            else:
                print(f"[{datetime.datetime.now()}] [INFO    ] ", "failed to find candle rotation", file=sys.stderr)
        else:
            print(f"[{datetime.datetime.now()}] [INFO    ] ", "failed to find current season", file=sys.stderr)

    async def send_shard_msg(self, time_to_wait):
        await discord.utils.sleep_until(time_to_wait)
        if self.shard_message == "":
            await self.check_shard()
        else:
            message = self.shard_message
            if len(self.converted_times) > 0:
                now_dt = datetime.datetime.now()
                deletion_time = None
                if now_dt < self.converted_times[1][1]:
                    message += f"1st shard: <t:{self.converted_times[0][0]}:t> to <t:{self.converted_times[1][0]}:t>\n"
                    if not deletion_time:
                        deletion_time = int((self.converted_times[1][1] - now_dt).total_seconds())
                if now_dt < self.converted_times[3][1]:
                    message += f"2nd shard: <t:{self.converted_times[2][0]}:t> to <t:{self.converted_times[3][0]}:t>\n"
                    if not deletion_time:
                        deletion_time = int((self.converted_times[3][1] - now_dt).total_seconds())
                if now_dt < self.converted_times[5][1]:
                    message += f"3rd shard: <t:{self.converted_times[4][0]}:t> to <t:{self.converted_times[5][0]}:t>\n"
                    if not deletion_time:
                        deletion_time = int((self.converted_times[5][1] - now_dt).total_seconds())
                if now_dt >= self.converted_times[5][1]:
                    message += "All shard windows have passed for today.\n"
                    if not deletion_time:
                        deletion_time = time_until_end_of_day()
                message += self.url_shard
            else:
                deletion_time = time_until_end_of_day()

            print(f"[{datetime.datetime.now()}] [INFO    ] ", "time until message deletion: ",
                  deletion_time, file=sys.stderr)
            await self.sky_channel.send(message, delete_after=deletion_time)

    def clear_jobs(self):
        for task in self.jobs:
            task.cancel()
        self.jobs = []

    @tasks.loop(time=reset_time)
    async def check_shard(self):
        self.converted_times = []
        self.shard_message = ""
        self.clear_jobs()

        self.driver.get(self.url_shard)
        bold_class = self.driver.find_elements(By.CLASS_NAME, 'font-bold')

        times = self.driver.find_elements(By.XPATH, "//*[contains(text(), ':')]")
        pattern = re.compile("..:.. (A|P)M")
        filtered_times = [element for element in times if pattern.search(element.text)]
        if bold_class[0].text.startswith("N"):
            self.shard_message = (f"Today there are no shard eruptions.\n" + self.url_shard)
        else:
            if bold_class[0].text.startswith("R"):
                item = "ascended candles"
            else:
                item = "cakes of wax"
            reward = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Giving')]").text
            num_list = re.findall(r'\d+\.?\d?', reward)
            converted_times = []
            now = str(datetime.datetime.now()).split(" ")[0]
            for i in range(2, 8):
                start = datetime.datetime.strptime(now + " " + filtered_times[i].text, '%Y-%m-%d %I:%M %p')
                seconds = round(start.timestamp())
                converted_times.append((seconds, start))

            self.converted_times = converted_times
            self.shard_message = (f"Today's {bold_class[0].text} is in {bold_class[1].text}, {bold_class[2].text}."
                                  f" The reward is {num_list[0]} {item}.\n")

            for i in range(0, len(self.converted_times), 2):
                await asyncio.create_task(self.send_shard_msg(self.converted_times[i][1]))

        await self.send_shard_msg(datetime.datetime.now())

    @tasks.loop(time=reset_time)
    async def check_ts(self):
        response = urlopen(self.url_ts).read().decode('utf-8')
        index = response.index('<td><a href="/wiki/')
        if index != -1:
            quote_index = response[index + 13:].index('"')
            spirit_url = self.base_url + response[index + 13:index + 13 + quote_index]
            spirit = response[index + 19:index + 13 + quote_index].replace("_", " ")
            match = re.search(r"[A-Za-z]{3} \d?\d, \d\d\d\d", response[index + 13:index + 1013], re.IGNORECASE)
            if match:
                date = match.group(0)
                converted_date = datetime.datetime.strptime(date, '%b %d, %Y')
                end_date = converted_date + datetime.timedelta(days=4)
                time_to_delete = int((end_date - datetime.datetime.now()).total_seconds())
                if time_to_delete > 0:
                    print(f"[{datetime.datetime.now()}] [INFO    ] ", "time until message deletion: ",
                          time_to_delete, file=sys.stderr)
                    message = (
                        f"The next traveling spirit is {spirit} from {date} to {end_date.strftime('%b %d, %Y')}.\n"
                        f"{spirit_url}")
                    await self.sky_channel.send(message, delete_after=time_until_end_of_day())
                else:
                    message = (
                        f"The last traveling spirit was {spirit} from {date} to {end_date.strftime('%b %d, %Y')}.\n"
                        f"The next traveling spirit has not been announced yet.\n"
                        f"{spirit_url}")
                    await self.sky_channel.send(message, delete_after=time_until_end_of_day())
            else:
                print(f"[{datetime.datetime.now()}] [INFO    ] ", "failed to find date of next spirit", file=sys.stderr)
                message = (f"The next traveling spirit is {spirit}.\n"
                           f"{spirit_url}")
                await self.sky_channel.send(message, delete_after=345600)
        else:
            print(f"[{datetime.datetime.now()}] [INFO    ] ", "failed to find last traveling spirit", file=sys.stderr)


# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return
#     if message.content == 'hi':
#         await message.channel.send('<:rip:280861016911380480>')
#
#     await bot.process_commands(message)


bot.run(TOKEN)
