import tkinter as tk
import ttkbootstrap as ttkb
from tkinter import ttk
from tkinter import messagebox
from cores import cor_fundo, cor_texto


def home(content):
    
    # Estilo para o conteúdo
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