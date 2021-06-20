import discord
from discord.ext import commands
import asyncio


def setup(bot):
    bot.add_cog(Vote(bot))

class Vote(commands.Cog):
    def __init__(self, bot):
        """Help for calling Vote"""
        self.special_char = '''!"#$%&'()*+,-./:;<=>?@[\]^_`{}|~'''
        self.bot = bot
        print('Cog "{}" loaded.'.format(self.__class__.__name__))


    @commands.command()
    async def callvote(self, ctx, *args):
        """{question} {emoji} {emoji}\n Outside server emojis will not work"""
        question = ''
        reactions = []


        # find if we're looking at the question or the emoji
        for i in args:
            # strip leading and trailing characters and check if the word is alphanumeric
            # this mostly works for what we want, but there are still some bugs with it
            if i.strip(self.special_char).isalnum():
                question += i + ' '
            # else if emoji, add to reactions list
            else:
                reactions.append(i)


        # create embed
        embed = discord.Embed(title = question, description = 'React using the emojis below to vote!')
        embed.color = 14423100

        # send embed to channel
        react_message = await ctx.send(embed=embed)


        # add each reaction from the reactions list to the message's reactions
        for reaction in reactions:
            try:
                await react_message.add_reaction(reaction)
            except discord.HTTPException:
                print("emoji", str(reaction), "not found - todo")


        # add id to poll embed
        # adding a poll id clutters up the embed object, commenting this out for now
        #embed.set_footer(text='Poll ID: {}'.format(react_message.id))
        #await react_message.edit(embed=embed)


        # sleep for some time
        await asyncio.sleep(5)

        # get reaction results from the original embed
        reactions = (await ctx.channel.fetch_message(react_message.id)).reactions

        # Sorting reactions by their count value from highest to lowest
        reactions.sort(key=lambda tup: tup.count, reverse=True)

        # output the winning reactions
        results = []
        for i in reactions:
            results.append('\n\n' + str(i.emoji) + ' ' + str(i.count))

        # embed the content, again, into a nice format
        embed = discord.Embed(title = '__RESULTS FOR: ' + question + '__', description = ''.join(results))
        embed.color = 43878
        embed.set_footer(text='Poll ID: {}'.format(react_message.id))

        # update embed with new content
        await ctx.send(embed=embed)