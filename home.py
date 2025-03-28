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
    # Criando os labels
    content_label = ttk.Label(content, text="\n Bem-vindo ao Manager Bread – Seu Gerenciador de Padarias! \n \n O Manager Bread é um sistema completo para gestão de padarias, \n ajudando no controle de estoque, pedidos, funcionários e muito mais.\n Facilitamos a administração do seu negócio para você focar no que realmente importa: \n Seus clientes! \n \n ✅ Controle de estoque eficiente; \n ✅ Gerenciamento de pedidos simplificado; \n ✅ Administração de funcionários fácil e segura; \n ✅ Informações precisas para melhorar a tomada de decisão; \n ✅ Interface amigável e intuitiva.", 
                              font=("Helvetica", 25, "bold"), 
                              background=cor_fundo, 
                              foreground=cor_texto,
                              justify="center")
    
    descricao_label1 = ttk.Label(content, text="", 
                              font=("Helvetica", 18, "bold"), 
                              background=cor_fundo, 
                              foreground=cor_texto,
                              justify="center")
    
    descricao_label2 = ttk.Label(content, text="", 
                              font=("Helvetica", 18, "bold"), 
                              background=cor_fundo, 
                              foreground=cor_texto,
                              justify="center")
    
    # Centralizando os labels no grid
    content_label.grid(row=0, column=50, pady=100, padx=120, sticky="nsew")
    descricao_label1.grid(row=1, column=50, pady=100, padx=120, sticky="nsew")
    descricao_label2.grid(row=2, column=50, pady=100, padx=120, sticky="nsew")

def criar_tela_principal():
    root = tk.Tk()
    
    # Definindo tamanho fixo da tela e impedindo o redimensionamento
    root.geometry("800x600")  # Tamanho fixo da tela (800x600 pixels)
    root.resizable(False, False)  # Impede o redimensionamento
    
    content = ttk.Frame(root)
    content.pack(fill="both", expand=True)

    # Definindo o evento para ajuste de tamanho de fonte ao redimensionar (se permitido)
    labels = []
    content.bind("<Configure>", lambda event: ajustar_tamanho_fonte(event, content, labels))
    
    # Chamando a função de criação da tela principal
    home(content)

    root.mainloop()


