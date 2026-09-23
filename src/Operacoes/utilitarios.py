from src.Banco.conexao import conectar


def listar_tabelas():
    sql = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
          AND table_type = 'BASE TABLE'
        ORDER BY table_name;
    """

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute(sql)

        tabelas = cursor.fetchall()

        print(f"=== TABELAS DO BANCO ({len(tabelas)}) ===")

        for tabela in tabelas:
            print(tabela[0])

    finally:
        cursor.close()
        conexao.close()
        
def mostrar_duas_tabelas(nome_tabela_1, nome_tabela_2):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        for nome_tabela in (nome_tabela_1, nome_tabela_2):
            cursor.execute(f"SELECT * FROM public.{nome_tabela};")

            registros = cursor.fetchall()

            print(f"\n=== {nome_tabela.upper()} ===")

            for registro in registros:
                print(registro)

    finally:
        cursor.close()
        conexao.close()
        
def mostrar_tudo():
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)

        tabelas = cursor.fetchall()

        print(f"=== BANCO DE DADOS ({len(tabelas)} TABELAS) ===")

        for tabela in tabelas:
            nome_tabela = tabela[0]

            cursor.execute(f"SELECT * FROM public.{nome_tabela};")
            registros = cursor.fetchall()

            print(f"\n=== {nome_tabela.upper()} ===")

            if registros:
                for registro in registros:
                    print(registro)
            else:
                print("(vazia)")

    finally:
        cursor.close()
        conexao.close()