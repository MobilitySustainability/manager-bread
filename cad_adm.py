import tkinter as tk
import ttkbootstrap as ttkb
import threading
from tkinter import ttk, messagebox
from banco import cadAdm, deleteCadAdm, listarUsuarios, cadPadaria, obter_dono_id, deletePadaria
from carregamento_de_telas import carregamento
from cores import cor_fundo, cor_texto

def AbrirCadAdm(container):
    def carregar():
        carregamento(container)
        container.after(0, cad_adm, container)
    thread = threading.Thread(target=carregar)
    thread.start()

def cad_adm(container):
    for widget in container.winfo_children():
        widget.destroy()

    # Título acima do formulário
    ttk.Label(container, text="Cadastrar Administrador", font=("Arial", 12, "bold"), background=cor_fundo, foreground=cor_texto).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="w")

    def adicionar_usuario():
        nome = entry_nome.get().strip()
        email = entry_email.get().strip()
        senha = entry_senha.get().strip()
        nome_padaria = entry_nome_padaria.get().strip()

        if nome and email and senha and nome_padaria:
            # Cadastrar o Administrador
            sucesso = cadAdm(nome, email, senha, 2)  # Supondo que o 2 seja para administradores
            if sucesso:
                # Sucesso ao cadastrar o administrador, agora vamos buscar o dono_id
                # Buscar o dono_id do novo administrador (o último registrado)
                dono_id = obter_dono_id(email)  # Função que retorna o dono_id a partir do e-mail

                if dono_id:
                    # Agora vamos cadastrar a padaria
                    sucesso_padaria = cadPadaria(nome_padaria, dono_id)
                    if sucesso_padaria:
                        lista_cad_adm.insert("", "end", values=(nome, email, "******", nome_padaria, "X"))
                        messagebox.showinfo("Sucesso", "Usuário e padaria cadastrados com sucesso!")
                    else:
                        messagebox.showerror("Erro", "Falha ao cadastrar a padaria no banco.")
                else:
                    messagebox.showerror("Erro", "Falha ao obter o dono_id para a padaria.")
                    
                # Limpar os campos após sucesso
                entry_nome.delete(0, tk.END)
                entry_email.delete(0, tk.END)
                entry_senha.delete(0, tk.END)
                entry_nome_padaria.delete(0, tk.END)
            else:
                messagebox.showerror("Erro", "Falha ao cadastrar usuário no banco.")
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")


    # Formulário de Cadastro
    ttk.Label(container, text="Nome:", background=cor_fundo, foreground=cor_texto).grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_nome = ttk.Entry(container, width=50)
    entry_nome.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    ttk.Label(container, text="E-mail:", background=cor_fundo, foreground=cor_texto).grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_email = ttk.Entry(container, width=50)
    entry_email.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    ttk.Label(container, text="Senha:", background=cor_fundo, foreground=cor_texto).grid(row=3, column=0, padx=10, pady=5, sticky="w")
    entry_senha = ttk.Entry(container, width=50, show="*")
    entry_senha.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

    ttk.Label(container, text="Nome Padaria:", background=cor_fundo, foreground=cor_texto).grid(row=4, column=0, padx=10, pady=5, sticky="w")
    entry_nome_padaria = ttk.Entry(container, width=50)
    entry_nome_padaria.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

    btn_adicionar = ttk.Button(container, text="Adicionar Usuário", command=adicionar_usuario)
    btn_adicionar.grid(row=5, column=1, padx=10, pady=10, sticky="ew")

    # Título abaixo do botão "Cadastro de Padaria"
    ttk.Label(container, text="Administradores cadastrados", font=("Arial", 12, "bold"), background=cor_fundo, foreground=cor_texto).grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="w")

    # Lista de usuários cadastrados
    colunas = ("Nome", "E-mail", "Senha", "Nome Padaria", "Remover")
    lista_cad_adm = ttk.Treeview(container, columns=colunas, show="headings", height=6)

    for coluna in colunas:
        lista_cad_adm.heading(coluna, text=coluna, anchor="center")
        lista_cad_adm.column(coluna, anchor="center")
    lista_cad_adm.grid(row=7, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

    # Preenchendo a lista com os usuários cadastrados
    usuarios = listarUsuarios()
    for usuario in usuarios:
        lista_cad_adm.insert("", "end", values=(usuario["nome"], usuario["email"], "******", usuario.get("nome_padaria", ""), "X"))

    # Função para remover usuário
    def remover_usuario(event):
        item_id = lista_cad_adm.identify_row(event.y)
        coluna = lista_cad_adm.identify_column(event.x)
        if not item_id or coluna != "#5":
            return  # Se não for clicado na coluna "Remover", retorna

        valores = lista_cad_adm.item(item_id, "values")
        nome_usuario = valores[0]
        email = valores[1]
        nome_padaria = valores[3]

        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja remover o administrador {nome_usuario} e a padaria {nome_padaria}?"):
            if nome_padaria != 'NAO TEM PADARIA':  # Verificar se o administrador tem padaria
                # Se o administrador tem uma padaria vinculada, excluir a padaria primeiro
                sucesso_padaria = deletePadaria(nome_padaria, email)  # Excluir a padaria associada
                if sucesso_padaria:
                    # Se a padaria foi excluída com sucesso, excluir o administrador
                    sucesso_usuario = deleteCadAdm(email)
                    if sucesso_usuario == "Cadastro deletado com sucesso":
                        lista_cad_adm.delete(item_id)
                        messagebox.showinfo("Sucesso", f"Administrador {nome_usuario} e a padaria {nome_padaria} removidos com sucesso!")
                    else:
                        messagebox.showerror("Erro", "Falha ao remover o administrador do banco de dados.")
                else:
                    messagebox.showerror("Erro", "Falha ao excluir a padaria. O administrador não será removido.")
            else:
                # Se o administrador não tem padaria, excluir apenas o administrador
                sucesso_usuario = deleteCadAdm(email)
                if sucesso_usuario == "Cadastro deletado com sucesso":
                    lista_cad_adm.delete(item_id)
                    messagebox.showinfo("Sucesso", f"Administrador {nome_usuario} removido com sucesso!")
                else:
                    messagebox.showerror("Erro", "Falha ao remover o administrador do banco de dados.")


    lista_cad_adm.bind("<ButtonRelease-1>", remover_usuario)
    
    
    
    container.grid_columnconfigure(0, weight=0)
    container.grid_columnconfigure(1, weight=0)
    
    container.grid_rowconfigure(0, weight=0)
    container.grid_rowconfigure(1, weight=0)
    container.grid_rowconfigure(2, weight=0)
    container.grid_rowconfigure(3, weight=0)
    container.grid_rowconfigure(4, weight=0)
    container.grid_rowconfigure(5, weight=0)
    container.grid_rowconfigure(6, weight=0)
    container.grid_rowconfigure(7, weight=0)