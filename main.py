import datetime
import json
import random
import discord
from decouple import config
from discord.ext import commands, tasks
from discord.ext.commands import MissingRequiredArgument, CommandNotFound

def initialize_date(current_day, interval):
    today = datetime.date.today()
    while current_day < today:
        current_day += datetime.timedelta(days=interval)
    return current_day


# Constants
PETIANES = "<@&823601627382153267>"
MATHEUS = "<@282646325185609728>"

RETRO_CHANNEL = 939127640898539520
BOT_RECOMMENDATIONS_CHANNEL = 939130179698196530

# Setup
bot_prefix = commands.Bot("pet.")
bot_prefix.remove_command("help")

retro_day = initialize_date(datetime.date(2022, 2, 23), 14)
interpet_day = initialize_date(datetime.date(2022, 2, 19), 30)


# Get swearings from file
with open('data.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

praise_list = data['praises']
offense_list = data['offenses']

# EVENTS
@bot_prefix.event
async def on_ready():
    print("Estou pronto!")


@bot_prefix.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send("Favor enviar todos os argumentos. Use pet.help para ver quais são os argumentos necessários.")
    if isinstance(error, CommandNotFound):
        await ctx.send("O comando não existe. Use pet.help para ver todos os comandos possíveis.")
    else:
        raise error


# COMMANDS
# Command: Xingar Matheus
@bot_prefix.command(name="xingar_matheus", help="não é necessário gastar sua saliva xingando o Matheus, o bot faz isso por você")
async def offend_matheus(ctx):
    num = random.randint(0, len(offense_list))
    await ctx.send(f'{offense_list[num]}, {MATHEUS}')   


# Command: Adicionar xingamento
@bot_prefix.command(name="add_xingamento", help="adicione uma nova forma de ofender o Matheus!")
async def add_offense(ctx, *args):
    message = ' '.join(args).lower()
    offense_list.append(message)

    di = {'offenses': offense_list, 'praises': praise_list}
    with open('data.json', 'w+', encoding='utf-8') as outfile:
        json.dump(di, outfile)
        await ctx.send(f'"{message}" foi adicionado à lista!')


# Command: Remover xingamento
@bot_prefix.command(name="rem_xingamento", help="não gostou de algum xingamento? ele nunca mais será usado")
async def remove_offense(ctx, *args):
    swear_to_be_removed = ' '.join(args).lower()
    if swear_to_be_removed in offense_list:
        offense_list.remove(swear_to_be_removed)

        di = {'offenses': offense_list, 'praises': praise_list}
        with open('data.json', 'w+', encoding='utf-8') as outfile:
            json.dump(di, outfile)
            await ctx.send(f'"{swear_to_be_removed}" foi removido da lista!')
    else:
        await ctx.send(f'esse xingamento não existe')


# Command: Mostrar xingamentos
@bot_prefix.command(name="xingamentos", help="lista todas as formas possíveis de ofender o Matheus")
async def show_offenses(ctx):
    printable_offense_list = ', '.join(offense_list).lower()
    em = discord.Embed(color=0xFF6347)
    em.add_field(
        name="**Lista de xingamentos:**",
        value=f'{printable_offense_list}'
    )
    await ctx.send(embed = em)


# Command: Elogiar
@bot_prefix.command(name="elogiar", help="elogie alguém que fez um bom trabalho recentemente!")
async def praise(ctx, arg):
    num = random.randint(0, len(praise_list))
    await ctx.send(f'{praise_list[num]}, {arg}!')   


# Command: Adionar elogio
@bot_prefix.command(name="add_elogio", help="adicione mais uma forma de falarmos bem dos nossos coleguinhas")
async def add_praise(ctx, *args):
    message = ' '.join(args).lower()
    praise_list.append(message)

    di = {'offenses': offense_list, 'praises': praise_list}
    with open('data.json', 'w+', encoding='utf-8') as outfile:
        json.dump(di, outfile)
        await ctx.send(f'"{message}" foi adicionado à lista!')


# Command: Remover elogio
@bot_prefix.command(name="rem_elogio", help="não gostou de algum elogio? só mandar o elogio a ser removido")
async def remove_praise(ctx, *args):
    praise_to_be_removed = ' '.join(args).lower()
    if praise_to_be_removed in praise_list:
        praise_list.remove(praise_to_be_removed)

        di = {'offenses': offense_list, 'praises': praise_list}
        with open('data.json', 'w+', encoding='utf-8') as outfile:
            json.dump(di, outfile)
            await ctx.send(f'"{praise_to_be_removed}" foi removido da lista!')
    else:
        await ctx.send(f'esse elogio não existe')


# Command: Mostrar elogios
@bot_prefix.command(name="elogios", help="mostra todas as formas de elogiar os outros")
async def show_praises(ctx):
    printable_praise_list = ', '.join(praise_list).lower()
    em = discord.Embed(color=0x9370DB)
    em.add_field(
        name="**Lista de elogios:**",
        value=f'{printable_praise_list}'
    )
    await ctx.send(embed = em) 


# Command: Hug    
@bot_prefix.command(name="hug", help="demonstre seu carinho por alguém")
async def hug(ctx, arg):
    await ctx.send(f'<@{ctx.author.id}> abraçou beeeeem forte {arg} <3')


# Command: Retrospectiva
@bot_prefix.command(name="retro", help="avisa quantos dias faltam pra retrospectiva")
async def retrospective(ctx):
    await ctx.reply(f'faltam {retro_day.day - datetime.date.today().day} dias até a próxima retrospectiva, que será no dia {retro_day.day}/{retro_day.month}.')


# Command: Retrospectiva Manual
@bot_prefix.command(name="retro_manual", help="seta a nova data para a retrospectiva, no formato dd/mm")
async def set_retrospective(ctx, arg):
    day, month = arg.split('/')

    try:
        global retro_day
        retro_day = datetime.datetime(int(datetime.date.today().year), int(month), int(day))
        is_retrospective_eve.start()
        await ctx.send(f'retrospectiva manualmente ajustada para a data {retro_day.day}/{retro_day.month}')
    except ValueError:
        print('Erro')


# Command: Retrospectiva Ferias
@bot_prefix.command(name="retro_ferias", help="desliga os avisos de retrospectiva")
async def set_retrospective_vacation(ctx):
    is_retrospective_eve.cancel()
    await ctx.reply("bot entrando de férias das retrospectivas! Sem mais avisos ou afins.")


# Command: Interpet
@bot_prefix.command(name="inter", help="avisa quantos dias faltam pra interpet")
async def interpet(ctx):
    await ctx.reply(f'faltam {interpet_day - datetime.date.today().day} dias até o próximo interpet, que será no dia {interpet_day.day}/{interpet_day.month}.')


# Command: Interpet Manual    
@bot_prefix.command(name="inter_manual", help="seta a nova data para a interpet, no formato dd/mm")
async def set_interpet(ctx, arg):
    day, month = arg.split('/')

    try:
        global interpet_day
        interpet_day = datetime.datetime(int(datetime.date.today().year), int(month), int(day))
        is_interpet_eve.start()
        await ctx.send(f'retrospectiva manualmente ajustada para a data {interpet_day.day}/{interpet_day.month}')
    except ValueError:
        print('Erro')


# Command: Interpet Ferias
@bot_prefix.command(name="inter_ferias", help="desliga os avisos de interpet")
async def set_interpet_vacation(ctx):
    is_interpet_eve.cancel()
    await ctx.reply("bot entrando de férias do interpet! Sem mais avisos ou afins.")


# ROTINES
@tasks.loop(hours=24)
async def is_retrospective_eve():
    global retro_day
    if retro_day == datetime.date.today() - datetime.timedelta(days=1):
        remember_retrospective.start()


@tasks.loop(count=1)
async def remember_retrospective():
    global retro_day
    retro_day += datetime.timedelta(days=14)
    channel = bot_prefix.get_channel(RETRO_CHANNEL)
    await channel.send(f'atenção, {PETIANES}!\n lembrando que amanhã é dia de retrospectiva, já aproveitem pra escrever o textos de vocês.')


@tasks.loop(hours=24)
async def is_interpet_eve():
    global interpet_day
    if interpet_day == datetime.date.today() - datetime.timedelta(days=1):
        remember_interpet.start()


@tasks.loop(count=1)
async def remember_interpet():
    global interpet_day
    interpet_day += datetime.timedelta(month=1)
    channel = bot_prefix.get_channel(RETRO_CHANNEL)
    await channel.send(f'atenção, {PETIANES}!\n lembrando que amanhã é dia de interpet, estejam acordados amanhã de manhã!')

# HELP COMMANDS
@bot_prefix.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(
        title="**Bem-vinde ao Bot do PET!**",
        url="https://github.com/petcomputacaoufrgs/bot-do-pet",
        description="Use pet.help para ter mais informações sobre o comando desejado.",
        color=0xFFFFFF
    )
    em.add_field(
        name="**Xingue o Matheus:**",
        value="""
            *pet.xingar_matheus*
            *pet.add_xingamento*
            *pet.rem_xingamento*
            *pet.xingamentos*
            """,
        inline=True
    )
    em.add_field(
        name="**Demonstre seu carinho:**",
        value="""
            *pet.elogiar*
            *pet.add_elogio*
            *pet.rem_elogio*
            *pet.elogios*
            *pet.hug*
            """,
        inline=True
    )
    em.add_field(
        name="⠀⠀⠀",
        value="⠀⠀⠀",
        inline=False
    )
    em.add_field(
        name="**Retrospectiva:**",
        value="""
            *pet.retro*
            *pet.retro_manual*
            *pet.retro_ferias*
            """,
        inline=True
    )
    em.add_field(
        name="**Interpet:**",
        value="""
            *pet.inter*
            *pet.inter_manual*
            *pet.inter_ferias*
            """,
        inline=True
    )
    em.add_field(
        name="⠀⠀⠀",
        value="⠀⠀⠀",
        inline=False
    )
    em.add_field(
        name="**Tem alguma outra sugestão para o bot?**",
        value=f'Escreva pra gente no chat <#{BOT_RECOMMENDATIONS_CHANNEL}>! Toda ajuda é sempre bem-vinda  🥰',
        inline=False
    )
    em.set_thumbnail(url="https://cdn.discordapp.com/attachments/938858934259822685/945718556732039219/LogoPET_oficial.png")
    await ctx.send(embed = em)


@help.command()
async def xingar_matheus(ctx):  
    em = discord.Embed(
        title="**Comando: xingar o Matheus**",
        description="Não é necessário gastar sua saliva xingando o Matheus, o bot faz isso por você.",
        color=0xFF6347
    )
    em.add_field(
       name="**Argumentos:**",
       value="Nenhum, use apenas a chamada para o comando.",
       inline=False
    )
    em.add_field(
       name="**Exemplo de uso:**",
       value="```pet.xingar_matheus```",
       inline=False
    )
    await ctx.send(embed = em)


@help.command()
async def add_xingamento(ctx):  
    em = discord.Embed(
        title="**Comando: adicionar xingamento**",
        description="Adicione uma nova forma de ofender o Matheus!",
        color=0xFF6347
    )
    em.add_field(
       name="**Argumentos:**",
       value="O xingamento a ser adicionado na lista, sem aspas.",
       inline=False
    )
    em.add_field(
       name="**Exemplo de uso:**",
       value="```pet.add_xingamento <xingamento goes here>```",
       inline=False
    )
    await ctx.send(embed = em)

@help.command()
async def rem_xingamento(ctx):  
    em = discord.Embed(
        title="**Comando: remover xingamento**",
        description="Não gostou de algum xingamento? Ele nunca mais será usado!",
        color=0xFF6347
    )
    em.add_field(
       name="**Argumentos:**",
       value="O xingamento a ser removido da lista, sem aspas.",
       inline=False
    )
    em.add_field(
       name="**Exemplo de uso:**",
       value="```pet.rem_xingamento <xingamento goes here>```",
       inline=False
    )
    await ctx.send(embed = em)


@help.command()
async def xingamentos(ctx):  
    em = discord.Embed(
        title="**Comando: listar xingamentos**",
        description="Lista todas as formas possíveis de ofender o Matheus.",
        color=0xFF6347
    )
    em.add_field(
       name="**Argumentos:**",
       value="Nenhum, use apenas a chamada para o comando.",
       inline=False
    )
    em.add_field(
       name="**Exemplo de uso:**",
       value="```pet.xingamentos```",
       inline=False
    )
    await ctx.send(embed = em)


@help.command()
async def elogiar(ctx):  
    em = discord.Embed(
        title="**Comando: elogiar**",
        description="Elogie alguém que fez um bom trabalho recentemente!",
        color=0x9370DB
    )
    em.add_field(
       name="**Argumentos:**",
       value="Escreva o @ da pessoa a ser elogiada.",
       inline=False
    )
    em.add_field(
       name="**Exemplo de uso:**",
       value="```pet.elogiar @someone```",
       inline=False
    )
    await ctx.send(embed = em)


@help.command()
async def add_elogio(ctx):  
    em = discord.Embed(
        title="**Comando: adicionar elogio**",
        description="Adicione mais uma forma de reconhecermos o bom trabalho dos nossos coleguinhas.",
        color=0x9370DB
    )
    em.add_field(
       name="**Argumentos:**",
       value="O elogio a ser adicionado na lista, sem aspas.",
       inline=False
    )
    em.add_field(
       name="**Exemplo de uso:**",
       value="```pet.add_elogio <elogio goes here>```",
       inline=False
    )
    await ctx.send(embed = em)


@help.command()
async def rem_elogio(ctx):  
    em = discord.Embed(
        title="**Comando: remover elogio**",
        description="Não gostou de algum elogio? Não usaremos mais.",
        color=0x9370DB
    )
    em.add_field(
       name="**Argumentos:**",
       value="O elogio a ser removido da lista, sem aspas.",
       inline=False
    )
    em.add_field(
       name="**Exemplo de uso:**",
       value="```pet.rem_elogio <elogio goes here>```",
       inline=False
    )
    await ctx.send(embed = em)


@help.command()
async def elogios(ctx):  
    em = discord.Embed(
        title="**Comando: listar elogios**",
        description="Lista todas as formas de elogiar os outros.",
        color=0x9370DB
    )
    em.add_field(
       name="**Argumentos:**",
       value="Nenhum, use apenas a chamada para o comando.",
       inline=False
    )
    em.add_field(
       name="**Exemplo de uso:**",
       value="```pet.elogios```",
       inline=False
    )
    await ctx.send(embed = em)


@help.command()
async def hug(ctx):  
    em = discord.Embed(
        title="**Comando: abraçar**",
        description="Demonstre seu carinho por alguém.",
        color=0x9370DB
    )
    em.add_field(
       name="**Argumentos:**",
       value="Escreva o @ da pessoa a ser abraçada.",
       inline=False
    )
    em.add_field(
       name="**Exemplo de uso:**",
       value="```pet.hug @someone```",
       inline=False
    )
    await ctx.send(embed = em)


@help.command()
async def retro(ctx):  
    em = discord.Embed(
        title="**Comando: mostrar próxima retrospectiva**",
        description="Avisa quantos dias faltam pra retrospectiva.",
        color=0xF0E68C
    )
    em.add_field(
       name="**Argumentos:**",
       value="Nenhum, use apenas a chamada para o comando.",
       inline=False
    )
    em.add_field(
       name="**Exemplo de uso:**",
       value="```pet.retro```",
       inline=False
    )
    await ctx.send(embed = em)


@help.command()
async def retro_manual(ctx):  
    em = discord.Embed(
        title="**Comando: settar a próxima retrospectiva**",
        description="Seta a nova data para a retrospectiva.",
        color=0xF0E68C
    )
    em.add_field(
       name="**Argumentos:**",
       value="A data no formato dd/mm.",
       inline=False
    )
    em.add_field(
       name="**Exemplo de uso:**",
       value="```pet.retro_manual <dia/mes>```",
       inline=False
    )
    await ctx.send(embed = em)


@help.command()
async def retro_ferias(ctx):  
    em = discord.Embed(
        title="**Comando: férias da retrospectiva**",
        description="Desliga os avisos de retrospectiva.",
        color=0xF0E68C
    )
    em.add_field(
       name="**Argumentos:**",
       value="Nenhum, use apenas a chamada para o comando.",
       inline=False
    )
    em.add_field(
       name="**Exemplo de uso:**",
       value="```pet.retro_ferias```",
       inline=False
    )
    await ctx.send(embed = em)

@help.command()
async def inter(ctx):  
    em = discord.Embed(
        title="**Comando: mostrar próximo interpet**",
        description="Avisa quantos dias faltam pra interpet.",
        color=0x98FB98
    )
    em.add_field(
       name="**Argumentos:**",
       value="Nenhum, use apenas a chamada para o comando.",
       inline=False
    )
    em.add_field(
       name="**Exemplo de uso:**",
       value="```pet.inter```",
       inline=False
    )
    await ctx.send(embed = em)


@help.command()
async def inter_manual(ctx):  
    em = discord.Embed(
        title="**Comando: settar o próximo interpet**",
        description="Seta a nova data para o interpet.",
        color=0x98FB98
    )
    em.add_field(
       name="**Argumentos:**",
       value="A data no formato dd/mm.",
       inline=False
    )
    em.add_field(
       name="**Exemplo de uso:**",
       value="```pet.inter_manual <dia/mes>```",
       inline=False
    )
    await ctx.send(embed = em)

@help.command()
async def inter_ferias(ctx):  
    em = discord.Embed(
        title="**Comando: férias do interpet**",
        description="Desliga os avisos do interpet.",
        color=0x98FB98
    )
    em.add_field(
       name="**Argumentos:**",
       value="Nenhum, use apenas a chamada para o comando.",
       inline=False
    )
    em.add_field(
       name="**Exemplo de uso:**",
       value="```pet.inter_ferias```",
       inline=False
    )
    await ctx.send(embed = em)


TOKEN = config("TOKEN")
bot_prefix.run(TOKEN)