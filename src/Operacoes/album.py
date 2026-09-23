from src.Operacoes.tabela import Tabela


class Album(Tabela):

    def inserir(self, dados):
        sql = """
            INSERT INTO public.Album (
                titulo,
                data_lancamento,
                capa,
                id_artista
            )
            VALUES (%s, %s, %s, %s);
        """

        self.executar(sql, dados)

    def selecionar(self, condicao=None, parametros=None):
        sql = """
            SELECT
                id_album,
                titulo,
                data_lancamento,
                capa,
                id_artista
            FROM public.Album
        """

        if condicao:
            sql += " WHERE " + condicao

        sql += ";"

        return self.executar(sql, parametros, fetch=True)

    def atualizar(self, dados):
        sql = """
            UPDATE public.Album
            SET
                titulo = %s,
                data_lancamento = %s,
                capa = %s,
                id_artista = %s
            WHERE id_album = %s;
        """

        self.executar(sql, dados)

    def deletar(self, condicao, parametros=None):
        sql = """
            DELETE FROM public.Album
            WHERE
        """ + condicao + ";"

        self.executar(sql, parametros)