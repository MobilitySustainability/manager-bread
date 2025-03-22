import tkinter as tk
import ttkbootstrap as ttkb
import matplotlib.pyplot as plt
import numpy as np
import threading
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from carregamento_de_telas import carregamento
from banco import pegar_pedidos
from cores import cor_fundo, cor_texto

def AbrirPedidos(container, tenant_id):
      
    def carregar():
    
        carregamento(container)
        
        lista_codigo_pedido = pegar_pedidos(tenant_id)
        
        container.after(0, pedidos, container, lista_codigo_pedido, tenant_id)
        
    thread = threading.Thread(target=carregar)
    thread.start()
      

def pedidos(container, lista_codigo_pedido, tenant_id):

    for widget in container.winfo_children():
            widget.destroy()

    def editar(event, lista_produto, container):
        
        from Abrir_pedidos import Abrir_pedidos
        
        item = lista_produto.selection()
        
        if(item != ""):
            item = lista_produto.item(item)["values"]
        
        Abrir_pedidos(container, item, tenant_id)


    ttk.Label(container, text="Controle de pedidos", font=("Arial", 12, "bold"), background=cor_fundo, foreground=cor_texto).grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")
    
    colunas = ("Nº do Pedido", "Vendedor", "Valor")
    lista_produto = ttk.Treeview(container, columns=colunas, show="headings", height=6)


    lista_produto.heading("Nº do Pedido", text="Nº do Pedido", anchor="w")
    lista_produto.heading("Vendedor", text="Vendedor", anchor="w")
    lista_produto.heading("Valor", text="Valor", anchor="w")
    
    lista_produto.bind("<Motion>", lambda event: lista_produto.config(cursor="hand2"))
    lista_produto.bind("<Leave>", lambda event: lista_produto.config(cursor=""))
    
    lista_produto.grid(row=2, column=0, columnspan=3, sticky="nsew")

    lista_produto.bind("<ButtonRelease-1>", lambda event: editar(event, lista_produto, container))


    for item in lista_codigo_pedido:
        lista_produto.insert("", "end", values=(item["id"], item["cliente"], item["valor"]))


    container.grid_columnconfigure(0, weight=0)
    container.grid_rowconfigure(0, weight=0)
    container.grid_rowconfigure(1, weight=0)
    container.grid_rowconfigure(2, weight=0)