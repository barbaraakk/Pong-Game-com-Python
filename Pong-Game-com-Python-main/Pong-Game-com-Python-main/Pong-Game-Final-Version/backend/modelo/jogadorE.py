from backend.geral.config import *

class JogadorE(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # posições do jogo
    pontos = db.Column(db.Integer)

    def __str__(self):
        return f'Pontuação: {self.pontos}'
    
    # expressao da classe no formato json
    def json(self):
        return {
            "id": self.id,
            "pontos": self.pontos
        }