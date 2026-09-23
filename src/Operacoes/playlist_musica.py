from src.Operacoes.tabela import Tabela


class PlaylistMusica(Tabela):

    def inserir(self, dados):
        sql = """
            INSERT INTO public.Playlist_Musica (
                id_playlist,
                id_musica,
                ordem,
                data_inclusao
            )
            VALUES (%s, %s, %s, %s);
        """

        self.executar(sql, dados)

    def selecionar(self, condicao=None, parametros=None):
        sql = """
            SELECT
                id_playlist,
                id_musica,
                ordem,
                data_inclusao
            FROM public.Playlist_Musica
        """

        if condicao:
            sql += " WHERE " + condicao

        sql += ";"

        return self.executar(sql, parametros, fetch=True)

    def atualizar(self, dados):
        sql = """
            UPDATE public.Playlist_Musica
            SET
                ordem = %s,
                data_inclusao = %s
            WHERE id_playlist = %s
              AND id_musica = %s;
        """

        self.executar(sql, dados)

    def deletar(self, condicao, parametros=None):
        sql = """
            DELETE FROM public.Playlist_Musica
            WHERE
        """ + condicao + ";"

        self.executar(sql, parametros)