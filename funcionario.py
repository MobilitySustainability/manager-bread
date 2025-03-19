import tkinter as tk
import ttkbootstrap as ttkb
import unicodedata
import threading
from tkinter import ttk
from tkinter import messagebox
from carregamento_de_telas import carregamento
from banco import pegar_funcionarios
from carregamento_de_telas import carregamento
from cores import cor_fundo, cor_texto, cor_borda, cor_botao, cor_sair, cor_hover_botao, cor_hover_sair

def AbrirFuncionario(container):
    
    def carregar():
        
        carregamento(container)
        
        funcionarios = pegar_funcionarios()
        
        container.after(0, funcionario, container, funcionarios)
        
    thread = threading.Thread(target=carregar)
    thread.start()

def funcionario(container, funcionarios):
    
    for widget in container.winfo_children():
        widget.destroy()
    



    ttk.Label(container, text="Nome:", background=cor_fundo, foreground=cor_texto).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    nome = ttk.Entry(container,background=cor_fundo, width=50)
    nome.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
    
    ttk.Label(container, text="Email:", background=cor_fundo, foreground=cor_texto).grid(row=1, column=0, padx=10, pady=5, sticky="w")
    email = ttk.Entry(container,background=cor_fundo, width=50)
    email.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
    
    ttk.Label(container, text="Senha:", background=cor_fundo, foreground=cor_texto).grid(row=2, column=0, padx=10, pady=5, sticky="w")
    senha = ttk.Entry(container,background=cor_fundo, width=50)
    senha.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
    
    ttk.Label(container, text="Salario:", background=cor_fundo, foreground=cor_texto).grid(row=3, column=0, padx=10, pady=5, sticky="w")
    salario = ttk.Entry(container,background=cor_fundo, width=50)
    salario.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
    
    
    colunas = ("Nome", "E-mail", "Salário", "Editar")
    
    lista_funcionario = ttk.Treeview(container, columns=colunas, show="headings", height=6)

    lista_funcionario.heading("Nome", text="Nome", anchor="w")
    lista_funcionario.heading("E-mail", text="E-mail", anchor="w")
    lista_funcionario.heading("Salário", text="Salário", anchor="w")
    lista_funcionario.heading("Editar", text="Editar", anchor="w")

    lista_funcionario.bind("<Motion>", lambda event: lista_funcionario.config(cursor="hand2"))
    lista_funcionario.bind("<Leave>", lambda event: lista_funcionario.config(cursor=""))

    lista_funcionario.grid(row=4, column=0, columnspan=4, sticky="nsew")
    # container.grid_rowconfigure(4, weight=1)
    
    for item in funcionarios:
        
        lista_funcionario.insert("", "end", values=(item["Nome"], item["Email"], item["Salario"], "📝"))