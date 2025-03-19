import tkinter as tk
import ttkbootstrap as ttkb
from tkinter import ttk
from tkinter import messagebox
from cores import cor_fundo, cor_texto

def home(content):
    # Obtém as dimensões da tela
    tela_largura = content.winfo_screenwidth()

    # Ajusta o tamanho da fonte com base na largura da tela
    if tela_largura > 1600:
        font_tamanho = 24  # Grande
    elif tela_largura > 1200:
        font_tamanho = 24  # Médio
    else:
        font_tamanho = 24  # Pequeno

    # Estilo para o conteúdo
    content_label = ttk.Label(content, text="\n" \
                            "Bem-vindo ao Manager Bread – Seu Gerenciador de Padarias!", 
                            font=("Helvetica", font_tamanho, "bold"), 
                            background=cor_fundo, 
                            foreground=cor_texto, 
                            wraplength=tela_largura - 100,  # Ajusta o wraplength com base na largura da tela
                            justify="center")
    content_label.grid(row=0, column=0, pady=10)

    descricao_label = ttk.Label(content, 
                                text=
                                    "\n" \
                                    "O Manager Bread é um sistema completo para gestão de padarias, " 
                                    "ajudando no controle de estoque, pedidos, funcionários e muito mais. "
                                    "Facilitamos a administração do seu negócio para você focar no que realmente importa: "
                                    "Seus clientes!",
                                font=("Helvetica", font_tamanho), 
                                background=cor_fundo, 
                                foreground="black", 
                                wraplength=tela_largura - 100,  # Ajusta o wraplength com base na largura da tela
                                justify="center")
    descricao_label.grid(row=1, column=0, pady=10)

    # Vantagens do sistema
    vantagens_texto = "\n" \
                    "✅ Controle de estoque eficiente;\n" \
                    "\n" \
                    "✅ Gerenciamento de pedidos simplificado;\n" \
                    "\n" \
                    "✅ Administração de funcionários fácil e segura;\n" \
                    "\n" \
                    "✅ Relatórios detalhados para melhor tomada de decisão;\n" \
                    "\n" \
                    "✅ Interface amigável e intuitiva."

    vantagens_label = ttk.Label(content, text=vantagens_texto, 
                                font=("Helvetica", font_tamanho - 6),  # Menor que o título
                                background=cor_fundo, 
                                foreground="black", 
                                justify="left", 
                                wraplength=tela_largura - 100)  # Ajusta o wraplength com base na largura da tela
    vantagens_label.grid(row=2, column=0, pady=10)
