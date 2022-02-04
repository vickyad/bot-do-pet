import datetime
import random
from decouple import config
from discord.ext import commands, tasks
from discord.ext.commands import MissingRequiredArgument, CommandNotFound

#Inícializações
bot = commands.Bot("pet.")
dataDaRetro = [0, 0] #Dia e mês
totalDias = [14]
minutos = []
horas = []

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
        f.write(', ')
        await ctx.send(f'Foi adicionado "{menssagem}" à lista de xingamentos!')

@bot.command(name="remover.xingamento", help="Argumento: posição do xingamento na lista de xingamentos")
async def removexing(ctx, arg):
    with open("xingamentos.txt", 'w+', encoding = 'utf-8') as f:
        todosOsXingos = f.read()
        xingamentos = todosOsXingos.split(", ")
        xingamentos.pop(int(arg)-1)
        novosXings = ', '.join(xingamentos)
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
        f.write(', ')
        await ctx.send(f'Foi adicionado "{menssagem}" à lista de elogios!')

@bot.command(name="remover.elog", help="Argumento: posição do elogio na lista de elogios")
async def removeelog(ctx, arg):
    with open("elogios.txt", 'w+', encoding = 'utf-8') as f:
        todosOsElogios = f.read()
        elogio = todosOsElogios.split(", ")
        elogio.pop(int(arg)-1)
        novosElogs = ', '.join(elogio)
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
    abracado = arg
    await ctx.send(f'<@{quemabraca}> abraçou beeeeem forte {abracado} <3')

@bot.command(name="retro", help="Sem argumentos")
async def retrospectiva(ctx):
    totalDias.pop()
    hoje = datetime.datetime.now()
    dia = int(hoje.strftime("%d"))
    mes = int(hoje.strftime("%m"))
    diasAteRetro = dataDaRetro[0] - dia
    if diasAteRetro < 0:
        if mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12:
            diasAteRetro += 31 
        elif mes == 2:
            diasAteRetro += 28
        else:   
            diasAteRetro += 30
    totalDias.append(diasAteRetro)
    if diasAteRetro == 1:
        await ctx.reply(f'Falta {diasAteRetro} dia para a próxima restrospectiva! A próxima retro será dia {dataDaRetro[0]}/{dataDaRetro[1]}')
    elif diasAteRetro == 0:
        await ctx.reply(f'Hoje tem retrospectiva!')
    else:
        await ctx.reply(f'Faltam {diasAteRetro} dias para a próxima restrospectiva! A próxima retro será dia {dataDaRetro[0]}/{dataDaRetro[1]}')

@bot.command(name="retro.ferias", help="Sem argumentos")
async def ferias(ctx):
    avisoRetro.cancel()
    await ctx.send("O bot não avisará mais sobre as retrospectivas.")

@bot.command(name="retro.volta", help="Sem argumentos")
async def volta(ctx):
    avisoRetro.start()
    await ctx.send("O bot voltará a avisar sobre as retrospectivas.")

@bot.command(name="retro.manual", help="Argumentos: dia da volta, mês da volta. Não use '/'.")
async def ferias(ctx, arg1, arg2):
    #Remove a data anterior
    dataDaRetro.pop()
    dataDaRetro.pop()
    #Atualiza a data
    dataDaRetro.append(int(arg1))
    dataDaRetro.append(int(arg2))
    await ctx.send(f'Retrospectiva manualmente ajustada para dia {arg1}/{arg2}')




#ROTINAS -> funções periódicas
@tasks.loop(hours=(totalDias[0] * 24))
async def avisoRetro():
    #Remove a data anterior
    dataDaRetro.pop()
    dataDaRetro.pop()
    #Atualiza a data
    hoje = datetime.datetime.now()
    dia = int(hoje.strftime("%d"))
    mes = int(hoje.strftime("%m"))
    if mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12:
        if dia + 14 > 31:    
            dia = dia + 14 - 31
            dataDaRetro.append(dia)
            dataDaRetro.append(mes+1)
        else:
            dataDaRetro.append(dia + 14)
            dataDaRetro.append(mes)
    elif mes == 2:
        if dia + 14 > 28:
            dia = dia + 14 - 28
            dataDaRetro.append(dia)
            dataDaRetro.append(mes+1)
        else:
            dataDaRetro.append(dia + 14)
            dataDaRetro.append(mes)
    else:
        if dia + 14 > 30:
            dia = dia + 14 - 30
            dataDaRetro.append(dia)
            dataDaRetro.append(mes+1)
        else:
            dataDaRetro.append(dia + 14)
            dataDaRetro.append(mes)
    petianos = "<@&823601627382153267>"
    channel = bot.get_channel(939127640898539520)
    await channel.send(f'ATENÇÃO PETIANOS: Lembrando que hoje é dia de retrospectiva!! {petianos}')

TOKEN = config("TOKEN")
bot.run(TOKEN)