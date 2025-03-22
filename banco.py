from conexao_bd import conectar_mysql
import mysql.connector
import random



def verificar_login_bd(usuario, senha):

    conn = conectar_mysql()

    if conn is not None and conn.is_connected():
        try:
            cursor = conn.cursor()
            query = """
            SELECT 
                Permissao.tipo,
            CASE 
                WHEN Usuario.ativo = 1 THEN 'Ativo'
                ELSE 'Inativo'
            END AS ativo_sn,
            Usuario.nome,
            Usuario.tenant_id
            FROM
            Usuario AS Usuario
            JOIN
            Permissao AS Permissao
            ON
            Usuario.permissao_id = Permissao.id
            WHERE
            Usuario.email = %s
            AND
            Usuario.senha = %s
            """

            cursor.execute(query, (usuario,senha))
            resultado = cursor.fetchall()
            
            for linha in resultado:
                resultado = linha
                
            cursor.close()
            conn.close()
            
            if(resultado != ""):
                
                return resultado
            
            else:
                
                resultado = "Não encontrado"
                return resultado
             
        except mysql.connector.Error as e:
            retorno = f"Erro ao executar a consulta: {e}"
            conn.close()
            return retorno
    else:
        retorno = "Conexão não disponível"
        conn.close()
        return retorno

def pegar_produtos(tenant_id):
    
    conn = conectar_mysql()

    if conn is not None and conn.is_connected():
        try:
            cursor = conn.cursor()
            query = """
            SELECT 
            id,
            nome,
            CASE
                WHEN quant <= 0 THEN 'Sem estoque'
                ELSE 'Com estoque'
            END AS estoque,
            valor
            FROM 
            Produto
            WHERE
            tenant_id = %s
            """
            
            cursor.execute(query, (tenant_id,))
            resultados = cursor.fetchall()
            cursor.close()
            conn.close()

            if resultados:
                produtos = []

                for resultado in resultados:
                    produto = {
                        "codigo": resultado[0],
                        "nome": resultado[1],
                        "preco": float(resultado[3]),
                        "Tem estoque": resultado[2],
                    }
                    produtos.append(produto)

                return produtos
            
            else:
                
                resultados = "Não encontrado"
                return resultados
             
        except mysql.connector.Error as e:
            retorno = f"Erro ao executar a consulta: {e}"
            conn.close()
            return retorno
    else:
        retorno = "Conexão não disponível"
        conn.close()
        return retorno
    
def confirmar_pagamento(total, carrinho, nome_usu, tenant_id):

    flag_controle = "S"

    tenant_id = int(tenant_id)

    conn = conectar_mysql()

    try:
        
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Pedido (cliente, valor, tenant_id) VALUES (%s, %s, %s)", (nome_usu, total, tenant_id))
        conn.commit()
        cursor.close()
        conn.close()

    except mysql.connector.Error as e:

        retorno = f"Erro ao executar o INSERT: {e}"
        conn.close()
        flag_controle = "N"
        
    
    if(flag_controle == "S"):

        conn = conectar_mysql()

        cursor = conn.cursor()

        query = """
                SELECT 
                    Pedido.id
                FROM
                    Pedido
                WHERE
                    Pedido.tenant_id = %s
                AND
                    Pedido.cliente = %s
                ORDER BY Pedido.id DESC
                LIMIT 1
                """

        cursor.execute(query, (tenant_id, nome_usu))
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()

        Pedido_id = resultado[0]
        Pedido_id = int(Pedido_id)

        for produtos_carrinho in carrinho:

            conn = conectar_mysql()

            produto_id = produtos_carrinho["codigo"]

            produto_id = int(produto_id)

            valor_produtos_carrinho = produtos_carrinho["preco"]

            valor_produtos_carrinho = float(valor_produtos_carrinho)

            cursor = conn.cursor()
            query = """
                    SELECT 
                        PedidoProduto.quantidade,
                        PedidoProduto.valor
                    FROM
                        PedidoProduto
                    WHERE
                        PedidoProduto.pedido_id = %s
                    AND
                        PedidoProduto.produto_id = %s
                    """

            cursor.execute(query, (Pedido_id, produto_id))
            resultado = cursor.fetchone()
            cursor.close()
            
            if resultado:
                
                quantidade_pedido = resultado[0]

                quantidade_pedido = int(quantidade_pedido)

                quantidade_pedido = quantidade_pedido + 1

                valor_pedido = resultado[1]

                valor_pedido = float(valor_pedido)

                valor_pedido = valor_pedido + valor_produtos_carrinho


                cursor = conn.cursor()
                cursor.execute("UPDATE PedidoProduto SET quantidade = %s, valor = %s WHERE pedido_id = %s AND produto_id = %s", (quantidade_pedido, valor_pedido, Pedido_id, produto_id))
                conn.commit()
                cursor.close()


            else:

                quantidade_pedido = 1

                cursor = conn.cursor()
                cursor.execute("INSERT INTO PedidoProduto (pedido_id, produto_id, quantidade, valor) VALUES (%s, %s, %s, %s)", (Pedido_id, produto_id, quantidade_pedido, valor_produtos_carrinho))
                conn.commit()
                cursor.close()

            conn.close()

    retorno_bd = "Feito"
    return retorno_bd

