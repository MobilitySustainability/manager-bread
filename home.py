import tkinter as tk
import ttkbootstrap as ttkb
from tkinter import ttk
from tkinter import messagebox
from cores import cor_fundo, cor_texto

def ajustar_tamanho_fonte(event, content, labels):
    largura_tela = event.width
    altura_tela = event.height
    
    nova_tamanho_fonte = int(largura_tela / 57)
    
    
    nova_tamanho_fonte = max(12, min(nova_tamanho_fonte, 36))
    
    for label in labels:
        label.config(font=("Helvetica", nova_tamanho_fonte, "bold"))

def home(content):
    
    content_label = ttk.Label(content, text="\n Bem-vindo ao Manager Bread – Seu Gerenciador de Padarias!", 
                              font=("Helvetica", 24, "bold"), 
                              background=cor_fundo, 
                              foreground=cor_texto, 
                              justify="center")
    content_label.grid(row=0, column=5, pady=10, padx=20)  
    
    descricao_label1 = ttk.Label(content, text="\n \n O Manager Bread é um sistema completo para gestão de padarias, \n ajudando no controle de estoque, pedidos, funcionários e muito mais.\n Facilitamos a administração do seu negócio para você focar no que realmente importa: \n Seus clientes!", 
                              font=("Helvetica", 16, "bold"), 
                              background=cor_fundo, 
                              foreground=cor_texto, 
                              justify="center")
    descricao_label1.grid(row=1, column=5, pady=10, padx=20)  
    
    descricao_label2 = ttk.Label(content, text="✅ Controle de estoque eficiente; \n ✅ Gerenciamento de pedidos simplificado; \n ✅ Administração de funcionários fácil e segura; \n ✅ Relatórios detalhados para melhor tomada de decisão; \n ✅ Interface amigável e intuitiva.", 
                              font=("Helvetica", 16, "bold"), 
                              background=cor_fundo, 
                              foreground=cor_texto, 
                              justify="center")
    descricao_label2.grid(row=2, column=5, pady=10, padx=20)  

    
    labels = [content_label, descricao_label1, descricao_label2]

   
    content.bind("<Configure>", lambda event, content=content, labels=labels: ajustar_tamanho_fonte(event, content, labels))
    
    content.grid_columnconfigure(5, weight=0)
    content.grid_rowconfigure(0, weight=0)
    content.grid_rowconfigure(1, weight=0)
    content.grid_rowconfigure(2, weight=0)
