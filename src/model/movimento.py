class Movimento:

    def __init__(self, inicial, final):
        self.inicial = inicial
        self.final = final

    def __str__(self):
        string = ''
        string += f'({self.inicial.coluna}, {self.inicial.linha})'
        string += f' -> ({self.final.coluna}, {self.final.linha})'
        return string

    def __eq__(self, other):
        return self.inicial == other.inicial and self.final == other.final