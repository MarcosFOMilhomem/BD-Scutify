from src.Operacoes.tabela import Tabela


class Musica(Tabela):

    def inserir(self, dados):
        sql = """
            INSERT INTO public.Musica (
                titulo,
                duracao,
                numero_faixa,
                arquivo_audio,
                id_album,
                id_genero
            )
            VALUES (%s, %s, %s, %s, %s, %s);
        """

        self.executar(sql, dados)

    def selecionar(self, condicao=None, parametros=None):
        sql = """
            SELECT
                id_musica,
                titulo,
                duracao,
                numero_faixa,
                arquivo_audio,
                id_album,
                id_genero
            FROM public.Musica
        """

        if condicao:
            sql += " WHERE " + condicao

        sql += ";"

        return self.executar(sql, parametros, fetch=True)

    def atualizar(self, dados):
        sql = """
            UPDATE public.Musica
            SET
                titulo = %s,
                duracao = %s,
                numero_faixa = %s,
                arquivo_audio = %s,
                id_album = %s,
                id_genero = %s
            WHERE id_musica = %s;
        """

        self.executar(sql, dados)

    def deletar(self, condicao, parametros=None):
        sql = """
            DELETE FROM public.Musica
            WHERE
        """ + condicao + ";"

        self.executar(sql, parametros)