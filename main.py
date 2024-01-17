import discord
from discord.ext import commands
from discord import app_commands
import time
from datetime import datetime

bot = commands.Bot(command_prefix=';', intents=discord.Intents.all())

@bot.event
async def on_ready():
    try:
        s = await bot.tree.sync()
        print(f'Synced {len(s)} commands')
    except Exception as e:
        print(f'Error syncing commands: {e}')

    print(f'Logged in as {bot.user.name}')


@bot.tree.command(name='vouch', description='Vouch for someone with a message and star rating')
async def vouch(interaction: discord.Interaction, message: str, stars: int, image_url: str=''):
    if 1 <= stars <= 5:
        vouch_data = {
            'user': interaction.user.name,
            'message': message,
            'stars': stars,
            'date': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'),
            'image': image_url
        }

        star_emojis = ' :star:' * stars

        embed = discord.Embed(
            title='Title',
            description=f'{star_emojis}',
            color=0x66FFFF
        )
        embed.add_field(name='Message', value=message, inline=True)
        embed.add_field(name='', value='', inline=False)

        embed.add_field(name='Vouched by', value=f'{interaction.user.name}', inline=True)
        embed.add_field(name='Vouched at', value=vouch_data['date'], inline=True)
        embed.add_field(name='', value='', inline=False)

        if vouch_data['image'] is not None:
            embed.set_image(url=vouch_data['image'])


        embed.set_footer(text=f'Thank you for vouching! • {vouch_data["date"]}')

        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message('Invalid star rating. Please provide a rating between 1 and 5.')

bot.run("TOKEN")
