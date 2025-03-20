import tkinter as tk
import ttkbootstrap as ttkb
import unicodedata
import threading
from tkinter import ttk
from tkinter import messagebox
from cores import cor_fundo, cor_texto, cor_borda, cor_botao, cor_sair, cor_hover_botao, cor_hover_sair


def editar_funcionario(container, funcionarios):
    
    for widget in container.winfo_children():
        widget.destroy()
    
    def editar_campos():
        
        print('aqui')
        
        
    ttk.Label(container, text="Nome:", background=cor_fundo, foreground=cor_texto).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    nome = ttk.Entry(container,background=cor_fundo, width=50)
    nome.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
    
    ttk.Label(container, text="Email:", background=cor_fundo, foreground=cor_texto).grid(row=1, column=0, padx=10, pady=5, sticky="w")
    email = ttk.Entry(container,background=cor_fundo, width=50)
    email.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
    
    
    ttk.Label(container, text="Ativo_sn:", background=cor_fundo, foreground=cor_texto).grid(row=3, column=0, padx=10, pady=5, sticky="w")
    opcoes = ["Sim", "Não"]
    combo = ttk.Combobox(container, values=opcoes, state="readonly", width=20)
    combo.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
    
    ttk.Label(container, text="", background=cor_fundo, foreground=cor_texto).grid(row=4, column=0, padx=10, pady=5, sticky="w")
    btn_adicionar = ttk.Button(container, text="Editar", command=editar_campos)
    btn_adicionar.grid(row=5, column=1, sticky="ew")
    ttk.Label(container, text="", background=cor_fundo, foreground=cor_texto).grid(row=6, column=0, padx=10, pady=5, sticky="w")
    
    if(funcionarios != ""):
        
        nome_item    = funcionarios[0]
        nome.insert(0, nome_item)
        email_item   = funcionarios[1]
        email.insert(0, email_item)
    
        
        
    