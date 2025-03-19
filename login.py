import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from banco import verificar_login_bd
from tela_inicial import criar_menu_principal
from cores import cor_fundo, cor_texto, cor_borda, cor_botao, cor_sair, cor_hover_botao, cor_hover_sair

def entrar():
    usuario = entry_usuario.get()
    senha = entry_senha.get()
    
    if not usuario or not senha:
        messagebox.showerror("Erro", "Preencher os campos")
        return
    
    carregando_label = tk.Label(frame, text="Carregando...", font=("Arial", 12), fg=cor_texto, bg=cor_fundo)
    carregando_label.pack(pady=6)
    login_window.update()
    
    retorno_banco = verificar_login_bd(usuario, senha)

    carregando_label.pack_forget()
    
    if retorno_banco:
        
        tipo_usu, usu_ativo, nome_usu, tenant_id = retorno_banco
        
        if usu_ativo == "Ativo":
            login_window.destroy()
            criar_menu_principal(tipo_usu, usu_ativo, nome_usu, tenant_id)
        else:
            
            messagebox.showerror("Erro", "Usuário não está ativo")
    else:
        
        messagebox.showerror("Erro", "Usuário ou senha inválidos")
        

def tela_login():
    global login_window, entry_usuario, entry_senha, frame
    
    login_window = tk.Tk()
    login_window.title("Login")
    screen_width = login_window.winfo_screenwidth()
    screen_height = login_window.winfo_screenheight()
    
    login_window.geometry(f"{screen_width}x{screen_height}")
    
    # Carregar imagem de fundo
    bg_img = Image.open("fundo_login.png")
    bg_width, bg_height = bg_img.size
    screen_width = login_window.winfo_screenwidth()
    screen_height = login_window.winfo_screenheight()
    
    # Criar canvas para o fundo
    bg_canvas = tk.Canvas(login_window, width=screen_width, height=screen_height)
    bg_canvas.pack(fill="both", expand=True)

    # Lista para armazenar referências das imagens
    bg_images = []
    
    for x in range(0, screen_width, bg_width):
        for y in range(0, screen_height, bg_height):
            img_part = ImageTk.PhotoImage(bg_img)
            bg_canvas.create_image(x, y, anchor="nw", image=img_part)
            bg_images.append(img_part)
    
    # Criar um frame sobre o Canvas
    frame = tk.Frame(login_window, bg=cor_fundo, bd=5, highlightbackground=cor_borda, highlightthickness=3)
    frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=550)

    # logo
    logo_img = Image.open("logo.png")
    logo_img = logo_img.resize((300, 200), Image.Resampling.LANCZOS)
    logo_img_tk = ImageTk.PhotoImage(logo_img)
    label_logo = tk.Label(frame, image=logo_img_tk, bg=cor_fundo)
    label_logo.image = logo_img_tk
    label_logo.pack(pady=20)
    
    # Usuário
    label_usuario = tk.Label(frame, text="Usuário", font=("Arial", 14), fg=cor_texto, bg=cor_fundo)
    label_usuario.pack()
    entry_usuario = tk.Entry(frame, font=("Arial", 14), bd=2, relief="solid", justify="center", width=30)
    entry_usuario.pack(pady=10)

    # Senha
    label_senha = tk.Label(frame, text="Senha", font=("Arial", 14), fg=cor_texto, bg=cor_fundo)
    label_senha.pack()
    entry_senha = tk.Entry(frame, font=("Arial", 14), bd=2, relief="solid", justify="center", show="*", width=30)
    entry_senha.pack(pady=10)
    
    def on_enter_entrar(e):
        btn_entrar.config(bg=cor_hover_botao, cursor="hand2")  # Muda a cor e o cursor no botão "Entrar"

    def on_leave_entrar(e):
        btn_entrar.config(bg=cor_botao, cursor="arrow")  # Restaura a cor original e o cursor para o padrão

    def on_enter_sair(e):
        btn_sair.config(bg=cor_hover_sair, cursor="hand2")  # Muda a cor e o cursor no botão "Sair"

    def on_leave_sair(e):
        btn_sair.config(bg=cor_sair, cursor="arrow")  # Restaura a cor original e o cursor para o padrão

    # Botão Entrar
    btn_entrar = tk.Button(frame, text="Entrar", font=("Helvetica", 16), bg=cor_botao, fg="white", command=entrar)
    btn_entrar.pack(pady=20, padx=20, fill="x")
    btn_entrar.bind("<Enter>", on_enter_entrar)
    btn_entrar.bind("<Leave>", on_leave_entrar)

    # Botão para sair da tela cheia
    btn_sair = tk.Button(login_window, text="Sair", font=("Helvetica", 12, "bold"), bg=cor_sair, fg="white", command=login_window.destroy)
    btn_sair.place(relx=0.95, rely=0.05, anchor="ne")
    btn_sair.bind("<Enter>", on_enter_sair)
    btn_sair.bind("<Leave>", on_leave_sair)
    
    login_window.mainloop()

tela_login()
