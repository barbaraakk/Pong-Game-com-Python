from backend.geral.config import *
from backend.modelo.jogador import *
from backend.modelo.jogadorE import *

# inserindo a aplicação em um contexto :-/
with app.app_context():

    if os.path.exists(arquivobd):
        os.remove(arquivobd)

    # criar tabelas
    db.create_all()

    print("Banco de dados e tabelas criadas")