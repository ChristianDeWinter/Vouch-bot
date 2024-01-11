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

@bot.tree.command(name='hello', description='Hello World!')
async def hello(interaction: discord.Interaction):
    # Send a message:
    await interaction.response.send_message('Hello World!')

@bot.tree.command(name='say', description='I\'ll repeat what you want to say!')
@app_commands.describe(what_to_say='The message you want me to say!')
async def say(interaction: discord.Interaction, what_to_say: str):
    await interaction.response.send_message(f'{what_to_say} - **{interaction.user.display_name}**')


@bot.tree.command(name='vouch', description='Vouch for someone with a message and star rating')
async def vouch(interaction: discord.Interaction, message: str, moons: int):
    if 1 <= moons <= 5:
        # Process the vouch, for example, you can save it to a database
        # You can customize this part based on your needs
        vouch_data = {
            'user': interaction.user.name,
            'message': message,
            'moons': moons,
            'date': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        }

        # Generate the moon emojis based on the number of moons
        moon_emojis = ' :crescent_moon:' * moons

        # Generate the embed
        embed = discord.Embed(
            title='Title',
            description=f'{moon_emojis}',
            color=0x66FFFF
        )
        # Add space under the first field
        embed.add_field(name='Message', value=message, inline=True)
        embed.add_field(name='', value='', inline=False)

        embed.add_field(name='Vouched by', value=f'{interaction.user.name}', inline=True)
        embed.add_field(name='Vouched at', value=vouch_data['date'], inline=True)
        embed.set_footer(text=f'Thank you for vouching! • {vouch_data["date"]}')

        # Send the thank you message
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message('Invalid star rating. Please provide a rating between 1 and 5.')

bot.run("TOKEN")
