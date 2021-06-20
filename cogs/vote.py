import discord
from discord.ext import commands

# these imports are no longer necessary
#import aiohttp
import asyncio


def setup(bot):
    bot.add_cog(Vote(bot))

class ConvertEmoji(commands.EmojiConverter):
    async def convert(self, ctx, argument):
        emoji = await super().convert(ctx,argument)
        return(emoji)


class Vote(commands.Cog):
    def __init__(self, bot):
        """Help for calling Vote"""
        # Creating this variable once, so we don't have to create it
        # everytime we call callvote()
        self.special_char = '''!"#$%&'()*+,-./:;<=>?@[\]^_`{}|~'''

        #self.session = aiohttp.ClientSession(loop=bot.loop)
        self.bot = bot
        print('Cog "{}" loaded.'.format(self.__class__.__name__))


    @commands.command()
    async def callvote(self, ctx, *args):
        """{question} *{emojis}"""
        question = 'vote: '
        reactions = []


        # find if we're looking at the question or the emoji
        # supplying for user error, doing a little extra to cut out the kinks
        for i in args:
            # if we're looking at the question, then add it to the question str
            if i.strip(self.special_char).isalnum():
                question += i + ' '
            # else if we're looking at an emoji, then add it to the reactions list
            else:
                print('appending', i)
                print('print ctx', ctx)
                emoji = commands.EmojiConverter().convert(self, ctx = ctx, argument = i)
                reactions.append(emoji)
                

        print("\n\nprinting reactions")
        for i in reactions:
            print(i)

        # https://gist.github.com/Vexs/f2c1bfd6bda68a661a71accd300d2adc
        # create a discord.Embed object to nicely create a voting poll
        #embed = discord.Embed(title = question, description = ' '.join(reactions))
        embed = discord.Embed(title = question, description = 'a description')
        embed.color = 14423100

        # migrating to v1
        #react_message = await self.bot.say(embed=embed)
        react_message = await ctx.send(embed=embed)


        # add each reaction from the reactions list to the message's reactions
        for reaction in reactions:

            #await self.bot.add_reaction(react_message, reaction)
            # migrating to v1
            
            print('adding reaction to message:', reaction)

            try:
                #await discord.Message.add_reaction(react_message, reaction)
                await react_message.add_reaction(reaction)
            #except discord.HTTPException:
            except:
                print("HTTP exception occurred")
                #await react_message.add_reaction('<:python3:232720527448342530>')



        # give the embed a poll id inside of the footer, so users know which poll this is
        embed.set_footer(text='Poll ID: {}'.format(react_message.id))

        #await self.bot.edit_message(react_message, embed=embed)
        # migrating to v1
        await react_message.edit(embed=embed)


        # sleep for a little for reactions to be made
        await asyncio.sleep(30)

        # redefining reactions variable here because we don't need the old one anymore
        # ctx.message.channel gets the message's channel from earlier

        #reactions = (await self.bot.get_message(ctx.message.channel, react_message.id)).reactions
        # migrating to v1
        reactions = (await ctx.channel.fetch_message(react_message.id)).reactions
        
        reaction_lot = []

        # get each discord.Reaction object and reaction.count int value, and store them inside
        # of a tuple inside of a list. ex: [(discord.Reaction, int)]
        # ps: using a dictionary wont work
        for reaction in reactions:
            reaction_lot.append((reaction, reaction.count))

        # Sorting reaction_lot by the 2nd value in each tuple inside the list, in reverse
        reaction_lot.sort(key=lambda tup: tup[1], reverse=True)

        # output the winning reactions
        # put the reaction_lot into a useable format
        results = []
        for i in range(len(reaction_lot)):
            results.append('\n\n' + reaction_lot[i][0].emoji + ' ' + str(reaction_lot[i][1]))

        # embed the content, again, into a nice format
        embed = discord.Embed(title = 'RESULTS for: ' + question, description = ''.join(results))
        embed.color = 43878
        embed.set_footer(text='Poll ID: {}'.format(react_message.id))

        # finally... let the bot output the results


        #await self.bot.say(embed = embed)
        # migrating to v1
        await ctx.send(embed=embed)

