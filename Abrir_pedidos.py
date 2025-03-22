import tkinter as tk
import ttkbootstrap as ttkb
import unicodedata
import threading
from tkinter import ttk
from tkinter import messagebox
from banco import pegar_pedidos_produto
from cores import cor_fundo, cor_texto  
    
def Abrir_pedidos(container, item, tenant_id):
    
    for widget in container.winfo_children():
        widget.destroy() 


    id_pedido = int(item[0])


    retorno_banco = pegar_pedidos_produto(id_pedido)

    # print(retorno_banco)
    # exit()
    
        
    ttk.Label(container, text="Listar pedidos", font=("Arial", 12, "bold"), background=cor_fundo, foreground=cor_texto).grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")
    
    colunas = ("Produtos", "Quantidade", "Valor")
    lista_produto = ttk.Treeview(container, columns=colunas, show="headings", height=6)


    lista_produto.heading("Produtos", text="Produtos", anchor="w")
    lista_produto.heading("Quantidade", text="Quantidade", anchor="w")
    lista_produto.heading("Valor", text="Valor", anchor="w")
    
    lista_produto.bind("<Motion>", lambda event: lista_produto.config(cursor="hand2"))
    lista_produto.bind("<Leave>", lambda event: lista_produto.config(cursor=""))
    
    lista_produto.grid(row=2, column=0, columnspan=3, sticky="nsew")


    for item2 in retorno_banco:
        
        lista_produto.insert("", "end", values=(item2["nome_produto"], item2["quantidade_produto"], item2["valor_doproduto"]))


    container.grid_columnconfigure(0, weight=0)
    container.grid_rowconfigure(0, weight=0)
    container.grid_rowconfigure(1, weight=0)
    container.grid_rowconfigure(2, weight=0)