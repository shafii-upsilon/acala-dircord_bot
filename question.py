import re
import discord
import asyncio
from discord.ext import commands
from discord.ext.commands.core import check, command
from discord_components import Button, ButtonStyle, ActionRow, Interaction
from models import Question
from tortoise import Tortoise
from db import init_db

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def remove_punctuation(string):
    return re.sub(r'[^\w\s]','', string)

class Questions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.disappointed_message = 'Unfortunately I cannot help you 😞. Maybe you want to ask something else?'

    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    #     if ctx.author.bot:
    #         return

    #     print(error)
        
    #     await ctx.channel.send(self.disappointed_message)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Acala bot is ready')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        await ctx.send('Hello {0.name}'.format(member))
    
    async def get_msg(self, ctx, title):
        await ctx.send(title)
        msg = await self.bot.wait_for('message')
        text = msg.content
        if text.replace('/', '') in self.bot.all_commands.keys():
            return
        else:
            msg.content = 'action'

        return text

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def q(self, ctx):
        await ctx.send('Canceled')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_question(self, ctx):
        question_text = await self.get_msg(ctx, 'Please enter your question:')

        if not question_text:
            return

        answer_text = await self.get_msg(ctx, 'Please enter answer:')

        if not answer_text:
            return

        await init_db()
        new_question = Question(
            question=question_text,
            answer=answer_text,
            user=ctx.author
        )
        await new_question.save()
        await Tortoise.close_connections()

        await ctx.send('Question successfully created!')

    @add_question.error
    async def add_question_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Not permited')
        else:
            await ctx.send('Something went wrong')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.content.lower().strip() or re.match(r'$', message.content):
            return
        
        message_text = message.content
        message_text = remove_punctuation(message_text.lower().strip())

        if message_text in self.bot.all_commands.keys():
            return
        
        if message_text == 'action':
            return

        await init_db()

        questions = await Question.all()
        questions_text = [remove_punctuation(q.question.lower().strip()) for q in questions]

        await Tortoise.close_connections()

        if message_text in questions_text:
            embed = discord.Embed(description=questions[questions_text.index(message_text)].answer)
            await message.channel.send(embed=embed)
        else:
            message_text = message_text.split(' ')
            values = [(i, len(intersection(qt.split(' ') , message_text))) for i, qt in enumerate(questions_text) if len(intersection(qt.split(' ') , message_text)) > 0]
            values.sort(reverse=True, key=lambda e: e[1])
            if not values:
                await message.channel.send(self.disappointed_message)
            else:
                async def callback(interaction: Interaction):
                    if interaction.custom_id == 'yes':
                        embed = discord.Embed(description=questions[values[0][0]].answer)
                        await interaction.send(embed=embed)
                    elif interaction.custom_id == 'no':
                        await interaction.send(self.disappointed_message)
                    else:
                        embeds = []
                        for value in values:
                            embed = discord.Embed(description=questions[value[0]].question)
                            embeds.append(embed)
                            
                        await interaction.send(embeds=embeds)

                await message.channel.send(
                    'Maybe you meant: "{0}"?'.format(questions[values[0][0]].question),
                    components=[
                        ActionRow(
                            self.bot.components_manager.add_callback(
                                Button(style=ButtonStyle.green, label='Yes', id='yes'), callback
                            ),
                            self.bot.components_manager.add_callback(
                                Button(style=ButtonStyle.red, label='No', id='no'), callback
                            ),
                            self.bot.components_manager.add_callback(
                                Button(style=ButtonStyle.grey, label='Show another variants', id='show_another'), callback
                            )
                        )
                    ],
                )
