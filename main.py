# -*- coding: utf-8 -*-
import interactions
from interactions.ext.wait_for import wait_for,setup
from interactions.ext.get import get
from interactions import Message
from threading import Thread
from interactions import Intents
from interactions import Client, CommandContext, Embed
import json,os,asyncio,random,requests,uuid,math,string

###CONFIG
bot_token=os.getenv("token")


bot = interactions.Client(token=bot_token,intents=interactions.Intents.DEFAULT|interactions.Intents.GUILD_MESSAGE_CONTENT)
setup(bot)


def create_mines_list(def_len:int,boom_len:int):
  import random
  number=[]
  for i in range(def_len-boom_len):
    number.append(0)
  for i in range(boom_len):
    number.append(1)
  
  random.shuffle(number)
  
  return(number)



@bot.command(
    name="casino", 
    description="casino test", 
    options= [
        interactions.Option(
            type=interactions.OptionType.INTEGER,
            name="bomb",
            description="爆弾の数", 
            required=True
        ),
    ],
)
async def casino_test(ctx: CommandContext):
    guild = await ctx.get_guild()
    guild_id = guild.id
    channel = await ctx.get_channel()
    button_opt=[]
    

    for i in range(25):
      button=interactions.Button(
        style=interactions.ButtonStyle.SECONDARY,
        label=" ",
        custom_id=f"{i}",
      )
      button_opt.append(button)
    button_opt_temp=button_opt
    button_send=[]
    kaisuu=0
    for aa in range(5):
      temp_data=[]
      for i in range(5):
        temp_data.append(button_opt_temp[kaisuu])
        kaisuu+=1
      button_send.append(interactions.ActionRow(components=temp_data))
    
      
    
    
    message_ = await ctx.send(components=button_send)
    message_id = message_.id
    
    button_opt_temp=button_opt
    kakuritu=create_mines_list(25,2)
  
    selected_data=[]
    while True:
      async def check(msg):
          if int(msg.author.id) == int(ctx.author.user.id) and int(msg.channel_id) == int(ctx.channel_id):
              return True
      try:
          select_wait = await bot.wait_for_component(components=button_send, check=check,timeout=80)
      except asyncio.TimeoutError:
          return
      await select_wait.send("a",ephemeral=True)
      if kakuritu[int(select_wait.custom_id)]==1:
        button_opt_temp[int(select_wait.custom_id)]=interactions.Button(
            style=interactions.ButtonStyle.DANGER,
            label="", 
            emoji=interactions.Emoji(name="💣"),
            custom_id=f"{select_wait.custom_id}",
            disabled=True
        )
        button_send=[]
        kaisuu=0
        for aa in range(5):
          temp_data=[]
          for i in range(5):
            temp_data.append(button_opt_temp[kaisuu])
            kaisuu+=1
          button_send.append(interactions.ActionRow(components=temp_data))
        await message_.edit(components=button_send)
        button_last=[]
        for n,i in enumerate(kakuritu):
          if i ==1:
            button=interactions.Button(
              style=interactions.ButtonStyle.DANGER,
              emoji=interactions.Emoji(name="💣"),
              label="",
              custom_id=f"{n}",
              disabled=True
            )
          elif str(n) in selected_data:
            button=interactions.Button(
              style=interactions.ButtonStyle.SUCCESS,
              emoji=interactions.Emoji(name="💎"),
              label="",
              custom_id=f"{n}",
              disabled=True
            )
          else:
            button=interactions.Button(
              style=interactions.ButtonStyle.SECONDARY,
              emoji=interactions.Emoji(name="💎"),
              label="",
              custom_id=f"{n}",
              disabled=True
            )
          button_last.append(button)
        button_send=[]
        kaisuu=0
        for aa in range(5):
          temp_data=[]
          for i in range(5):
            temp_data.append(button_last[kaisuu])
            kaisuu+=1
          button_send.append(interactions.ActionRow(components=temp_data))
        await message_.edit(components=button_send)
        return
      else:
        button_opt_temp[int(select_wait.custom_id)]=interactions.Button(
                style=interactions.ButtonStyle.SUCCESS,
                label="", 
                emoji=interactions.Emoji(name="💎"),
                custom_id=f"{select_wait.custom_id}",
                disabled=True)
        selected_data.append(select_wait.custom_id)
      button_send=[]
      kaisuu=0
      for aa in range(5):
        temp_data=[]
        for i in range(5):
          temp_data.append(button_opt_temp[kaisuu])
          kaisuu+=1
        button_send.append(interactions.ActionRow(components=temp_data))
      await message_.edit(components=button_send)



bot.start()
