from PySide6.QtWidgets import (
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView
)


class CrudJanela:

    def __init__(self, janela, operacoes, nome_tabela,
                 colunas, indice_id=0):

        self.janela = janela
        self.operacoes = operacoes
        self.colunas = colunas
        self.indice_id = indice_id

        self.estado = "inicial"
        self.id_selecionado = None

        # Componentes comuns a todas as janelas
        self.tabela = self.buscar(
            QTableWidget, nome_tabela
        )

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

        self.configurar_tabela()
        self.conectar_botoes()

        self.tabela.itemSelectionChanged.connect(
            self.selecionar_registro
        )

    # COMPONENTES

    def buscar(self, tipo, nome):
        elemento = self.janela.findChild(tipo, nome)

        if elemento is None:
            raise RuntimeError(
                f"Componente não encontrado: {nome}"
            )

        return elemento

    def configurar_tabela(self):
        self.tabela.setColumnCount(len(self.colunas))
        self.tabela.setHorizontalHeaderLabels(
            self.colunas
        )

        self.tabela.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.tabela.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.tabela.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.tabela.setAlternatingRowColors(True)

        self.tabela.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.tabela.clearSelection()

    def conectar_botoes(self):
        self.btn_inserir.clicked.connect(self.inserir)
        self.btn_pesquisar.clicked.connect(self.pesquisar)
        self.btn_atualizar.clicked.connect(self.atualizar)
        self.btn_deletar.clicked.connect(self.deletar)
        self.btn_resetar.clicked.connect(self.resetar)

    # ESTADOS

    def estado_inicial(self):
        self.estado = "inicial"
        self.id_selecionado = None

        self.limpar_campos()
        self.ativar_campos(False)

        self.btn_inserir.setEnabled(True)
        self.btn_pesquisar.setEnabled(True)
        self.btn_atualizar.setEnabled(False)
        self.btn_deletar.setEnabled(False)

        self.tabela.blockSignals(True)
        self.tabela.clearSelection()
        self.tabela.blockSignals(False)

        self.tabela.setEnabled(True)

    def bloquear_botoes(self, excecao):
        botoes = {
            "inserir": self.btn_inserir,
            "pesquisar": self.btn_pesquisar,
            "atualizar": self.btn_atualizar,
            "deletar": self.btn_deletar
        }

        for nome, botao in botoes.items():
            botao.setEnabled(nome == excecao)

    def resetar(self):
        self.estado_inicial()
        self.carregar_registros()

    # TABELA

    def carregar_registros(
        self, condicao=None, parametros=None
    ):
        try:
            registros = self.operacoes.selecionar(
                condicao, parametros
            )

            self.tabela.blockSignals(True)
            self.tabela.setRowCount(0)

            for registro in registros:
                linha = self.tabela.rowCount()
                self.tabela.insertRow(linha)

                dados = self.dados_tabela(registro)

                for coluna, valor in enumerate(dados):
                    if valor is None:
                        texto = ""
                    elif hasattr(valor, "strftime"):
                        texto = valor.strftime("%d/%m/%Y")
                    else:
                        texto = str(valor)

                    self.tabela.setItem(
                        linha,
                        coluna,
                        QTableWidgetItem(texto)
                    )

            self.tabela.clearSelection()
            return True

        except Exception as erro:
            QMessageBox.critical(
                self.janela,
                "Erro no banco de dados",
                str(erro)
            )
            return False

        finally:
            self.tabela.blockSignals(False)

    def selecionar_registro(self):
        if self.estado not in (
            "inicial", "selecionado"
        ):
            return

        linha = self.tabela.currentRow()

        if linha < 0:
            return

        item = self.tabela.item(linha, 0)

        if item is None:
            return

        id_registro = int(item.text())

        try:
            registros = self.operacoes.selecionar(
                self.condicao_id(),
                self.parametros_id(id_registro)
            )

            if not registros:
                return

            self.id_selecionado = id_registro

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

    # INSERIR

    def inserir(self):
        if self.estado == "inicial":
            self.estado = "inserindo"

            self.ativar_campos(True)
            self.bloquear_botoes("inserir")
            self.tabela.setEnabled(False)

            self.focar_campo_principal()
            return

        if self.estado != "inserindo":
            return

        dados = self.dados_formulario()

        if not self.validar_insercao(dados):
            return

        try:
            self.operacoes.inserir(
                self.parametros_insercao(dados)
            )

            QMessageBox.information(
                self.janela,
                "Sucesso",
                "Registro inserido com sucesso!"
            )

            self.carregar_registros()
            self.estado_inicial()

        except Exception as erro:
            QMessageBox.critical(
                self.janela,
                "Erro ao inserir",
                str(erro)
            )

    # PESQUISAR

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

        texto = self.texto_pesquisa().strip()

        if not texto:
            QMessageBox.warning(
                self.janela,
                "Campo obrigatório",
                "Digite um valor para pesquisar!"
            )
            return

        condicao, parametros = (
            self.parametros_pesquisa(texto)
        )

        if self.carregar_registros(
            condicao, parametros
        ):
            self.estado_inicial()

    # ATUALIZAR

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
            registros = self.operacoes.selecionar(
                self.condicao_id(),
                self.parametros_id(
                    self.id_selecionado
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

            parametros = self.parametros_atualizacao(
                dados, registros[0]
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

    # DELETAR

    def deletar(self):
        if self.estado != "selecionado":
            return

        if self.id_selecionado is None:
            return

        id_registro = self.id_selecionado
        descricao = self.descricao_registro()

        self.estado = "excluindo"
        self.bloquear_botoes(None)
        self.tabela.setEnabled(False)

        resposta = QMessageBox.question(
            self.janela,
            "Confirmar exclusão",
            f"Deseja deletar este registro?\n\n"
            f"ID: {id_registro}\n"
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
                self.parametros_id(id_registro)
            )

            QMessageBox.information(
                self.janela,
                "Sucesso",
                "Registro deletado com sucesso!"
            )

        except Exception as erro:
            QMessageBox.critical(
                self.janela,
                "Erro ao deletar",
                str(erro)
            )

        finally:
            self.estado_inicial()
            self.carregar_registros()

    # MÉTODOS ESPECÍFICOS DE CADA JANELA

    def limpar_campos(self):
        raise NotImplementedError

    def ativar_campos(self, ativar):
        raise NotImplementedError

    def dados_formulario(self):
        raise NotImplementedError

    def dados_tabela(self, registro):
        raise NotImplementedError

    def preencher_formulario(self, registro):
        raise NotImplementedError

    def validar_insercao(self, dados):
        raise NotImplementedError

    def validar_atualizacao(self, dados):
        raise NotImplementedError

    def parametros_insercao(self, dados):
        raise NotImplementedError

    def parametros_atualizacao(
        self, dados, registro_original
    ):
        raise NotImplementedError

    def condicao_id(self):
        raise NotImplementedError

    def parametros_id(self, id_registro):
        return (id_registro,)

    def ativar_campo_pesquisa(self):
        raise NotImplementedError

    def texto_pesquisa(self):
        raise NotImplementedError

    def parametros_pesquisa(self, texto):
        raise NotImplementedError

    def descricao_registro(self):
        raise NotImplementedError

    def focar_campo_principal(self):
        raise NotImplementedError