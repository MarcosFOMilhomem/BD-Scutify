from src.Operacoes.usuario import Usuario

from PySide6.QtWidgets import (
    QMessageBox,
    QLineEdit,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QTableWidget,
    QPushButton,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView
)


class UsuarioJanela:

    def __init__(self, janela):
        self.janela = janela

        # Campos do formulário
        self.nome = self.buscar(QLineEdit, "txtNome")
        self.email = self.buscar(QLineEdit, "txtEmail")
        self.senha = self.buscar(QLineEdit, "txtSenha")
        self.nascimento = self.buscar(QDateEdit, "dateNascimento")
        self.plano = self.buscar(QComboBox, "comboPlano")
        self.cadastro = self.buscar(QDateTimeEdit, "dateCadastro")

        # Tabela de registros
        self.tabela = self.buscar(
            QTableWidget, "tabelaUsuarios"
        )

        # Botões CRUD
        self.btn_inserir = self.buscar(
            QPushButton, "btnInserir"
        )
        self.btn_pesquisar = self.buscar(
            QPushButton, "btnPesquisar"
        )
        self.btn_atualizar = self.buscar(
            QPushButton, "btnAtualizar"
        )
        self.btn_deletar = self.buscar(
            QPushButton, "btnDeletar"
        )
        self.btn_resetar = self.buscar(
            QPushButton, "btnResetar"
        )

        self.usuario_db = Usuario()
        self.id_selecionado = None

        self.configurar_tabela()
        self.carregar_usuarios()
        
        self.tabela.itemSelectionChanged.connect(
            self.selecionar_usuario
        )
        
        self.configurar()
        self.conectar_botoes()
        
        self.estado = "inicial"
        self.estado_inicial()

    def ativar_campos(self, ativar):
        self.nome.setEnabled(ativar)
        self.email.setEnabled(ativar)
        self.senha.setEnabled(ativar)
        self.nascimento.setEnabled(ativar)
        self.plano.setEnabled(ativar)

        # Gerado automaticamente pelo banco
        self.cadastro.setEnabled(False)
        
    def estado_inicial(self):
        self.estado = "inicial"
        self.id_selecionado = None

        # Limpar os campos
        self.nome.clear()
        self.email.clear()
        self.senha.clear()
        self.nascimento.clear()
        self.plano.setCurrentIndex(-1)

        # Bloquear os campos
        self.ativar_campos(False)

        # Configurar os botões
        self.btn_inserir.setEnabled(True)
        self.btn_pesquisar.setEnabled(True)
        self.btn_atualizar.setEnabled(False)
        self.btn_deletar.setEnabled(False)

        # Remover seleção da tabela
        self.tabela.blockSignals(True)
        self.tabela.clearSelection()
        self.tabela.blockSignals(False)
        self.tabela.setEnabled(True)

    def ativar_botoes(self, ativar):
        self.btn_pesquisar.setEnabled(ativar)
        self.btn_atualizar.setEnabled(ativar)
        self.btn_deletar.setEnabled(ativar)
        
    def buscar(self, tipo, nome):
        elemento = self.janela.findChild(tipo, nome)

        if elemento is None:
            raise RuntimeError(
                f"Componente não encontrado: {nome}"
            )

        return elemento

    def configurar(self):
        self.senha.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.cadastro.setReadOnly(True)

        self.tabela.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.tabela.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

    def conectar_botoes(self):
        self.btn_inserir.clicked.connect(self.inserir)
        self.btn_pesquisar.clicked.connect(self.pesquisar)
        self.btn_atualizar.clicked.connect(self.atualizar)
        self.btn_deletar.clicked.connect(self.deletar)
        self.btn_resetar.clicked.connect(self.resetar)
    
    def resetar(self):
        self.estado_inicial()
        self.carregar_usuarios()

    def dados_formulario(self):
        return {
            "nome": self.nome.text().strip(),
            "email": self.email.text().strip(),
            "senha": self.senha.text(),
            "data_nascimento": self.nascimento.date().toPython(),
            "plano": self.plano.currentText()
        }

    def inserir(self):
        # PRIMEIRO CLIQUE
        if self.estado == "inicial":
            self.estado = "inserindo"

            self.ativar_campos(True)

            self.btn_pesquisar.setEnabled(False)
            self.btn_atualizar.setEnabled(False)
            self.btn_deletar.setEnabled(False)

            # Impedir seleção durante a inserção
            self.tabela.setEnabled(False)

            self.nome.setFocus()
            return

        # SEGUNDO CLIQUE
        if self.estado != "inserindo":
            return

        dados = self.dados_formulario()

        # Validar campos de texto
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
            return

        # Validar a data de nascimento
        if not self.nascimento.date().isValid():
            QMessageBox.warning(
                self.janela,
                "Data inválida",
                "Informe uma data de nascimento válida."
            )
            return

        # Preparar dados para o PostgreSQL
        parametros = (
            dados["nome"],
            dados["email"],
            dados["senha"],
            dados["data_nascimento"],
            dados["plano"]
        )

        try:
            self.usuario_db.inserir(parametros)

            QMessageBox.information(
                self.janela,
                "Sucesso",
                "Usuário cadastrado com sucesso!"
            )

            # Restaurar a tabela e a interface
            self.tabela.setEnabled(True)
            self.carregar_usuarios()
            self.estado_inicial()

        except Exception as erro:
            QMessageBox.critical(
                self.janela,
                "Erro ao inserir usuário",
                str(erro)
            )

    def pesquisar(self):
        # PRIMEIRO CLIQUE: iniciar pesquisa
        if self.estado == "inicial":
            self.estado = "pesquisando"

            # Limpar os campos
            self.nome.clear()
            self.email.clear()
            self.senha.clear()
            self.plano.setCurrentIndex(-1)

            # Bloquear todos os campos
            self.ativar_campos(False)

            # Liberar somente o nome
            self.nome.setEnabled(True)
            self.nome.setFocus()

            # Desativar os outros botões
            self.btn_inserir.setEnabled(False)
            self.btn_atualizar.setEnabled(False)
            self.btn_deletar.setEnabled(False)

            # Impedir seleção durante a pesquisa
            self.tabela.setEnabled(False)

            return

        # SEGUNDO CLIQUE: executar pesquisa
        if self.estado != "pesquisando":
            return

        nome = self.nome.text().strip()

        if not nome:
            QMessageBox.warning(
                self.janela,
                "Campo obrigatório",
                "Digite um nome para pesquisar!"
            )
            self.nome.setFocus()
            return

        try:
            # Pesquisa parcial, ignorando maiúsculas e minúsculas
            self.carregar_usuarios(
                "nome ILIKE %s",
                (f"%{nome}%",)
            )

            # Limpar e bloquear o campo de pesquisa
            self.nome.clear()
            self.ativar_campos(False)

            # Restaurar os botões
            self.btn_inserir.setEnabled(True)
            self.btn_pesquisar.setEnabled(True)
            self.btn_atualizar.setEnabled(False)
            self.btn_deletar.setEnabled(False)

            # Reativar a tabela
            self.tabela.setEnabled(True)

            # Permitir selecionar os resultados
            self.estado = "inicial"

        except Exception as erro:
            QMessageBox.critical(
                self.janela,
                "Erro na pesquisa",
                str(erro)
            )

    def atualizar(self):
        # PRIMEIRO CLIQUE
        if self.estado == "selecionado":
            self.estado = "atualizando"

            self.ativar_campos(True)

            # Data de cadastro não pode ser alterada
            self.cadastro.setEnabled(False)

            # Desativar os outros botões
            self.btn_inserir.setEnabled(False)
            self.btn_pesquisar.setEnabled(False)
            self.btn_deletar.setEnabled(False)

            # Bloquear seleção da tabela
            self.tabela.setEnabled(False)

            self.nome.setFocus()
            return

        # SEGUNDO CLIQUE
        if self.estado != "atualizando":
            return

        dados = self.dados_formulario()

        # Validar os campos obrigatórios
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
            return

        if not self.nascimento.date().isValid():
            QMessageBox.warning(
                self.janela,
                "Data inválida",
                "Informe uma data de nascimento válida."
            )
            return

        try:
            # Recuperar o usuário original
            usuarios = self.usuario_db.selecionar(
                "id_usuario = %s",
                (self.id_selecionado,)
            )

            if not usuarios:
                QMessageBox.warning(
                    self.janela,
                    "Usuário não encontrado",
                    "Este usuário não existe mais."
                )
                self.tabela.setEnabled(True)
                self.estado_inicial()
                self.carregar_usuarios()
                return

            usuario_original = usuarios[0]

            # Manter a senha anterior se nenhuma nova for digitada
            senha = dados["senha"]

            if not senha:
                senha = usuario_original[3]

            # Preservar a data original de cadastro
            data_cadastro = usuario_original[6]

            parametros = (
                dados["nome"],
                dados["email"],
                senha,
                dados["data_nascimento"],
                dados["plano"],
                data_cadastro,
                self.id_selecionado
            )

            # Atualizar no PostgreSQL
            self.usuario_db.atualizar(parametros)

            QMessageBox.information(
                self.janela,
                "Sucesso",
                "Usuário atualizado com sucesso!"
            )

            # Atualizar a tabela e restaurar a interface
            self.tabela.setEnabled(True)
            self.carregar_usuarios()
            self.estado_inicial()

        except Exception as erro:
            QMessageBox.critical(
                self.janela,
                "Erro ao atualizar usuário",
                str(erro)
            )

    def deletar(self):
        # Só permitir exclusão com um usuário selecionado
        if self.estado != "selecionado":
            return

        if self.id_selecionado is None:
            return

        # Guardar os dados do usuário selecionado
        id_usuario = self.id_selecionado
        nome_usuario = self.nome.text()

        # Desativar os outros botões
        self.btn_inserir.setEnabled(False)
        self.btn_pesquisar.setEnabled(False)
        self.btn_atualizar.setEnabled(False)
        self.btn_deletar.setEnabled(False)

        # Bloquear a tabela durante a confirmação
        self.tabela.setEnabled(False)

        self.estado = "excluindo"

        # Perguntar antes de excluir
        resposta = QMessageBox.question(
            self.janela,
            "Confirmar exclusão",
            f"Deseja deletar o usuário?\n\n"
            f"ID: {id_usuario}\n"
            f"Nome: {nome_usuario}",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        # Se o usuário escolher NÃO
        if resposta == QMessageBox.StandardButton.No:
            self.tabela.setEnabled(True)
            self.estado_inicial()
            return

        # Se o usuário escolher SIM
        try:
            self.usuario_db.deletar(
                "id_usuario = %s",
                (id_usuario,)
            )

            QMessageBox.information(
                self.janela,
                "Sucesso",
                "Usuário deletado com sucesso!"
            )

            # Restaurar a interface e atualizar a tabela
            self.tabela.setEnabled(True)
            self.estado_inicial()
            self.carregar_usuarios()

        except Exception as erro:
            QMessageBox.critical(
                self.janela,
                "Erro ao deletar usuário",
                str(erro)
            )

            self.tabela.setEnabled(True)
            self.estado_inicial()
            self.carregar_usuarios()
    
    def configurar_tabela(self):
        self.tabela.setColumnCount(6)

        self.tabela.setHorizontalHeaderLabels([
            "ID",
            "Nome",
            "E-mail",
            "Nascimento",
            "Plano",
            "Data de cadastro"
        ])

        # Selecionar a linha inteira
        self.tabela.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        # Permitir selecionar somente uma linha
        self.tabela.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        # Impedir edição diretamente na tabela
        self.tabela.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        # Alternar as cores das linhas
        self.tabela.setAlternatingRowColors(True)

        # Ajustar a largura das colunas
        self.tabela.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        # Impedir seleção inicial
        self.tabela.clearSelection()
    
    def carregar_usuarios(self, condicao=None, parametros=None):
        try:
            usuarios = self.usuario_db.selecionar(
                condicao,
                parametros
            )
            
            self.tabela.blockSignals(True)
            self.tabela.setRowCount(0)

            for usuario in usuarios:
                linha = self.tabela.rowCount()
                self.tabela.insertRow(linha)

                # Ignoramos a senha, que está no índice 3.
                dados = [
                    usuario[0],  # ID
                    usuario[1],  # Nome
                    usuario[2],  # E-mail
                    usuario[4],  # Nascimento
                    usuario[5],  # Plano
                    usuario[6]   # Cadastro
                ]

                for coluna, valor in enumerate(dados):
                    if valor is None:
                        texto = ""
                    elif hasattr(valor, "strftime"):
                        texto = valor.strftime("%d/%m/%Y")
                    else:
                        texto = str(valor)

                    item = QTableWidgetItem(texto)
                    self.tabela.setItem(linha, coluna, item)
                
                self.tabela.clearSelection()
                self.tabela.blockSignals(False)

        except Exception as erro:
            QMessageBox.critical(
                self.janela,
                "Erro no banco de dados",
                str(erro)
            )
            
    def selecionar_usuario(self):
        if self.estado not in ("inicial", "selecionado"):
            return
        
        linha = self.tabela.currentRow()

        if linha < 0:
            return

        # Recuperar o ID da linha selecionada
        self.id_selecionado = int(
            self.tabela.item(linha, 0).text()
        )

        # Consultar os dados completos do usuário
        usuarios = self.usuario_db.selecionar(
            "id_usuario = %s",
            (self.id_selecionado,)
        )

        if not usuarios:
            return

        usuario = usuarios[0]

        # Preencher os campos
        self.nome.setText(usuario[1])
        self.email.setText(usuario[2])

        # Não exibir a senha armazenada
        self.senha.clear()

        if usuario[4] is not None:
            self.nascimento.setDate(usuario[4])

        indice = self.plano.findText(usuario[5])

        if indice >= 0:
            self.plano.setCurrentIndex(indice)

        if usuario[6] is not None:
            self.cadastro.setDateTime(usuario[6])

        # Bloquear todos os campos
        self.ativar_campos(False)

        # Configurar os botões
        self.btn_inserir.setEnabled(False)
        self.btn_pesquisar.setEnabled(False)
        self.btn_atualizar.setEnabled(True)
        self.btn_deletar.setEnabled(True)

        self.estado = "selecionado"