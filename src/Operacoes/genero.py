from src.Operacoes.tabela import Tabela


class Genero(Tabela):

    def inserir(self, dados):
        sql = """
            INSERT INTO public.Genero (
                nome
            )
            VALUES (%s);
        """

        self.executar(sql, dados)

    def selecionar(self, condicao=None, parametros=None):
        sql = """
            SELECT
                id_genero,
                nome
            FROM public.Genero
        """

        if condicao:
            sql += " WHERE " + condicao

        sql += ";"

        return self.executar(sql, parametros, fetch=True)

    def atualizar(self, dados):
        sql = """
            UPDATE public.Genero
            SET
                nome = %s
            WHERE id_genero = %s;
        """

        self.executar(sql, dados)

    def deletar(self, condicao, parametros=None):
        sql = """
            DELETE FROM public.Genero
            WHERE
        """ + condicao + ";"

        self.executar(sql, parametros)