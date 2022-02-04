import datetime
import random
from decouple import config
from discord.ext import commands, tasks
from discord.ext.commands import MissingRequiredArgument, CommandNotFound

xingamentos = ["Você é um bobão", "Que baita paspalho"]
bot = commands.Bot("pet.")
dataDaRetro = [0, 0] #Dia e mês

@bot.event
async def on_ready():
    print("Estou pronto!")
    avisoRetro.start()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send("Favor enviar todos os argumentos. Use pet.help para ver quais são os argumentos necessários.")
    if isinstance(error, CommandNotFound):
        await ctx.send("O comando não existe. Use pet.help para ver todos os comandos possíveis.")
    else:
        raise error

@bot.command(name="xingar.matheus", help="Sem argumentos")
async def xingar(ctx):
    matheus = "<@282646325185609728>"
    numero = random.randint(0, len(xingamentos))
    await ctx.send(f'{xingamentos[numero]}, {matheus}')

@bot.command(name="adicionar.xingamento", help="Argumento: xingamento a ser passado")
async def addxing(ctx, *args):
    menssagem = ' '.join(args)
    xingamentos.append(menssagem)
    await ctx.send(f'Foi adicionado "{menssagem}" à lista de xingamentos!')

@bot.command(name="remover.xingamento", help="Argumento: posição do xingamento na lista de xingamentos")
async def addxing(ctx, arg):
    xingamentos.pop(int(arg)-1)
    await ctx.send(f'Foi removido o {arg}º xingamento da lista!')

@bot.command(name="mostrar.xingamentos", help="Sem argumentos")
async def addxing(ctx):
    await ctx.send(f'Lista de xingamentos: {xingamentos}')

@bot.command(name="retro", help="Sem argumentos")
async def retrospectiva(ctx):
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

    await ctx.reply(f'Falta {diasAteRetro} para a próxima restrospectiva! A próxima retro será dia {dataDaRetro[0]}/{dataDaRetro[1]}') 

@bot.command(name="retro.ferias", help="Sem argumentos")
async def ferias(ctx):
    avisoRetro.cancel()
    await ctx.send("O bot não avisará mais sobre as retros.")

@bot.command(name="retro.volta", help="Sem argumentos")
async def volta(ctx):
    avisoRetro.start()
    await ctx.send("O bot voltará a avisar sobre as retros.")

@bot.command(name="retro.manual", help="Argumentos: dia da volta, mês da volta")
async def ferias(ctx, arg1, arg2):
    #Remove a data anterior
    dataDaRetro.pop()
    dataDaRetro.pop()
    #Atualiza a data
    dataDaRetro.append(int(arg1))
    dataDaRetro.append(int(arg2))
    await ctx.send(f'Retro manualmente ajustada para dia {arg1}/{arg2}')
    
@tasks.loop(hours=336)
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
    channel = bot.get_channel(938858934259822685)
    await channel.send(f'ATENÇÃO PETIANOS: Lembrando que hoje é dia de retrospectiva!! {petianos}')

TOKEN = config("TOKEN")
bot.run(TOKEN)