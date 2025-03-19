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

def pegar_produtos():

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
            """
            cursor.execute(query)
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

def pegar_funcionarios():

    funcionarios = []
    
    conn = conectar_mysql()

    if conn is not None and conn.is_connected():
        try:
            cursor = conn.cursor()
            query = """
            SELECT 
            nome,
            email,
            ativo AS salario
            FROM 
            Usuario
            WHERE
            permissao_id = %s
            """
            cursor.execute(query, (3,))
            resultados = cursor.fetchall()
            
            for linha in resultados:
                
                funcionario = {
                    "Nome": linha[0],
                    "Email": linha[1],
                    "Salario": float(linha[2]),
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