import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from banco import verificar_login_bd
from tela_inicial import criar_menu_principal


def entrar():

    usuario = entry_usuario.get()
    senha   = entry_senha.get()
    flag_preencher = "N"

    if((usuario == "" and senha == "") or (usuario == "" or senha == "")):

        messagebox.showerror("Erro", "Preencher os campos")
        flag_preencher = "S"
        

    if(flag_preencher == "N"):    

        retorno_banco = verificar_login_bd(usuario, senha)

        if(retorno_banco != ""):
            
            tipo_usu  = retorno_banco[0]
            usu_ativo = retorno_banco[1]
            nome_usu  = retorno_banco[2]
            tenant_id = retorno_banco[3]

            if(usu_ativo == "Ativo"):

                login_window.destroy()
                criar_menu_principal(tipo_usu, usu_ativo, nome_usu, tenant_id)

            else:

                messagebox.showerror("Erro", "Usuário não esta ativo")

        else:

            messagebox.showerror("Erro", "Usuário ou senha inválidos")


def tela_login():

    global login_window, entry_usuario, entry_senha

    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("400x350")
    login_window.config(bg="#2c3e50")


    logo_img     = Image.open("logo.png")
    resized_logo = logo_img.resize((150, 100), Image.Resampling.LANCZOS)
    logo_img_tk  = ImageTk.PhotoImage(resized_logo)
    label_logo   = tk.Label(login_window, image=logo_img_tk, bg="#2c3e50")
    label_logo.image = logo_img_tk
    label_logo.pack(pady=20)
    
   
    label_usuario = tk.Label(login_window, text="Usuário", font=("Arial", 12), fg="white", bg="#2c3e50")
    label_usuario.pack()
    entry_usuario = tk.Entry(login_window, font=("Arial", 12), bd=2, relief="solid", justify="center")
    entry_usuario.pack(pady=7)
    
    
    label_senha = tk.Label(login_window, text="Senha", font=("Arial", 12), fg="white", bg="#2c3e50")
    label_senha.pack()
    entry_senha = tk.Entry(login_window, font=("Arial", 12), bd=2, relief="solid", justify="center", show="*")
    entry_senha.pack(pady=7)
    

    btn_entrar = tk.Button(login_window, text="Entrar", font=("Helvetica", 14), bg="#4CAF50", fg="white", command=entrar)
    btn_entrar.pack(pady=20, padx=20, fill="x")   

    
    login_window.mainloop()


tela_login()
