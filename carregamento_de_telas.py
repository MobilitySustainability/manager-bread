import tkinter as tk
import ttkbootstrap as ttkb
from tkinter import ttk
from cores import cor_fundo, cor_texto

def carregamento(content):
    # Criação do estilo usando o ttkbootstrap
    style = ttkb.Style()
    
    # Label de "Carregando..."
    label_carregando = ttk.Label(content, text="Carregando...", background=cor_fundo, font=("Helvetica", 18), foreground=cor_texto)
    label_carregando.grid(row=0, column=0)

    # Barra de progresso
    progressbar = ttk.Progressbar(content, mode='indeterminate')
    progressbar.grid(row=1, column=0)
    progressbar.start()



