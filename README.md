# Bot para Discord
#### Projeto: Atividade Internas
#### Linguagem utilizada: Python (versão 3.9.2)
##### Autor: [Nathan](https://github.com/neitaans)


## Descrição
Bot do Discord com diversas funcionalidades para ajudar no dia a dia dos bolsistas, contribuir com o aprendizado de Python e da biblioteca `discord.py` e funcionalidades divertidas para integração e descontração


## Bibliotecas utilizadas
#### Discord.py
```
pip install discord.py
```

#### Decouple
```
pip install python-decouple
```


## Comandos disponíveis
> prefixo: `pet.`

### Help
Mostra todos os comandos possíveis

#### Uso
```
pet.help
```
---------------------------------------

### Xingar o Matheus
Não é necessário gastar sua saliva xingando o Matheus, o bot faz isso por você

#### Uso
```
pet.xingar_matheus
```
---------------------------------------

### Adionar xingamento
Adicione uma nova forma de ofender o Matheus!

#### Uso
```
pet.add_xingamento <xingamento goes here>
```
---------------------------------------

### Remover xingamento
Não gostou de algum xingamento? Ele nunca mais será usado

#### Uso
```
pet.rem_xingamento <xingamento goes here>
```
---------------------------------------

### Listar xingamentos
Lista todas as formas possíveis de ofender o Matheus

#### Uso
```
pet.xingamentos
```
---------------------------------------

### Elogiar
Elogie alguém que fez um bom trabalho recentemente!

#### Uso
```
pet.elogiar @someone
```
---------------------------------------

### Adicionar elogio
Adicione mais uma forma de reconhecermos o bom trabalho dos nossos coleguinhas

#### Uso
```
pet.add_elogio <elogio goes here>
```
---------------------------------------

### Remover elogio
Não gostou de algum elogio? Não usaremos mais

#### Uso
```
pet.rem_elogio <elogio goes here>
```
---------------------------------------

### Listar elogios
Lista todas as formas de elogiar os outros

#### Uso
```
pet.elogios
```
---------------------------------------

### Abraçar
Demonstre seu carinho por alguém

#### Uso
```
pet.hug @someone
```
---------------------------------------

### Mostrar próxima retrospectiva
Avisa quantos dias faltam pra retrospectiva

#### Uso
```
pet.retro
```
---------------------------------------

### Settar a próxima retrospectiva
Seta a nova data para a retrospectiva, no formato *dd/mm*

#### Uso
```
pet.retro.manual <dia/mes>
```
---------------------------------------

### Férias da retrospectiva
Desliga os avisos de retrospectiva

#### Uso
```
pet.retro.ferias
```
---------------------------------------

### Mostrar próximo interpet
Avisa quantos dias faltam pra interpet

#### Uso
```
pet.inter
```
---------------------------------------

### Settar a próximo interpet
Seta a nova data para a interpet, no formato *dd/mm*

#### Uso
```
pet.inter.manual <dia/mes>
```
---------------------------------------

### Férias do interpet
Desliga os avisos de interpet

#### Uso
```
pet.inter.ferias
```
---------------------------------------

## Melhorias a serem feitas
- Troca dos documentos `.txt` para `.json`
- Melhoria do comando de help
- Melhorar a verificação de datas válidas para retrospectiva e interpet
- Melhorar os avisos nos canais sobre os eventos
- Arrumar as datas do interpet
- Adição da funcionalidade de agendar um evento em uma data
- Adição da funcionalidade para lembrar os líderes do mês
- Adição de arquivo para funções auxiliares
