import os
import random
import discord
import emojis
import re
from discord.ext import commands
from discord.ext.commands import Bot
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = Bot(command_prefix='>')
hm_game_dictionary = {}
ttt_game_dictionary = {}


class Dungeon(commands.Cog):
    """Docs here"""


    #class Mage:
    #    def __init__(self):
    #        self.armorType = cloth


    #class Priest:


    #class Warrior:


    #class Archer:


    #class Thief:

    #@commands.command(name='dsetup', help='Start a new Dungeon session.')
    #async def dungeon_setup(self, ctx):
    #    bot.add_cog(Dungeon())

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
                elif tt_list[offset] == 2:
                    if ttt_game_dictionary[ctx.channel][2] is not f'{bot.user.name}':
                        await ctx.channel.send(f'{ttt_game_dictionary[ctx.channel][2].mention} has won the game!')
                    else:
                        await ctx.channel.send('Better luck next time!')
                await Tictactoe.ttt_quit(ttt_game_dictionary[ctx.channel], ctx)
                return
        for column in range(0, 3):
            if tt_list[column] == tt_list[column + 3] and tt_list[column + 3] == tt_list[column + 6]:
                if tt_list[column] == 0:
                    return
                elif tt_list[column] == 1:
                    await ctx.channel.send(f'{ttt_game_dictionary[ctx.channel][1].mention} has won the game!')
                elif tt_list[column] == 2:
                    if ttt_game_dictionary[ctx.channel][2] is not f'{bot.user.name}':
                        await ctx.channel.send(f'{ttt_game_dictionary[ctx.channel][2].mention} has won the game!')
                    else:
                        await ctx.channel.send('Better luck next time!')
                await Tictactoe.ttt_quit(ttt_game_dictionary[ctx.channel], ctx)
                return
        if (tt_list[0] == tt_list[4] and tt_list[4] == tt_list[8]) or (tt_list[2] == tt_list[4] and tt_list[4] == tt_list[6]):
            if tt_list[4] == 0:
                return
            elif tt_list[4] == 1:
                await ctx.channel.send(f'{ttt_game_dictionary[ctx.channel][1].mention} has won the game!')
            elif tt_list[4] == 2:
                if ttt_game_dictionary[ctx.channel][2] is not f'{bot.user.name}':
                    await ctx.channel.send(f'{ttt_game_dictionary[ctx.channel][2].mention} has won the game!')
                else:
                    await ctx.channel.send('Better luck next time!')
            await Tictactoe.ttt_quit(ttt_game_dictionary[ctx.channel], ctx)
            return
        if 0 not in tt_list:
            await ctx.channel.send('It\'s a tie!')
            await Tictactoe.ttt_quit(ttt_game_dictionary[ctx.channel], ctx)

    @commands.command(name='ttsetup', help='Customize the marker you place on the board. Type bot after to randomize the bot marker.')
    async def ttt_game_setup(self, ctx, message='not bot'):

        def ttt_get_emoji(emoji_response):
            return ctx.channel == emoji_response.channel and ctx.message.author == emoji_response.author and\
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
        bot.remove_cog('Tictactoe')

    @commands.command(name='tt', help="To mark a square, type >tt # according to the grid.")
    async def ttt_mark_square(self, ctx, message):
        if ctx.message.author == ttt_game_dictionary[ctx.channel][1] or ctx.message.author == ttt_game_dictionary[ctx.channel][2]:
            if int(message.strip()) in range(1, 10):
                if ttt_game_dictionary[ctx.channel][0].tt_board_list[int(message.strip()) - 1] == 0:
                    if ctx.message.author == ttt_game_dictionary[ctx.channel][1] and ttt_game_dictionary[ctx.channel][0].ttt_first_player == 1:
                        ttt_game_dictionary[ctx.channel][0].tt_board_list[int(message.strip()) - 1] = 1
                        ttt_game_dictionary[ctx.channel][0].ttt_first_player = 2
                    elif ctx.message.author == ttt_game_dictionary[ctx.channel][2] and ttt_game_dictionary[ctx.channel][0].ttt_first_player == 2:
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
            if ttt_game_dictionary[ctx.channel][2] is f'{bot.user.name}' and 0 in ttt_game_dictionary[ctx.channel][0].tt_board_list and ttt_game_dictionary[ctx.channel][0].ttt_first_player == 2:
                await Tictactoe.ttt_ai_move(ttt_game_dictionary[ctx.channel][0], ctx)
                ttt_game_dictionary[ctx.channel][0].ttt_first_player = 1
                await Tictactoe.ttt_output(ttt_game_dictionary[ctx.channel][0], ctx)


