from PySide6.QtWidgets import QMessageBox, QLineEdit

from src.Operacoes.artista import Artista
from src.Interface.janelas.crud_janela import CrudJanela


class ArtistaJanela(CrudJanela):

    def __init__(self, janela):
        super().__init__(
            janela=janela,
            operacoes=Artista(),
            nome_tabela="tabelaArtista",
            colunas=[
                "ID",
                "Nome",
                "Biografia",
                "País",
                "Foto"
            ]
        )

        self.nome = self.buscar(QLineEdit, "txtNome")
        self.biografia = self.buscar(QLineEdit, "txtBiografia")
        self.pais = self.buscar(QLineEdit, "txtPais")
        self.foto = self.buscar(QLineEdit, "txtFoto")

        self.carregar_registros()
        self.estado_inicial()

    # CAMPOS

    def limpar_campos(self):
        self.nome.clear()
        self.biografia.clear()
        self.pais.clear()
        self.foto.clear()

    def ativar_campos(self, ativar):
        self.nome.setEnabled(ativar)
        self.biografia.setEnabled(ativar)
        self.pais.setEnabled(ativar)
        self.foto.setEnabled(ativar)

    def focar_campo_principal(self):
        self.nome.setFocus()

    # DADOS DO FORMULÁRIO

    def dados_formulario(self):
        return {
            "nome_artistico": self.nome.text().strip(),
            "biografia": self.biografia.text().strip(),
            "pais_origem": self.pais.text().strip(),
            "foto": self.foto.text().strip()
        }

    def preencher_formulario(self, registro):
        # Ordem de Artista.selecionar:
        # 0 - ID; 1 - Nome artístico; 2 - Biografia;
        # 3 - País de origem; 4 - Foto.
        self.nome.setText(registro[1] or "")
        self.biografia.setText(registro[2] or "")
        self.pais.setText(registro[3] or "")
        self.foto.setText(registro[4] or "")

    # DADOS DA TABELA

    def dados_tabela(self, registro):
        return [
            registro[0],
            registro[1],
            registro[2],
            registro[3],
            registro[4]
        ]

    # VALIDAÇÕES

    def validar_insercao(self, dados):
        if not all(dados.values()):
            QMessageBox.warning(
                self.janela,
                "Campos obrigatórios",
                "Preencha todos os campos!"
            )
            return False
        return True

    def validar_atualizacao(self, dados):
        if not all(dados.values()):
            QMessageBox.warning(
                self.janela,
                "Campos obrigatórios",
                "Preencha todos os campos!"
            )
            return False
        return True

    # PARÂMETROS SQL

    def parametros_insercao(self, dados):
        return (
            dados["nome_artistico"],
            dados["biografia"],
            dados["pais_origem"],
            dados["foto"]
        )

    def parametros_atualizacao(self, dados, registro_original):
        return (
            dados["nome_artistico"],
            dados["biografia"],
            dados["pais_origem"],
            dados["foto"],
            self.id_selecionado
        )

    # IDENTIFICAÇÃO DO REGISTRO

    def condicao_id(self):
        return "id_artista = %s"

    def descricao_registro(self):
        return f"Nome artístico: {self.nome.text()}"

    # PESQUISA

    def ativar_campo_pesquisa(self):
        self.nome.setEnabled(True)
        self.nome.setFocus()

    def texto_pesquisa(self):
        return self.nome.text()

    def parametros_pesquisa(self, texto):
        return (
            "nome_artistico ILIKE %s",
            (f"%{texto}%",)
        )
