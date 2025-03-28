import discord
from discord.ext import commands
import random
import datetime
import os
from dotenv import load_dotenv

# Load token dari file .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
OWNER_ID = 762806349074661416 # Ganti dengan ID Discord pemilik bot

# Intents diperlukan untuk fitur membaca pesan dan masuk voice
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True  # Penting untuk membaca pesan pengguna
intents.voice_states = True  # Diperlukan untuk fitur voice
intents.members = True  # Untuk mendapatkan informasi anggota

# Prefix command bot
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game("with Machmud💕 "))
    print(f'Bot {bot.user} sudah online dengan status idle!')

@bot.command()
async def halo(ctx):
    await ctx.send(f'Halo {ctx.author.mention}!')

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="Informasi Bot", description="Bot ini dibuat dengan discord.py", color=0x00ff00)
    embed.add_field(name="Prefix", value="!", inline=False)
    await ctx.send(embed=embed)

# Perintah untuk mengirim pesan embed
@bot.command()
async def embed(ctx):
    embed = discord.Embed(
        title="Judul Embed",
        description="Ini adalah contoh pesan embed",
        color=discord.Color.blue()
    )
    embed.set_footer(text="Footer text")
    embed.set_thumbnail(url=ctx.author.avatar.url)
    embed.add_field(name="Field 1", value="Ini isi dari field 1", inline=False)
    embed.add_field(name="Field 2", value="Ini isi dari field 2", inline=True)
    await ctx.send(embed=embed)

# Perintah untuk mengirim embed dari Owner dengan validasi input
@bot.command()
async def send_embed(ctx, channel: discord.TextChannel = None, title: str = None, *, message: str = None):
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Kamu tidak memiliki izin untuk menggunakan perintah ini!")
        return
    
    if channel is None or title is None or message is None:
        await ctx.send('❌ Format salah! Gunakan: `!send_embed #channel "Judul" Isi Pesan`.')
        return
    
    embed = discord.Embed(title=title, description=message, color=discord.Color.gold())
    embed.set_footer(text=f'Dikirim oleh {ctx.author}', icon_url=ctx.author.avatar.url)
    await channel.send(embed=embed)
    await ctx.send(f'✅ Pesan embed berhasil dikirim ke {channel.mention}')

# Perintah untuk mengirim pesan biasa dari Owner
@bot.command()
async def send_message(ctx, channel: discord.TextChannel = None, *, message: str = None):
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Kamu tidak memiliki izin untuk menggunakan perintah ini!")
        return
    
    if channel is None or message is None:
        await ctx.send('❌ Format salah! Gunakan: `!send_message #channel Isi Pesan`.')
        return
    
    await channel.send(message)
    await ctx.send(f'✅ Pesan berhasil dikirim ke {channel.mention}')

# Perintah untuk menampilkan ping bot
@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

# Perintah untuk mendapatkan informasi pengguna
@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f'Info Pengguna - {member}', color=discord.Color.green())
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Nama", value=member.name, inline=True)
    embed.add_field(name="Bergabung Sejak", value=member.joined_at.strftime("%Y-%m-%d"), inline=False)
    await ctx.send(embed=embed)
# Perintah untuk bot bergabung ke voice channel dan auto-deafen
@bot.command()
async def joinvoice(ctx):
    """Memaksa bot bergabung ke voice channel dalam keadaan deafen."""
    if ctx.author.voice:  # Pastikan pengguna ada di voice channel
        channel = ctx.author.voice.channel
        if ctx.voice_client:  # Jika bot sudah ada di voice channel, pindahkan
            await ctx.voice_client.move_to(channel)
        else:
            vc = await channel.connect()
            await vc.guild.change_voice_state(channel=channel, self_deaf=True)  # Deafen bot
        
        await ctx.send(f"✅ Bot telah bergabung ke {channel.name} dan dalam keadaan deafen.")
    else:
        await ctx.send("❌ Kamu harus berada di voice channel untuk menjalankan perintah ini!")

# Perintah agar bot tetap di voice channel meskipun kosong
@bot.command()
async def stayvoice(ctx):
    """Memastikan bot tetap berada di voice channel dan selalu dalam keadaan deafen."""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client:
            await ctx.voice_client.move_to(channel)
        else:
            vc = await channel.connect()
            await vc.guild.change_voice_state(channel=channel, self_deaf=True)  # Auto-deafen bot
        
        await ctx.send(f"✅ Bot akan tetap berada di {channel.name} dalam keadaan deafen.")

        while True:
            await asyncio.sleep(300)  # Mengecek setiap 5 menit apakah bot masih di channel
            if not ctx.voice_client or not ctx.voice_client.is_connected():
                break  # Jika bot terputus, loop berhenti
    else:
        await ctx.send("❌ Kamu harus berada di voice channel untuk menjalankan perintah ini!")


# Jalankan bot
bot.run(TOKEN)

