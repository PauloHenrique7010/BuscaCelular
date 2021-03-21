from datetime import datetime, timezone, timedelta

def addLog(frase, arrayLog):
    print(frase)
    arrayLog.append(frase)
    return arrayLog


def pegarDataAtual():
    dataHoraAtual = datetime.now()
    diferenca = timedelta(hours=-3)    
    fuso_horario = timezone(diferenca)
    return dataHoraAtual

def formatarDataParaArquivo(dataNoTipoDate):
    dataFormatada = dataNoTipoDate.strftime('%d/%m/%Y %H:%M')
    dataFormatada = dataFormatada.replace('/','.').replace(' ','_').replace(':','.')
    return dataFormatada

def checkFileExistance(filePath):
    try:
        with open(filePath, 'r') as f:
            return True
    except FileNotFoundError as e:
        return False
    except IOError as e:
        return False
def arquivoVazio(filePath):
    if (checkFileExistance(filePath)):
        with open(filePath) as file:
            contLinha = 0
            for line in file:
                contLinha += 1
        file.close()        
        if (contLinha > 0):
            return False
        else:
            return True       
        
    else:
        print('[RESPOSTA FUNÇÃO] Arquivo não encontrado!')
        return False
def criarArquivo(conteudo, diretorio):
    arquivo = open(diretorio,'w')
    arquivo.write(conteudo)
    arquivo.close()

##FIM FUNÇÕES GERAIS
    

def celularInteressante(tituloAnuncio, descAnuncio, precoAnuncio):
    tituloCorrigido = tituloAnuncio.upper().replace(' ','')
    descCorrigido = descAnuncio.upper().replace(' ','')
    arrayCelulares = []
    
    '''arrayCelulares = [
            [400, 'MOTOROLAG7', 'MOTOG7'],
            [300, 'SAMSUNGGALAXYJ8','J8'],
            [450, 'G8PLUS']
    ]
    '''    
    
    archive = open('bd_aceitar.txt', 'r')
    for linha in archive:        
        linha = linha.replace('\n','')
        arrayLinha = linha.split(',')
        arrayLinha[0] = float(arrayLinha[0])                                    
        arrayCelulares.append(arrayLinha)
    archive.close()

    arrayIgnorar = []
    archive = open('bd_ignorar.txt','r')    
    for linha in archive:        
        linha = linha.replace('\n','')
        arrayLinha = linha.split(',')        
        arrayIgnorar.append(arrayLinha)
    archive.close()
        

    ''' TABELA PARA RESPOSTAS '''
    '''
        1 - Cadastrado, pode pegar
        2 - Cadastrado, mas está alto o preço
        3 - Não cadastrado, MOSTRAR NO EMAIL
        4 - CELULAR NA LISTA NEGRA..
    '''

    #VERIFICA SE O CELULAR ESTÁ NA LISTA NEGRA.. CASO NÃO QUEIRA QUE BUSQUE POR ESTE MODELO
    for x in arrayIgnorar:        
        qtdeEncontrado = len([s for s in x if s in tituloCorrigido])
        #não coloquei or para achar primeiro no titulo.. (anuncios com tags tb)
        if (qtdeEncontrado == 0):            
            qtdeEncontrado = len([s for s in x if s in descCorrigido])            
        if (qtdeEncontrado > 0):        
            return 4    
    

    for x in arrayCelulares:        
        qtdeEncontrado = len([s for s in x[1:] if s in tituloCorrigido])
        #não coloquei or para achar primeiro no titulo.. (anuncios com tags tb)
        if (qtdeEncontrado == 0):            
            qtdeEncontrado = len([s for s in x[1:] if s in descCorrigido])            
        if (qtdeEncontrado > 0):        
            if precoAnuncio <= x[0]:            
                return 1
            else:
                return 2
            break
        else:
            return 3
def emailConfigurado():
    nomeArquivo = 'conf_email.txt'   
    if (checkFileExistance(nomeArquivo) == True):
        
        if (arquivoVazio(nomeArquivo)):
            print('NECESSÁRIO CONFIGURAÇÃO DE E-MAIL:\nESTE PROGRAMA RODA APENAS PARA GMAIL!\n\nSIGA INSTRUÇÕES ABAIXO!\n\n1º Ative o "lesssecureapps" na sua conta google.\n\n1º Linha: E-mail remetente\n2º Linha: Senha remetente\n3º Linha: smtp remetente(smtp.gmail.com)\n4º Linha: porta SSL (465).\n5º linha em diante(um destinatario por linha)')
            return False
        else:
            return True
    else:        
        print('Arquivo "conf_email.txt" não encontrado!')
        return False
    

def enviarEmail(array):
    nomeArquivo = 'conf_email.txt' 
    if (emailConfigurado):        
        archive = open(nomeArquivo, 'r')
        linhas = archive.readlines()
        archive.close
                
        login = linhas[0]
        senha = linhas[1]
        smtpServer = linhas[2].replace('\n','')
        sslPort    = int(linhas[3].replace('\n',''))
            
        destinatario = linhas[4:]
        destinatarioCorrigido = []
        for x in destinatario:            
            destinatarioCorrigido.append(x.replace('\n',''))      
            
        import smtplib            
        from email.mime.text import MIMEText
        

        # conexão com os servidores do google
        smtp_ssl_host = smtpServer
        smtp_ssl_port = sslPort
        # username ou email para logar no servidor
        username = login
        password = senha
        from_addr = login
        to_addrs = destinatarioCorrigido

        # a biblioteca email possuí vários templates
        # para diferentes formatos de mensagem
        # neste caso usaremos MIMEText para enviar
        # somente texto

        msgEmail = ""
        for x in array:
            msgEmail += x+'\n'                        

        msgEmail = "Encontramos alguns itens que vale apena conferir!\n\n"+msgEmail
                
        message = MIMEText(msgEmail)
        message['subject'] = 'BuscaCelular - Encontramos algo!'
        message['from'] = 'BuscaCelular'
        message['to'] = ', '.join(to_addrs)       

            
        # conectaremos de forma segura usando SSL
        server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
        # para interagir com um servidor externo precisaremos
        # fazer login nele
        server.login(username, password)
        server.sendmail(from_addr, to_addrs, message.as_string())
        server.quit()
