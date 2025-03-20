import tkinter as tk
import ttkbootstrap as ttkb
import unicodedata
import threading
from tkinter import ttk
from tkinter import messagebox
from carregamento_de_telas import carregamento
from banco import pegar_funcionarios, CadEditarFunc
from carregamento_de_telas import carregamento
from editar_funcionario import editar_funcionario
from cores import cor_fundo, cor_texto, cor_borda, cor_botao, cor_sair, cor_hover_botao, cor_hover_sair

def AbrirFuncionario(container, tenant_id):
    
    def carregar():
        
        carregamento(container)
        
        funcionarios = pegar_funcionarios(tenant_id)
        
        container.after(0, funcionario, container, funcionarios, tenant_id)
        
    thread = threading.Thread(target=carregar)
    thread.start()

def funcionario(container, funcionarios, tenant_id):
    
    for widget in container.winfo_children():
        widget.destroy()
    

    def adicionar_funcionario():
        
        lista_para_edicao = []
        
        nome_novo = nome.get().strip()
        
        lista_para_edicao.append({'nome': nome_novo})
        
        email_novo = email.get().strip()
        
        lista_para_edicao.append({'email': email_novo})
        
        senha_novo = senha.get().strip()
        
        lista_para_edicao.append({'senha': senha_novo})
        
        tipo = "Adicionar"
        
        CadEditarFunc(lista_para_edicao, tenant_id, tipo)
        
        funcionarios = pegar_funcionarios(tenant_id)
        lista_funcionario.delete(*lista_funcionario.get_children())
        for item in funcionarios:
            lista_funcionario.insert("", "end", values=(item["Nome"], item["Email"], "📝"))
        
        
        
    def editar(event, lista_funcionario, container):
        
        item = lista_funcionario.selection()
        
        if(item != ""):
            item = lista_funcionario.item(item)["values"]
        
        editar_funcionario(container, item)

    ttk.Label(container, text="Nome:", background=cor_fundo, foreground=cor_texto).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    nome = ttk.Entry(container,background=cor_fundo, width=50)
    nome.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
    
    ttk.Label(container, text="Email:", background=cor_fundo, foreground=cor_texto).grid(row=1, column=0, padx=10, pady=5, sticky="w")
    email = ttk.Entry(container,background=cor_fundo, width=50)
    email.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
    
    ttk.Label(container, text="Senha:", background=cor_fundo, foreground=cor_texto).grid(row=2, column=0, padx=10, pady=5, sticky="w")
    senha = ttk.Entry(container,background=cor_fundo, width=50)
    senha.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
    
    ttk.Label(container, text="", background=cor_fundo, foreground=cor_texto).grid(row=3, column=0, padx=10, pady=5, sticky="w")
    btn_adicionar = ttk.Button(container, text="Adicionar", command=adicionar_funcionario)
    btn_adicionar.grid(row=4, column=1, sticky="ew")
    ttk.Label(container, text="", background=cor_fundo, foreground=cor_texto).grid(row=5, column=0, padx=10, pady=5, sticky="w")
    
    
    colunas = ("Nome", "E-mail", "Editar")
    lista_funcionario = ttk.Treeview(container, columns=colunas, show="headings", height=6)

    lista_funcionario.heading("Nome", text="Nome", anchor="w")
    lista_funcionario.heading("E-mail", text="E-mail", anchor="w")
    lista_funcionario.heading("Editar", text="Editar", anchor="w")

    lista_funcionario.bind("<Motion>", lambda event: lista_funcionario.config(cursor="hand2"))
    lista_funcionario.bind("<Leave>", lambda event: lista_funcionario.config(cursor=""))

    lista_funcionario.grid(row=6, column=0, padx=10, columnspan=3, sticky="nsew")
    # container.grid_rowconfigure(4, weight=1)
    
    lista_funcionario.bind("<ButtonRelease-1>", lambda event: editar(event, lista_funcionario,container))
    
    for item in funcionarios:
        
        lista_funcionario.insert("", "end", values=(item["Nome"], item["Email"], "📝"))
        
        
    