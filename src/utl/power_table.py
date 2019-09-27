import bot_helper.resources.spreadsheet as spreadsheet
from typing import List, Tuple


class PowerTable(spreadsheet.Spreadsheet):
    """
    Modifications to the Sheets Spreadsheet to include God Emperor Specific functionality
    """

    def __init__(self, *kwargs):

        super().__init__(*kwargs)
        self.next_row = self.find_empty_cell_in_column(
            'PowerLog', 'C', '3')

    def get_scores(self) -> List[str]:
        """
        Gets the list of scores in alphabetical order by house
        """
        return self.read_column('CurrentPower', 'B', '3', '11')

    def write_display(self) -> None:
        """
        Writes current scores to the display page, with an x in the ones place
        """
        def convert_score(score):
            """
            Changes the last digit of the score into an x
            """
            score = list(score)
            score[-1] = 'x'
            return ''.join(score)
        scores = self.get_scores()
        result = []
        for score in scores:
            result.append(convert_score(score))
        self.write_column('DisplayPower', 'C', '3', '11', result)

    def write_entry(self, house, score, author, time) -> str:
        """
        Writes the associated row in the Power table for a Power change
        """
        self.next_row = self.find_empty_cell_in_column(
            'PowerLog', 'C', '3')
        time = self._convert_time(time)
        data = [time, house, score, author]
        self.write_row(
            'PowerLog', 'B', 'E', str(self.next_row), data)
        self.next_row += 1
        return '{0} gets {1} power from {2}\n'.format(house, score, author)

    @staticmethod
    def _convert_time(time: str) -> str:
        """
        Converts the time from UTC to EST
        """

        time = time[11:-10]
        hours = time[:2]
        minutes = time[2:]
        hours = int(hours)
        hours -= 4
        if hours > 12:
            hours -= 12
        if hours <= 0:
            hours += 12
        hours = str(hours)
        return hours + minutes
