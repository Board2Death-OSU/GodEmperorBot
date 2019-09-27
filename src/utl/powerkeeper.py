import json
from typing import List, Tuple
import re
import utl.power_table as power_table
import utl.marriage_handler as marriage_handler


class PowerKeeper:

    def __init__(self, data_file: str, spreadsheet):

        # Open Data for House Information
        data_in = open(data_file, 'r')
        data: dict = json.loads(data_in.read())
        data_in.close()

        self.house_names: List[str] = data['house_names']
        self.houses: List[str] = data['houses']
        self.spreadsheet = spreadsheet
        self.scores = {}
        # Generate House Regex
        reg_ex_str = '('
        for house in self.houses:
            reg_ex_str += house + '|'
        reg_ex_str += 'ALL)'

        # Save Regex's
        self.house_regex = re.compile(reg_ex_str)
        self.score_regex = re.compile('\+?-?\d+')
        self.read_scores()

    def process_score_message(self, message: str, author: str, time: str) -> str:
        """
        Process a message to see if it invokes a PR change, and make the associated change.
        """

        # Check for Houses, and record them
        matches = re.findall(self.house_regex, message)
        houses = [str(match) for match in matches]

        # Check for Score changes
        match = re.search(self.score_regex, message)
        score_change = None
        if(match is not None):
            score_change = match.group()

        # Loop over Houses marked, and make the changes
        response = ''
        if score_change is not None and len(houses) > 0:
            for house in houses:
                self.scores[house] += int(score_change)
                response += self.spreadsheet.write_entry(
                    house, score_change, author, time)
        self.spreadsheet.write_display()
        self.write_scores()
        return response

    def read_scores(self) -> None:
        """
        Initializes score dictionary with the current scores in the spreadsheet
        """
        print('Reading scores')
        values = self.spreadsheet.read_column('ScoreTest', 'B', '4', '12')
        for house, value in zip(self.houses, values):
            self.scores[house] = int(value)

    def write_scores(self) -> None:
        """
        Saves current scores to the score table on the spreadsheet
        """
        print('Writing Scores')
        values = []
        for value in self.scores.values():
            values.append(value)
        self.spreadsheet.write_column('ScoreTest', 'B', '4', '12', values)

    def check_player_deaths(self, message: str, author: str, time: str) -> str:
        """
        Process a message to see if it involves a player death
        """
        if '!KILL' not in message:
            return ''

        # Search for associated arguments
        house = re.search(self.house_regex, message).group()
        matches = re.findall(r'\d', message)
        players = [int(str(match)) for match in matches]

        # Kill the associated players
        return self.kill_player(house, players, author, time)

    def display_scores(self) -> List[Tuple[str, str]]:
        """
        Constructs a display for the scores of each house with there scores
        """
        scores = self.spreadsheet.get_scores()
        response = ''
        for house, score in zip(self.house_names, scores):
            response += '{0}: {1}\n'.format(house, score)
        return response

    def kill_player(self, house: str, players: List[int], author: str, time: str) -> str:
        """
        Performs the necessary Power Calculations on a player death
        """

        # Gets the associated houses score
        scores = self.spreadsheet.get_scores()
        score = int(scores[self.houses.index(house)])

        # Calculate the loss and make it happen
        loss = int(score * len(players) / 5.0)
        msg = '{0} -{1}'.format(house, loss)
        self.process_score_message(msg, author, time)
        response = ''

        players.sort(reverse=True)

        # Construct a response for each player's death (for f sake)
        for player in players:

            # Check if the player is married
            partner = self.marriage_handler.in_marriage(house, player)
            if partner is not None:
                # Give the Spouse of the Dying Player Power
                mh = partner[0:3]
                mp = partner[4]
                msg = '{0} + {1}'.format(mh, int(loss / len(players)))
                self.process_score_message(msg, author, time)
                response += 'House {0} got {1} power from player {2} dying due to marriage\n'.format(
                    mh, int(loss / len(players)), player)

                # Death Ends a Marriage
                self.marriage_handler.remove_marriage(house, player)

            response += 'House {0} lost {1} power from player {2} dying\n'.format(
                house, int(loss / len(players)), player)

        # Promote Necessary Players after a death
        for player in players:
            self.marriage_handler.promote_team(house, player)
        return response

    def register_marriage_handler(self, handler):
        self.marriage_handler = handler


def get_inst(spreadsheet):
    return PowerKeeper('data/score_data.json', spreadsheet)
