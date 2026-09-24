
from src.Operacoes.usuario import Usuario
from src.Interface.janelas.crud_janela import CrudJanela

from PySide6.QtWidgets import (
    QMessageBox,
    QLineEdit,
    QComboBox,
    QDateEdit,
    QDateTimeEdit
)


class UsuarioJanela(CrudJanela):

    def __init__(self, janela):

        # Inicializar a classe genérica
        super().__init__(
            janela=janela,
            operacoes=Usuario(),
            nome_tabela="tabelaUsuarios",
            colunas=[
                "ID",
                "Nome",
                "E-mail",
                "Nascimento",
                "Plano",
                "Data de cadastro"
            ]
        )

        # Campos específicos de usuários
        self.nome = self.buscar(
            QLineEdit, "txtNome"
        )
        self.email = self.buscar(
            QLineEdit, "txtEmail"
        )
        self.senha = self.buscar(
            QLineEdit, "txtSenha"
        )
        self.nascimento = self.buscar(
            QDateEdit, "dateNascimento"
        )
        self.plano = self.buscar(
            QComboBox, "comboPlano"
        )
        self.cadastro = self.buscar(
            QDateTimeEdit, "dateCadastro"
        )

        # Configurações específicas
        self.senha.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.cadastro.setReadOnly(True)
        self.cadastro.setEnabled(False)

        # Carregar os usuários e preparar a interface
        self.carregar_registros()
        self.estado_inicial()

    # CAMPOS

    def limpar_campos(self):
        self.nome.clear()
        self.email.clear()
        self.senha.clear()
        self.nascimento.clear()
        self.plano.setCurrentIndex(-1)
        self.cadastro.clear()

    def ativar_campos(self, ativar):
        self.nome.setEnabled(ativar)
        self.email.setEnabled(ativar)
        self.senha.setEnabled(ativar)
        self.nascimento.setEnabled(ativar)
        self.plano.setEnabled(ativar)

        # Gerado automaticamente pelo PostgreSQL
        self.cadastro.setEnabled(False)

    def focar_campo_principal(self):
        self.nome.setFocus()

    # DADOS DO FORMULÁRIO

    def dados_formulario(self):
        return {
            "nome": self.nome.text().strip(),
            "email": self.email.text().strip(),
            "senha": self.senha.text(),
            "data_nascimento":
                self.nascimento.date().toPython(),
            "plano": self.plano.currentText()
        }

    def preencher_formulario(self, registro):
        # Ordem das colunas retornadas por Usuario.selecionar:
        # 0 - ID
        # 1 - Nome
        # 2 - E-mail
        # 3 - Senha
        # 4 - Nascimento
        # 5 - Plano
        # 6 - Cadastro

        self.nome.setText(registro[1])
        self.email.setText(registro[2])

        # Nunca mostrar a senha armazenada
        self.senha.clear()

        if registro[4] is not None:
            self.nascimento.setDate(registro[4])

        indice = self.plano.findText(registro[5])

        if indice >= 0:
            self.plano.setCurrentIndex(indice)
        else:
            self.plano.setCurrentIndex(-1)

        if registro[6] is not None:
            self.cadastro.setDateTime(registro[6])

    # DADOS DA TABELA

    def dados_tabela(self, registro):
        # Não incluir a senha
        return [
            registro[0],
            registro[1],
            registro[2],
            registro[4],
            registro[5],
            registro[6]
        ]

    # VALIDAÇÕES

    def validar_insercao(self, dados):
        if not all([
            dados["nome"],
            dados["email"],
            dados["senha"],
            dados["plano"]
        ]):
            QMessageBox.warning(
                self.janela,
                "Campos obrigatórios",
                "Preencha todos os campos!"
            )
            return False

        if not self.nascimento.date().isValid():
            QMessageBox.warning(
                self.janela,
                "Data inválida",
                "Informe uma data de nascimento válida."
            )
            return False

        return True

    def validar_atualizacao(self, dados):
        # A senha é opcional durante a atualização
        if not all([
            dados["nome"],
            dados["email"],
            dados["plano"]
        ]):
            QMessageBox.warning(
                self.janela,
                "Campos obrigatórios",
                "Preencha todos os campos obrigatórios!"
            )
            return False

        if not self.nascimento.date().isValid():
            QMessageBox.warning(
                self.janela,
                "Data inválida",
                "Informe uma data de nascimento válida."
            )
            return False

        return True

    # INSERÇÃO

    def parametros_insercao(self, dados):
        return (
            dados["nome"],
            dados["email"],
            dados["senha"],
            dados["data_nascimento"],
            dados["plano"]
        )

    # ATUALIZAÇÃO

    def parametros_atualizacao(
        self, dados, registro_original
    ):
        # Manter a senha anterior se o campo estiver vazio
        senha = dados["senha"]

        if not senha:
            senha = registro_original[3]

        # Preservar a data original de cadastro
        data_cadastro = registro_original[6]

        return (
            dados["nome"],
            dados["email"],
            senha,
            dados["data_nascimento"],
            dados["plano"],
            data_cadastro,
            self.id_selecionado
        )

    # IDENTIFICAÇÃO DO REGISTRO

    def condicao_id(self):
        return "id_usuario = %s"

    def descricao_registro(self):
        return f"Nome: {self.nome.text()}"

    # PESQUISA

    def ativar_campo_pesquisa(self):
        self.nome.setEnabled(True)
        self.nome.setFocus()

    def texto_pesquisa(self):
        return self.nome.text()

    def parametros_pesquisa(self, texto):
        return (
            "nome ILIKE %s",
            (f"%{texto}%",)
        )