@bot.command(name='ttstart', help='Starts a game of tic tac toe.')
async def ttt_start(ctx):

    def ttt_get_players(num_response):
        # Check to make sure the game starter is answering the question.
        return ctx.message.author == num_response.author and ctx.channel == num_response.channel and \
               num_response.content.lower().strip() in ['1', '2', 'one', 'two', '1p', '2p']

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
            if response.content.lower().strip() in ['1', 'one', '1p']:
                ttt_player_one = response.author
                ttt_player_two = f'{bot.user.name}'
                ttt_players = 1
            elif response.content.lower().strip() in ['2', 'two', '2p']:
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
    bot.add_cog(Tictactoe(ctx))


class Hangman(commands.Cog):
    """Allows users to play hangman. Use function hangman_start to create game instances.

    Function hangman_custom allows a user to submit their own word and restarts the game with that word as self.word[0].

    Function hangman_check is used to check if the user's guess of a single letter or a full word matches self.word[0].

    Function hangman_wrong is used when a guess is incorrect. It adds a hangman body part to the gallows, and when
    the man is complete, it causes the user to lose the game.

    Function hangman_win is used when the user has successfully guessed the entire word and won the game.

    Function hangman_output uses hangman_guess_filler to display the current state of the word and the man in chat."""

    from module_vars import hangman_vocab, hangman_list

    def __init__(self):
        self.hangman_image_counter = 0
        self.word = random.choice(self.hangman_vocab)
        self.used_word_list = []
        Hangman.hangman_guess_list(self)

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

    @commands.command(name='hmword', help='Submit a custom word in spoiler tags, ex. ||word||. This will restart the game.')
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
        await Hangman.hangman_output(hm_game_dictionary[ctx.channel], ctx.message)
        if hm_game_dictionary[ctx.channel].hangman_image_counter == 6:
            bot_message = f'Your man is hung. RIP. The word was {hm_game_dictionary[ctx.channel].word[0].lower()}, ' \
                          f'which means {hm_game_dictionary[ctx.channel].word[1]}.'
            await ctx.channel.send(bot_message)
            hm_game_dictionary.pop(ctx.channel, None)

    async def hangman_win(self, ctx):
        bot_message = f'Congratulations! You won. The word was {hm_game_dictionary[ctx.channel].word[0].lower()}, ' \
                      f'which means {hm_game_dictionary[ctx.channel].word[1]}.'
        await ctx.channel.send(bot_message)
        hm_game_dictionary.pop(ctx.channel, None)

    @commands.command(name='hm', help='Make a guess. Use single letters unless you are confident you know the entire word!')
    async def hangman_check(self, ctx, message):
        if message.strip().isalpha() is False:
            await ctx.channel.send('Use a letter.')
        else:
            if len(message.strip()) == 1 and message.strip().lower() not in hm_game_dictionary[ctx.channel].used_word_list:
                hm_game_dictionary[ctx.channel].used_word_list.append(message.strip().lower())
                hm_letter_counter = 0
                for letter in range(0, len(hm_game_dictionary[ctx.channel].word[0])):
                    if message[-1].strip().lower() == hm_game_dictionary[ctx.channel].word[0][letter].lower():
                        hm_letter_counter += 1
                        hm_game_dictionary[ctx.channel].guess_list[letter] = hm_game_dictionary[ctx.channel].word[0][letter].upper()
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
                        hm_game_dictionary[ctx.channel].guess_list[letter] = hm_game_dictionary[ctx.channel].word[0][letter].upper()
                    await Hangman.hangman_output(hm_game_dictionary[ctx.channel], ctx.message)
                    await Hangman.hangman_win(hm_game_dictionary[ctx.channel], ctx)
                else:
                    hm_game_dictionary[ctx.channel].used_word_list.append(message.strip().lower())
                    await Hangman.hangman_wrong(hm_game_dictionary[ctx.channel], ctx)
            if '_' not in hm_game_dictionary[ctx.channel].guess_list:
                await Hangman.hangman_win(hm_game_dictionary[ctx.channel], ctx)

    @commands.command(name='hmquit', help='Quit the current hangman game.')
    async def hangman_quit(self, ctx):
        if ctx.channel in hm_game_dictionary:
            hm_game_dictionary.pop(ctx.channel, None)
            await ctx.channel.send('The hangman game has ended.')
        else:
            await ctx.channel.send('There is currently no hangman game in this channel.')
        bot.remove_cog('Hangman')


@bot.command(name='hmstart', help='Starts a game of hangman.')
async def hangman_start(message):
    if message.channel not in hm_game_dictionary:
        hm_game_dictionary[message.channel] = Hangman()
        await message.channel.send('Type >help to see a list of commands available for hangman.')
        await Hangman.hangman_output(hm_game_dictionary[message.channel], message)
    else:
        await message.channel.send('There is already a hangman game in this channel!')
    bot.add_cog(Hangman())


@bot.event
async def on_ready():
    ready_message = f'{bot.user.name} is here! Type ">help" for a basic command list.'
    channel = discord.utils.get(bot.get_all_channels(), name='playfriend')
    await channel.send(ready_message)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == 'hi':
        await message.channel.send('<:rip:280861016911380480>')

    await bot.process_commands(message)


bot.run(TOKEN)
