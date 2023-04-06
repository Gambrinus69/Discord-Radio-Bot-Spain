import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
from typing import Optional
import interactions

my_secret = os.environ['TOKEN_GAMBRIRADIO_BOT']

bot = interactions.Client(token=my_secret)

@bot.event
async def on_voice_state_update(member, before, after):
    if member == bot.user:
        return

    if before.channel is None and after.channel is not None:
        # El miembro se ha conectado a un canal de voz
        member.voice = after

    if before.channel is not None and after.channel is None:
        # El miembro se ha desconectado de un canal de voz
        member.voice = None
        
@bot.command(
    name="join",
    description="Conéctate al canal de voz actual del usuario"
)
async def join(ctx: interactions.CommandContext):
    voice_state = ctx.author.voice
    if not voice_state or not voice_state.channel:
        await ctx.send("No estás conectado a un canal de voz")
        return
    channel = voice_state.channel
    await channel.connect()
    await ctx.send(f"Conectado al canal de voz {channel.name}")


@bot.command(
    name="leave",
    description="Desconéctate del canal de voz actual"
)
async def leave(ctx: interactions.CommandContext):
    voice_client = ctx.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
        await ctx.send("Desconectado del canal de voz")

@bot.command(
    name="play",
    description="Reproduce una emisora de radio"
)
async def play(ctx: interactions.CommandContext, radio: Optional[str] = None):
    async def play_radio(radio):
        if radio == "KissFM":
            source = await interactions.FFmpegOpusAudio.from_probe('https://20823.live.streamtheworld.com/KISS.mp3')
            vc.play(source)
            await ctx.respond("Reproduciendo KissFM...")
        elif radio == "M80":
            source = await interactions.FFmpegOpusAudio.from_probe('https://21233.live.streamtheworld.com/M80AAC.aac')
            vc.play(source)
            await ctx.respond("Reproduciendo M80...")
        elif radio == "MaximaFM":
            source = await interactions.FFmpegOpusAudio.from_probe('https://19983.live.streamtheworld.com/MAXIMAFMAAC.aac')
            vc.play(source)
            await ctx.respond("Reproduciendo MaximaFM...")
        elif radio == "RockFM":
            source = await interactions.FFmpegOpusAudio.from_probe('http://stream.rockfm.fm/rockfm.mp3')
            vc.play(source)
            await ctx.respond("Reproduciendo RockFM...")
        # Agregar más casos para otras emisoras de radio

    if not ctx.author.voice:
        await ctx.send("No estás conectado a un canal de voz")
        return
    else:
        channel = ctx.author.voice.channel
        vc = await channel.connect()
    if radio is None:
        await ctx.send("Debes especificar la emisora que quieres reproducir")
        return
    await play_radio(radio)

#pip show interactions
#print(dir(interactions))
#keep_alive()
bot.start()
