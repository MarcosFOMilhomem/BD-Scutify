from pathlib import Path

from PySide6.QtCore import QObject
from PySide6.QtGui import QAction
from PySide6.QtUiTools import QUiLoader

from src.Interface.janelas.usuario_janela import UsuarioJanela
from src.Interface.janelas.artista_janela import ArtistaJanela
from src.Interface.janelas.genero_janela import GeneroJanela
from src.Interface.janelas.playlist_janela import PlaylistJanela
from src.Interface.janelas.album_janela import AlbumJanela
from src.Interface.janelas.musica_janela import MusicaJanela
from src.Interface.janelas.playlist_musica_janela import PlaylistMusicaJanela
from src.Interface.janelas.historico_reproducao_janela import HistoricoReproducaoJanela

class GerenciadorJanelas(QObject):

    def __init__(self):
        super().__init__()

        self.pasta = Path(__file__).resolve().parent
        self.loader = QUiLoader()

        # Arquivos das janelas
        self.arquivos = {
            "inicio": "MainJanela.ui",
            "artistas": "ArtistaJanela.ui",
            "usuarios": "UsuarioJanela.ui",
            "generos": "GeneroJanela.ui",
            "playlists": "PlaylistJanela.ui",
            "albuns": "AlbumJanela.ui",
            "musicas": "MusicaJanela.ui",
            "musicas_playlist": "Playlist_MusicaJanela.ui",
            "historico": "HistoricoJanela.ui",
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

            self.janelas[nome] = janela

        # Inicializar as classes específicas
        self.usuario = UsuarioJanela(
            self.janelas["usuarios"]
        )
        self.artista = ArtistaJanela(
            self.janelas["artistas"]
        )
        self.genero = GeneroJanela(
            self.janelas["generos"]
        )
        self.playlist = PlaylistJanela(
            self.janelas["playlists"]
        )
        self.album = AlbumJanela(
            self.janelas["albuns"]
        )
        self.musica = MusicaJanela(
            self.janelas["musicas"]
        )
        self.playlist_musica = PlaylistMusicaJanela(
            self.janelas["musicas_playlist"]
        )
        self.historico = HistoricoReproducaoJanela(
            self.janelas["historico"]
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
        self.conectar(
            "inicio", "actionArtistas", "artistas"
        )
        self.conectar(
            "inicio", "actionUsuarios", "usuarios"
        )
        self.conectar(
            "inicio", "actionGeneros", "generos"
        )
        self.conectar(
            "inicio", "actionPlaylists", "playlists"
        )
        self.conectar(
            "inicio", "actionAlbuns", "albuns"
        )
        self.conectar(
            "inicio", "actionMusicas", "musicas"
        )
        self.conectar(
            "inicio", "actionMusicasPlaylist", "musicas_playlist"
        )
        self.conectar(
            "inicio","actionHistoricoReproducao","historico"
        )

        # Retorno para a janela principal
        self.conectar(
            "artistas", "actionInicio", "inicio"
        )
        self.conectar(
            "usuarios", "actionInicio", "inicio"
        )
        self.conectar(
            "generos", "actionInicio", "inicio"
        )
        self.conectar(
            "playlists", "actionInicio", "inicio"
        )
        self.conectar(
            "albuns", "actionInicio", "inicio"
        )
        self.conectar(
            "musicas", "actionInicio", "inicio"
        )
        self.conectar(
            "musicas_playlist", "actionInicio", "inicio"
        )
        self.conectar(
            "historico","actionInicio","inicio"
        )
            
    
    def abrir(self, nome):
        # Atualiza as opções das chaves estrangeiras
        # sempre que a janela for aberta.
        atualizadores = {
            "playlists": self.playlist.carregar_usuarios,
            "albuns": self.album.carregar_artistas,
            "musicas": lambda: (
                self.musica.carregar_albuns(),
                self.musica.carregar_generos()
            ),
            "musicas_playlist": lambda: (
                self.playlist_musica.carregar_playlists(),
                self.playlist_musica.carregar_musicas()
            ),
            "historico": lambda: (
                self.historico.carregar_usuarios(),
                self.historico.carregar_musicas()
            )
        }

        if nome in atualizadores:
            atualizadores[nome]()

        proxima = self.janelas[nome]
        proxima.show()

        if self.atual is not None and self.atual != proxima:
            self.atual.hide()

        self.atual = proxima