def inserir_usuario_bd(usuario, senha, ativo, nome):

    conn = conectar_mysql()

    if conn is not None and conn.is_connected():
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (usuarios_ativo_sn, usuarios_nome, usuarios_login, usuarios_senha) VALUES (%s, %s, %s, %s)", (ativo, nome, usuario, senha))
            conn.commit()
            cursor.close()
            conn.close()
            return "Usuário inserido com sucesso."
        except mysql.connector.Error as e:
            retorno = f"Erro ao executar o INSERT: {e}"
            conn.close()
            return retorno
    else:
        retorno = "Conexão não disponível."
        conn.close()
        return retorno

def excluir():

    conn = conectar_mysql()

    try:
        cursor = conn.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")  # Desativa restrições
        cursor.execute("TRUNCATE TABLE Pedido")  
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")  # Reativa restrições
        conn.commit()
    except Exception as e:
        print(f"Erro ao truncar a tabela Pedido: {e}")
        conn.rollback()
    finally:
        cursor.close()

def permissaoUsu():

    conn = conectar_mysql()

    if conn is not None and conn.is_connected():
        try:
            cursor = conn.cursor()
            query = """
            SELECT 
            *
            FROM 
            Permissao
            """
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()
            conn.close()

            if resultados:
                permissoes = []

                for resultado in resultados:
                    produto = {
                        "id": resultado[0],
                        "tipo": resultado[1],
                    }
                    permissoes.append(produto)

                return permissoes
            
            else:
                
                resultados = "Não encontrado"
                return resultados
             
        except mysql.connector.Error as e:
            retorno = f"Erro ao executar a consulta: {e}"
            conn.close()
            return retorno
    else:
        retorno = "Conexão não disponível"
        conn.close()
        return retorno

def cadAdm(nome, email, senha, permissao_id):
    conn = conectar_mysql()

    if conn is not None and conn.is_connected():
        try:
            cursor = conn.cursor()
            query = """
            SELECT 
            email
            FROM 
            Usuario
            WHERE email = %s
            """
            cursor.execute(query, (email,))  # Passando o email para verificar se já existe
            resultados = cursor.fetchall()
            cursor.close()
            
            # Verificar se o e-mail já existe
            if resultados:
                # O email já existe, então fazemos um UPDATE
                update_result = updateCadAdm(nome, email, senha, permissao_id)
                if update_result == "Cadastro atualizado com sucesso":
                    return True
                else:
                    return False
            else:
                # O email não existe, então fazemos um INSERT
                insert_result = insertCadAdm(nome, email, senha, permissao_id)
                if insert_result:
                    return True
                else:
                    return False
            
            conn.close()

        except mysql.connector.Error as e:
            conn.close()
            return False  # Retorna False em caso de erro
    else:
        conn.close()
        return False  # Conexão não disponível, retorna False

def insertCadAdm(nome, email, senha, permissao_id):
    conn = conectar_mysql()

    if conn is not None and conn.is_connected():
        try:
            cursor = conn.cursor()

            query = """
            INSERT INTO Usuario (nome, email, senha, permissao_id, ativo, tenant_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            """

            dados = (nome, email, senha, permissao_id, 1, 101)  # Ativo é 1 e tenant_id é 101

            cursor.execute(query, dados)
            conn.commit()  # Confirma a operação no banco de dados

            cursor.close()
            conn.close()

            return True  # Sucesso

        except mysql.connector.Error as e:
            conn.close()
            return False  # Falha ao inserir

    else:
        conn.close()
        return False  # Conexão não disponível

