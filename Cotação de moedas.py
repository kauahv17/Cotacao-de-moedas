import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter.filedialog import askopenfilename
import pandas as pd
import requests
from datetime import datetime
import numpy as np

tela = tk.Tk()

requisicao = requests.get("https://economia.awesomeapi.com.br/json/all")
dicionario_moedas = requisicao.json()
lista_moedas = list(dicionario_moedas.keys())

titulo_1moeda = tk.Label(text='cotação de 1 moeda específica',borderwidth=3,relief="solid")
titulo_1moeda.grid(row=0,column=0,padx=10,pady=10,columnspan=3,sticky="NSWE")

pergunta_selecionar = tk.Label(text='selecione a moeda para pegar a cotação:',anchor="e")
pergunta_selecionar.grid(row=1,column=0,padx=10,pady=10,columnspan=2,sticky="NSWE")

combobox_selecionar = ttk.Combobox(values=lista_moedas)
combobox_selecionar.grid(row=1,column=2,padx=10,pady=10,sticky="NSWE")

pergunta_Selecionar_Data = tk.Label(text='selecione a data que deseja pegar a cotação:',anchor="e")
pergunta_Selecionar_Data.grid(row=2,column=0,columnspan=2,padx=10,pady=10,sticky="NSWE")

calendario = DateEntry(year=2023,locale='pt_br')
calendario.grid(row=2,column=2,padx=10,pady=10,sticky="NSWE")

cotacao_1moeda = tk.Label(text='',fg="green")
cotacao_1moeda.grid(row=3,column=0,columnspan=2,padx=10,pady=10,sticky="NSWE")

def pegar_cotacao():
    moeda = combobox_selecionar.get()
    data = calendario.get()
    list_data = data.split(r"/")
    dia = list_data[0]
    mes = list_data[1]
    ano = list_data[2]
    
    link = f"https://economia.awesomeapi.com.br/{moeda}-BRL/10?start_date={ano}{mes}{dia}&end_date={ano}{mes}{dia}"
    
    requisicao_moeda = requests.get(link)
    cotacao = requisicao_moeda.json()
    print(cotacao)
    valor_moeda = cotacao[0]["bid"]
    
    #----------------formatação----------------#
    valor_moeda = f"{float(valor_moeda):_.2f}"
    valor_moeda = valor_moeda.replace(".",",").replace("_",".")
    #------------------------------------------#
    
    cotacao_1moeda["text"] = f"valor da moeda {moeda} no dia estava: R$ {valor_moeda}"
    print(valor_moeda)

botao_1cotacao = tk.Button(text='pegar cotação',command=pegar_cotacao)
botao_1cotacao.grid(row=3,column=2,padx=10,pady=10,sticky="NSWE")

#buscar cotações com multiplas moedas:

titulo_multiplas_moedas = tk.Label(text='cotação de multiplas moedas',borderwidth=3,relief="solid") 
titulo_multiplas_moedas.grid(row=4,column=0,padx=10,pady=10,columnspan=3,sticky="NSWE")

pergunta_arquivo = tk.Label(text='selecione um arquivo em Excel com as Moedas na coluna A:')
pergunta_arquivo.grid(row=5,column=0,padx=10,pady=10,columnspan=2,sticky="NSWE")


def buscar_local():
    caminho_arquivo = askopenfilename(title="selecione um arquivo para abrir")
    vef = "NEGADA"
    if caminho_arquivo:
        if caminho_arquivo[-5:] == ".xlsx":
            vef = "OK"
            var_caminho_arquivo.set(caminho_arquivo)
            mensagem_local_arquivo["fg"] = "green"
            mensagem_local_arquivo['text'] = caminho_arquivo
        else:
            var_caminho_arquivo.set("0")
            mensagem_local_arquivo["fg"] = "red"
            mensagem_local_arquivo['text'] = "o arquivo precisa ser obrigatoriamente de Excel"
    else:
        var_caminho_arquivo.set("0")
        mensagem_local_arquivo["fg"] = "red"
        mensagem_local_arquivo['text'] = "Nenhum arquivo selecionado"
        
    print(f"verificação arquivo = {vef}")
        
var_caminho_arquivo = tk.StringVar(value="0")
    
