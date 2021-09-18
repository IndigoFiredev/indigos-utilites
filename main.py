import discord
from discord.ext import commands
from discord.ext import tasks
import time
from itertools import cycle
from keep_alive import keep_alive


client = commands.Bot(command_prefix = '-')
status = cycle(['with the mods...', 'fortnite', 'minecraft', 'no', 'leaking staff channels', 'i am a youtuber', 'roblox', 'Indigo is cool'])


@client.event
async def on_ready():
  change_status.start()
  print('Logged in as:\n{0.user.name}\n{0.user.id}'.format(client))

@tasks.loop(seconds=60)
async def change_status():
  await client.change_presence(status=discord.Status.online, activity=discord.Game(next(status)))

@client.command(description="pings the mods for support")
  await ctx.send('hey there, i noticed you need support! I will now ping mods for you <@&871708036367016007>')

@client.command(description="sets the slowmode of a channel")
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, amount):
    try:
        await ctx.channel.edit(reason='Bot Slowmode Command', slowmode_delay=int(amount))
        await ctx.send('Slowmode has been changed. Good job everyone. You made the server slow')
    except discord.Errors.Forbidden:
        await ctx.send('I do not have the permission to do this, please try again')

@client.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

   await member.remove_roles(mutedRole)
   await member.send(f" you have unmuted from: - {ctx.guild.name}")
   embed = discord.Embed(title="unmute", description=f" unmuted-{member.mention}",colour=discord.Colour.light_gray())
   await ctx.send(embed=embed)

@client.command(description="mutes a member. GIVE ME A REASON")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, time: int, d, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")
    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

    for channel in guild.channels:
        await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True)

    await member.add_roles(mutedRole)

    embed = discord.Embed(title="TempMuted!", description=f"{member.mention} has been tempmuted.", colour=discord.Colour.light_gray())
    embed.add_field(name="Reason:", value=reason, inline=False)
    embed.add_field(name="Time for the mute:", value=f"{time}{d}", inline=False)
    await ctx.send(embed=embed)

    if d == "s":
        mutetime = time

    if d == "m":
        mutetime = time*60

    if d == "h":
        mutetime = time*60*60

    if d == "d":
        mutetime = time*60*60*24

    with open("TXT_FILE_PATH", "w+") as mutetimef:
        mutetime.write(mutetime)
    
    while True:
        with open("TXT_FILE_PATH", "w+") as mutetimef:
            if int(mutetimef.read()) == 0:
                await member.remove_roles(mutedRole)

                embed = discord.Embed(title="Unmute (temp mute expired) ", description=f"Unmuted -{member.mention} ", colour=discord.Colour.light_gray())
                await ctx.send(embed=embed)
  
                return
            else:
                mutetime -= 1
                mutetimef.seek(0)
                mutetimef.truncate()
                mutetimef.write(mutetime)
        await asyncio.sleep(1)

@client.command(description="gives you the info on a role")
async def roleinfo(ctx, role: discord.Role):
  await ctx.send(f'This role is called {role.mention} and its ID is {role.id}')

@client.command(description="gives you info on a user")
async def userinfo(ctx, member: discord.Member):
  await ctx.send(f'{member.mention}s ID is {member.id} and their discriminator is {member.discriminator}. They also seem really cool.')

@client.command(description="unmutes a member")
@commands.has_permissions(administrator=True)
async def unwarn(ctx, member: discord.Member):
  await ctx.send(f'unwarned {member.mention}. Count yourself lucky')

@client.command(description="gives you info on the server")
async def info(ctx):
  await ctx.send('Fires World is all about trying to bring users together so that you can make friends and also enjoy your time on discord!')

@client.command(description="clears the messages of a channel")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
  await ctx.channel.purge(limit=amount)
  await ctx.send('Cleared messages!')

cmds = commands

@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    await ctx.send('Hey there, why dont you use a command that actually exists!')

@client.command(description="warns a member")
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member):
  await ctx.send(f'{member.mention} has been warned! Here is a top tip {member.mention}, dont break rules :wink:')

@clear.error
async def clear_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(' Next time, tell me how much you want to delete')

@client.command(description="gives you the bots ping")
async def ping(ctx):
  await ctx.send(f':ping_pong: Pong! My latency is {round(client.latency)}ms')

@client.command(description="kicks people for being bad")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
  await member.kick(reason=reason)
  await ctx.send(f'Kicked {member.mention}')
  return

@client.command(description="gives the invite link")
async def invite(ctx):
  await ctx.send(f'hey there {member.mention}, I noticed you tried to invite me to your server. Sadly i cannot be invited however all of my code is open source. you can find it at https://github.com/IndigoFiredev/indigos-utilites!')

@client.command(description="bans a member")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
  await member.ban(reason=reason)
  await ctx.send(f'i have banned {user.mention}')
  return

@client.command(description="unbans a member")
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split('#')

  for ban_entry in banned_users:
    user = ban_entry.user

    if (user.name, user.discriminator) == (member_name, member_discriminator):
      await ctx.guild.unban(user)
      await ctx.send(f'Unbanned {user.mention}')
      return

keep_alive()
client.run('your token here')
