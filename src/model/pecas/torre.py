from model.peca import Peca


class Torre(Peca):

    def __init__(self, cor):
        super().__init__('torre', cor, 5.0)