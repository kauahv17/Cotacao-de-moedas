from bs4 import BeautifulSoup as bs4
import tkinter as tk
import requests
import re

tela = tk.Tk()
tela.title('pesquisa WEB - cotação'.upper())

cor_borda = '#2c2c2c'.upper()

margem_cima = tk.Label(text='',bg='black',height=1,width=100)
margem_cima.grid(row=0,column=1,columnspan = 6,sticky="NSWE")

margem_left = tk.Label(text='',bg='black',height=1,width=5)
margem_left.grid(row=0,column=0,rowspan = 6,sticky="NSWE")

margem_right = tk.Label(text='',bg='black',height=1,width=5)
margem_right.grid(row=0,column=8,rowspan = 6,sticky="NSWE")

margem_baixo = tk.Label(text='',bg='black',height=1,width=100)
margem_baixo.grid(row=5,column=1,columnspan = 6,sticky="NSWE")

mensagem = tk.Label(text = 'busca de cotação de moedas'.upper(),bg='black',fg='red', font=("Arial", 20),height=11,width=40)
mensagem.grid(row=1,column=1,columnspan = 6,sticky="NSWE")

pergunta = tk.Label(text = 'digite o nome da moeda:'.upper(),bg='black',fg='red', font=("Arial", 13),height=2)
pergunta.grid(row=3,column=1,columnspan = 3,sticky="NSWE")

pesquisa = tk.Entry(bg = 'red',fg = 'black', font=("Arial", 16))
pesquisa.grid(row = 3,column = 4,columnspan=2,sticky="NSWE")

resposta = tk.Label(text='',bg='black',fg='green', font=("Arial", 11))
resposta.grid(row=4,column=1,columnspan=3,sticky="NSWE")

nada = tk.Label(text='',bg='black')
nada.grid(row=3,column=6,rowspan=2,sticky="NSWE")

def pesquisa_WEB():
    moeda = pesquisa.get()
    moeda = moeda.casefold()
    link = f'https://www.google.com/search?q=valor+{moeda}&oq=valor+&aqs=chrome.0.69i59j69i64j69i57j69i59l2j0i131i433i512l2j69i60.1854j1j7&sourceid=chrome&ie=UTF-8'
    requisicao = requests.get(link)
    site = bs4(requisicao.text,'html.parser')
    
    DIVs = site.find_all('div')
    
    for div in DIVs:
        vet = div.find_all(string = re.compile('Real'))
        try:
            if 'Real' in vet[0]:
                lista = vet[0]
                lista = lista.replace(' ','_')
                vet_valor = lista.split('_')
                valor = vet_valor[0]
                resposta["text"] = f'cotação atual do {moeda}:'.upper() + f' R$ {valor} Reais'
            break
        except IndexError:
            continue

tela.columnconfigure([0,8], weight = 1)
tela.rowconfigure([1], weight = 1)
            
botao = tk.Button(text = 'buscar'.upper(),command=pesquisa_WEB)
botao.grid(row=4,column=4,columnspan = 2,sticky="NSWE")

tela.mainloop()