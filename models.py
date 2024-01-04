class User:
    def __init__(self, nome, nickname):
        self.nome = nome
        self.nickname = nickname

    @classmethod
    def create_user(cls, name, nickname):
        return cls(name, nickname)
