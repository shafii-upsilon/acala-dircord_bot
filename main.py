from discord_components import ComponentsBot
from question import Questions

bot = ComponentsBot(command_prefix='/')
bot.add_cog(Questions(bot))

bot.run('')
