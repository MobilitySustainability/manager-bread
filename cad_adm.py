import tkinter as tk
import ttkbootstrap as ttkb
from tkinter import ttk, messagebox
from banco import cadAdm, permissaoUsu, deleteCadAdm
from cores import cor_fundo, cor_texto

def cad_adm(container):
    for widget in container.winfo_children():
        widget.destroy()

    # Buscar permissões do banco de dados
    permissoes = permissaoUsu()  
    opcoes_permissao = [p["tipo"] for p in permissoes] if isinstance(permissoes, list) else ["Nenhuma Permissão"]

    def adicionar_usuario():
        nome = entry_nome.get().strip()
        email = entry_email.get().strip()
        senha = entry_senha.get().strip()
        permissao = combobox_permissao.get()

        if nome and email and senha and permissao:
            permissao_id = {"master": 1, "admin": 2, "usuario": 3}.get(permissao, None)
            if permissao_id is None:
                messagebox.showerror("Erro", "Permissão inválida.")
                return

            sucesso = cadAdm(nome, email, senha, permissao_id)

            if sucesso:
                lista_cad_adm.insert("", "end", values=(nome, email, "******", permissao, "X"))
                
                messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
                entry_nome.delete(0, tk.END)
                entry_email.delete(0, tk.END)
                entry_senha.delete(0, tk.END)
                combobox_permissao.current(0)
            else:
                messagebox.showerror("Erro", "Falha ao cadastrar usuário no banco.")
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")

    # Criando Labels e Entradas
    ttk.Label(container, text="Nome:", background=cor_fundo, foreground=cor_texto).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_nome = ttk.Entry(container,background=cor_fundo, width=50)
    entry_nome.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    ttk.Label(container, text="E-mail:", background=cor_fundo, foreground=cor_texto).grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_email = ttk.Entry(container, width=50)
    entry_email.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    ttk.Label(container, text="Senha:", background=cor_fundo, foreground=cor_texto).grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_senha = ttk.Entry(container, width=50, show="*")  # Esconder senha
    entry_senha.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    # Combobox para Permissão
    ttk.Label(container, text="Permissão:", background=cor_fundo, foreground=cor_texto).grid(row=3, column=0, padx=10, pady=5, sticky="w")
    combobox_permissao = ttk.Combobox(container, values=opcoes_permissao, state="readonly", width=47)
    combobox_permissao.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
    combobox_permissao.current(0)

    # Botão para adicionar usuário
    btn_adicionar = ttk.Button(container, text="Adicionar Usuário", command=adicionar_usuario)
    btn_adicionar.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

    # Configuração do Treeview (Tabela)
    colunas = ("Nome", "E-mail", "Senha", "Permissão", "Remover")
    lista_cad_adm = ttk.Treeview(container, columns=colunas, show="headings", height=6)
    
    # Configurando as colunas
    lista_cad_adm.heading("Nome", text="Nome", anchor="w")
    lista_cad_adm.heading("E-mail", text="E-mail", anchor="w")
    lista_cad_adm.heading("Senha", text="Senha", anchor="w")
    lista_cad_adm.heading("Permissão", text="Permissão", anchor="w")
    lista_cad_adm.heading("Remover", text="Remover", anchor="center")

    lista_cad_adm.column("Nome", width=150, anchor="w")
    lista_cad_adm.column("E-mail", width=200, anchor="w")
    lista_cad_adm.column("Senha", width=100, anchor="center")
    lista_cad_adm.column("Permissão", width=100, anchor="center")
    lista_cad_adm.column("Remover", width=80, anchor="center")

    lista_cad_adm.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

    container.grid_rowconfigure(5, weight=1)

    for i in range(4):
        container.grid_columnconfigure(i, weight=1, uniform="equal")

    def remover_usuario(event):
        item_id = lista_cad_adm.identify_row(event.y)
        coluna = lista_cad_adm.identify_column(event.x)

        if not item_id or coluna != "#5":  
            return  

        valores = lista_cad_adm.item(item_id, "values")
        email = valores[1]  

        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja remover {valores[0]}?"):
            sucesso = deleteCadAdm(email)

            if sucesso == "Cadastro deletado com sucesso":
                lista_cad_adm.delete(item_id)  
                messagebox.showinfo("Sucesso", "Usuário removido com sucesso!")
            else:
                messagebox.showerror("Erro", "Falha ao remover usuário do banco de dados.")

    lista_cad_adm.bind("<ButtonRelease-1>", remover_usuario)