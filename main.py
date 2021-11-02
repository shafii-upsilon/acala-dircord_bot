from discord_components import ComponentsBot
from question import Questions

bot = ComponentsBot(command_prefix='/')
bot.add_cog(Questions(bot))

bot.run('OTA1MDY5NDUzODk1NjcxODQ4.YYEtnQ.ZAwzvFRjn3krY-_ISPP1PwpPBDk')
# bot.run('OTA0NDIwOTg2OTA3MTY0NzQy.YX7Rrg.RkuuXz1sDpCm7CCMYdqddpn6dr0')