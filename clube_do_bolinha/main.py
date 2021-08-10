import discord 
import os
from discord.ext import commands
from dotenv import load_dotenv
import requests
import json 
import random 
from replit import db
from music_cog import music_cog
from main_cog import main_cog

load_dotenv()  #rodar arquivos do tipo env sem gerar exception 

bot = commands.Bot(command_prefix='/')
bot.remove_command('help') 
bot.add_cog(main_cog(bot))
bot.add_cog(music_cog(bot))

client = discord.Client()

sad_words = [
    "triste"
    ,"depressivo"
    ,"chateado"
    ,"mal"
    ,"desanimado"
    ,"irritado"
    ,"quero desistir de tudo"
    ,"segunda feira"
]

conselhos = [
    "Nao desista de quem você é, a tristeza é passageira mas a gloria é eterna",
    "As pessoas podem nao tem entender, mas saiba que no fundo ninguem e mais forte que você mesmo !",
    "Nao fique mal meu parceiro, procure um membro do grupo para conversar, você vera que as coisas vão melhorar",
    "Em desenvolvimento",
    "Em desenvolvimento",
    "Em desenvolvimento",
    "O desafio pode parecer impossivel agora, mas se acalme e tente denovo, verá que as coisas serão mais faceis",
]

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + ' - ' + json_data[0]['a']
    return(quote)

def update_conselhos(conselhos_messages):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(conselhos_messages)
        db["encouragemnets"] = encouragements
    else:
        db["encouragemnets"] = [conselhos_messages] ## https://www.freecodecamp.org/news/create-a-discord-bot-with-python/  parei ak

def  delete_encouragment(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
    db["encouragements"] = encouragements


@client.event
async def on_ready():
    print("Bot {0.user} LOGADO !!!".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('-me ajuda'):
        quote = get_quote()
        await message.channel.send(quote)
    
    elif any(word in msg for word in sad_words):
        await message.channel.send(random.choice(conselhos))

    if message.content.startswith("-adm"):
        await message.channel.send("Marcio Alac, o grande fodão dos fps, assistam minha live, porra !!!")
    
    elif message.content.startswith("-me ajude"):
        quote = get_quote()
        await message.channel.send(quote)

    elif message.content.startswith("-show"):
        await message.channel.send("Show ak só do Sando e Junior")
    
    elif message.content.startswith("-massa"):
        await message.channel.send("De pão ou bolo ???")
    elif message.content.startswith("-bolo"):
        await message.channel.send("Se pega 2Kg de farinha e cheira tudo")
    elif message.content.startswith("-pao"):
        await message.channel.send("Ai eu nao sei fazer, procura no google ;-;")
    elif message.content.startswith("-comandos"):   #  TODOS OS COMANDOS DE CHATE
        await message.channel.send("-Ola\n-giovani\n-tudo bem\n-estou mal\n-seja ruim\n-me ofenda\n-foda-se\n-equipe python\n-me ajude\n-adm\n-me ajuda\n-show\n-massa")
    
    elif message.content.startswith("-Ola") or message.content.startswith("-ola"):
        await message.channel.send("Ola, bem vindo ao clube do bolinha !")
    
    elif message.content.startswith("-giovani"):
        await message.channel.send("O pvt do Flask, motoBoy du mal. O VEI CHEGA AI CHEGA AIII, kaskdaksdkkak")
    
    elif message.content.startswith("-tudo bem"):
        await message.channel.send("tudo bem comigo, e com você ?")
    
    elif message.content.startswith("-estou mal"):
        await message.channel.send("Nao fique mal meu amigo, amanha vai ser pior !!!")
    
    elif message.content.startswith("-seja ruim"):
        await message.channel.send("Você é um lixo, e tudo que você faz vai dar errado, se mate logo !!!")
    
    elif message.content.startswith("-me ofenda"):
        await message.channel.send("Vai tomar no seu cu, sua mae é uma puta barata, eu mesmo paguei 1 real por um bola gato dela...")
    
    elif message.content.startswith("-foda-se"):
        await message.channel.send("Ai nossa ele é mau mermo em... Vou cholar")
    
    elif message.content.startswith("-equipe python"):
        await message.channel.send("Flask man: Giovani\nPython man: Hendrick\nDjando man: Marcos Paulo\nFrappe man: Marcio Alac")

bot.run(os.getenv("DISCORD_TOKEN"))