from abc import ABC, abstractmethod
from src.Banco.conexao import conectar


class Tabela(ABC):

    def executar(self, sql, parametros=None, fetch=False):
        conexao = conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, parametros)

            if fetch:
                resultado = cursor.fetchall()
            else:
                resultado = None

            conexao.commit()

            return resultado

        except Exception:
            conexao.rollback()
            raise

        finally:
            cursor.close()
            conexao.close()

    @abstractmethod
    def inserir(self, dados):
        pass

    @abstractmethod
    def selecionar(self, condicao=None, parametros=None):
        pass

    @abstractmethod
    def atualizar(self, dados):
        pass

    @abstractmethod
    def deletar(self, condicao, parametros=None):
        pass