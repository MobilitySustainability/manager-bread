import tkinter as tk
import ttkbootstrap as ttkb
import unicodedata
import threading
from tkinter import ttk
from tkinter import messagebox
from banco import CadEditarFunc
from cores import cor_fundo, cor_texto  
    
def editar_funcionario(container, funcionarios, tenant_id):
    
    for widget in container.winfo_children():
        widget.destroy()
    
    def editar_campos():
        
        lista_para_edicao = []
        
        id = funcionarios[0]
        
        lista_para_edicao.append({'id': id})
        
        nome_novo = nome.get().strip()
        
        lista_para_edicao.append({'nome': nome_novo})
        
        email_novo = email.get().strip()
        
        lista_para_edicao.append({'email': email_novo})
        
        combo_novo = combo.get().strip()
        
        lista_para_edicao.append({'ativo_sn': combo_novo})
        
        tipo = "Editar"
        
        CadEditarFunc(lista_para_edicao, tenant_id, tipo)
        
        from funcionario import AbrirFuncionario
        
        AbrirFuncionario(container, tenant_id)
        
        
        
    ttk.Label(container, text="Editar funcionario", font=("Arial", 12, "bold"), background=cor_fundo, foreground=cor_texto).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="w")
    
    ttk.Label(container, text="Nome:", background=cor_fundo, foreground=cor_texto).grid(row=1, column=0, padx=10, pady=5, sticky="w")
    nome = ttk.Entry(container, width=50)
    nome.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
    
    ttk.Label(container, text="Email:", background=cor_fundo, foreground=cor_texto).grid(row=2, column=0, padx=10, pady=5, sticky="w")
    email = ttk.Entry(container, width=50)
    email.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
    
    ttk.Label(container, text="Ativo:", background=cor_fundo, foreground=cor_texto).grid(row=3, column=0, padx=10, pady=5, sticky="w")
    opcoes = ["Sim", "Não"]
    combo = ttk.Combobox(container, values=opcoes, state="readonly", width=20)
    combo.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
    
    btn_adicionar = ttk.Button(container, text="Editar", command=editar_campos)
    btn_adicionar.grid(row=4, column=1, padx=10, pady=10, sticky="ew")
    
    
    if(funcionarios != ""):
        
        nome_item    = funcionarios[1]
        nome.insert(0, nome_item)
        email_item   = funcionarios[2]
        email.insert(0, email_item)
        nome_item = "Sim"
        combo.set(nome_item)

        
    container.grid_columnconfigure(0, weight=0)
    container.grid_columnconfigure(1, weight=0)
    container.grid_rowconfigure(1, weight=0)
    container.grid_rowconfigure(3, weight=0)
    container.grid_rowconfigure(4, weight=0)
        
    