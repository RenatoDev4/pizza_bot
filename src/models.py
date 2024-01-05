class User:
    def __init__(self, nome: str, nickname: str) -> None:
        """
        Initializes the object with the given nome and nickname.

        Args:
            nome (str): The name of the object.
            nickname (str): The nickname of the object.

        Returns:
            None
        """
        self.nome = nome
        self.nickname = nickname

    @classmethod
    def create_user(cls, name: str, nickname: str) -> "User":
        """
        Create a new User instance.

        Args:
            name (str): The name of the user.
            nickname (str): The nickname of the user.

        Returns:
            User: The newly created User instance.
        """
        return cls(name, nickname)
