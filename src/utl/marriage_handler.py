import re
from typing import Tuple, List
import utl.power_table as power_table
from utl.marriage import Marriage


class MarriageHandler:

    def __init__(self, hlist, ptable):
        """
        Initializes a new Marriage Handler.
        """
        self.houses = hlist
        self.spreadsheet = ptable
        self.marriages = set()
        reg_ex_str = '('
        for house in self.houses:
            reg_ex_str += house + '|'

        # Save Regex's
        self.player_regex = re.compile(reg_ex_str[0:-1] + ')\s?(1|2|3|4|5)')
        self.read_marriages()

    def parse_message(self, message: str, channel_name: str) -> str:
        """
        Checks if a message is a marriage command, and performs the appropriate operations
        """
        if '!MARRY' in message.upper() and channel_name == 'logistics':
            matches = re.findall(self.player_regex, message)
            players = [match for match in matches]
            if len(players) < 2:
                return None
            return self.handle_marriage(players[0], players[1])
        elif '!MARRIAGE' in message.upper():
            return self.list_marriages()

    def handle_marriage(self, p1: str, p2: str) -> str:
        """
        Updates Marriage Sheet with a new marriage
        """

        marriage = Marriage(p1[0], p1[1], p2[0], p2[1])

        self.marriages.add(marriage)
        self.write_marriages()
        message = 'Successfully married {0} and {1}'.format(
            marriage.player1(), marriage.player2())
        print(message)
        return message

    def list_marriages(self) -> str:
        """
        Returns a response listing each marriage
        """
        response = 'Marriages:\n'
        for marriage in self.marriages:
            response += '{}\n'.format(marriage)
        print(response)
        return response

    def in_marriage(self, house: str, number: int) -> Tuple[str, str]:
        for marriage in self.marriages:
            if marriage.contains(house, number) == 1:
                return marriage.player2()
            elif marriage.contains(house, number) == 2:
                return marriage.player1()
        return None

    def remove_marriage(self, house: str, number: int) -> None:
        remove = None
        for marriage in self.marriages:
            if marriage.contains(house, number) > 0:
                remove = marriage
                print('Removing Marriage between {0} and {1}'.format(
                    marriage.player1(), marriage.player2()))

        self.marriages.remove(remove)
        self.write_marriages()

    def read_marriages(self):
        print('Reading from Marriage Log')
        values = self.spreadsheet.read_block('Marriage Log', 'B', 'C', '3', '')
        self.marriages = set()
        for row in values:
            if(len(row) > 1):
                if(len(row[0]) > 4 and len(row[1]) > 4):
                    marriage = Marriage(row[0][0:3], int(
                        row[0][4]), row[1][0:3], int(row[1][4]))
                    self.marriages.add(marriage)

    def write_marriages(self):
        print('Writing to Marriage Log')
        values = []
        for marriage in self.marriages:
            values.append([marriage.player1(), marriage.player2()])
        values.append(['', ''])
        self.spreadsheet.write_block(
            'Marriage Log', 'B', 'C', '3', '', values)

    def promote_team(self, house: str, number: int) -> None:

        for marriage in self.marriages:
            marriage.promote(house, number)


def get_callback_function(houses: List[str], powertable) -> Tuple[callable, List[MarriageHandler]]:
    """
    Creates a new marriage handler, and returns a standard callback function
    """
    handler = MarriageHandler(houses, powertable)

    def marriage_callback(message, handler):
        """
        A simple callback function for marriage handling
        """
        response = handler.parse_message(message.content, str(message.channel))
        return (response, message.channel)

    return (marriage_callback, [handler])