def updateCadAdm(nome, email, senha, permissao_id):
    conn = conectar_mysql()

    if conn is not None and conn.is_connected():
        try:
            cursor = conn.cursor()

            # Query para atualizar um usuário existente
            query = """
            UPDATE Usuario
            SET nome = %s, email = %s, senha = %s, permissao_id = %s
            WHERE email = %s  # Atualiza baseado no e-mail
            """

            # Dados a serem atualizados (campos nome, email, senha, permissao_id, com base no email)
            dados = (nome, email, senha, permissao_id, email)

            cursor.execute(query, dados)
            conn.commit()  # Confirma a operação no banco de dados

            cursor.close()
            conn.close()

            return "Cadastro atualizado com sucesso"

        except mysql.connector.Error as e:
            retorno = f"Erro ao executar a consulta: {e}"
            conn.close()
            return retorno
    else:
        retorno = "Conexão não disponível"
        return retorno

def deleteCadAdm(email):
    conn = conectar_mysql()

    if conn is not None and conn.is_connected():
        try:
            cursor = conn.cursor()

            # Query para deletar um usuário baseado no e-mail
            query = """
            DELETE FROM Usuario
            WHERE email = %s
            """

            cursor.execute(query, (email,))
            conn.commit()  # Confirma a operação no banco de dados

            cursor.close()
            conn.close()

            return "Cadastro deletado com sucesso"

        except mysql.connector.Error as e:
            retorno = f"Erro ao executar a consulta: {e}"
            conn.close()
            return retorno
    else:
        retorno = "Conexão não disponível"
        return retorno

def buscar_donos():
    
    conn = conectar_mysql()

    if conn is not None and conn.is_connected():
        try:
            cursor = conn.cursor()
            query = """
            SELECT 
            *
            FROM 
            Usuario
            """
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()
            conn.close()

            if resultados:
                permissoes = []

                for resultado in resultados:
                    produto = {
                        "id": resultado[0],
                        "nome": resultado[1],
                    }
                    permissoes.append(produto)

                return permissoes
            
            else:
                
                resultados = "Não encontrado"
                return resultados
             
        except mysql.connector.Error as e:
            retorno = f"Erro ao executar a consulta: {e}"
            conn.close()
            return retorno
    else:
        retorno = "Conexão não disponível"
        conn.close()
        return retorno

def gerar_tenant_id():
    return random.randint(100, 999) 

def cadPadaria(nome, dono_id):
    # Conectar ao banco de dados
    conn = conectar_mysql()

    if conn is not None and conn.is_connected():
        try:
            cursor = conn.cursor()

            # Buscar o tenant_id do dono
            query_tenant = "SELECT tenant_id FROM Usuario WHERE id = %s"
            cursor.execute(query_tenant, (dono_id,))
            resultado = cursor.fetchone()

            if resultado:
                tenant_id = resultado[0]  # Obtém o tenant_id do dono

                # Inserir a padaria com o tenant_id encontrado
                query_padaria = """
                INSERT INTO Padaria (nome, dono_id, tenant_id)
                VALUES (%s, %s, %s)
                """
                dados_padaria = (nome, dono_id, tenant_id)
                cursor.execute(query_padaria, dados_padaria)
                conn.commit()  # Confirma a inserção no banco

                cursor.close()
                conn.close()

                return True  # Sucesso ao inserir
            else:
                cursor.close()
                conn.close()
                print("Dono não encontrado.")
                return False  # Falha ao encontrar o dono

        except mysql.connector.Error as e:
            conn.close()
            print(f"Erro ao inserir padaria: {e}")
            return False  # Falha ao inserir

    else:
        conn.close()
        return False  # Conexão não disponível

