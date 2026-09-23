from src.Operacoes.tabela import Tabela


class Playlist(Tabela):

    def inserir(self, dados):
        sql = """
            INSERT INTO public.Playlist (
                nome,
                descricao,
                visibilidade,
                id_usuario
            )
            VALUES (%s, %s, %s, %s);
        """

        self.executar(sql, dados)

    def selecionar(self, condicao=None, parametros=None):
        sql = """
            SELECT
                id_playlist,
                nome,
                descricao,
                visibilidade,
                id_usuario
            FROM public.Playlist
        """

        if condicao:
            sql += " WHERE " + condicao

        sql += ";"

        return self.executar(sql, parametros, fetch=True)

    def atualizar(self, dados):
        sql = """
            UPDATE public.Playlist
            SET
                nome = %s,
                descricao = %s,
                visibilidade = %s,
                id_usuario = %s
            WHERE id_playlist = %s;
        """

        self.executar(sql, dados)

    def deletar(self, condicao, parametros=None):
        sql = """
            DELETE FROM public.Playlist
            WHERE
        """ + condicao + ";"

        self.executar(sql, parametros)