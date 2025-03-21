import tkinter as tk
import ttkbootstrap as ttkb
import unicodedata
import threading
from tkinter import ttk
from tkinter import messagebox
from banco import estoqueEditarProduto
from cores import cor_fundo, cor_texto  
    
def editar_estoque(container, item, tenant_id):
    
    for widget in container.winfo_children():
        widget.destroy()
    
    def editar_campos():
        
        lista_para_edicao = []
        
        id    = item[0]
        
        lista_para_edicao.append({'id': id})
        
        nome_novo = nome.get().strip()
        
        lista_para_edicao.append({'nome': nome_novo})
        
        quantidade_novo = quantidade.get().strip()
        
        lista_para_edicao.append({'quantidade': quantidade_novo})
        
        preco_novo = preco.get().strip()
        
        lista_para_edicao.append({'preco': preco_novo})
        
        combo_novo = combo.get().strip()
        
        lista_para_edicao.append({'ativo_sn': combo_novo})
        
        tipo = "Editar"
        
        estoqueEditarProduto(lista_para_edicao, tenant_id, tipo)
        
        from estoque import abrirEstoque
        
        abrirEstoque(container, tenant_id)
        
    
    ttk.Label(container, text="Editar produtos", font=("Arial", 12, "bold"), background=cor_fundo, foreground=cor_texto).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="w")
    
    ttk.Label(container, text="Nome:", background=cor_fundo, foreground=cor_texto).grid(row=1, column=0, padx=10, pady=5, sticky="w")
    nome = ttk.Entry(container, width=50)
    nome.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
    
    ttk.Label(container, text="Quantidade:", background=cor_fundo, foreground=cor_texto).grid(row=2, column=0, padx=10, pady=5, sticky="w")
    quantidade = ttk.Entry(container, width=50)
    quantidade.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
    
    ttk.Label(container, text="Preço:", background=cor_fundo, foreground=cor_texto).grid(row=3, column=0, padx=10, pady=5, sticky="w")
    preco = ttk.Entry(container, width=50)
    preco.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
    
    ttk.Label(container, text="Ativo:", background=cor_fundo, foreground=cor_texto).grid(row=4, column=0, padx=10, pady=5, sticky="w")
    opcoes = ["Sim", "Não"]
    combo = ttk.Combobox(container, values=opcoes, state="readonly", width=20)
    combo.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
    
    btn_adicionar = ttk.Button(container, text="Editar produto", command=editar_campos)
    btn_adicionar.grid(row=6, column=1, padx=10, pady=10, sticky="ew")
   
    if(item != ""):
        
        nome_item    = item[1]
        nome.insert(0, nome_item)
        quantidade_item   = item[2]
        quantidade.insert(0, quantidade_item)
        preco_item   = item[3]
        preco.insert(0, preco_item)
        combo_item = "Sim"
        combo.set(combo_item)

        
    container.grid_columnconfigure(0, weight=0)
    container.grid_columnconfigure(1, weight=0)
    container.grid_rowconfigure(1, weight=0)
    container.grid_rowconfigure(3, weight=0)
    container.grid_rowconfigure(4, weight=0)
    container.grid_rowconfigure(5, weight=0)
    container.grid_rowconfigure(6, weight=0)
    