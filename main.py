import datetime
import random
from decouple import config
from discord.ext import commands, tasks
from discord.ext.commands import MissingRequiredArgument, CommandNotFound

#Inícializações
bot = commands.Bot("pet.")
dataDaRetro = [11, 2] #Dia e mês
totalDiasRetro = [1]
dataDoInter = [12, 2] #Dia e mês
totalDiasInter = [2]


#EVENTOS -> triggers específicos a parte dos comandos
@bot.event
async def on_ready():
    print("Estou pronto!")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send("Favor enviar todos os argumentos. Use pet.help para ver quais são os argumentos necessários.")
    if isinstance(error, CommandNotFound):
        await ctx.send("O comando não existe. Use pet.help para ver todos os comandos possíveis.")
    else:
        raise error




#COMANDOS -> inicializados com 'pet.'
@bot.command(name="xingar.matheus", help="Sem argumentos")
async def xingamath(ctx):
    with open("xingamentos.txt", 'r', encoding = 'utf-8') as f:
        todosOsXingos = f.read()
        xingamentos = todosOsXingos.split(", ")
        matheus = "<@282646325185609728>"
        numero = random.randint(0, len(xingamentos))
        await ctx.send(f'{xingamentos[numero]}, {matheus}')   

@bot.command(name="adicionar.xingamento", help="Argumento: xingamento a ser passado.")
async def addxing(ctx, *args):
    with open("xingamentos.txt", 'a', encoding = 'utf-8') as f:
        menssagem = ' '.join(args)
        f.write(menssagem)
        f.write(", ")
        await ctx.send(f'Foi adicionado "{menssagem}" à lista de xingamentos!')

@bot.command(name="remover.xingamento", help="Argumento: posição do xingamento na lista de xingamentos")
async def removexing(ctx, arg):
    with open("xingamentos.txt", 'w+', encoding = 'utf-8') as f:
        todosOsXingos = f.read()
        xingamentos = todosOsXingos.split(", ")
        xingamentos.pop(int(arg)-1)
        novosXings = ", ".join(xingamentos)
        f.write(novosXings)
        await ctx.send(f'Foi removido o {arg}º xingamento da lista!')

@bot.command(name="mostrar.xingamentos", help="Sem argumentos")
async def mostraxing(ctx):
    with open("xingamentos.txt", 'r', encoding = 'utf-8') as f:
        todosOsXingos = f.read()
        xingamentos = todosOsXingos.split(", ")
        await ctx.send(f'Lista de xingamentos: {xingamentos}')

@bot.command(name="elogiar", help="Argumento: @da pessoa elogiada")
async def elogiar(ctx, arg):
    with open("elogios.txt", 'r', encoding = 'utf-8') as f:
        todosOsElogios = f.read()
        elogio = todosOsElogios.split(", ")
        numero = random.randint(0, len(elogio))
        await ctx.send(f'{elogio[numero]}, {arg}!')   

@bot.command(name="adicionar.elogio", help="Argumento: elogio a ser passado.")
async def addelog(ctx, *args):
    with open("elogios.txt", 'a', encoding = 'utf-8') as f:
        menssagem = ' '.join(args)
        f.write(menssagem)
        f.write(", ")
        await ctx.send(f'Foi adicionado "{menssagem}" à lista de elogios!')

@bot.command(name="remover.elogio", help="Argumento: posição do elogio na lista de elogios")
async def removeelog(ctx, arg):
    with open("elogios.txt", 'w+', encoding = 'utf-8') as f:
        todosOsElogios = f.read()
        elogio = todosOsElogios.split(", ")
        elogio.pop(int(arg)-1)
        novosElogs = ", ".join(elogio)
        f.write(novosElogs)
        await ctx.send(f'Foi removido o {arg}º elogio da lista!')

@bot.command(name="mostrar.elogios", help="Sem argumentos")
async def mostraelog(ctx):
    with open("xingamentos.txt", 'r', encoding = 'utf-8') as f:
        todosOsElogios = f.read()
        elogios = todosOsElogios.split(", ")
        await ctx.send(f'Lista de xingamentos: {elogios}')  
    
@bot.command(name="hug", help="Argumento: @ da pessoa abraçada")
async def abraco(ctx, arg):
    quemabraca = ctx.author.id
    await ctx.send(f'<@{quemabraca}> abraçou beeeeem forte {arg} <3')

@bot.command(name="retro", help="Sem argumentos")
async def retro(ctx):
    await ctx.reply(f'Faltam {totalDiasRetro[0]} dias até a próxima retrospectiva, que será no dia {dataDaRetro[0]}/{dataDaRetro[1]}.')

