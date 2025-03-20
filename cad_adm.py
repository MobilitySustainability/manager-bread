import tkinter as tk
import ttkbootstrap as ttkb
import threading
from tkinter import ttk, messagebox
from banco import cadAdm, deleteCadAdm, cadPadaria, buscar_donos, atualizar_padaria
from carregamento_de_telas import carregamento
from cores import cor_fundo, cor_texto

def AbrirCadAdm(container):
    
    def carregar():
        
        carregamento(container)
        
        donos = buscar_donos() 
        
        container.after(0, cad_adm, container, donos)
        
    thread = threading.Thread(target=carregar)
    thread.start()

def cad_adm(container, donos):
    
    for widget in container.winfo_children():
        widget.destroy()

    opcoes_donos = [dono["nome"] for dono in donos] if isinstance(donos, list) else []

    def adicionar_usuario():
        nome = entry_nome.get().strip()
        email = entry_email.get().strip()
        senha = entry_senha.get().strip()

        if nome and email and senha :
           
            sucesso = cadAdm(nome, email, senha, 2)

            if sucesso:
                lista_cad_adm.insert("", "end", values=(nome, email, "******", "X"))
                
                messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
                entry_nome.delete(0, tk.END)
                entry_email.delete(0, tk.END)
                entry_senha.delete(0, tk.END)
            else:
                messagebox.showerror("Erro", "Falha ao cadastrar usuário no banco.")
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")

    def abrir_cadastro_padaria():
        
        def cadastrar_padaria():
            
            nome_padaria = entry_nome_padaria.get().strip()
            dono_padaria = combobox_dono.get()

            if nome_padaria and dono_padaria:
                dono_id = next((d["id"] for d in donos if d["nome"] == dono_padaria), None)
                if dono_id is None:
                    messagebox.showerror("Erro", "Dono não encontrado.")
                    return

                
                sucesso_update = atualizar_padaria(nome_padaria, dono_id)
                if sucesso_update:
                    messagebox.showinfo("Sucesso", "Padaria atualizada com sucesso!")
                else:
                    sucesso = cadPadaria(nome_padaria, dono_id)

                    if sucesso:
                        messagebox.showinfo("Sucesso", "Padaria cadastrada com sucesso!")
                    else:
                        messagebox.showerror("Erro", "Falha ao cadastrar padaria no banco.")
                
                # Limpar os campos
                entry_nome_padaria.delete(0, tk.END)
                combobox_dono.current(0)

            else:
                messagebox.showwarning("Aviso", "Preencha todos os campos!")

        # Janela de cadastro de padaria
        janela_padaria = tk.Toplevel()
        janela_padaria.title("Cadastro de Padaria")
        janela_padaria.geometry("500x300")

        ttk.Label(janela_padaria, text="Nome da Padaria:", background=cor_fundo, foreground=cor_texto).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        entry_nome_padaria = ttk.Entry(janela_padaria, background=cor_fundo, width=50)
        entry_nome_padaria.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(janela_padaria, text="Dono da Padaria:", background=cor_fundo, foreground=cor_texto).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        combobox_dono = ttk.Combobox(janela_padaria, values=opcoes_donos, state="readonly", width=47)
        combobox_dono.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        combobox_dono.current(0)

        # Botão para adicionar padaria
        btn_adicionar_padaria = ttk.Button(janela_padaria, text="Cadastrar Padaria", command=cadastrar_padaria)
        btn_adicionar_padaria.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

    # Criando Labels e Entradas para Cadastro de Usuário
    ttk.Label(container, text="Nome:", background=cor_fundo, foreground=cor_texto).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_nome = ttk.Entry(container, background=cor_fundo, width=50)
    entry_nome.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    ttk.Label(container, text="E-mail:", background=cor_fundo, foreground=cor_texto).grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_email = ttk.Entry(container, width=50)
    entry_email.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    ttk.Label(container, text="Senha:", background=cor_fundo, foreground=cor_texto).grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_senha = ttk.Entry(container, width=50, show="*")  # Esconder senha
    entry_senha.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

  

    # Botão para adicionar usuário
    btn_adicionar = ttk.Button(container, text="Adicionar Usuário", command=adicionar_usuario)
    btn_adicionar.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

    # Botão para abrir o cadastro de padaria
    btn_cadastro_padaria = ttk.Button(container, text="Cadastro de Padaria", command=abrir_cadastro_padaria)
    btn_cadastro_padaria.grid(row=5, column=1, padx=10, pady=10, sticky="ew")

    # Configuração do Treeview (Tabela de Usuários)
    colunas = ("Nome", "E-mail", "Senha", "Remover")
    lista_cad_adm = ttk.Treeview(container, columns=colunas, show="headings", height=6)
    
    # Configurando as colunas
    lista_cad_adm.heading("Nome", text="Nome", anchor="center")
    lista_cad_adm.heading("E-mail", text="E-mail", anchor="center")
    lista_cad_adm.heading("Senha", text="Senha", anchor="center")
    lista_cad_adm.heading("Remover", text="Remover", anchor="center")

    lista_cad_adm.column("Nome", width=150, anchor="center")
    lista_cad_adm.column("E-mail", width=200, anchor="center")
    lista_cad_adm.column("Senha", width=80, anchor="center")  # Reduzindo um pouco a largura da senha
    lista_cad_adm.column("Remover", width=50, anchor="center") 

    lista_cad_adm.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

    # container.grid_rowconfigure(6, weight=1)

    for i in range(4):
        container.grid_columnconfigure(i, weight=1, uniform="equal")

    def remover_usuario(event):
        item_id = lista_cad_adm.identify_row(event.y)
        coluna = lista_cad_adm.identify_column(event.x)

        if not item_id or coluna != "#4":  
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