def atualizar_padaria(nome, novo_dono_id):
    conn = conectar_mysql()

    if conn is not None and conn.is_connected():
        try:
            cursor = conn.cursor()

            # Verificando se a padaria existe no banco
            query_verificacao = """
            SELECT id
            FROM Padaria
            WHERE nome = %s
            """
            cursor.execute(query_verificacao, (nome,))
            resultado = cursor.fetchone()

            if resultado:  # Se a padaria foi encontrada
                padaria_id = resultado[0]  # Obter o ID da padaria

                # Query de atualização
                query_update = """
                UPDATE Padaria
                SET dono_id = %s
                WHERE id = %s
                """

                cursor.execute(query_update, (novo_dono_id, padaria_id))
                conn.commit()  # Confirma a atualização no banco

                cursor.close()
                conn.close()

                return True  # Sucesso ao atualizar

            else:
                cursor.close()
                conn.close()
                return False  # Padaria não encontrada

        except mysql.connector.Error as e:
            conn.close()
            print(f"Erro ao atualizar padaria: {e}")
            return False  # Falha ao atualizar

    else:
        conn.close()
        return False  # Conexão não disponível

def listarUsuarios():
    conn = conectar_mysql()

    if conn is not None and conn.is_connected():
        try:
            cursor = conn.cursor(dictionary=True)  # Retorna os dados como dicionário

            # Atualizando a consulta para pegar também o nome da padaria
            query = """
                SELECT u.nome, u.email, p.nome AS nome_padaria
                FROM Usuario u
                LEFT JOIN Padaria p ON u.id = p.dono_id
            """
            cursor.execute(query)
            usuarios = cursor.fetchall()  # Pegando todos os usuários

            # Ajustar para "NAO TEM PADARIA" caso o administrador não tenha padaria
            for usuario in usuarios:
                if usuario['nome_padaria'] is None:
                    usuario['nome_padaria'] = 'NAO TEM PADARIA'

            cursor.close()
            conn.close()

            return usuarios  # Retorna a lista de usuários com o nome da padaria

        except mysql.connector.Error as e:
            print(f"Erro na listagem de usuários: {e}")
            return []  # Retorna uma lista vazia em caso de erro

    return []  # Retorna uma lista vazia se a conexão falhar

