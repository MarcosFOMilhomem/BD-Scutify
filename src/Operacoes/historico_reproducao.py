from src.Operacoes.tabela import Tabela


class HistoricoReproducao(Tabela):

    def inserir(self, dados):
        sql = """
            INSERT INTO public.Historico_Reproducao (
                id_usuario,
                id_musica,
                data_hora
            )
            VALUES (%s, %s, %s);
        """

        self.executar(sql, dados)

    def selecionar(self, condicao=None, parametros=None):
        sql = """
            SELECT
                id_historico,
                id_usuario,
                id_musica,
                data_hora
            FROM public.Historico_Reproducao
        """

        if condicao:
            sql += " WHERE " + condicao

        sql += ";"

        return self.executar(sql, parametros, fetch=True)

    def atualizar(self, dados):
        sql = """
            UPDATE public.Historico_Reproducao
            SET
                id_usuario = %s,
                id_musica = %s,
                data_hora = %s
            WHERE id_historico = %s;
        """

        self.executar(sql, dados)

    def deletar(self, condicao, parametros=None):
        sql = """
            DELETE FROM public.Historico_Reproducao
            WHERE
        """ + condicao + ";"

        self.executar(sql, parametros)