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
async def vouch(interaction: discord.Interaction, message: str, moons: int):
    if 1 <= moons <= 5:
        vouch_data = {
            'user': interaction.user.name,
            'message': message,
            'moons': moons,
            'date': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        }

        moon_emojis = ' :crescent_moon:' * moons

        embed = discord.Embed(
            title='Title',
            description=f'{moon_emojis}',
            color=0x66FFFF
        )
        embed.add_field(name='Message', value=message, inline=True)
        embed.add_field(name='', value='', inline=False)

        embed.add_field(name='Vouched by', value=f'{interaction.user.name}', inline=True)
        embed.add_field(name='Vouched at', value=vouch_data['date'], inline=True)
        embed.set_footer(text=f'Thank you for vouching! • {vouch_data["date"]}')

        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message('Invalid star rating. Please provide a rating between 1 and 5.')

bot.run("TOKEN")
