
from datetime import datetime

from PySide6.QtCore import QDateTime
from PySide6.QtWidgets import (
    QMessageBox,
    QComboBox,
    QDateTimeEdit,
)

from src.Interface.janelas.crud_janela import CrudJanela
from src.Operacoes.historico_reproducao import HistoricoReproducao
from src.Operacoes.usuario import Usuario
from src.Operacoes.musica import Musica


class HistoricoReproducaoJanela(CrudJanela):

    def __init__(self, janela):
        self.combo_usuario = janela.findChild(
            QComboBox, "comboUsuario"
        )
        self.combo_musica = janela.findChild(
            QComboBox, "comboMusica"
        )
        self.date_cadastro = janela.findChild(
            QDateTimeEdit, "dateCadastro"
        )

        self.operacoes_usuario = Usuario()
        self.operacoes_musica = Musica()

        super().__init__(
            janela=janela,
            operacoes=HistoricoReproducao(),
            nome_tabela="tabelaHistorico",
            colunas=[
                "ID",
                "Usuário",
                "Música",
                "Data e hora"
            ]
        )

        self.carregar_usuarios()
        self.carregar_musicas()

        self.estado_inicial()
        self.carregar_registros()

    # CARREGAR COMBOS

    def carregar_usuarios(self):
        registros = self.operacoes_usuario.selecionar()

        self.combo_usuario.clear()

        for registro in registros:
            id_usuario = registro[0]
            nome_usuario = registro[1]

            self.combo_usuario.addItem(
                str(nome_usuario),
                id_usuario
            )

    def carregar_musicas(self):
        registros = self.operacoes_musica.selecionar()

        self.combo_musica.clear()

        for registro in registros:
            id_musica = registro[0]
            titulo_musica = registro[1]

            self.combo_musica.addItem(
                str(titulo_musica),
                id_musica
            )

    # CAMPOS

    def limpar_campos(self):
        self.combo_usuario.setCurrentIndex(-1)
        self.combo_musica.setCurrentIndex(-1)
        self.date_cadastro.setDateTime(
            QDateTime.currentDateTime()
        )

    def ativar_campos(self, ativar):
        self.combo_usuario.setEnabled(ativar)
        self.combo_musica.setEnabled(ativar)
        self.date_cadastro.setEnabled(ativar)

    def dados_formulario(self):
        return {
            "id_usuario": self.combo_usuario.currentData(),
            "id_musica": self.combo_musica.currentData(),
            "data_hora": (
                self.date_cadastro.dateTime()
                .toPython()
            )
        }

    def dados_tabela(self, registro):
        return registro

    def preencher_formulario(self, registro):
        self.combo_usuario.setCurrentIndex(
            self.combo_usuario.findData(registro[1])
        )

        self.combo_musica.setCurrentIndex(
            self.combo_musica.findData(registro[2])
        )

        data_hora = registro[3]

        self.date_cadastro.setDateTime(
            QDateTime(data_hora)
        )

    # VALIDAÇÃO

    def validar_insercao(self, dados):
        if dados["id_usuario"] is None:
            QMessageBox.warning(
                self.janela,
                "Campo obrigatório",
                "Selecione um usuário."
            )
            return False

        if dados["id_musica"] is None:
            QMessageBox.warning(
                self.janela,
                "Campo obrigatório",
                "Selecione uma música."
            )
            return False

        return True

    def validar_atualizacao(self, dados):
        return self.validar_insercao(dados)

    # PARÂMETROS SQL

    def parametros_insercao(self, dados):
        return (
            dados["id_usuario"],
            dados["id_musica"],
            dados["data_hora"]
        )

    def parametros_atualizacao(
        self, dados, registro_original
    ):
        return (
            dados["id_usuario"],
            dados["id_musica"],
            dados["data_hora"],
            registro_original[0]
        )

    def condicao_id(self):
        return "id_historico = %s"

    # PESQUISA

    def ativar_campo_pesquisa(self):
        self.combo_usuario.setEnabled(True)

    def texto_pesquisa(self):
        return self.combo_usuario.currentText()

    def parametros_pesquisa(self, texto):
        id_usuario = self.combo_usuario.currentData()

        return (
            "id_usuario = %s",
            (id_usuario,)
        )

    # OUTROS

    def descricao_registro(self):
        return (
            f"Usuário: {self.combo_usuario.currentText()}\n"
            f"Música: {self.combo_musica.currentText()}"
        )

    def focar_campo_principal(self):
        self.combo_usuario.setFocus()
