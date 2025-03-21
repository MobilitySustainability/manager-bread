import tkinter as tk
import ttkbootstrap as ttkb
import matplotlib.pyplot as plt
import numpy as np
import subprocess
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from caixa import AbrirCaixa
from cad_adm import AbrirCadAdm
from estoque import abrirEstoque
from funcionario import AbrirFuncionario
from home import home
from cores import cor_fundo, cor_texto, cor_borda, cor_botao, cor_hover_botao


def criar_menu_principal(tipo_usu, usu_ativo, nome_usu, tenant_id):

    # Criação da janela principal
    global root,content
    
    root = ttkb.Window(themename="flatly")
    root.title("Menager Bread")
    root.state("zoomed")
    
    # Função de logout (exemplo)
    def logout():
        messagebox.showinfo("Logout", "Você foi desconectado.")
        root.destroy()
        subprocess.run(["python", "login.py"])

    # Barra de navegação superior (navbar)
    navbar = ttk.Frame(root, padding=5)
    navbar.pack(side=tk.TOP, fill=tk.X, anchor="w")

    label_titulo = ttk.Label(navbar, text="MANAGER BREAD", background=cor_fundo, font=("Helvetica", 24), foreground=cor_texto)
    label_titulo.pack(side=tk.LEFT, padx=10, )

    # Menu suspenso para o usuário
    usuario_btn = tk.Menubutton(navbar, text=f"Bem Vindo(a), {nome_usu}", font=("Helvetica", 24), direction="below")
    usuario_btn.config(background=cor_fundo, foreground=cor_texto)
    usuario_menu = tk.Menu(usuario_btn, tearoff=0)
    usuario_menu.add_command(label="Sair", command=logout)
    usuario_btn.config(menu=usuario_menu)
    usuario_btn.pack(side=tk.RIGHT)

    # Sidebar (menu lateral)
    sidebar = ttk.Frame(root, width=200, relief="sunken", padding=20, style="TFrame")
    sidebar.pack(side=tk.LEFT, fill=tk.Y)

    # Alterar o fundo da sidebar para combinar com os botões
    sidebar.configure(style="TFrame")

    if(tipo_usu == "master" and usu_ativo == "Ativo"):

        # Criando o menu lateral
        menu_items = [
            ("Home 🏠", "fas fa-bell"),
            ("Caixa 💰", "fas fa-bell"),
            ("Pedidos 🛒", "fas fa-bell"),
            ("Estoque 📦", "fas fa-bell"),
            ("Funcionários 👨‍💼", "fas fa-bell"),
            ("Cadastro de Administrador 🏛️", "fas fa-bell"),
        ]

    elif(tipo_usu == "admin" and usu_ativo == "Ativo"):

        # Criando o menu lateral
        menu_items = [
            ("Home 🏠", "fas fa-bell"),
            ("Caixa 💰", "fas fa-bell"),
            ("Pedidos 🛒", "fas fa-bell"),
            ("Estoque 📦", "fas fa-bell"),
            ("Funcionários 👨‍💼", "fas fa-bell"),
            
        ]

    elif(tipo_usu == "usuario" and usu_ativo == "Ativo"):

        # Criando o menu lateral
        menu_items = [
            ("Home 🏠", "fas fa-bell"),
            ("Caixa 💰", "fas fa-bell"),
        ]
        

    for item, icon in menu_items:
        button = ttk.Button(sidebar, 
                            text=item, 
                            command=lambda 
                            item=item: menu_item_click(item), 
                            width=40, 
                            style="Custom.TButton")
        button.pack(pady=20)

    # Estilo para os botões do menu
    root.style.configure("TButton", background=cor_botao, relief="flat")
    root.style.configure("TFrame", background=cor_fundo)

    # Divisão do conteúdo principal
    content = ttk.Frame(root, padding=10, style="TFrame")
    content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Obtém as dimensões da tela
    tela_largura = content.winfo_screenwidth()

    home(content)
    
    # Alterar conforme escolha
    def menu_item_click(item):
        # Limpar o conteúdo atual (remover todos os widgets)
        for widget in content.winfo_children():
            widget.destroy()
            
        if item == "Home 🏠":
            
            home(content)
            
            if(item == "Home 🏠"):
                
                home(content)
                
            elif(item == "Caixa 💰"):

                AbrirCaixa(content, tipo_usu, nome_usu, tenant_id)

            elif(item == "Pedidos 🛒"):

                #pedidos(content)
                messagebox.showerror("Erro", "Em desenvolvimento")

            elif(item == "Cadastro de Administrador 🏛️"):

                AbrirCadAdm(content)

            elif(item == "Funcionários 👨‍💼"):
            
                AbrirFuncionario(content, tenant_id)
        
        elif item == "Estoque 📦":
            
            abrirEstoque(content, tenant_id)
            
            if(item == "Home 🏠"):
                
                home(content)
                
            elif(item == "Caixa 💰"):

                AbrirCaixa(content, tipo_usu, nome_usu, tenant_id)

            elif(item == "Pedidos 🛒"):

                #pedidos(content)
                messagebox.showerror("Erro", "Em desenvolvimento")

            elif(item == "Cadastro de Administrador 🏛️"):

                AbrirCadAdm(content)

            elif(item == "Funcionários 👨‍💼"):

                AbrirFuncionario(content, tenant_id)

        elif item == "Caixa 💰":
            
            AbrirCaixa(content, tipo_usu, nome_usu, tenant_id)
            
            if(item == "Home 🏠"):
                
                home(content)
                
            elif(item == "Estoque 📦"):

                abrirEstoque(content, tenant_id)

            elif(item == "Pedidos 🛒"):

                #pedidos(content)
                messagebox.showerror("Erro", "Em desenvolvimento")

            elif(item == "Cadastro de Administrador 🏛️"):

                AbrirCadAdm(content)

            elif(item == "Funcionários 👨‍💼"):

                AbrirFuncionario(content, tenant_id)

        elif item == "Pedidos 🛒":
            #pedidos(content)
            messagebox.showerror("Erro", "Em desenvolvimento")
            
            if(item == "Home 🏠"):
                
                home(content)
                
            elif(item == "Estoque 📦"):

                abrirEstoque(content, tenant_id)

            elif(item == "Caixa 💰"):

                AbrirCaixa(content, tipo_usu, nome_usu, tenant_id)

            elif(item == "Cadastro de Administrador 🏛️"):

                AbrirCadAdm(content)

            elif(item == "Funcionários 👨‍💼"):

                AbrirFuncionario(content, tenant_id)

        elif item == "Cadastro de Administrador 🏛️":
            
            AbrirCadAdm(content)
            
            if(item == "Home 🏠"):
                
                home(content)
                
            elif(item == "Estoque 📦"):

                abrirEstoque(content, tenant_id)

            elif(item == "Caixa 💰"):

                AbrirCaixa(content, tipo_usu, nome_usu, tenant_id)

            elif(item == "Pedidos 🛒"):

                #pedidos(content)
                messagebox.showerror("Erro", "Em desenvolvimento")

            elif(item == "Funcionários 👨‍💼"):

                AbrirFuncionario(content, tenant_id)

        elif item == "Funcionários 👨‍💼":
            
            AbrirFuncionario(content, tenant_id)
            
            if(item == "Home 🏠"):
                
                home(content)
                
            elif(item == "Estoque 📦"):

                abrirEstoque(content, tenant_id)

            elif(item == "Caixa 💰"):

                AbrirCaixa(content, tipo_usu, nome_usu, tenant_id)

            elif(item == "Pedidos 🛒"):

                #pedidos(content)
                messagebox.showerror("Erro", "Em desenvolvimento")

            elif(item == "Cadastro de Administrador 🏛️"):

                AbrirCadAdm(content)
            
            if(item == "Home 🏠"):
                
                home(content)
                
            elif(item == "Estoque 📦"):

                abrirEstoque(content, tenant_id)

            elif(item == "Caixa 💰"):

                AbrirCaixa(content, tipo_usu, nome_usu, tenant_id)

            elif(item == "Pedidos 🛒"):

                #pedidos(content)
                messagebox.showerror("Erro", "Em desenvolvimento")

            elif(item == "Cadastro de Administrador 🏛️"):

                AbrirCadAdm(content)

            elif(item == "Funcionários 👨‍💼"):

                AbrirFuncionario(content, tenant_id)
            
    # Iniciar a interface
    root.mainloop()
