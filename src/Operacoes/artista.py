from src.Operacoes.tabela import Tabela


class Artista(Tabela):

    def inserir(self, dados):
        sql = """
            INSERT INTO public.Artista (
                nome_artistico,
                biografia,
                pais_origem,
                foto
            )
            VALUES (%s, %s, %s, %s);
        """

        self.executar(sql, dados)

    def selecionar(self, condicao=None, parametros=None):
        sql = """
            SELECT
                id_artista,
                nome_artistico,
                biografia,
                pais_origem,
                foto
            FROM public.Artista
        """

        if condicao:
            sql += " WHERE " + condicao

        sql += ";"

        return self.executar(sql, parametros, fetch=True)

    def atualizar(self, dados):
        sql = """
            UPDATE public.Artista
            SET
                nome_artistico = %s,
                biografia = %s,
                pais_origem = %s,
                foto = %s
            WHERE id_artista = %s;
        """

        self.executar(sql, dados)

    def deletar(self, condicao, parametros=None):
        sql = """
            DELETE FROM public.Artista
            WHERE
        """ + condicao + ";"

        self.executar(sql, parametros)