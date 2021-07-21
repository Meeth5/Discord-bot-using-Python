import discord
from discord.ext import commands, tasks
import discord.voice_client 

from random import choice

client = commands.Bot(command_prefix='ADD YOUR COMMAND PREFIX') ##add your command prefix here

status = [''] ## add your bot status use commas and single inveted commas after each status

#join and leave
@client.event
async def on_member_join(context, member):
    context.send(f'{member} has joined the server.')

@client.event
async def on_member_remove(context, member):
    context.send(f'{member} has left the server')



@client.event
async def on_ready():
    change_status.start()
    print("I am ready")

@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(status)))


#kick
@client.command(name='kick', pass_context = True)
@commands.has_permissions(kick_members = True)
async def kick(context, member: discord.Member,*,reason= "No reason provided"):
    try:
        await member.send("You have been kicked from the server!! And if you want to join the server again, This is the link ADD YPUR SERVER LINK HERE") ## add your server invite link 
    except:
        await context.send("The member has their DMs close ")
    await context.send('User ' + member.display_name + ' has been kicked!!!')
    await member.kick(reason=reason) 

@client.event
async def on_command_error(context,error):
    if isinstance(error,commands.MissingPermissions):
        await context.send("You can't do that ;-;")
        await context.message.delete()
    elif isinstance(error,commands.MissingRequiredArgument):
        await context.send("Please enter all the required arguements")
        await context.message.delete()
    else:
        raise error        

#ban
@client.command(name='ban', pass_context = True)
@commands.has_permissions(ban_members=True)
async def ban(context, member: discord.Member, *, reason=reason):
  await context.send(member.display_name + " has been BANNED from the sever, Because " + reason)
  await member.ban(reason=reason)

#unban
@client.command(aliases=['ub'])
@commands.has_permissions(ban_members=True)
async def unban(context,*,member):
    banned_users = await context.guild.bans()
    member_name, member_disc = member.split('#')

    for banned_entry in banned_users:
        user = banned_entry.user
        if(user.name, user.discriminator)==(member_name,member_disc):
            await context.guild.unban(user)
            await context.send(member_name +" has been unbanned")
            return


#clear 
@client.command(aliases=['c'])
@commands.has_permissions(manage_messages = True)
async def clear(context,amount=3):
    await context.channel.purge(limit = amount)

#mute
@client.command(aliases=['m'])
@commands.has_permissions(kick_members = True)
async def mute(context,member : discord.Member):
    muted_role = context.guild.get_role() ##enter the mute role id in the brackets 
    await member.add_roles(muted_role)
    await context.send(member.mention + " has been muted")

filtered_words = ["gandu","bhosadike","madarchod","mc","mc motaa bhai","Mc"] ## add the bad words here which you dont want your members to use in the server


@client.event
async def on_message(message):
    for word in filtered_words:
        if  word in message.content:
           await message.delete()

    await client.process_commands(message)  

client.run("YOUR BOT CLIENT ID") ## add your bot client id in here
