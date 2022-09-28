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

class bairitu:
  _1=[1,1.03,1.08,1.12,1.18,1.24,1.3,1.37,1.46,1.55,1.65,1.77,1.9,2.06,2.25,2.47,2.75,3.09,3.54,4.12,4.95,6.19,8.25,12.38,24.75]
  _2=[1,1.08,1.17,1.29,1.41,1.56,1.74,1.64,2.18,2.47,2.83,3.26,3.81,4.5,5.4,6.6,8.25,10.61,14.14,19.8,29.7,49.5,99,297]
  _3=[1,1.12,1.29,1.48,1.71,2,2.35,2.79,3.35,4.07,5,6.26,7.96,10.35,13.8,18.97,27.11,40.66,65.06,113.85,227.7,569.25,2277]
  _4=[1,1.18,1.41,1.71,2.09,2.58,3.23,4.09,5.26,6.88,9.17,12.51,17.52,25.3,37.95,59.64,99.39,178.91,357.81,834.9,2504.7,12523.5]




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
    press_len=0
    embed=interactions.Embed(title="Info",color=0xafeee,description=f"倍率:{bairitu._2[press_len]}\n1000円賭けた場合:{bairitu._2[press_len]*1000}")
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
      press_len+=1
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
