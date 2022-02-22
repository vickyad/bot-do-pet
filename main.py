import datetime
import random
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

# Setup
bot_prefix = commands.Bot("teste.")
praise_list = []
praise_list = []

retro_day = initialize_date(datetime.date(2022, 2, 23), 14)
interpet_day = initialize_date(datetime.date(2022, 2, 19), 30)


# Get swearings from file
with open("xingamentos.txt", 'r', encoding='utf-8') as file:
        raw_data = file.read()
        praise_list = raw_data.split(", ")

# Get praises from file
with open("elogios.txt", 'r', encoding = 'utf-8') as f:
        raw_data = f.read()
        praise_list = raw_data.split(", ")


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
    num = random.randint(0, len(praise_list))
    await ctx.send(f'{praise_list[num]}, {MATHEUS}')   


# Command: Adicionar xingamento
@bot_prefix.command(name="add_xingamento", help="adicione uma nova forma de ofender o Matheus!")
async def add_offense(ctx, *args):
    message = ' '.join(args).lower()
    praise_list.append(message)
    with open("xingamentos.txt", 'a', encoding = 'utf-8') as file:
        file.write(f', {message}')
        await ctx.send(f'"{message}" foi adicionado à lista!')


# Command: Remover xingamento
@bot_prefix.command(name="rem_xingamento", help="não gostou de algum xingamento? ele nunca mais será usado")
async def remove_offense(ctx, *args):
    swear_to_be_removed = ' '.join(args).lower()
    if swear_to_be_removed in praise_list:
        praise_list.remove(swear_to_be_removed)
        with open("xingamentos.txt", 'w+', encoding = 'utf-8') as file:
            new_swearing_list = ", ".join(praise_list)
            file.write(new_swearing_list)
            await ctx.send(f'"{swear_to_be_removed}" foi removido da lista!')
    else:
        await ctx.send(f'esse xingamento não existe')


# Command: Mostrar xingamentos
@bot_prefix.command(name="xingamentos", help="lista todas as formas possíveis de ofender o Matheus")
async def show_offenses(ctx):
    await ctx.send(f'lista de xingamentos: {praise_list}')


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

    with open("elogios.txt", 'a', encoding = 'utf-8') as f:
        f.write(f', {message}')
        await ctx.send(f'"{message}" foi adicionado à lista!')


# Command: Remover elogio
@bot_prefix.command(name="rem_elogio", help="não gostou de algum elogio? só mandar o elogio a ser removido")
async def remove_praise(ctx, *args):
    praise_to_be_removed = ' '.join(args).lower()
    if praise_to_be_removed in praise_list:
        praise_list.remove(praise_to_be_removed)
        with open("elogios.txt", 'w+', encoding = 'utf-8') as file:
            new_praise_list = ", ".join(praise_list)
            file.write(new_praise_list)
            await ctx.send(f'"{praise_to_be_removed}" foi removido da lista!')
    else:
        await ctx.send(f'esse elogio não existe')


# Command: Mostrar elogios
@bot_prefix.command(name="elogios", help="mostra todas as formas de elogiar os outros")
async def show_praises(ctx):
    await ctx.send(f'lista de elogios: {praise_list}')  


# Command: Hug    
@bot_prefix.command(name="hug", help="demonstre seu carinho por alguém")
async def hug(ctx, arg):
    await ctx.send(f'<@{ctx.author.id}> abraçou beeeeem forte {arg} <3')


# Command: Retrospectiva
@bot_prefix.command(name="retro", help="avisa quantos dias faltam pra retrospectiva")
async def retrospective(ctx):
    await ctx.reply(f'faltam {retro_day.day - datetime.date.today().day} dias até a próxima retrospectiva, que será no dia {retro_day.day}/{retro_day.month}.')


# Command: Retrospectiva Manual
@bot_prefix.command(name="retro.manual", help="seta a nova data para a retrospectiva, no formato dd/mm")
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
@bot_prefix.command(name="retro.ferias", help="desliga os avisos de retrospectiva")
async def set_retrospective_vacation(ctx):
    is_retrospective_eve.cancel()
    await ctx.reply("bot entrando de férias das retrospectivas! Sem mais avisos ou afins.")


# Command: Interpet
@bot_prefix.command(name="inter", help="avisa quantos dias faltam pra interpet")
async def interpet(ctx):
    await ctx.reply(f'faltam {interpet_day - datetime.date.today().day} dias até o próximo interpet, que será no dia {interpet_day.day}/{interpet_day.month}.')


# Command: Interpet Manual    
@bot_prefix.command(name="inter.manual", help="seta a nova data para a interpet, no formato dd/mm")
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
@bot_prefix.command(name="inter.ferias", help="desliga os avisos de interpet")
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

TOKEN = config("TOKEN")
bot_prefix.run(TOKEN)