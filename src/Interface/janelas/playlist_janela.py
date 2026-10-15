from PySide6.QtWidgets import (
    QLineEdit,
    QComboBox,
    QMessageBox
)

from src.Interface.janelas.crud_janela import CrudJanela
from src.Operacoes.playlist import Playlist
from src.Operacoes.usuario import Usuario


class PlaylistJanela(CrudJanela):

    def __init__(self, janela):
        self.txt_nome = janela.findChild(
            QLineEdit, "txtNome"
        )
        self.txt_descricao = janela.findChild(
            QLineEdit, "txtDescricao"
        )
        self.txt_visibilidade = janela.findChild(
            QLineEdit, "txtVisibilidade"
        )
        self.combo_usuario = janela.findChild(
            QComboBox, "comboUsuario"
        )

        componentes = {
            "txtNome": self.txt_nome,
            "txtDescricao": self.txt_descricao,
            "txtVisibilidade": self.txt_visibilidade,
            "comboUsuario": self.combo_usuario
        }

        for nome, componente in componentes.items():
            if componente is None:
                raise RuntimeError(
                    f"Componente não encontrado: {nome}"
                )

        self.operacoes_usuario = Usuario()

        super().__init__(
            janela=janela,
            operacoes=Playlist(),
            nome_tabela="tabelaPlaylist",
            colunas=[
                "ID",
                "Nome",
                "Descrição",
                "Visibilidade",
                "Usuário"
            ]
        )

        self.carregar_usuarios()
        self.estado_inicial()
        self.carregar_registros()

    # USUÁRIOS

    def carregar_usuarios(self):
        try:
            usuarios = self.operacoes_usuario.selecionar()

            self.combo_usuario.clear()

            for usuario in usuarios:
                id_usuario = usuario[0]
                nome_usuario = usuario[1]

                self.combo_usuario.addItem(
                    str(nome_usuario),
                    id_usuario
                )

        except Exception as erro:
            QMessageBox.critical(
                self.janela,
                "Erro ao carregar usuários",
                str(erro)
            )

    # CAMPOS

    def limpar_campos(self):
        self.txt_nome.clear()
        self.txt_descricao.clear()
        self.txt_visibilidade.clear()
        self.combo_usuario.setCurrentIndex(-1)

    def ativar_campos(self, ativar):
        self.txt_nome.setEnabled(ativar)
        self.txt_descricao.setEnabled(ativar)
        self.txt_visibilidade.setEnabled(ativar)
        self.combo_usuario.setEnabled(ativar)

    # DADOS

    def dados_formulario(self):
        return {
            "nome": self.txt_nome.text().strip(),
            "descricao": self.txt_descricao.text().strip(),
            "visibilidade": self.txt_visibilidade.text().strip(),
            "id_usuario": self.combo_usuario.currentData()
        }

    def dados_tabela(self, registro):
        return registro

    def preencher_formulario(self, registro):
        self.txt_nome.setText(str(registro[1]))
        self.txt_descricao.setText(str(registro[2]))
        self.txt_visibilidade.setText(str(registro[3]))

        indice = self.combo_usuario.findData(registro[4])
        self.combo_usuario.setCurrentIndex(indice)

    # VALIDAÇÃO

    def validar_insercao(self, dados):
        if not dados["nome"]:
            QMessageBox.warning(
                self.janela,
                "Campo obrigatório",
                "Digite o nome da playlist!"
            )
            self.txt_nome.setFocus()
            return False

        if not dados["descricao"]:
            QMessageBox.warning(
                self.janela,
                "Campo obrigatório",
                "Digite a descrição da playlist!"
            )
            self.txt_descricao.setFocus()
            return False

        if not dados["visibilidade"]:
            QMessageBox.warning(
                self.janela,
                "Campo obrigatório",
                "Digite a visibilidade da playlist!"
            )
            self.txt_visibilidade.setFocus()
            return False

        if dados["id_usuario"] is None:
            QMessageBox.warning(
                self.janela,
                "Campo obrigatório",
                "Selecione um usuário!"
            )
            self.combo_usuario.setFocus()
            return False

        return True

    def validar_atualizacao(self, dados):
        return self.validar_insercao(dados)

    # PARÂMETROS DO BANCO

    def parametros_insercao(self, dados):
        return (
            dados["nome"],
            dados["descricao"],
            dados["visibilidade"],
            dados["id_usuario"]
        )

    def parametros_atualizacao(
        self, dados, registro_original
    ):
        return (
            dados["nome"],
            dados["descricao"],
            dados["visibilidade"],
            dados["id_usuario"],
            self.id_selecionado
        )

    def condicao_id(self):
        return "id_playlist = %s"

    # PESQUISA

    def ativar_campo_pesquisa(self):
        self.txt_nome.setEnabled(True)

    def texto_pesquisa(self):
        return self.txt_nome.text()

    def parametros_pesquisa(self, texto):
        return (
            "nome ILIKE %s",
            (f"%{texto}%",)
        )

    # DESCRIÇÃO E FOCO

    def descricao_registro(self):
        return (
            f"Playlist: {self.txt_nome.text()}"
        )

    def focar_campo_principal(self):
        self.txt_nome.setFocus()
