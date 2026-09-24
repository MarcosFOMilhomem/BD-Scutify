from pathlib import Path

from PySide6.QtCore import QObject
from PySide6.QtGui import QAction
from PySide6.QtUiTools import QUiLoader
from src.Interface.janelas.usuario_janela import UsuarioJanela

class GerenciadorJanelas(QObject):

    def __init__(self):
        super().__init__()

        self.pasta = Path(__file__).resolve().parent
        self.loader = QUiLoader()

        # Arquivos das janelas
        self.arquivos = {
            "inicio": "MainJanela.ui",
            #"albuns": "AlbumJanela.ui",

            # "artistas": "ArtistaJanela.ui",
            # "generos": "GeneroJanela.ui",
            # "historico": "HistoricoJanela.ui",
            # "musicas": "MusicaJanela.ui",
            # "musicas_playlist": "PlaylistMusicaJanela.ui",
            # "playlists": "PlaylistJanela.ui",
            "usuarios": "UsuarioJanela.ui"
        }

        self.janelas = {}
        self.atual = None

        # Carregar janelas
        for nome, arquivo in self.arquivos.items():
            caminho = self.pasta / arquivo

            print(f"Carregando: {caminho}")
            print(f"Arquivo existe: {caminho.exists()}")

            janela = self.loader.load(str(caminho))

            if janela is None:
                raise RuntimeError(
                    f"Erro ao carregar {arquivo}: "
                    f"{self.loader.errorString()}"
                )

            if janela is None:
                raise RuntimeError(
                    f"Erro ao carregar {arquivo}"
                )

            self.janelas[nome] = janela
        self.usuario = UsuarioJanela(
            self.janelas["usuarios"]
        )
        self.conectar_menus()

    def conectar(self, origem, acao, destino):
        janela = self.janelas[origem]

        elemento = janela.findChild(QAction, acao)

        if elemento is None:
            raise RuntimeError(
                f"Ação {acao} não encontrada em {origem}!"
            )

        elemento.triggered.connect(
            lambda: self.abrir(destino)
        )

    def conectar_menus(self):

        # Menu da janela principal
        # self.conectar("inicio", "actionAlbuns", "albuns")
        # self.conectar("inicio", "actionArtistas", "artistas")
        # self.conectar("inicio", "actionGeneros", "generos")
        # self.conectar("inicio", "actionHistorico", "historico")
        # self.conectar("inicio", "actionMusicas", "musicas")
        # self.conectar("inicio", "actionMusicasPlaylist", "musicas_playlist")
        # self.conectar("inicio", "actionPlaylists", "playlists")
        self.conectar("inicio", "actionUsuarios", "usuarios")

        # Retorno para a janela principal
        # self.conectar("albuns", "actionInicio", "inicio")

        # self.conectar("artistas", "actionInicio", "inicio")
        # self.conectar("generos", "actionInicio", "inicio")
        # self.conectar("historico", "actionInicio", "inicio")
        # self.conectar("musicas", "actionInicio", "inicio")
        # self.conectar("musicas_playlist", "actionInicio", "inicio")
        # self.conectar("playlists", "actionInicio", "inicio")
        self.conectar("usuarios", "actionInicio", "inicio")

    def abrir(self, nome):
        proxima = self.janelas[nome]

        proxima.show()

        if self.atual is not None and self.atual != proxima:
            self.atual.hide()

        self.atual = proxima