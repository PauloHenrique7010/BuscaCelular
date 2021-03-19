import requests
from bs4 import BeautifulSoup
#user-agent serve para simular como se eu fosse um navegador acessando a pagina
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

#os itens a serem pesquisados estão neste arquivo..
arquivo = open('o_que_buscar.txt', 'r')

#para cada linha, ele ira pesquisar alguma coisa
for linha in arquivo:
    celularDaVez = linha
    celularDaVez = celularDaVez.replace(' ', '%20') #na url, é trocado o espaço por "%20"   
    url = "https://sp.olx.com.br/vale-do-paraiba-e-litoral-norte/eletronicos-e-celulares?q="+celularDaVez   

    page = requests.get(url,headers=headers)
    #print(page.status_code) 200 para resposta OK
    #print(page.text) # consigo ver o codigo fonte da pagina

    #converto para um tipo onde posso navegar entre os trechos html
    soup = BeautifulSoup(page.text, 'html.parser')

    #procuro onde começa a lista de anuncios
    listaCelular = soup.find_all('li', class_='sc-1fcmfeb-2')

    #para cada bloco de anuncio
    for x in listaCelular:
        primeiro = x        
        #primeiro = listaCelular[2]
        '''faço um try catch para quando o anuncio
            da olx for um anuncio de publicidade'''
        try:
            linkAnuncio = primeiro.a['href']           
    
            infoAnuncio = primeiro.div.find('div', class_ = 'fnmrjs-2 jiSLYe')
            tituloAnuncio = infoAnuncio.div.find('div', class_ = 'fnmrjs-6 iNpuEh').text
            precoAnuncio = infoAnuncio.div.find('div', class_ = 'fnmrjs-9 gqfQzY').text

            

            #agora preciso fazer outra raspagem para trazer a descrição do anuncio..
            pageDescricao = requests.get(linkAnuncio,headers=headers)
            soupDescricao = BeautifulSoup(pageDescricao.text, 'html.parser')            
            descricaoAnuncio = soupDescricao.find_all('div', class_='sc-hmzhuo iaXUER sc-jTzLTM iwtnNi')
            descricaoAnuncio = descricaoAnuncio[1].span.text

            print('Titulo: '+tituloAnuncio)
            print('Preço.: '+precoAnuncio)
            print('Link..: '+linkAnuncio)
            print('Desc..: '+descricaoAnuncio)
        except:
          print('')
        break
    break    
    

arquivo.close()
