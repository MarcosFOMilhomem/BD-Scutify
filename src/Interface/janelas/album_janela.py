from datetime import date

from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QMessageBox,
    QLineEdit,
    QDateEdit,
    QComboBox
)

from src.Interface.janelas.crud_janela import CrudJanela
from src.Operacoes.album import Album
from src.Operacoes.artista import Artista


class AlbumJanela(CrudJanela):

    def __init__(self, janela):
        self.txt_titulo = janela.findChild(
            QLineEdit, "txtTitulo"
        )
        self.date_lancamento = janela.findChild(
            QDateEdit, "dateLancamento"
        )
        self.txt_capa = janela.findChild(
            QLineEdit, "txtCapa"
        )
        self.combo_artista = janela.findChild(
            QComboBox, "comboArtista"
        )

        componentes = {
            "txtTitulo": self.txt_titulo,
            "dateLancamento": self.date_lancamento,
            "txtCapa": self.txt_capa,
            "comboArtista": self.combo_artista
        }

        for nome, componente in componentes.items():
            if componente is None:
                raise RuntimeError(
                    f"Componente não encontrado: {nome}"
                )

        self.operacoes_artista = Artista()

        super().__init__(
            janela=janela,
            operacoes=Album(),
            nome_tabela="tabelaAlbum",
            colunas=[
                "ID",
                "Título",
                "Data de lançamento",
                "Capa",
                "Artista"
            ]
        )

        self.carregar_artistas()
        self.estado_inicial()
        self.carregar_registros()

    # ARTISTAS

    def carregar_artistas(self):
        try:
            artistas = self.operacoes_artista.selecionar()

            self.combo_artista.clear()

            for artista in artistas:
                id_artista = artista[0]
                nome_artista = artista[1]

                self.combo_artista.addItem(
                    str(nome_artista),
                    id_artista
                )

        except Exception as erro:
            QMessageBox.critical(
                self.janela,
                "Erro ao carregar artistas",
                str(erro)
            )

    # CAMPOS

    def limpar_campos(self):
        self.txt_titulo.clear()
        self.txt_capa.clear()

        self.date_lancamento.setDate(
            self.date_lancamento.minimumDate()
        )

        self.combo_artista.setCurrentIndex(-1)

    def ativar_campos(self, ativar):
        self.txt_titulo.setEnabled(ativar)
        self.date_lancamento.setEnabled(ativar)
        self.txt_capa.setEnabled(ativar)
        self.combo_artista.setEnabled(ativar)

    # DADOS

    def dados_formulario(self):
        data_qdate = self.date_lancamento.date()

        data_lancamento = date(
            data_qdate.year(),
            data_qdate.month(),
            data_qdate.day()
        )

        return {
            "titulo": self.txt_titulo.text().strip(),
            "data_lancamento": data_lancamento,
            "capa": self.txt_capa.text().strip(),
            "id_artista": self.combo_artista.currentData()
        }

    def dados_tabela(self, registro):
        return registro

    def preencher_formulario(self, registro):
        self.txt_titulo.setText(str(registro[1]))

        data = registro[2]

        self.date_lancamento.setDate(
            QDate(data.year, data.month, data.day)
        )

        self.txt_capa.setText(str(registro[3]))

        indice = self.combo_artista.findData(registro[4])
        self.combo_artista.setCurrentIndex(indice)

    # VALIDAÇÃO

    def validar_insercao(self, dados):
        if not dados["titulo"]:
            QMessageBox.warning(
                self.janela,
                "Campo obrigatório",
                "Digite o título do álbum!"
            )
            self.txt_titulo.setFocus()
            return False

        if not dados["capa"]:
            QMessageBox.warning(
                self.janela,
                "Campo obrigatório",
                "Informe o caminho ou endereço da capa!"
            )
            self.txt_capa.setFocus()
            return False

        if dados["id_artista"] is None:
            QMessageBox.warning(
                self.janela,
                "Campo obrigatório",
                "Selecione um artista!"
            )
            self.combo_artista.setFocus()
            return False

        return True

    def validar_atualizacao(self, dados):
        return self.validar_insercao(dados)

    # PARÂMETROS DO BANCO

    def parametros_insercao(self, dados):
        return (
            dados["titulo"],
            dados["data_lancamento"],
            dados["capa"],
            dados["id_artista"]
        )

    def parametros_atualizacao(
        self, dados, registro_original
    ):
        return (
            dados["titulo"],
            dados["data_lancamento"],
            dados["capa"],
            dados["id_artista"],
            self.id_selecionado
        )

    def condicao_id(self):
        return "id_album = %s"

    # PESQUISA

    def ativar_campo_pesquisa(self):
        self.txt_titulo.setEnabled(True)

    def texto_pesquisa(self):
        return self.txt_titulo.text()

    def parametros_pesquisa(self, texto):
        return (
            "titulo ILIKE %s",
            (f"%{texto}%",)
        )

    # DESCRIÇÃO E FOCO

    def descricao_registro(self):
        return f"Álbum: {self.txt_titulo.text()}"

    def focar_campo_principal(self):
        self.txt_titulo.setFocus()