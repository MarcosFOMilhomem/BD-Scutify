from datetime import datetime

from PySide6.QtCore import QDateTime
from PySide6.QtWidgets import (
    QMessageBox,
    QLineEdit,
    QComboBox,
    QDateTimeEdit
)

from src.Interface.janelas.crud_janela import CrudJanela
from src.Operacoes.playlist_musica import PlaylistMusica
from src.Operacoes.playlist import Playlist
from src.Operacoes.musica import Musica


class PlaylistMusicaJanela(CrudJanela):

    def __init__(self, janela):
        self.combo_playlist = janela.findChild(
            QComboBox, "comboPlaylist"
        )
        self.combo_musica = janela.findChild(
            QComboBox, "comboMusica"
        )
        self.txt_ordem = janela.findChild(
            QLineEdit, "txtOrdem"
        )
        self.date_cadastro = janela.findChild(
            QDateTimeEdit, "dateCadastro"
        )

        componentes = {
            "comboPlaylist": self.combo_playlist,
            "comboMusica": self.combo_musica,
            "txtOrdem": self.txt_ordem,
            "dateCadastro": self.date_cadastro
        }

        for nome, componente in componentes.items():
            if componente is None:
                raise RuntimeError(
                    f"Componente não encontrado: {nome}"
                )

        self.operacoes_playlist = Playlist()
        self.operacoes_musica = Musica()

        super().__init__(
            janela=janela,
            operacoes=PlaylistMusica(),
            nome_tabela="tabelaPlaylist_Musica",
            colunas=[
                "Playlist",
                "Música",
                "Ordem",
                "Data de inclusão"
            ]
        )

        self.carregar_playlists()
        self.carregar_musicas()
        self.estado_inicial()
        self.carregar_registros()

    # PLAYLISTS E MÚSICAS

    def carregar_playlists(self):
        try:
            playlists = self.operacoes_playlist.selecionar()

            self.combo_playlist.clear()

            for playlist in playlists:
                id_playlist = playlist[0]
                nome_playlist = playlist[1]

                self.combo_playlist.addItem(
                    str(nome_playlist),
                    id_playlist
                )

        except Exception as erro:
            QMessageBox.critical(
                self.janela,
                "Erro ao carregar playlists",
                str(erro)
            )

    def carregar_musicas(self):
        try:
            musicas = self.operacoes_musica.selecionar()

            self.combo_musica.clear()

            for musica in musicas:
                id_musica = musica[0]
                titulo_musica = musica[1]

                self.combo_musica.addItem(
                    str(titulo_musica),
                    id_musica
                )

        except Exception as erro:
            QMessageBox.critical(
                self.janela,
                "Erro ao carregar músicas",
                str(erro)
            )

    # ESTADOS E CAMPOS

    def limpar_campos(self):
        self.combo_playlist.setCurrentIndex(-1)
        self.combo_musica.setCurrentIndex(-1)
        self.txt_ordem.clear()
        self.date_cadastro.setDateTime(
            QDateTime.currentDateTime()
        )

    def ativar_campos(self, ativar):
        self.combo_playlist.setEnabled(ativar)
        self.combo_musica.setEnabled(ativar)
        self.txt_ordem.setEnabled(ativar)
        self.date_cadastro.setEnabled(ativar)

    # DADOS

    def dados_formulario(self):
        ordem_texto = self.txt_ordem.text().strip()

        ordem = (
            int(ordem_texto)
            if ordem_texto.isdigit()
            else None
        )

        data_qdatetime = self.date_cadastro.dateTime()

        data_inclusao = datetime(
            data_qdatetime.date().year(),
            data_qdatetime.date().month(),
            data_qdatetime.date().day(),
            data_qdatetime.time().hour(),
            data_qdatetime.time().minute(),
            data_qdatetime.time().second()
        )

        return {
            "id_playlist": self.combo_playlist.currentData(),
            "id_musica": self.combo_musica.currentData(),
            "ordem": ordem,
            "data_inclusao": data_inclusao
        }

    def dados_tabela(self, registro):
        return (
            registro[0],
            registro[1],
            registro[2],
            registro[3]
        )

    def preencher_formulario(self, registro):
        indice_playlist = self.combo_playlist.findData(
            registro[0]
        )
        self.combo_playlist.setCurrentIndex(indice_playlist)

        indice_musica = self.combo_musica.findData(
            registro[1]
        )
        self.combo_musica.setCurrentIndex(indice_musica)

        self.txt_ordem.setText(str(registro[2]))

        data = registro[3]
        self.date_cadastro.setDateTime(
            QDateTime(
                data.year,
                data.month,
                data.day,
                data.hour,
                data.minute,
                data.second
            )
        )

    # VALIDAÇÃO

    def validar_insercao(self, dados):
        if dados["id_playlist"] is None:
            QMessageBox.warning(
                self.janela,
                "Campo obrigatório",
                "Selecione uma playlist!"
            )
            self.combo_playlist.setFocus()
            return False

        if dados["id_musica"] is None:
            QMessageBox.warning(
                self.janela,
                "Campo obrigatório",
                "Selecione uma música!"
            )
            self.combo_musica.setFocus()
            return False

        if dados["ordem"] is None or dados["ordem"] <= 0:
            QMessageBox.warning(
                self.janela,
                "Valor inválido",
                "A ordem deve ser um inteiro positivo."
            )
            self.txt_ordem.setFocus()
            return False

        return True

    def validar_atualizacao(self, dados):
        return self.validar_insercao(dados)

    # PARÂMETROS DO BANCO

    def parametros_insercao(self, dados):
        return (
            dados["id_playlist"],
            dados["id_musica"],
            dados["ordem"],
            dados["data_inclusao"]
        )

    def parametros_atualizacao(
        self, dados, registro_original
    ):
        return (
            dados["ordem"],
            dados["data_inclusao"],
            registro_original[0],
            registro_original[1]
        )

    # CHAVE PRIMÁRIA COMPOSTA

    def condicao_id(self):
        return (
            "id_playlist = %s AND id_musica = %s"
        )

    def parametros_id(self, id_registro):
        return id_registro

    def selecionar_registro(self):
        if self.estado not in (
            "inicial", "selecionado"
        ):
            return

        linha = self.tabela.currentRow()

        if linha < 0:
            return

        item_playlist = self.tabela.item(linha, 0)
        item_musica = self.tabela.item(linha, 1)

        if item_playlist is None or item_musica is None:
            return

        try:
            id_playlist = int(item_playlist.text())
            id_musica = int(item_musica.text())

            registros = self.operacoes.selecionar(
                self.condicao_id(),
                (id_playlist, id_musica)
            )

            if not registros:
                return

            self.id_selecionado = (
                id_playlist,
                id_musica
            )

            self.preencher_formulario(registros[0])
            self.ativar_campos(False)

            self.btn_inserir.setEnabled(False)
            self.btn_pesquisar.setEnabled(False)
            self.btn_atualizar.setEnabled(True)
            self.btn_deletar.setEnabled(True)

            self.estado = "selecionado"

        except Exception as erro:
            QMessageBox.critical(
                self.janela,
                "Erro ao selecionar registro",
                str(erro)
            )

    # ATUALIZAÇÃO COM CHAVE COMPOSTA

    def atualizar(self):
        if self.estado == "selecionado":
            self.estado = "atualizando"

            self.ativar_campos(True)
            self.bloquear_botoes("atualizar")
            self.tabela.setEnabled(False)

            self.focar_campo_principal()
            return

        if self.estado != "atualizando":
            return

        dados = self.dados_formulario()

        if not self.validar_atualizacao(dados):
            return

        try:
            id_playlist_original, id_musica_original = (
                self.id_selecionado
            )

            registros = self.operacoes.selecionar(
                self.condicao_id(),
                (
                    id_playlist_original,
                    id_musica_original
                )
            )

            if not registros:
                QMessageBox.warning(
                    self.janela,
                    "Registro não encontrado",
                    "Este registro não existe mais."
                )
                self.estado_inicial()
                self.carregar_registros()
                return

            registro_original = registros[0]

            # A operação SQL atualiza apenas ordem e data.
            parametros = self.parametros_atualizacao(
                dados, registro_original
            )

            self.operacoes.atualizar(parametros)

            QMessageBox.information(
                self.janela,
                "Sucesso",
                "Registro atualizado com sucesso!"
            )

            self.carregar_registros()
            self.estado_inicial()

        except Exception as erro:
            QMessageBox.critical(
                self.janela,
                "Erro ao atualizar",
                str(erro)
            )

    # PESQUISA

    
    # PESQUISA

    def pesquisar(self):
        if self.estado == "inicial":
            self.estado = "pesquisando"

            self.limpar_campos()
            self.ativar_campos(False)
            self.ativar_campo_pesquisa()

            self.bloquear_botoes("pesquisar")
            self.tabela.setEnabled(False)
            return

        if self.estado != "pesquisando":
            return

        id_playlist = self.combo_playlist.currentData()

        if id_playlist is None:
            QMessageBox.warning(
                self.janela,
                "Campo obrigatório",
                "Selecione uma playlist para pesquisar!"
            )
            self.combo_playlist.setFocus()
            return

        texto = self.texto_pesquisa().strip()

        condicao, parametros = self.parametros_pesquisa(texto)

        if self.carregar_registros(condicao, parametros):
            self.estado_inicial()

    def ativar_campo_pesquisa(self):
        self.combo_playlist.setEnabled(True)

    def texto_pesquisa(self):
        return self.combo_playlist.currentText()

    def parametros_pesquisa(self, texto):
        id_playlist = self.combo_playlist.currentData()

        return (
            "id_playlist = %s",
            (id_playlist,)
        )

    # EXCLUSÃO COM CHAVE COMPOSTA

    def deletar(self):
        if self.estado != "selecionado":
            return

        if self.id_selecionado is None:
            return

        id_playlist, id_musica = self.id_selecionado

        descricao = (
            f"Playlist ID: {id_playlist}\n"
            f"Música ID: {id_musica}"
        )

        self.estado = "excluindo"
        self.bloquear_botoes(None)
        self.tabela.setEnabled(False)

        resposta = QMessageBox.question(
            self.janela,
            "Confirmar exclusão",
            "Deseja remover esta música da playlist?\n\n"
            f"{descricao}",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if resposta != QMessageBox.StandardButton.Yes:
            self.estado_inicial()
            return

        try:
            self.operacoes.deletar(
                self.condicao_id(),
                (id_playlist, id_musica)
            )

            QMessageBox.information(
                self.janela,
                "Sucesso",
                "Música removida da playlist com sucesso!"
            )

        except Exception as erro:
            QMessageBox.critical(
                self.janela,
                "Erro ao excluir",
                str(erro)
            )

        finally:
            self.estado_inicial()
            self.carregar_registros()

    # DESCRIÇÃO E FOCO

    def descricao_registro(self):
        return (
            f"Playlist: {self.combo_playlist.currentText()}\n"
            f"Música: {self.combo_musica.currentText()}"
        )

    def focar_campo_principal(self):
        self.combo_playlist.setFocus()