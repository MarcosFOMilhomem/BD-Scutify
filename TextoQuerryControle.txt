-- ============================================
-- BANCO DE DADOS: BD-Scutify
-- Apenas estrutura, sem dados
-- ============================================


-- ============================================
-- TABELA USUARIO
-- ============================================

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

CREATE SEQUENCE public.usuario_id_seq
    START WITH 1
    INCREMENT BY 1
    MINVALUE 1;

ALTER TABLE public.usuario
ALTER COLUMN id_usuario
SET DEFAULT nextval('public.usuario_id_seq');


-- ============================================
-- TABELA ARTISTA
-- ============================================

CREATE TABLE public.Artista (
    id_artista INTEGER NOT NULL,
    nome_artistico VARCHAR(150) NOT NULL,
    biografia TEXT NOT NULL,
    pais_origem VARCHAR(100) NOT NULL,
    foto VARCHAR(255) NOT NULL,
    PRIMARY KEY (id_artista)
);

CREATE SEQUENCE public.artista_id_seq
    START WITH 1
    INCREMENT BY 1
    MINVALUE 1;

ALTER TABLE public.artista
ALTER COLUMN id_artista
SET DEFAULT nextval('public.artista_id_seq');


-- ============================================
-- TABELA GENERO
-- ============================================

CREATE TABLE public.Genero (
    id_genero INTEGER NOT NULL,
    nome VARCHAR(80) NOT NULL UNIQUE,
    PRIMARY KEY (id_genero)
);

CREATE SEQUENCE public.genero_id_seq
    START WITH 1
    INCREMENT BY 1
    MINVALUE 1;

ALTER TABLE public.genero
ALTER COLUMN id_genero
SET DEFAULT nextval('public.genero_id_seq');


-- ============================================
-- TABELA ALBUM
-- ============================================

CREATE TABLE public.Album (
    id_album INTEGER NOT NULL,
    titulo VARCHAR(150) NOT NULL,
    data_lancamento DATE NOT NULL,
    capa VARCHAR(255) NOT NULL,
    id_artista INTEGER NOT NULL,

    PRIMARY KEY (id_album),

    FOREIGN KEY (id_artista)
        REFERENCES public.Artista(id_artista)
);

CREATE SEQUENCE public.album_id_seq
    START WITH 1
    INCREMENT BY 1
    MINVALUE 1;

ALTER TABLE public.album
ALTER COLUMN id_album
SET DEFAULT nextval('public.album_id_seq');


-- ============================================
-- TABELA MUSICA
-- ============================================

CREATE TABLE public.Musica (
    id_musica INTEGER NOT NULL,
    titulo VARCHAR(150) NOT NULL,
    duracao INTEGER NOT NULL,
    numero_faixa INTEGER NOT NULL,
    arquivo_audio VARCHAR(255) NOT NULL,
    id_album INTEGER NOT NULL,
    id_genero INTEGER NOT NULL,

    PRIMARY KEY (id_musica),

    FOREIGN KEY (id_album)
        REFERENCES public.Album(id_album),

    FOREIGN KEY (id_genero)
        REFERENCES public.Genero(id_genero)
);

CREATE SEQUENCE public.musica_id_seq
    START WITH 1
    INCREMENT BY 1
    MINVALUE 1;

ALTER TABLE public.musica
ALTER COLUMN id_musica
SET DEFAULT nextval('public.musica_id_seq');


-- ============================================
-- TABELA PLAYLIST
-- ============================================

CREATE TABLE public.Playlist (
    id_playlist INTEGER NOT NULL,
    nome VARCHAR(150) NOT NULL,
    descricao TEXT NOT NULL,
    visibilidade VARCHAR(20) NOT NULL,
    id_usuario INTEGER NOT NULL,

    PRIMARY KEY (id_playlist),

    FOREIGN KEY (id_usuario)
        REFERENCES public.Usuario(id_usuario)
);

CREATE SEQUENCE public.playlist_id_seq
    START WITH 1
    INCREMENT BY 1
    MINVALUE 1;

ALTER TABLE public.playlist
ALTER COLUMN id_playlist
SET DEFAULT nextval('public.playlist_id_seq');


-- ============================================
-- TABELA PLAYLIST_MUSICA
-- ============================================

CREATE TABLE public.Playlist_Musica (
    id_playlist INTEGER NOT NULL,
    id_musica INTEGER NOT NULL,
    ordem INTEGER NOT NULL,
    data_inclusao TIMESTAMP NOT NULL,

    PRIMARY KEY (id_playlist, id_musica),

    FOREIGN KEY (id_playlist)
        REFERENCES public.Playlist(id_playlist),

    FOREIGN KEY (id_musica)
        REFERENCES public.Musica(id_musica)
);


-- ============================================
-- TABELA HISTORICO_REPRODUCAO
-- ============================================

CREATE TABLE public.Historico_Reproducao (
    id_historico BIGINT NOT NULL,
    id_usuario INTEGER NOT NULL,
    id_musica INTEGER NOT NULL,
    data_hora TIMESTAMP NOT NULL,

    PRIMARY KEY (id_historico),

    FOREIGN KEY (id_usuario)
        REFERENCES public.Usuario(id_usuario),

    FOREIGN KEY (id_musica)
        REFERENCES public.Musica(id_musica)
);

CREATE SEQUENCE public.historico_reproducao_id_seq
    START WITH 1
    INCREMENT BY 1
    MINVALUE 1;

ALTER TABLE public.historico_reproducao
ALTER COLUMN id_historico
SET DEFAULT nextval('public.historico_reproducao_id_seq');