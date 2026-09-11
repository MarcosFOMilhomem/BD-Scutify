CREATE TABLE public.Usuario (
    id_usuario INTEGER NOT NULL,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    data_nascimento DATE NOT NULL,
    plano VARCHAR(30) NOT NULL,
    data_cadastro TIMESTAMP NOT NULL,

    PRIMARY KEY (id_usuario)
);


CREATE TABLE public.Artista (
    id_artista INTEGER NOT NULL,
    nome_artistico VARCHAR(150) NOT NULL,
    biografia TEXT NOT NULL,
    pais_origem VARCHAR(100) NOT NULL,
    foto VARCHAR(255) NOT NULL,

    PRIMARY KEY (id_artista)
);


CREATE TABLE public.Genero (
    id_genero INTEGER NOT NULL,
    nome VARCHAR(80) NOT NULL UNIQUE,

    PRIMARY KEY (id_genero)
);


CREATE TABLE public.Album (
    id_album INTEGER NOT NULL,
    titulo VARCHAR(150) NOT NULL,
    data_lancamento DATE NOT NULL,
    capa VARCHAR(255) NOT NULL,
    id_artista INTEGER NOT NULL,

    PRIMARY KEY (id_album),

    FOREIGN KEY (id_artista) REFERENCES Artista(id_artista)
);


CREATE TABLE public.Musica (
    id_musica INTEGER NOT NULL,
    titulo VARCHAR(150) NOT NULL,
    duracao INTEGER NOT NULL,
    numero_faixa INTEGER NOT NULL,
    arquivo_audio VARCHAR(255) NOT NULL,
    id_album INTEGER NOT NULL,
    id_genero INTEGER NOT NULL,

    PRIMARY KEY (id_musica),

    FOREIGN KEY (id_album) REFERENCES Album(id_album),

    FOREIGN KEY (id_genero) REFERENCES Genero(id_genero)
);


CREATE TABLE public.Playlist (
    id_playlist INTEGER NOT NULL,
    nome VARCHAR(150) NOT NULL,
    descricao TEXT NOT NULL,
    visibilidade VARCHAR(20) NOT NULL,
    id_usuario INTEGER NOT NULL,

    PRIMARY KEY (id_playlist),

    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);


CREATE TABLE public.Playlist_Musica (
    id_playlist INTEGER NOT NULL,
    id_musica INTEGER NOT NULL,
    ordem INTEGER NOT NULL,
    data_inclusao TIMESTAMP NOT NULL,

    PRIMARY KEY (id_playlist, id_musica),

    FOREIGN KEY (id_playlist) REFERENCES Playlist(id_playlist),

    FOREIGN KEY (id_musica) REFERENCES Musica(id_musica)
);


CREATE TABLE public.Historico_Reproducao (
    id_historico BIGINT NOT NULL,
    id_usuario INTEGER NOT NULL,
    id_musica INTEGER NOT NULL,
    data_hora TIMESTAMP NOT NULL,

    PRIMARY KEY (id_historico),

    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),

    FOREIGN KEY (id_musica) REFERENCES Musica(id_musica)
);