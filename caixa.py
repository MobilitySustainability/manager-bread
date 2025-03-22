import tkinter as tk
import ttkbootstrap as ttkb
import unicodedata
from tkinter import ttk
from tkinter import messagebox
from banco import pegar_produtos
from banco import confirmar_pagamento
from carregamento_de_telas import carregamento
from cores import cor_fundo, cor_texto, cor_borda, cor_botao, cor_hover_botao
import threading

def AbrirCaixa(container, tipo_usu, nome_usu, tenant_id):
    
    def carregar():
        
        carregamento(container)
        
        produtos = pegar_produtos(tenant_id)
        
        container.after(0, iniciar_caixa_supermercado, container, tipo_usu, nome_usu, tenant_id, produtos)
        
    thread = threading.Thread(target=carregar)
    thread.start()


def iniciar_caixa_supermercado(container, tipo_usu, nome_usu, tenant_id, produtos):

    for widget in container.winfo_children():
        widget.destroy()
    
    carrinho = []

    def remove_item(event, treeview):
        item = treeview.selection()
        if item:
            item_values = treeview.item(item)["values"]
            produto_nome = item_values[0]

            for contador in range(len(carrinho)):
                valor = carrinho[contador]
                if valor["nome"] == produto_nome:
                    del carrinho[contador]
                    break

            treeview.delete(item)
            total = sum(item["preco"] for item in carrinho)
            total_label.config(text=f"Total: R$ {total:.2f}")

    def atualizar_carrinho():
        lista_carrinho.delete(*lista_carrinho.get_children())
        for item in carrinho:
            lista_carrinho.insert("", "end", values=(item["nome"], item["preco"], "X"))
        total = sum(item["preco"] for item in carrinho)
        total_label.config(text=f"Total: R$ {total:.2f}")

    def adicionar_produto(event=None):
        codigo = entrada_codigo.get().strip()
        try:
            codigo = int(codigo)
            if codigo:
                for produto in produtos:
                    produto_carrinho = produto
                    produto = produto["codigo"]
                    produto = int(produto)
                    codigo = int(codigo)
                    if produto == codigo:
                        carrinho.append(produto_carrinho)
                        atualizar_carrinho()
                        return
                messagebox.showerror("Erro", "Produto não encontrado com este código.")
            else:
                messagebox.showwarning("Entrada inválida", "Digite o código do produto.")
        except ValueError:
            try:
                codigo = float(codigo)
                if codigo:
                    for produto in produtos:
                        produto_carrinho = produto
                        produto = produto["codigo"]
                        produto = int(produto)
                        codigo = int(codigo)
                        if produto == codigo:
                            carrinho.append(produto_carrinho)
                            atualizar_carrinho()
                            return
                    messagebox.showerror("Erro", "Produto não encontrado com este código.")
                else:
                    messagebox.showwarning("Entrada inválida", "Digite o código do produto.")
            except ValueError:
                if codigo:
                    for produto in produtos:
                        produto_carrinho = produto
                        produto = produto["nome"]
                        produto = remover_acentos(produto).lower()
                        codigo = remover_acentos(codigo).lower()

                        if codigo in produto:
                            carrinho.append(produto_carrinho)
                            atualizar_carrinho()
                            return
                    messagebox.showerror("Erro", "Produto não encontrado com este nome.")
                else:
                    messagebox.showwarning("Entrada inválida", "Digite o código ou nome do produto.")

    def processar_pagamento():
        total = sum(item["preco"] for item in carrinho)
        retorno = confirmar_pagamento(total, carrinho, nome_usu, tenant_id)
        if retorno == "Feito":
            lista_carrinho.delete(*lista_carrinho.get_children())
            entrada_codigo.delete(0, tk.END)
            total = 0.00
            total_label.config(text=f"Total: R$ {total:.2f}")

    entrada_codigo = ttk.Entry(container, width=50)
    entrada_codigo.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    
    btn_adicionar = ttk.Button(container, text="Adicionar", command=adicionar_produto)
    btn_adicionar.grid(row=0, column=1, sticky="ew")
    
    style = ttk.Style()
    style.configure("Treeview", foreground=cor_texto, fieldbackground=cor_fundo)
    style.configure("Treeview.Heading", foreground=cor_texto)

    lista_carrinho = ttk.Treeview(container, columns=("Produto", "Preço", "Remover"), show="headings", style="Treeview", height=6)
    lista_carrinho.heading("Produto", text="Produto", anchor="w")
    lista_carrinho.heading("Preço", text="Preço", anchor="w")
    lista_carrinho.heading("Remover", text="Remover", anchor="w")
    lista_carrinho.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

    total_label = ttk.Label(container, text="Total: R$ 0.00", background=cor_fundo, foreground=cor_texto, font=("Arial", 14))
    total_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    btn_grafico = ttk.Button(container, text="Confirmar", command=processar_pagamento)
    btn_grafico.grid(row=3, column=1, columnspan=2, sticky="ew")

    lista_carrinho.bind("<ButtonRelease-1>", lambda event: remove_item(event, lista_carrinho))
    entrada_codigo.bind("<Return>", adicionar_produto)

    container.grid_columnconfigure(0, weight=1, uniform="equal")
    container.grid_columnconfigure(1, weight=1, uniform="equal")
    container.grid_columnconfigure(2, weight=1, uniform="equal")
    container.grid_columnconfigure(3, weight=1, uniform="equal")
    
    container.grid_rowconfigure(0, weight=0)
    container.grid_rowconfigure(1, weight=0)
    container.grid_rowconfigure(2, weight=1)
    container.grid_rowconfigure(3, weight=0)
    container.grid_rowconfigure(4, weight=0)
    container.grid_rowconfigure(5, weight=1)
    
def remover_acentos(texto):
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
