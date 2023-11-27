from backend.geral.config import *
from backend.modelo.jogador import *
from backend.testes import testar
from backend.modelo.jogadorE import *

# inserindo a aplicação em um contexto :-/
with app.app_context():
    testar.run()