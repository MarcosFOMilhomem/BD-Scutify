from src.Operacoes.tabela import Tabela


class Usuario(Tabela):

    def inserir(self, dados):
        sql = """
            INSERT INTO public.usuario (
                nome,
                email,
                senha,
                data_nascimento,
                plano,
                data_cadastro
            )
            VALUES (%s, %s, %s, %s, %s, %s);
        """

        self.executar(sql, dados)

    def selecionar(self, condicao=None, parametros=None):
        sql = """
            SELECT
                id_usuario,
                nome,
                email,
                senha,
                data_nascimento,
                plano,
                data_cadastro
            FROM public.Usuario
        """

        if condicao:
            sql += " WHERE " + condicao

        sql += ";"

        return self.executar(sql, parametros, fetch=True)

    def atualizar(self, dados):
        sql = """
            UPDATE public.Usuario
            SET
                nome = %s,
                email = %s,
                senha = %s,
                data_nascimento = %s,
                plano = %s,
                data_cadastro = %s
            WHERE id_usuario = %s;
        """

        self.executar(sql, dados)

    def deletar(self, condicao, parametros=None):
        sql = """
            DELETE FROM public.Usuario
            WHERE
        """ + condicao + ";"

        self.executar(sql, parametros)