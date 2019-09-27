
class Marriage:
    """
    Represents a Marriage between 2 players
    """

    def __init__(self, h1: str, n1: int, h2: str, n2: int):
        self.h1: str = h1
        self.h2: str = h2
        self.n1: int = n1
        self.n2: int = n2

    def promote(self, house: str, number: int) -> None:
        """
        Checks if a marriage contains a player who needs promoted, and performs the promotion
        """

        if self.h1 == house and self.n1 > number:
            self.n1 -= 1
        elif self.h2 == house and self.n2 > number:
            self.n2 -= 1

    def player1(self) -> str:
        """
        Returns a string representation of the first player
        """
        return self.h1 + ' ' + str(self.n1)

    def player2(self) -> str:
        """
        Returns a string representation of the first player
        """
        return self.h2 + ' ' + str(self.n2)

    def contains(self, house, number) -> int:
        """
        Checks if a player is in this marriage, and returns which position the player is in if so
        """
        if self.h1 == house and self.n1 == number:
            return 1
        elif self.h2 == house and self.n2 == number:
            return 2
        return 0

    def __str__(self) -> str:
        """
        Returns string representation of this Marriage
        """
        return self.p1 + ':' + self.p2
