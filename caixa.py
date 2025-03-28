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
            lista_carrinho.insert("", "end", values=(item["nome"], item["qtd"], item["preco"], "X"))
        total = sum(item["preco"] for item in carrinho)
        total_label.config(text=f"Total: R$ {total:.2f}")

    def adicionar_produto(event=None):
        codigo = entrada_codigo.get().strip()
        quantidade = quantidade_entrar.get().strip()

        try:
            codigo = int(codigo)
            if codigo:
                
                for produto in produtos:
                    produto_carrinho = produto
                    produto_codigo = produto["codigo"]
                    qtd_estoque = produto["qtd"]
                    
                    if produto_codigo == codigo:
                            
                        produto_nome = produto_carrinho['nome']
                        
                        valor_unitario = float(produto_carrinho['preco'])
                        quantidade_nova = int(quantidade)
                        
                        if(qtd_estoque == 0 or (qtd_estoque < quantidade_nova)):
                            messagebox.showerror("Erro", f"O produto selecionado, {produto_nome}, está com estoque de {qtd_estoque}.")
                            return

                        
                        produto_no_carrinho = None
                        for item in carrinho:
                            if item['codigo'] == codigo:
                                produto_no_carrinho = item
                                break

                        if produto_no_carrinho:
                            
                            produto_no_carrinho['qtd'] += quantidade_nova
                            produto_no_carrinho['preco'] = valor_unitario * produto_no_carrinho['qtd']
                        else:
                            
                            produto_carrinho['qtd'] = quantidade_nova
                            produto_carrinho['preco'] = valor_unitario * produto_carrinho['qtd']
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
                        produto_codigo = produto["codigo"]
                        qtd_estoque = produto["qtd"]
                        
                        if produto_codigo == codigo:
                            produto_nome = produto_carrinho['nome']
                            valor_unitario = float(produto_carrinho['preco'])
                            quantidade_nova = int(quantidade)
                            
                            if(qtd_estoque == 0 or (qtd_estoque < quantidade_nova)):
                                messagebox.showerror("Erro", f"O produto selecionado, {produto_nome}, está com estoque de {qtd_estoque}.")
                                return
                            
                            produto_no_carrinho = None
                            for item in carrinho:
                                if item['codigo'] == codigo:
                                    produto_no_carrinho = item
                                    break

                            if produto_no_carrinho:
                                
                                produto_no_carrinho['qtd'] += quantidade_nova
                                produto_no_carrinho['preco'] = produto_no_carrinho['qtd'] * valor_unitario
                            else:
                                
                                produto_carrinho['qtd'] = quantidade_nova
                                produto_carrinho['preco'] = produto_carrinho['qtd'] * valor_unitario
                                carrinho.append(produto_carrinho)

                            atualizar_carrinho()
                            # print(carrinho)
                            return
                    messagebox.showerror("Erro", "Produto não encontrado com este código.")
                else:
                    messagebox.showwarning("Entrada inválida", "Digite o código do produto.")
            except ValueError:
                messagebox.showwarning("Entrada inválida", "Digite o código ou nome do produto.")

    def processar_pagamento():
        total = sum(item["preco"] for item in carrinho)
        retorno = confirmar_pagamento(total, carrinho, nome_usu, tenant_id)
        if retorno == "Feito":
            lista_carrinho.delete(*lista_carrinho.get_children())
            entrada_codigo.delete(0, tk.END)
            quantidade_entrar.delete(0, tk.END)
            combo.set("")
            total = 0.00
            total_label.config(text=f"Total: R$ {total:.2f}")
            
            
    def entrada_codigo_in(event):
        
        if entrada_codigo.get() == "Código":
            entrada_codigo.delete(0, tk.END)

    def entrada_codigo_out(event):
        
        if entrada_codigo.get() == "":
            
            entrada_codigo.insert(0, "Código")
            
        else:
            
            codigo = int(entrada_codigo.get().strip())
            
            for produto in produtos:
                
                produto_carrinho = produto
                produto = produto["codigo"]
                produto = int(produto)
                codigo = int(codigo)
                if produto == codigo:
                    produto_carrinho = produto_carrinho["nome"]
                    combo.set(produto_carrinho)
                    break
                    
            
    def quantidade_entrar_in(event):
        
        if quantidade_entrar.get() == "Quantidade":
            quantidade_entrar.delete(0, tk.END)

    def quantidade_entrar_out(event):
        
        if quantidade_entrar.get() == "":
            quantidade_entrar.insert(0, "Quantidade")
            
            
    def combo_out(event):
        
        combo_novo = combo.get().strip()
        
        for produto in produtos:
            produto_carrinho = produto
            produto = produto["nome"]
            if produto == combo_novo:
                produto_carrinho = produto_carrinho["codigo"]
                entrada_codigo.delete(0, tk.END)
                entrada_codigo.insert(0, produto_carrinho)
                break
            

    entrada_codigo = ttk.Entry(container, width=10)
    entrada_codigo.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    entrada_codigo.insert(0, "Código")
    
    opcoes = [""]
    for produto in produtos:
        produto_carrinho = produto
        produto_carrinho = produto_carrinho["nome"]
        opcoes.append(produto_carrinho)
    
    combo = ttk.Combobox(container, values=opcoes, state="readonly", width=20)
    combo.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
    
    quantidade_entrar = ttk.Entry(container, width=5)
    quantidade_entrar.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
    quantidade_entrar.insert(0, "Quantidade")
    
    
    
    btn_adicionar = ttk.Button(container, text="Adicionar", command=adicionar_produto)
    btn_adicionar.grid(row=0, column=3, sticky="ew")
    
    style = ttk.Style()
    style.configure("Treeview", foreground=cor_texto, fieldbackground=cor_fundo)
    style.configure("Treeview.Heading", foreground=cor_texto)

    lista_carrinho = ttk.Treeview(container, columns=("Produto", "Qtd" , "Preço", "Remover"), show="headings", style="Treeview", height=6)
    lista_carrinho.heading("Produto", text="Produto", anchor="w")
    lista_carrinho.heading("Qtd", text="Qtd", anchor="w")
    lista_carrinho.heading("Preço", text="Preço", anchor="w")
    lista_carrinho.heading("Remover", text="Remover", anchor="w")
    lista_carrinho.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

    total_label = ttk.Label(container, text="Total: R$ 0.00", background=cor_fundo, foreground=cor_texto, font=("Arial", 14))
    total_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    btn_grafico = ttk.Button(container, text="Confirmar", command=processar_pagamento)
    btn_grafico.grid(row=3, column=1, columnspan=2, sticky="ew")

    lista_carrinho.bind("<ButtonRelease-1>", lambda event: remove_item(event, lista_carrinho))
    entrada_codigo.bind("<Return>", adicionar_produto)
    
    entrada_codigo.bind("<FocusIn>", entrada_codigo_in)
    entrada_codigo.bind("<FocusOut>", entrada_codigo_out)
    
    quantidade_entrar.bind("<FocusIn>", quantidade_entrar_in)
    quantidade_entrar.bind("<FocusOut>", quantidade_entrar_out)
    
    
    combo.bind("<FocusOut>", combo_out)
    

    container.grid_columnconfigure(0, weight=1)
    container.grid_columnconfigure(1, weight=1)
    container.grid_columnconfigure(2, weight=1)
    container.grid_columnconfigure(3, weight=1)
    
    container.grid_rowconfigure(0, weight=0)
    container.grid_rowconfigure(1, weight=0)
    container.grid_rowconfigure(2, weight=1)
    container.grid_rowconfigure(3, weight=0)
    container.grid_rowconfigure(4, weight=0)
    container.grid_rowconfigure(5, weight=1)
    
def remover_acentos(texto):
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
