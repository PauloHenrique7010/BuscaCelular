import funcoes
import requests
from bs4 import BeautifulSoup

#user-agent serve para simular como se eu fosse um navegador acessando a pagina
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

print('v1.1(Apenas vale-paraiba) - 21/03/2021 15:50')

funcoes.criarPasta('log')
funcoes.criarPasta('raspados')



if (funcoes.emailConfigurado() == False):
    print('CONFIGURE E-MAIL PARA PROSSEGUIR!')
elif (funcoes.checkFileExistance('o_que_buscar.txt') == False):
    print('O arquivo "o_que_buscar.txt" não existe do diretório deste arquivo python.')
else:
    arrayPaginacao = []
    arrayEnviarEmail = []
    arrayLog = []

    nomeArquivo = 'qtde_pagina_pesquisar.txt'
    if (funcoes.checkFileExistance(nomeArquivo) == False):
        arquivo = open(nomeArquivo, 'w')
        arquivo.writelines('1')
        arquivo.close()

    archive = open('qtde_pagina_pesquisar.txt','r')
    arrayPaginacao = archive.readlines()
    archive.close()

    qtdePagina = 1
    if (len(arrayPaginacao) > 0):
        qtdePagina = arrayPaginacao[0]
        if ((qtdePagina.replace(' ','')) != ''):            
            qtdePagina = int(qtdePagina)       
    

    archive = open('url_enviada.txt', 'r')
    urlEnviada = archive.readlines()
    archive.close()

    arrayUrlEnviada = []
    novasUrls = []
    for x in urlEnviada:        
        arrayUrlEnviada.append(x.replace('\n',''))

    #os itens a serem pesquisados estão neste arquivo..    
    archive = open('o_que_buscar.txt', 'r')
    arquivo = archive.readlines()
    archive.close()    
    
    if (len(arquivo) == 0):
        funcoes.addLog('PESQUISANDO NA CATEGORIA ELETRÔNICOS OS ANÚNCIOS MAIS RECENTES', arrayLog)
        arquivo.append('')      
    
    #para cada linha, ele ira pesquisar alguma coisa
    for linha in arquivo:

        pesquisa = ''
        #pego o celular que vai ser pesquisado
        celularDaVez = linha
        celularDaVez = celularDaVez.replace(' ', '%20') #na url, é trocado o espaço por "%20"
        if (celularDaVez != ''):            
            celularDaVez = 'q='+celularDaVez  
        
        for x in range(qtdePagina):
            contadorPagina = x+1

            pesquisa = ''
            if (contadorPagina > 1):
                if (pesquisa != ''):
                    pesquisa = '&'
                pesquisa = pesquisa+'o='+str(contadorPagina)

            if (celularDaVez != '') and (pesquisa != ''):
                pesquisa += '&'
            pesquisa = pesquisa+celularDaVez
            if (pesquisa != ''):
                pesquisa +='&'
            url = "https://sp.olx.com.br/vale-do-paraiba-e-litoral-norte/vale-do-paraiba/celulares?"+pesquisa+'sf=1'
            funcoes.addLog(url, arrayLog)        

            if (linha != ""):
                funcoes.addLog('Pesquisando na olx como: '+linha, arrayLog)

            page = requests.get(url,headers=headers)
            #print(page.status_code) 200 para resposta OK
            #print(page.text) # consigo ver o codigo fonte da pagina
            funcoes.criarArquivo(page.text, 'raspados/arquivoRaspado_'+funcoes.formatarDataParaArquivo(funcoes.pegarDataAtual())+'.html')            

            #converto para um tipo onde posso navegar entre os trechos html
            soup = BeautifulSoup(page.text, 'html.parser')

            #procuro onde começa a lista de anuncios
            listaCelular = soup.find_all('li', class_='sc-1fcmfeb-2')        

            #para cada bloco de anuncio
            contador = 0
            for x in listaCelular:
                contador += 1            
                
                #x = listaCelular[2] caso queira ver uma posição exatamente
                '''faço um try catch para quando o anuncio
                    da olx for um anuncio de publicidade'''
                funcoes.addLog('////////////////////////////////////////////////////////////', arrayLog)
                try:
                    linkAnuncio = x.a['href']           
            
                    infoAnuncio = x.div.find('div', class_ = 'fnmrjs-2 jiSLYe')
                    tituloAnuncio = infoAnuncio.div.find('div', class_ = 'fnmrjs-6 iNpuEh').h2.text
                    precoAnuncio = infoAnuncio.div.find('div', class_ = 'fnmrjs-9 gqfQzY').span.text #puxo o primeiro span (quando desce o preço.. o mais novo vai pro primeiro
                    dataAnuncio =  infoAnuncio.div.find_all('span', class_='wlwg1t-1 fsgKJO sc-ifAKCX eLPYJb')
                    horaAnuncio = dataAnuncio[1].text
                    dataAnuncio = dataAnuncio[0].text
                    
                    if ((dataAnuncio.upper() == 'HOJE') or (dataAnuncio.upper() == 'ONTEM')):                        
                        dtAnuncio = funcoes.pegarDataAtual()
                        if (dataAnuncio.upper() == 'ONTEM'):
                            dtAnuncio = funcoes.subData(dtAnuncio,1)
                        dataAnuncio = dtAnuncio.strftime("%d/%m/%Y")          
                    
                    #agora preciso fazer outra raspagem para trazer a descrição do anuncio..
                    pageDescricao       = requests.get(linkAnuncio,headers=headers)
                    soupDescricao       = BeautifulSoup(pageDescricao.text, 'html.parser')                

                        
                    imagensAnuncio = soupDescricao.find_all('div', class_='sc-28oze1-5 bQbWAr')
                    
                    descricaoAnuncio    = soupDescricao.find_all('div', class_='sc-hmzhuo iaXUER sc-jTzLTM iwtnNi')
                    descricaoAnuncio    = descricaoAnuncio[1].span.text                
                    localizacaoAnuncio  = soupDescricao.find_all('dd', class_='sc-1f2ug0x-1 ljYeKO sc-ifAKCX kaNiaQ')                
                    
                    cepAnuncio          = localizacaoAnuncio[0].text
                    cidadeAnuncio       = localizacaoAnuncio[1].text
                    bairroAnuncio       = localizacaoAnuncio[2].text               
                    
                    precoAnuncio = precoAnuncio.replace('R$','')
                    try:
                        precoAnuncio = float(precoAnuncio.replace('.','').replace(',','.'))
                    except:
                        precoAnuncio = 0                    

                    
                    funcoes.addLog('Pos...: '+str(contador)+' de '+str(len(listaCelular)) +' - página: '+str(contadorPagina)+' de '+str(qtdePagina),arrayLog)
                    ''' TABELA PARA RESPOSTAS '''
                    '''
                        1 - Cadastrado, pode pegar
                        2 - Cadastrado, mas está alto o preço
                        3 - Não cadastrado, MOSTRAR NO EMAIL
                        4 - CELULAR NA LISTA NEGRA..

                    '''
                    
                    resposta = funcoes.celularInteressante(tituloAnuncio,descricaoAnuncio,precoAnuncio)
                    
                    
                    if (resposta > 0):                    
                        msgResposta = 'Titulo: '+tituloAnuncio+'\nLink: '+linkAnuncio+'\nPreço: '+str(precoAnuncio)                   
                        
                        if (resposta == 1):
                            funcoes.addLog('Nota...: INTERESSANTE',arrayLog)
                            msgResposta += ' - CADASTRADO E PREÇO BOM\n'
                        elif (resposta == 3):                        
                            msgResposta += ' - NÃO CADASTRADO NA BASE DE DADOS\n'                        
                            funcoes.addLog('Nota...: CELULAR NÃO CADASTRADO NA BASE DE DADOS', arrayLog)
                        elif (resposta == 2):
                            funcoes.addLog('Nota...: CELULAR NO BD, MAS ESTÁ CARO')
                        elif (resposta == 4):
                            funcoes.addLog('Nota...: CELULAR NA LISTA NEGRA', arrayLog)

                        
                        if ((resposta == 1) or ((resposta == 3 and (funcoes.checkFileExistance('apenasCadastrados.inf')==False)))):                        
                            #so cadastra se o anuncio for "novo"
                            if (linkAnuncio not in arrayUrlEnviada):                            
                                arrayEnviarEmail.append(msgResposta)
                                novasUrls.append(linkAnuncio)
                                                  
                    funcoes.addLog('Link..: '+linkAnuncio, arrayLog)
                    funcoes.addLog('Preço.: '+str(precoAnuncio), arrayLog)
                    funcoes.addLog('Data..: '+dataAnuncio+' '+horaAnuncio, arrayLog)
                    funcoes.addLog('Titulo: '+tituloAnuncio, arrayLog)
                    funcoes.addLog('Desc..: '+descricaoAnuncio, arrayLog)
                    funcoes.addLog('-------------------------------------------------', arrayLog)
                    funcoes.addLog('Imagens do anuncio', arrayLog)
                    for x in imagensAnuncio:
                        funcoes.addLog(x.img['src'], arrayLog)
                    funcoes.addLog('', arrayLog) #pulo uma linha para separar a descrição
                    funcoes.addLog(cidadeAnuncio+', '+bairroAnuncio+' - '+cepAnuncio, arrayLog)                
                except Exception as e:
                    funcoes.addLog('Possível Anuncio', arrayLog)
                    
                funcoes.addLog('////////////////////////////////////////////////////////////', arrayLog)
                funcoes.addLog('',arrayLog)

                
    if (len(arrayEnviarEmail) > 0):
        funcoes.enviarEmail(arrayEnviarEmail, 'Encontramos algo!!!',"Encontramos alguns itens que vale apena conferir!\n\n")
        funcoes.addLog('||||||||||||| Email enviado! |||||||||||||', arrayLog)
        funcoes.addLog('SIGA ABAIXO OS CELULARES INTERESSANTES ENVIADOS POR E-MAIL: ', arrayLog)
        funcoes.addLog('', arrayLog)
        for x in arrayEnviarEmail:
            funcoes.addLog(x, arrayLog)            
    #gero aqui um arquivo de log com os dados raspados
    stringLog = ''
    for x in arrayLog:
        stringLog += x + '\n'
    funcoes.criarArquivo(stringLog,'log/'+funcoes.formatarDataParaArquivo(funcoes.pegarDataAtual())+'.txt')
    #funcoes.enviarEmail(arrayLog, 'Log de execução','Segue abaixo log detalhado da operação realizada em '+funcoes.formatarDataParaArquivo(funcoes.pegarDataAtual())+'\n\n')

    #Adiciono as novas urls enviadas por email para nao haver repetição
    archive = open('url_enviada.txt', 'a')
    for x in novasUrls:
        archive.write(x)
    archive.close()
    
