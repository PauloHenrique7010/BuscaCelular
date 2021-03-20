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
   
    
    #para cada linha, ele ira pesquisar alguma coisa
    for linha in arquivo:
        print('Pesquisando na olx como: '+linha)
        celularDaVez = linha
        celularDaVez = celularDaVez.replace(' ', '%20') #na url, é trocado o espaço por "%20"   
        url = "https://sp.olx.com.br/vale-do-paraiba-e-litoral-norte/eletronicos-e-celulares?q="+celularDaVez+'&sf=1'   

        page = requests.get(url,headers=headers)
        #print(page.status_code) 200 para resposta OK
        #print(page.text) # consigo ver o codigo fonte da pagina
        arquivo = open('arquivoRaspado.html','w')
        arquivo.write(page.text)
        arquivo.close()       

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
            print('////////////////////////////////////////////////////////////')
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
                
                if (funcoes.celularInteressante(tituloAnuncio,descricaoAnuncio,precoAnuncio)):
                    arrayEnviarEmail.append('Titulo: '+tituloAnuncio+'\nLink:'+linkAnuncio)
                    print('ANÚNCIO INTERESSANTE')                
                               
    
                print('Pos...: '+str(contador)+' de '+str(len(listaCelular)))                
                print('Link..: '+linkAnuncio)
                print('Preço.: '+str(precoAnuncio))                
                print('Titulo: '+tituloAnuncio)                               
                print('---------------------------------------')
                print('Desc..: '+descricaoAnuncio)
                print('---------------------------------------')
                print('Imagens do anuncio')
                for x in imagensAnuncio:
                    print(x.img['src'])
                print('') #pulo uma linha para separar a descrição
                print(cidadeAnuncio+', '+bairroAnuncio+' - '+cepAnuncio)
            except: 
              print('ocorreu algum erro')
            print('////////////////////////////////////////////////////////////')
            print('')
        
        if (len(arrayEnviarEmail) > 0):
            funcoes.enviarEmail(arrayEnviarEmail)
    
    arquivo.close()
