from src.Operacoes.usuario import Usuario


usuario = Usuario()

usuario.inserir((
    "João",
    "joao@email.com",
    "123456",
    "2005-05-15",
    "Premium"
))

usuario.inserir((
    "Maria",
    "maria@email.com",
    "654321",
    "2004-10-20",
    "Gratuito"
))

print("\n--- TODOS OS USUÁRIOS ---")

usuarios = usuario.selecionar()

for u in usuarios:
    print(u)

print("\n--- PESQUISA POR NOME ---")

usuarios = usuario.selecionar(
    "nome ILIKE %s",
    ("%João%",)
)

for u in usuarios:
    print(u)

print("\n--- ATUALIZANDO JOÃO ---")

id_usuario = usuarios[0][0]
data_cadastro = usuarios[0][6]

usuario.atualizar((
    "João Atualizado",
    "joao.novo@email.com",
    "654321",
    "2005-05-15",
    "Premium",
    data_cadastro,
    id_usuario
))


usuarios = usuario.selecionar(
    "id_usuario = %s",
    (id_usuario,)
)

for u in usuarios:
    print(u)

print("\n--- DELETANDO MARIA ---")

usuarios = usuario.selecionar(
    "email = %s",
    ("maria@email.com",)
)

id_maria = usuarios[0][0]

usuario.deletar(
    "id_usuario = %s",
    (id_maria,)
)

print("\n--- USUÁRIOS FINAIS ---")

usuarios = usuario.selecionar()

for u in usuarios:
    print(u)
