import tkinter as tk
import ttkbootstrap as ttkb
from tkinter import ttk
from cores import cor_fundo, cor_texto

def carregamento(content):
    # Criação do estilo usando o ttkbootstrap
    style = ttkb.Style()
    
    # Label de "Carregando..."
    label_carregando = ttk.Label(content, text="Carregando...", background=cor_fundo, font=("Helvetica", 18), foreground=cor_texto)
    label_carregando.grid(row=5, column=5, padx=450, pady=100)  # Ajuste o pady para dar espaço

    # Barra de progresso
    progressbar = ttk.Progressbar(content, mode='indeterminate')
    progressbar.grid(row=6, column=5, padx=25, pady=25)  # Colocar em uma linha diferente
    progressbar.start()



