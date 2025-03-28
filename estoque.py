import tkinter as tk
import ttkbootstrap as ttkb
import matplotlib.pyplot as plt
import numpy as np
import subprocess
import threading
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from carregamento_de_telas import carregamento
from banco import estoque_listar_itens, estoqueEditarProduto

from cores import cor_fundo, cor_texto

def abrirEstoque(container, tenant_id):
    
    def carregar():
        
        carregamento(container)
        
        listaDeItens = estoque_listar_itens(tenant_id)
        
        container.after(0, estoque, container, listaDeItens, tenant_id)
        
    thread = threading.Thread(target=carregar)
    thread.start()


def estoque(container, listaDeItens, tenant_id):
    
    # Desabilitar a propagação de layout no container
    container.grid_propagate(False)
    
    for widget in container.winfo_children():
        widget.destroy()

    def editar(event, listaEstoque, container):
        from editar_estoque import editar_estoque
        item = listaEstoque.selection()
        
        if(item != ""):
            item = listaEstoque.item(item)["values"]
        
        editar_estoque(container, item, tenant_id)

    def adicionar_produto():
        
        lista_para_edicao = []
        nome       = entry_nome.get().strip()
        quantidade = entry_quantidade.get().strip()
        preco      = entry_preco.get().strip()
        combo_novo = combo.get().strip()
        
        lista_para_edicao.append({'nome': nome})
        lista_para_edicao.append({'quantidade': quantidade})
        lista_para_edicao.append({'preco': preco})
        lista_para_edicao.append({'tipo_produto': combo_novo})
        
        tipo = "Adicionar"
        
        retorno_adicionar = estoqueEditarProduto(lista_para_edicao, tenant_id, tipo)
        
        if retorno_adicionar:
            
            listaDeItens = estoque_listar_itens(tenant_id)
            listaEstoque.delete(*listaEstoque.get_children())
            for item in listaDeItens:
                listaEstoque.insert("", "end", values=(item["id"], item["nome"], item["quant"], item["valor"]))
    
    ttk.Label(container, text="Cadastro de produtos", font=("Arial", 24, "bold"), background=cor_fundo, foreground=cor_texto).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="w")
    
    # Formulário de Cadastro
    ttk.Label(container, text="Nome:", background=cor_fundo, foreground=cor_texto).grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_nome = ttk.Entry(container, width=50)
    entry_nome.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    ttk.Label(container, text="Quantidade:", background=cor_fundo, foreground=cor_texto).grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_quantidade = ttk.Entry(container, width=50)
    entry_quantidade.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    ttk.Label(container, text="Preço:", background=cor_fundo, foreground=cor_texto).grid(row=3, column=0, padx=10, pady=5, sticky="w")
    entry_preco = ttk.Entry(container, width=50)
    entry_preco.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
    
    ttk.Label(container, text="Tipo:", background=cor_fundo, foreground=cor_texto).grid(row=4, column=0, padx=10, pady=5, sticky="w")
    opcoes = ["Pães", "Bolos", "Salgados", "Bebidas"]
    combo = ttk.Combobox(container, values=opcoes, state="readonly", width=20)
    combo.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

    btn_adicionar = ttk.Button(container, text="Adicionar produto", command=adicionar_produto)
    btn_adicionar.grid(row=6, column=1, padx=10, pady=10, sticky="ew")

    ttk.Label(container, text="Estoque disponível", font=("Arial", 12, "bold"), background=cor_fundo, foreground=cor_texto).grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky="w")
    
    colunas = ("ID", "Nome", "Quantidade", "Preço")
    listaEstoque = ttk.Treeview(container, columns=colunas, show="headings", height=6)

    listaEstoque.heading("ID", text="ID", anchor="w")
    listaEstoque.heading("Nome", text="Nome", anchor="w")
    listaEstoque.heading("Quantidade", text="Quantidade", anchor="w")
    listaEstoque.heading("Preço", text="Preço", anchor="w")

    listaEstoque.bind("<Motion>", lambda event: listaEstoque.config(cursor="hand2"))
    listaEstoque.bind("<Leave>", lambda event: listaEstoque.config(cursor=""))

    listaEstoque.grid(row=8, column=0, columnspan=4, sticky="nsew")

    listaEstoque.bind("<ButtonRelease-1>", lambda event: editar(event, listaEstoque, container))
    
    listaEstoque.delete(*listaEstoque.get_children())
    for item in listaDeItens:
        listaEstoque.insert("", "end", values=(item["id"], item["nome"], item["quant"], item["valor"]))
    
    # Ajustando a configuração das colunas e linhas para manter o layout fixo
    container.grid_columnconfigure(0, weight=0, minsize=100)
    container.grid_columnconfigure(1, weight=1, minsize=200)
    container.grid_rowconfigure(1, weight=0, minsize=30)
    container.grid_rowconfigure(2, weight=0, minsize=30)
    container.grid_rowconfigure(3, weight=0, minsize=30)
    container.grid_rowconfigure(4, weight=0, minsize=30)
    container.grid_rowconfigure(5, weight=0, minsize=30)
    container.grid_rowconfigure(6, weight=0, minsize=30)
    container.grid_rowconfigure(7, weight=0, minsize=30)
    container.grid_rowconfigure(8, weight=1, minsize=100)

    
    for widget in container.winfo_children():
        widget.destroy()
        
        
    def editar(event, listaEstoque, container):
        from editar_estoque import editar_estoque
        item = listaEstoque.selection()
        
        if(item != ""):
            item = listaEstoque.item(item)["values"]
        
        editar_estoque(container, item, tenant_id)
        
    def adicionar_produto():
        
        lista_para_edicao = []
        nome       = entry_nome.get().strip()
        quantidade = entry_quantidade.get().strip()
        preco      = entry_preco.get().strip()
        combo_novo = combo.get().strip()
        
        lista_para_edicao.append({'nome': nome})
        lista_para_edicao.append({'quantidade': quantidade})
        lista_para_edicao.append({'preco': preco})
        lista_para_edicao.append({'tipo_produto': combo_novo})
        
        tipo = "Adicionar"
        
        retorno_adicionar = estoqueEditarProduto(lista_para_edicao, tenant_id, tipo)
        
        if retorno_adicionar:
            
            listaDeItens = estoque_listar_itens(tenant_id)
            listaEstoque.delete(*listaEstoque.get_children())
            for item in listaDeItens:
                listaEstoque.insert("", "end", values=(item["id"], item["nome"], item["quant"], item["valor"]))
            
    
    ttk.Label(container, text="Cadastro de produtos", font=("Arial", 12, "bold"), background=cor_fundo, foreground=cor_texto).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="w")
    
    # Formulário de Cadastro
    ttk.Label(container, text="Nome:", background=cor_fundo, foreground=cor_texto).grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_nome = ttk.Entry(container, width=50)
    entry_nome.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    ttk.Label(container, text="Quantidade:", background=cor_fundo, foreground=cor_texto).grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_quantidade = ttk.Entry(container, width=50)
    entry_quantidade.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    ttk.Label(container, text="Preço:", background=cor_fundo, foreground=cor_texto).grid(row=3, column=0, padx=10, pady=5, sticky="w")
    entry_preco = ttk.Entry(container, width=50)
    entry_preco.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
    
    ttk.Label(container, text="Tipo:", background=cor_fundo, foreground=cor_texto).grid(row=4, column=0, padx=10, pady=5, sticky="w")
    opcoes = ["Pães", "Bolos", "Salgados", "Bebidas", "Pães", "Bebidas"]
    combo = ttk.Combobox(container, values=opcoes, state="readonly", width=20)
    combo.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

    btn_adicionar = ttk.Button(container, text="Adicionar produto", command=adicionar_produto)
    btn_adicionar.grid(row=6, column=1, padx=10, pady=10, sticky="ew")
    
    
        
    ttk.Label(container, text="Estoque disponivel", font=("Arial", 12, "bold"), background=cor_fundo, foreground=cor_texto).grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky="w")
    
    colunas = ("ID", "Nome", "Quantidade", "Preço")
    listaEstoque = ttk.Treeview(container, columns=colunas, show="headings", height=6)

    listaEstoque.heading("ID", text="ID", anchor="w")
    listaEstoque.heading("Nome", text="Nome", anchor="w")
    listaEstoque.heading("Quantidade", text="Quantidade", anchor="w")
    listaEstoque.heading("Preço", text="Preço", anchor="w")

    listaEstoque.bind("<Motion>", lambda event: listaEstoque.config(cursor="hand2"))
    listaEstoque.bind("<Leave>", lambda event: listaEstoque.config(cursor=""))

    listaEstoque.grid(row=8, column=0, columnspan=4, sticky="nsew")
    
    listaEstoque.bind("<ButtonRelease-1>", lambda event: editar(event, listaEstoque,container))
    
    listaEstoque.delete(*listaEstoque.get_children())
    for item in listaDeItens:
        
        listaEstoque.insert("", "end", values=(item["id"], item["nome"], item["quant"], item["valor"]))
    
    
    container.grid_columnconfigure(0, weight=0)
    container.grid_columnconfigure(1, weight=0)
    container.grid_rowconfigure(1, weight=0)
    container.grid_rowconfigure(3, weight=0)
    container.grid_rowconfigure(4, weight=0)
    container.grid_rowconfigure(5, weight=0)
    container.grid_rowconfigure(6, weight=0)
    container.grid_rowconfigure(7, weight=0)
    container.grid_rowconfigure(8, weight=0)