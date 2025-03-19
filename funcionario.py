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
    
    
    style = ttk.Style()
    
    style.configure("Custom.Treeview",
                    background=cor_fundo,
                    foreground=cor_texto,
                    fieldbackground=cor_fundo)

    
    lista_funcionario = ttk.Treeview(container, columns=("Nome", "E-mail", "Salário"), style="Custom.Treeview")

    lista_funcionario.heading("Nome", text="Nome", anchor="w")
    lista_funcionario.heading("E-mail", text="E-mail", anchor="w")
    lista_funcionario.heading("Salário", text="Salário", anchor="w")

    
    lista_funcionario.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
    container.grid_rowconfigure(2, weight=1)
    
    for item in funcionarios:
        
        lista_funcionario.insert("", "end", values=(item["Nome"], item["Email"], item["Salario"]))