def obter_dono_id(email):
    conn = conectar_mysql()

    if conn is not None and conn.is_connected():
        try:
            cursor = conn.cursor()
            query = "SELECT id FROM Usuario WHERE email = %s"
            cursor.execute(query, (email,))
            resultado = cursor.fetchone()

            if resultado:
                return resultado[0]  # Retorna o id do dono
            else:
                return None  # Não encontrou o dono

        except mysql.connector.Error as e:
            print(f"Erro ao buscar dono_id: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    else:
        return None
   
def deletePadaria(nome_padaria, email):
    conn = conectar_mysql()

    if conn is not None and conn.is_connected():
        try:
            cursor = conn.cursor(dictionary=True)  # Use dictionary=True para retornar resultados como dicionário

            # Primeiro, buscar o ID da padaria associada ao nome da padaria e ao email do dono
            query = """
                SELECT p.id
                FROM Padaria p
                JOIN Usuario u ON p.dono_id = u.id
                WHERE p.nome = %s AND u.email = %s
            """
            cursor.execute(query, (nome_padaria, email))
            padaria = cursor.fetchone()  # Agora 'padaria' será um dicionário

            if padaria:
                padaria_id = padaria['id']  # Acessando o valor como um dicionário

                # Excluir a padaria usando o ID encontrado
                delete_query = "DELETE FROM Padaria WHERE id = %s"
                cursor.execute(delete_query, (padaria_id,))
                conn.commit()

                cursor.close()
                conn.close()

                return True  # Se a padaria foi removida com sucesso
            else:
                return False  # Se não encontrar a padaria correspondente

        except mysql.connector.Error as e:
            print(f"Erro ao excluir padaria: {e}")
            return False  # Se ocorrer algum erro

    return False  # Retorna False se a conexão falhar

def pegar_funcionarios(tenant_id):

    funcionarios = []
    
    conn = conectar_mysql()

    if conn is not None and conn.is_connected():
        try:
            cursor = conn.cursor()
            query = """
            SELECT 
            nome,
            email,
            id
            FROM 
            Usuario
            WHERE
            permissao_id = %s
            AND
            tenant_id = %s
            """
            cursor.execute(query, (3, tenant_id,))
            resultados = cursor.fetchall()
            
            for linha in resultados:
                
                funcionario = {
                    "Nome": linha[0],
                    "Email": linha[1],
                    "id": int(linha[2]),
                }
                funcionarios.append(funcionario)
                
            cursor.close()
            conn.close()

            if (funcionarios != ""):

                return funcionarios
            
            else:
                funcionarios = ""
                return funcionarios
             
        except mysql.connector.Error as e:
            funcionarios = f"Erro ao executar a consulta: {e}"
            conn.close()
            return funcionarios
    else:
        funcionarios = "Conexão não disponível"
        conn.close()
        return funcionarios
    
    
def CadEditarFunc(lista_para_edicao, tenant_id, tipo):
    
    conn = conectar_mysql()
    
    if(tipo == "Adicionar"):
        
        nome  = lista_para_edicao[0]['nome']
        email = lista_para_edicao[1]['email']
        senha = lista_para_edicao[2]['senha']
        
        if conn is not None and conn.is_connected():
            try:
                cursor = conn.cursor()

                query = """
                INSERT INTO Usuario (nome, email, senha, permissao_id, ativo, tenant_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                """

                dados = (nome, email, senha, 3 , 1 , tenant_id)

                cursor.execute(query, dados)
                conn.commit()

                cursor.close()
                conn.close()

                return True

            except mysql.connector.Error as e:
                conn.close()
                return False

        else:
            conn.close()
            return False
        
    elif(tipo == "Editar"):
        
        id       = lista_para_edicao[0]['id']
        nome     = lista_para_edicao[1]['nome']
        email    = lista_para_edicao[2]['email']
        ativo_sn = lista_para_edicao[3]['ativo_sn']
        
        if(ativo_sn == "Sim"):
            
            if conn is not None and conn.is_connected():
                try:
                    cursor = conn.cursor()

                    query = """
                    UPDATE Usuario 
                    SET nome = %s, email = %s, ativo = %s
                    WHERE
                    tenant_id = %s
                    AND
                    id = %s
                    """

                    dados = (nome, email, ativo_sn, tenant_id, id, )

                    cursor.execute(query, dados)
                    conn.commit()

                    cursor.close()
                    conn.close()

                    return True

                except mysql.connector.Error as e:
                    conn.close()
                    return False

            else:
                conn.close()
                return False
            
        elif(ativo_sn == "Não"):
            
            if conn is not None and conn.is_connected():
                try:
                    cursor = conn.cursor()

                    query = """
                    DELETE FROM Usuario WHERE id = %s
                    """

                    dados = (id, )

                    cursor.execute(query, dados)
                    conn.commit()

                    cursor.close()
                    conn.close()

                    return True

                except mysql.connector.Error as e:
                    conn.close()
                    return False

            else:
                conn.close()
                return False
            

def estoque_listar_itens(tenant_id):

    listaDeItens = []
    
    conn = conectar_mysql()

    if conn is not None and conn.is_connected():
        try:
            cursor = conn.cursor()
            query = """
            SELECT 
            id,
            nome,
            quant,
            valor
            FROM 
            Produto
            WHERE
            tenant_id = %s
            """
            cursor.execute(query, (tenant_id,))
            resultados = cursor.fetchall()
            
            for linha in resultados:
                
                valoresAchados = {
                    "id": linha[0],
                    "nome": linha[1],
                    "quant": int(linha[2]),
                    "valor": float(linha[2]),
                }
                listaDeItens.append(valoresAchados)
                
            cursor.close()
            conn.close()

            if (listaDeItens != ""):

                return listaDeItens
            
            else:
                listaDeItens = ""
                return listaDeItens
             
        except mysql.connector.Error as e:
            listaDeItens = f"Erro ao executar a consulta: {e}"
            conn.close()
            return listaDeItens
    else:
        listaDeItens = "Conexão não disponível"
        conn.close()
        return listaDeItens

def estoqueEditarProduto(lista_para_edicao, tenant_id, tipo):
    
    conn = conectar_mysql()
    
    if(tipo == "Adicionar"):
        
        nome         = lista_para_edicao[0]['nome']
        quantidade   = lista_para_edicao[1]['quantidade']
        preco        = float(lista_para_edicao[2]['preco'])
        tipo_produto = lista_para_edicao[3]['tipo_produto']
        
        if(tipo_produto == "Pães"):
            
            tipo_produto = "1"
            
        elif(tipo_produto == "Bolos"):
            
            tipo_produto = "2"
            
        elif(tipo_produto == "Salgados"):
            
            tipo_produto = "3"
        
        elif(tipo_produto == "Bebidas"):
            
            tipo_produto = "4"
            
        tipo_produto = int(tipo_produto)
        tenant_id    = int(tenant_id)
        quantidade   = int(quantidade)
        
        if conn is not None and conn.is_connected():
            try:
                cursor = conn.cursor()

                query = """
                INSERT INTO Produto (nome, tipo_id, quant, valor, tenant_id)
                VALUES (%s, %s, %s, %s, %s)
                """

                dados = (nome, tipo_produto, quantidade, preco, tenant_id)

                cursor.execute(query, dados,)
                conn.commit()

                cursor.close()
                conn.close()

                return True

            except mysql.connector.Error as e:
                
                conn.close()
                return False

        else:
            conn.close()
            return False
        
    elif(tipo == "Editar"):
        
        id          = lista_para_edicao[0]['id']
        nome        = lista_para_edicao[1]['nome']
        quantidade  = lista_para_edicao[2]['quantidade']
        preco       = float(lista_para_edicao[3]['preco'])
        ativo_sn    = lista_para_edicao[4]['ativo_sn']
        
        if(ativo_sn == "Sim"):
            
            if conn is not None and conn.is_connected():
                try:
                    cursor = conn.cursor()

                    query = """
                    UPDATE Produto 
                    SET nome = %s, quant = %s, valor = %s
                    WHERE
                    tenant_id = %s
                    AND
                    id = %s
                    """

                    dados = (nome, quantidade, preco, tenant_id, id, )

                    cursor.execute(query, dados)
                    conn.commit()

                    cursor.close()
                    conn.close()

                    return True

                except mysql.connector.Error as e:
                    conn.close()
                    return False

            else:
                conn.close()
                return False
            
        elif(ativo_sn == "Não"):
            
            if conn is not None and conn.is_connected():
                try:
                    cursor = conn.cursor()

                    query = """
                    DELETE FROM Produto WHERE id = %s
                    """

                    dados = (id, )

                    cursor.execute(query, dados)
                    conn.commit()

                    cursor.close()
                    conn.close()

                    return True

                except mysql.connector.Error as e:
                    conn.close()
                    return False

            else:
                conn.close()
                return False
            
def pegar_pedidos(tenant_id):

    pedidos = []
    
    conn = conectar_mysql()

    if conn is not None and conn.is_connected():
        try:
            cursor = conn.cursor()
            query = """
            SELECT 
            id,
            cliente,
            valor
            FROM
            Pedido
            WHERE
            tenant_id = %s
            """
            cursor.execute(query, (tenant_id,))
            resultados = cursor.fetchall()
            
            for linha in resultados:
                
                pediddo = {
                    "id": linha[0],
                    "cliente": linha[1],
                    "valor": linha[2],
                }
                pedidos.append(pediddo)
                
            cursor.close()
            conn.close()

            if (pedidos != ""):

                return pedidos
            
            else:
                pedidos = ""
                return pedidos
             
        except mysql.connector.Error as e:
            pedidos = f"Erro ao executar a consulta: {e}"
            conn.close()
            return pedidos
    else:
        pedidos = "Conexão não disponível"
        conn.close()
        return pedidos
   
def pegar_pedidos_produto(id_pedido):

    pedidos = []
    
    conn = conectar_mysql()

    if conn is not None and conn.is_connected():
        try:
            cursor = conn.cursor()
            query = """
            SELECT
            A.valor,
            B.nome,
            A.quantidade
            FROM 
            PedidoProduto AS A
            JOIN
            Produto AS B
            ON
            A.produto_id = B.id
            WHERE
            A.pedido_id = %s
            """
            cursor.execute(query, (id_pedido,))
            resultados = cursor.fetchall()
            
            for linha in resultados:
                
                pediddo = {
                    "nome_produto": linha[1],
                    "valor_doproduto": linha[0],
                    "quantidade_produto": linha[2],
                }
                pedidos.append(pediddo)
                
            cursor.close()
            conn.close()

            if (pedidos != ""):

                return pedidos
            
            else:
                pedidos = ""
                return pedidos
             
        except mysql.connector.Error as e:
            pedidos = f"Erro ao executar a consulta: {e}"
            conn.close()
            return pedidos
    else:
        pedidos = "Conexão não disponível"
        conn.close()
        return pedidos
   