@bot.command(name="retro.manual", help="Argumentos: data e mês da retro, separados por uma '/'.")
async def retro_manual(ctx, arg):
    data = arg.split('/')
    dataDaRetro[0] = int(data[0])
    dataDaRetro[1] = int(data[1])
    hoje = datetime.datetime.now()
    dia = int(hoje.strftime("%d"))
    mes = int(hoje.strftime("%m"))
    diasAteRetro = dataDaRetro[0] - dia
    mesesAteRetro = dataDaRetro[1] - mes
    if mesesAteRetro == 0:
        if diasAteRetro < 0:
            if mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12:
                diasAteRetro += 31 
            elif mes == 2:
                diasAteRetro += 28
            else: 
                diasAteRetro += 30
    else:
        if mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12:
            diasAteRetro += 31 
        elif mes == 2:
            diasAteRetro += 28
        else: 
            diasAteRetro += 30
    totalDiasRetro[0] = diasAteRetro
    passar_dia_Retro()
    await ctx.send(f'Retrospectiva manualmente ajustada para a data {dataDaRetro[0]}/{dataDaRetro[1]}')

@bot.command(name="ferias", help="Sem argumentos")
async def retro_ferias(ctx):
    passar_dia_Interpet.cancel()
    passar_dia_Retro.cancel()
    await ctx.reply("Bot entrando de férias! Sem mais avisos da retrospectiva ou afins.")


@bot.command(name="interpet", help="Sem argumentos")
async def interpet(ctx):
    await ctx.reply(f'Faltam {totalDiasInter[0]} dias até a próxima retrospectiva, que será no dia {dataDaRetro[0]}/{dataDaRetro[1]}.')
    
@bot.command(name="interpet.manual", help="Argumentos: data e mês do interpet, separados por uma '/'.")
async def interpet_manual(ctx, arg):
    data = arg.split('/')
    dataDoInter[0] = int(data[0])
    dataDoInter[1] = int(data[1])
    hoje = datetime.datetime.now()
    dia = int(hoje.strftime("%d"))
    mes = int(hoje.strftime("%m"))
    diasAteInter = dataDoInter[0] - dia
    mesesAteInter = dataDoInter[1] - mes
    if mesesAteInter == 0:
        if diasAteInter < 0:
            if mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12:
                diasAteInter += 31 
            elif mes == 2:
                diasAteInter += 28
            else: 
                diasAteInter += 30
    else:
        if mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12:
            diasAteInter += 31 
        elif mes == 2:
            diasAteInter += 28
        else: 
            diasAteInter += 30
    totalDiasRetro[0] = diasAteInter
    passar_dia_Interpet.start()
    await ctx.send(f'Retrospectiva manualmente ajustada para a data {dataDoInter[0]}/{dataDoInter[1]}')

#ROTINAS -> funções periódicas
@tasks.loop(hours=24)
async def passar_dia_Retro():
    if totalDiasRetro[0] != 0:
        totalDiasRetro[0] -= 1
    else:
        avisa_retro()

async def avisa_retro():
    petianos = "<@&823601627382153267>"
    channel = bot.get_channel(939127640898539520)
    if dataDaRetro[1] == 1 or dataDaRetro[1] == 3 or dataDaRetro[1] == 5 or dataDaRetro[1] == 7 or dataDaRetro[1] == 8 or dataDaRetro[1] == 10 or dataDaRetro[1] == 12:
        if dataDaRetro[0] + 14 > 31:
            dataDaRetro[0] = dataDaRetro[0] + 14 - 30
        else:
            dataDaRetro[0] += 14
    elif dataDaRetro[1] == 2:
        if dataDaRetro[0] + 14 > 28:
            dataDaRetro[0] = dataDaRetro[0] + 14 - 28
        else:
            dataDaRetro[0] += 14
    else: 
        if dataDaRetro[0] + 14 > 30:
            dataDaRetro[0] = dataDaRetro[0] + 14 - 30
        else:
            dataDaRetro[0] += 14
    totalDiasRetro[0] = 14+1
    passar_dia_Retro.start()
    await channel.send(f'Atenção, {petianos}!\n Lembrando que amanhã é dia de retrospectiva, já aproveitem pra escrever o textos de vocês.')

@tasks.loop(hours=24)
async def passar_dia_Interpet():
    if totalDiasInter[0] != 0:
        totalDiasInter[0] -= 1
    else:
        avisa_inter()

async def avisa_inter():
    petianos = "<@&823601627382153267>"
    channel = bot.get_channel(939127640898539520)
    passar_dia_Interpet.cancel()
    await channel.send(f'Atenção, {petianos}!\n Lembrando que amanhã é dia de interpet, estejam acordados amanhã de manhã!')

TOKEN = config("TOKEN")
bot.run(TOKEN)