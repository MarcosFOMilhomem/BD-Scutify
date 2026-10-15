from PySide6.QtWidgets import (
    QMessageBox,
    QLineEdit,
    QComboBox
)

from src.Interface.janelas.crud_janela import CrudJanela
from src.Operacoes.musica import Musica
from src.Operacoes.album import Album
from src.Operacoes.genero import Genero


class MusicaJanela(CrudJanela):

    def __init__(self, janela):
        self.txt_titulo = janela.findChild(
            QLineEdit, "txtTitulo"
        )
        self.txt_duracao = janela.findChild(
            QLineEdit, "txtDuracao"
        )
        self.txt_num_faixa = janela.findChild(
            QLineEdit, "txtNumFaixa"
        )
        self.txt_arq_audio = janela.findChild(
            QLineEdit, "txtArqAudio"
        )
        self.combo_album = janela.findChild(
            QComboBox, "comboAlbum"
        )
        self.combo_genero = janela.findChild(
            QComboBox, "comboGenero"
        )

        componentes = {
            "txtTitulo": self.txt_titulo,
            "txtDuracao": self.txt_duracao,
            "txtNumFaixa": self.txt_num_faixa,
            "txtArqAudio": self.txt_arq_audio,
            "comboAlbum": self.combo_album,
            "comboGenero": self.combo_genero
        }

        for nome, componente in componentes.items():
            if componente is None:
                raise RuntimeError(
                    f"Componente não encontrado: {nome}"
                )

        self.operacoes_album = Album()
        self.operacoes_genero = Genero()

        super().__init__(
            janela=janela,
            operacoes=Musica(),
            nome_tabela="tabelaMusica",
            colunas=[
                "ID",
                "Título",
                "Duração",
                "Arquivo de áudio",
                "Álbum",
                "Gênero"
            ]
        )

        self.carregar_albuns()
        self.carregar_generos()
        self.estado_inicial()
        self.carregar_registros()

    # ÁLBUNS E GÊNEROS

    def carregar_albuns(self):
        try:
            albuns = self.operacoes_album.selecionar()

            self.combo_album.clear()

            for album in albuns:
                id_album = album[0]
                titulo_album = album[1]

                self.combo_album.addItem(
                    str(titulo_album),
                    id_album
                )

        except Exception as erro:
            QMessageBox.critical(
                self.janela,
                "Erro ao carregar álbuns",
                str(erro)
            )

    def carregar_generos(self):
        try:
            generos = self.operacoes_genero.selecionar()

            self.combo_genero.clear()

            for genero in generos:
                id_genero = genero[0]
                nome_genero = genero[1]

                self.combo_genero.addItem(
                    str(nome_genero),
                    id_genero
                )

        except Exception as erro:
            QMessageBox.critical(
                self.janela,
                "Erro ao carregar gêneros",
                str(erro)
            )

    # CAMPOS

    def limpar_campos(self):
        self.txt_titulo.clear()
        self.txt_duracao.clear()
        self.txt_num_faixa.clear()
        self.txt_arq_audio.clear()

        self.combo_album.setCurrentIndex(-1)
        self.combo_genero.setCurrentIndex(-1)

    def ativar_campos(self, ativar):
        self.txt_titulo.setEnabled(ativar)
        self.txt_duracao.setEnabled(ativar)
        self.txt_num_faixa.setEnabled(ativar)
        self.txt_arq_audio.setEnabled(ativar)
        self.combo_album.setEnabled(ativar)
        self.combo_genero.setEnabled(ativar)

    # DADOS

    def dados_formulario(self):
        duracao_texto = self.txt_duracao.text().strip()
        faixa_texto = self.txt_num_faixa.text().strip()

        duracao = (
            int(duracao_texto)
            if duracao_texto.isdigit()
            else None
        )

        numero_faixa = (
            int(faixa_texto)
            if faixa_texto.isdigit()
            else None
        )

        return {
            "titulo": self.txt_titulo.text().strip(),
            "duracao": duracao,
            "numero_faixa": numero_faixa,
            "arquivo_audio": self.txt_arq_audio.text().strip(),
            "id_album": self.combo_album.currentData(),
            "id_genero": self.combo_genero.currentData()
        }

    def dados_tabela(self, registro):
        return (
            registro[0],
            registro[1],
            registro[2],
            registro[4],
            registro[5],
            registro[6]
        )

    def preencher_formulario(self, registro):
        self.txt_titulo.setText(str(registro[1]))
        self.txt_duracao.setText(str(registro[2]))
        self.txt_num_faixa.setText(str(registro[3]))
        self.txt_arq_audio.setText(str(registro[4]))

        indice_album = self.combo_album.findData(
            registro[5]
        )
        self.combo_album.setCurrentIndex(indice_album)

        indice_genero = self.combo_genero.findData(
            registro[6]
        )
        self.combo_genero.setCurrentIndex(indice_genero)

    # VALIDAÇÃO

    def validar_insercao(self, dados):
        if not dados["titulo"]:
            QMessageBox.warning(
                self.janela,
                "Campo obrigatório",
                "Digite o título da música!"
            )
            self.txt_titulo.setFocus()
            return False

        if dados["duracao"] is None or dados["duracao"] <= 0:
            QMessageBox.warning(
                self.janela,
                "Valor inválido",
                "A duração deve ser um inteiro positivo."
            )
            self.txt_duracao.setFocus()
            return False

        if (
            dados["numero_faixa"] is None
            or dados["numero_faixa"] <= 0
        ):
            QMessageBox.warning(
                self.janela,
                "Valor inválido",
                "O número da faixa deve ser um inteiro positivo."
            )
            self.txt_num_faixa.setFocus()
            return False

        if not dados["arquivo_audio"]:
            QMessageBox.warning(
                self.janela,
                "Campo obrigatório",
                "Informe o caminho ou endereço do arquivo de áudio!"
            )
            self.txt_arq_audio.setFocus()
            return False

        if dados["id_album"] is None:
            QMessageBox.warning(
                self.janela,
                "Campo obrigatório",
                "Selecione um álbum!"
            )
            self.combo_album.setFocus()
            return False

        if dados["id_genero"] is None:
            QMessageBox.warning(
                self.janela,
                "Campo obrigatório",
                "Selecione um gênero!"
            )
            self.combo_genero.setFocus()
            return False

        return True

    def validar_atualizacao(self, dados):
        return self.validar_insercao(dados)

    # PARÂMETROS DO BANCO

    def parametros_insercao(self, dados):
        return (
            dados["titulo"],
            dados["duracao"],
            dados["numero_faixa"],
            dados["arquivo_audio"],
            dados["id_album"],
            dados["id_genero"]
        )

    def parametros_atualizacao(
        self, dados, registro_original
    ):
        return (
            dados["titulo"],
            dados["duracao"],
            dados["numero_faixa"],
            dados["arquivo_audio"],
            dados["id_album"],
            dados["id_genero"],
            self.id_selecionado
        )

    def condicao_id(self):
        return "id_musica = %s"

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
        return f"Música: {self.txt_titulo.text()}"

    def focar_campo_principal(self):
        self.txt_titulo.setFocus()