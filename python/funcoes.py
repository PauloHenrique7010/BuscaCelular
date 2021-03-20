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

def celularInteressante(tituloAnuncio, descAnuncio, precoAnuncio):
    precoIdeal = 0
    motoG7 = ['MOTOROLAG7','MOTOG7']
    MOTOE7 = ['MOTOROLAE7PLUS','MOTOE7']
    tituloCorrigido = tituloAnuncio.upper().replace(' ','')
    
    qtdeEncontrado = 0
    
    #moto g7    
    if (verSeTem(tituloCorrigido, descAnuncio, motoG7, 400, precoAnuncio)):
        return True

    #moto e7
    if (verSeTem(tituloCorrigido, descAnuncio, MOTOE7, 2400, precoAnuncio)):
        return True

    print('')
    print('')
    print('CELULAR NÃO ENCONTRADO NA BASE DE DADOS. ')
    print('SIGA ABAIXO INFOS DO ANÚNCIO')
    print('')
    print('Titulo: '+tituloAnuncio)
    print('')
    print('Descrição: \n'+descAnuncio)
    print(precoAnuncio)
    return False       

def verSeTem(titulo, descricao, array, precoIdeal, precoAnuncio):
    OPTem = False
    qtdeEncontrado = len([s for s in array if s in titulo])   
    
    #não coloquei or por causa de que em alguns anuncios.. os vendedores
    #colocam outros nomes de aparelhos para aparecer na busca!
    if (qtdeEncontrado == 0):
        qtdeEncontrado = len([s for s in array if s in descricao])    
    if (qtdeEncontrado > 0):        
        if precoAnuncio <= precoIdeal:            
            OPTem = True    
    
    return OPTem

def enviarEmail(array):
    nomeArquivo = 'conf_email.txt'
    if (checkFileExistance(nomeArquivo) == True):
        if (arquivoVazio(nomeArquivo)):
            print('NECESSÁRIO CONFIGURAÇÃO DE E-MAIL:\n1º Linha: email\n2º Linha: senha\n3º linha em diante(um destinatario por linha)')
        else:
            archive = open(nomeArquivo, 'r')
            linhas = archive.readlines()
            archive.close
            
            login = linhas[0]
            senha = linhas[1]
            
            destinatario = linhas[2:]
            destinatarioCorrigido = []
            for x in destinatario:
                destinatarioCorrigido.append(x.replace('\n',''))      

            import smtplib            
            from email.mime.text import MIMEText

            
            # conexão com os servidores do google
            smtp_ssl_host = 'smtp.gmail.com'
            smtp_ssl_port = 465
            # username ou email para logar no servidor
            username = login
            password = senha
            from_addr = login
            to_addrs = [destinatarioCorrigido]

            # a biblioteca email possuí vários templates
            # para diferentes formatos de mensagem
            # neste caso usaremos MIMEText para enviar
            # somente texto

            msgEmail = ""
            for x in array:
                msgEmail += x+'\n'
            print(msgEmail)

            msgEmail = "Encontramos alguns itens que vale apena conferir!\n\n"+msgEmail
                
            message = MIMEText(msgEmail)
            message['subject'] = 'BuscaCelular - Encontramos algo!'
            message['from'] = from_addr
            message['to'] = ', '.join(to_addrs)

            # conectaremos de forma segura usando SSL
            server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
            # para interagir com um servidor externo precisaremos
            # fazer login nele
            server.login(username, password)
            server.sendmail(from_addr, to_addrs, message.as_string())
            server.quit()
            
        
    else:
        print('Arquivo "conf_email.txt" não encontrado!')    
