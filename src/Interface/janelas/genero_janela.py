from PySide6.QtWidgets import QLineEdit

from src.Interface.janelas.crud_janela import CrudJanela
from src.Operacoes.genero import Genero


class GeneroJanela(CrudJanela):

    def __init__(self, janela):
        self.txt_nome = janela.findChild(
            QLineEdit, "txtNome"
        )

        if self.txt_nome is None:
            raise RuntimeError(
                "Componente não encontrado: txtNome"
            )

        super().__init__(
            janela=janela,
            operacoes=Genero(),
            nome_tabela="tabelaGenero",
            colunas=["ID", "Nome"]
        )

        self.estado_inicial()
        self.carregar_registros()

    # CAMPOS

    def limpar_campos(self):
        self.txt_nome.clear()

    def ativar_campos(self, ativar):
        self.txt_nome.setEnabled(ativar)

    # DADOS

    def dados_formulario(self):
        return {
            "nome": self.txt_nome.text().strip()
        }

    def dados_tabela(self, registro):
        return registro

    def preencher_formulario(self, registro):
        self.txt_nome.setText(str(registro[1]))

    # VALIDAÇÃO

    def validar_insercao(self, dados):
        if not dados["nome"]:
            from PySide6.QtWidgets import QMessageBox

            QMessageBox.warning(
                self.janela,
                "Campo obrigatório",
                "Digite o nome do gênero!"
            )
            self.txt_nome.setFocus()
            return False

        return True

    def validar_atualizacao(self, dados):
        return self.validar_insercao(dados)

    # PARÂMETROS DO BANCO

    def parametros_insercao(self, dados):
        return (dados["nome"],)

    def parametros_atualizacao(
        self, dados, registro_original
    ):
        return (
            dados["nome"],
            self.id_selecionado
        )

    def condicao_id(self):
        return "id_genero = %s"

    # PESQUISA

    def ativar_campo_pesquisa(self):
        self.txt_nome.setEnabled(True)

    def texto_pesquisa(self):
        return self.txt_nome.text()

    def parametros_pesquisa(self, texto):
        return "nome ILIKE %s", (f"%{texto}%",)

    # DESCRIÇÃO E FOCO

    def descricao_registro(self):
        return f"Gênero: {self.txt_nome.text()}"

    def focar_campo_principal(self):
        self.txt_nome.setFocus()
