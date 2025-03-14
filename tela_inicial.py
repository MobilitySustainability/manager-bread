import tkinter as tk
import ttkbootstrap as ttkb
import matplotlib.pyplot as plt
import numpy as np
import subprocess
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from caixa import iniciar_caixa_supermercado
from cad_adm import cad_adm
from estoque import estoque
from funcionario import funcionario
from gerenciar_usu import gerenciar_usu
from pedidos import pedidos


def criar_menu_principal(tipo_usu, usu_ativo, nome_usu, tenant_id):

    # Criação da janela principal
    global root
    root = ttkb.Window(themename="flatly")
    root.title("Menu - menager bread")

    # Configuração da largura e altura da janela
    root.geometry("800x600")
    # root.attributes("-fullscreen", True)
    
    
    # Função de logout (exemplo)
    def logout():
        messagebox.showinfo("Logout", "Você foi desconectado.")
        root.destroy()
        subprocess.run(["python", "login.py"])

    # Função para exibir o nome do usuário
    def exibir_usuario():
        messagebox.showinfo("Bem Vindo(a)", f"{nome_usu}")

    # Barra de navegação superior (navbar)
    navbar = ttk.Frame(root, padding=5)
    navbar.pack(side=tk.TOP, fill=tk.X, anchor="w")

    label_titulo = ttk.Label(navbar, text="MENU - MANAGER - BREAD", background="#2c3e50", font=("Helvetica", 16),foreground="white")
    label_titulo.pack(side=tk.LEFT, padx=10, )

    # Menu suspenso para o usuário
    usuario_btn = ttk.Menubutton(navbar, text=f"Bem Vindo(a), {nome_usu}", direction="below")
    usuario_menu = tk.Menu(usuario_btn, tearoff=0)
    usuario_menu.add_command(label="Sair", command=logout)
    usuario_btn.config(menu=usuario_menu)
    usuario_btn.pack(side=tk.RIGHT)

    # Sidebar (menu lateral)
    sidebar = ttk.Frame(root, width=200, relief="sunken", padding=5, style="TFrame")
    sidebar.pack(side=tk.LEFT, fill=tk.Y)

    # Alterar o fundo da sidebar para combinar com os botões
    sidebar.configure(style="TFrame")


    if(tipo_usu == "master" and usu_ativo == "Ativo"):

        # Criando o menu lateral
        menu_items = [
            ("Home", "fas fa-bell"),
            ("Estoque", "fas fa-bell"),
            ("Pedidos", "fas fa-bell"),
            ("Cad adm", "fas fa-bell"),
        ]

    elif(tipo_usu == "admin" and usu_ativo == "Ativo"):

        # Criando o menu lateral
        menu_items = [
            ("Home", "fas fa-bell"),
            ("Caixa", "fas fa-bell"),
            ("Estoque", "fas fa-bell"),
            ("Funcionario", "fas fa-bell"),
            ("Pedidos", "fas fa-bell"),
            ("Gereciar usu", "fas fa-bell"),
        ]

    elif(tipo_usu == "usuario" and usu_ativo == "Ativo"):

        # Criando o menu lateral
        menu_items = [
            ("Home", "fas fa-bell"),
            ("Caixa", "fas fa-bell"),
        ]


    for item, icon in menu_items:
        button = ttk.Button(sidebar, text=item, command=lambda item=item: menu_item_click(item), width=20, style="TButton")
        button.pack(pady=5)

    # Estilo para os botões do menu
    root.style.configure("TButton", background="#2c3e50", relief="flat")
    root.style.configure("TFrame", background="#2c3e50")

    # Divisão do conteúdo principal
    content = ttk.Frame(root, padding=10, style="TFrame")
    content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Estilo para o conteúdo
    root.style.configure("TFrame", background="#2c3e50")
    content_label = ttk.Label(content, text="Bem-vindo à área de MENU!", font=("Helvetica", 14), background="#2c3e50", style="TLabel", foreground="white")
    content_label.pack(pady=20)
    
    #alterar conforme escolha
    def menu_item_click(item):

        if(item == "Estoque"):

            estoque(content)

        elif(item == "Caixa"):

            iniciar_caixa_supermercado(content, tipo_usu, nome_usu, tenant_id)

        elif(item == "Pedidos"):

            pedidos(content)

        elif(item == "Cad adm"):

            cad_adm(content)

        elif(item == "Funcionario"):

            funcionario(content)

        elif(item == "Gereciar usu"):

            gerenciar_usu(content)
            

    # Iniciar a interface
    root.mainloop()

# Chama a função que cria a interface gráfica
# criar_menu_principal()
