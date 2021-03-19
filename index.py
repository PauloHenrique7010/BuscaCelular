import requests
from bs4 import BeautifulSoup
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

arquivo = open('o_que_buscar.txt', 'r')
#para cada linha, ele ira pesquisar alguma coisa
for linha in arquivo:
    celularDaVez = linha
    celularDaVez = celularDaVez.replace(' ', '%20')    
    url = "https://sp.olx.com.br/vale-do-paraiba-e-litoral-norte/eletronicos-e-celulares?q="+celularDaVez   

    page = requests.get(url,headers=headers)
    #print(page.status_code)
    #print(page.text)

    soup = BeautifulSoup(page.text, 'html.parser')
    print('estou aqui')
    teste = soup.find_all('li', class_='sc-1fcmfeb-2')
    for x in teste:
        print (x)
    
    '''soup.find_all(id='third')
    teste = soup.find_all('li', class_='fnmrjs-6 iNpuEh')
    for x in teste:
        print(teste)
        break
    '''
    break

    
    

arquivo.close()
