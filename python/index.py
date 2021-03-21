import funcoes
import requests
from bs4 import BeautifulSoup

#user-agent serve para simular como se eu fosse um navegador acessando a pagina
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

if (funcoes.checkFileExistance('o_que_buscar.txt') == False):
    print('O arquivo "o_que_buscar.txt" não existe do diretório deste arquivo python.')
else:  
    #os itens a serem pesquisados estão neste arquivo..
    arquivo = open('o_que_buscar.txt', 'r')
    arrayEnviarEmail = []
    arrayLog = []
   
    
    #para cada linha, ele ira pesquisar alguma coisa
    for linha in arquivo:
        funcoes.addLog('Pesquisando na olx como: '+linha, arrayLog)
        celularDaVez = linha
        celularDaVez = celularDaVez.replace(' ', '%20') #na url, é trocado o espaço por "%20"   
        url = "https://sp.olx.com.br/vale-do-paraiba-e-litoral-norte/eletronicos-e-celulares?q="+celularDaVez+'&sf=1'   

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

                
                funcoes.addLog('Pos...: '+str(contador)+' de '+str(len(listaCelular)),arrayLog)
                ''' TABELA PARA RESPOSTAS '''
                '''
                    1 - Cadastrado, pode pegar
                    2 - Cadastrado, mas está alto o preço
                    3 - Não cadastrado, MOSTRAR NO EMAIL
                    4 - CELULAR NA LISTA NEGRA..

                '''
                
                resposta = funcoes.celularInteressante(tituloAnuncio,descricaoAnuncio,precoAnuncio)
                
                
                if (resposta > 0):                    
                    msgResposta = 'Titulo: '+tituloAnuncio+'\nLink: '+linkAnuncio                   
                    
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
                    
                    if ((resposta == 1) or (resposta == 3)):
                        arrayEnviarEmail.append(msgResposta)
                
                    
                                              
                funcoes.addLog('Link..: '+linkAnuncio, arrayLog)
                funcoes.addLog('Preço.: '+str(precoAnuncio), arrayLog)
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
            funcoes.enviarEmail(arrayEnviarEmail)
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

    arquivo.close()