botao_Selecionar_Arquivo = tk.Button(text='selecionar arquivo',command=buscar_local)
botao_Selecionar_Arquivo.grid(row=5,column=2,padx=10,pady=10,sticky="NSWE")

mensagem_local_arquivo = tk.Label(text='Nenhum arquivo selecionado',fg='red',anchor="e")
mensagem_local_arquivo.grid(row=6,column=0,columnspan=3,padx=10,pady=10,sticky="NSWE")

mensagem_data_inicial = tk.Label(text='selecione a data inicial:')
mensagem_data_inicial.grid(row=7,column=0,padx=10,pady=10,sticky="NSWE")

data_inicial = DateEntry(year=2023,locale='pt_br')
data_inicial.grid(row=7,column=1,padx=10,pady=10,sticky="NSWE")

mensagem_data_final = tk.Label(text='selecione a data final:')
mensagem_data_final.grid(row=8,column=0,padx=10,pady=10,sticky="NSWE")

data_final = DateEntry(year=2023,locale='pt_br')
data_final.grid(row=8,column=1,padx=10,pady=10,sticky="NSWE")
print('')
def mudar_cotacao_arquivo():
    if var_caminho_arquivo.get() != "0":
        try:
            # ler o dataframe de moedas
            df = pd.read_excel(var_caminho_arquivo.get())
            moedas = df.iloc[:, 0]
            # pegar a data de inicio e data de fim das cotacoes
            df = pd.read_excel(var_caminho_arquivo.get())
            tamanho = 200

            inicial = data_inicial.get()
            final = data_final.get()

            list_data_inicial = inicial.split(r"/")
            dia_inicial = list_data_inicial[0]
            mes_inicial = list_data_inicial[1]
            ano_inicial = list_data_inicial[2]

            list_data_final = final.split(r"/")
            dia_final = list_data_final[0]
            mes_final = list_data_final[1]
            ano_final = list_data_final[2]

            for moeda in moedas:
                link = f"https://economia.awesomeapi.com.br/json/daily/{moeda}-BRL/{tamanho}?" \
                       f"start_date={ano_inicial}{mes_inicial}{dia_inicial}&" \
                       f"end_date={ano_final}{mes_final}{dia_final}"
                print(link)
                requisicao_moeda = requests.get(link)
                cotacoes = requisicao_moeda.json()
                for cotacao in cotacoes:
                    timestamp = int(cotacao['timestamp'])
                    valor_moeda = float(cotacao['bid'])
                    #----------------formatação----------------#
                    valor_moeda = f"{float(valor_moeda):_.2f}"
                    valor_moeda = valor_moeda.replace(".",",").replace("_",".")
                    #------------------------------------------#
                    data = datetime.fromtimestamp(timestamp)
                    data = data.strftime('%d/%m/%Y')
                    if data not in df:
                        df[data] = np.nan

                    df.loc[df.iloc[:, 0] == moeda, data] = valor_moeda
            df.to_excel("cotações - moedas (novo).xlsx")
            mensagem_cotacao_atualizada["fg"] = "green"
            mensagem_cotacao_atualizada['text'] = "Arquivo Atualizado com Sucesso"
            
            mensagem_local_cotacao = tk.Label(text='o arquivo foi criado na mesma pasta do arquivo fornecido',fg="green")
            mensagem_local_cotacao.grid(row=10,column=0,columnspan=2,padx=10,pady=10,sticky="NSWE")
            print('')
            print(df)
            
        except:
            mensagem_cotacao_atualizada["fg"] = "red"
            mensagem_cotacao_atualizada['text'] = "todas as moedas tem que estar na coluna A do excel"
    else:
        mensagem_cotacao_atualizada["fg"] = "red"
        mensagem_cotacao_atualizada["text"] = "Selecione o arquivo certo"

botao_atualizar_arquivo = tk.Button(text='atualizar cotação',command=mudar_cotacao_arquivo)
botao_atualizar_arquivo.grid(row=9,column=0,padx=10,pady=10,sticky="NSWE")

mensagem_cotacao_atualizada = tk.Label(text='',fg="green")
mensagem_cotacao_atualizada.grid(row=9,column=1,columnspan=2,padx=10,pady=10,sticky="NSWE")

botao_fechar = tk.Button(text='Fechar',command=tela.destroy)
botao_fechar.grid(row=10,column=2,padx=10,pady=10,sticky="NSWE")

tela.mainloop()