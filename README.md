<h1 align="center">BuscaCelular</h1>
🚀 Projeto em python para buscar no site da olx os anuncios mais recentes com base na sua pesquisa.

<h4 align="center"> 
	🚧  🚀 Em construção...  🚧
</h4>

### Features

- [x] Pesquisa na OLX ultimos anuncios
- [x] Pesquisa de acordo com a escolha do usuário
- [x] Opção de escolher um preço de aviso para x produto
- [x] Envia para e-mail cadastrado os anuncios que atendem aos requisitos.
- [x] Opção de lista negra para não olhar para alguns anúncios.
- [ ] Opção de trazer apenas os celulares escolhidos 

### A quem se destina
 - Esta aplicação se destina a pessoas que estejam procurando algum aparelho celular na olx e ao invés de ficar toda hora pesquisando para ver se há alguma novidade, poderá recorrer ao programa em tela realizando suas devidas configurações.
 - Configurando em um agendador de tarefa por exemplo em um intervalo de 1 hora, cada vez que o programa encontrar algo interessante para o usuário, será enviado um e-mail com o titulo do anuncio, link e preço.

### Pré-requisitos

Antes de começar, é necessário ter em sua máquina:
<br>
[Git](https://git-scm.com)
<br>
[Python 3.9.2 ou superior](https://www.python.org/). 

```bash
# Clone este repositório
$ git clone <https://github.com/PauloHenrique7010/BuscaCelular>

# Acesse a pasta do projeto no terminal/cmd

# Vá para a pasta python
$ cd python

# Execute o arquivo "PIP INSTALL.bat" (Aviso, existe um comando para atualizar para a versão mais recente do python)

# Abra o arquivo "o_que_buscar.txt" 
# Coloque neste arquivo os itens a serem buscados.
# Respeitando um item por linha.
# OBS: Caso não deseja procurar nada, apenas trazer os itens mais recentes da categoria.. 
  deixar arquivo em branco.
# Crie o arquivo "conf_email.txt" na mesma pasta dos arquivos ".py".
# Dentro deste arquivo, configure da seguinte forma:

# 1º Linha: E-mail remetente
# 2º Linha: Senha remetente
# 3º Linha: Servidor SMTP -> Colocar "smtp.gmail.com"
# 4º Linha: Porta SSL -> Colocar "465"
# Da 5º Linha em diante, coloque os destinatários para o envio do e-mail. (um destinatário por linha!)


# Caso deseje que não apareça um anúncio como sugestão no seu e-mail, ex:
# "Quero pesquisar por motorola, mas não quero que o motog1 apareça."
# Dessa forma, abra o arquivo "bd_ignorar.txt" e em cada linha separe por virgula e sem espaço como o 
# aparelho pode ser reconhecido.
# Ex:
# Para ignorar aparelhos como Motorola G1 e Samsung Galaxy J1, colocar
# 1º Linha: "MOTOG1,MOTOROLAG1" 
# 2º Linha: "J1,GALAXYJ1,SAMSUNGJ1"
# LEMBRE-SE, TUDO EM CAIXA ALTA SEM ESPAÇOS E SEPARADO POR VÍRGULA!!

# Para os celulares desejados, altere o arquivo "bd_aceitar.txt" de acordo com o padrão a seguir:
# Primeira posição o valor máximo que o produto deverá ter para aparecer
# Segunda posição em diante será como o produto poderá ser reconhecido.
# Ex:
# 1º Linha: 400,MOTOROLAG3,MOTOG3,G3
# 2º Linha: 1000,XIAOMINOTE8,XIAOMI8
# LEMBRETE, NÃO DEVERÁ CONTER ESPAÇOS E OS NOMES PARA REFERÊNCIA DEVERÃO ESTAR EM CAPS LOCK!

# Rode o arquivo "index.py" pela IDLE ou clicando duas vezes.
```
