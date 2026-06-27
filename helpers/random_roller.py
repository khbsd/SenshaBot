import re
import secrets
from enum import Enum

test_msg = "1d4, 3d7,2d8 5d4"


TOTAL_STRINGS_POSITIVE = [
    "Omg you rolled a result? Fucking wild, good job!",
    "I've never rolled higher than a result before!!",
    "Damn, if your DM lets you keep result as the roll, you're set!",
    "I wish I had rolled a result in my last session...",
    "If I say what I had to do to get result as my last roll, I'd be executed.",
]

TOTAL_STRINGS_NEGATIVE = [
    "You got a result. Bad roll? Nah, bad *you*.",
    "You rolled a result. Good for you or whatever.",
    "I could roll higher than a result in my sleep. Wow.",
    "result? I would beg on my knees for a re-roll.",
    "I'd rather be on fucking twitter than keep a result.",
]


# i use this because it allows for:
# 1) a consistent name scheme source of truth
# 2) intuitive values to iterate through for indices,
# ie dice[DieData.DICE.value] for the zeroth index
# 
# its clunky for the regex but it helps keep things consistent
class DieData(Enum):
    DICE = 0
    AMOUNT = 1
    SIDES = 2


# this is named after dice but coins are dice
# so we will use it for the coinflip command
# too. i will not be elaborating
class Die:
    def __init__(self, data: re.Match):
        self.name = str(data.group(DieData.DICE.name.lower()))
        self.amount = int(data.group(DieData.AMOUNT.name.lower()))
        self.sides = int(data.group(DieData.SIDES.name.lower()))

    def roll(self) -> int:
        total = 0
        for _ in range(0, self.amount):
            total += secrets.randbelow(self.sides) + 1

        return total


class roller:
    def __init__(self, is_sassy: bool | None = False) -> None:
        self.dice_pattern = re.compile(
            rf"(?P<{DieData.DICE.name.lower()}>(?P<{DieData.AMOUNT.name.lower()}>\d)d(?P<{DieData.SIDES.name.lower()}>\d))[\s,]*"
        )
        self.dice: list = []
        self.roll_totals: list = []
        self.sassy: bool | None = is_sassy

    def get_dice(self, msg: str) -> None:
        m = self.dice_pattern.finditer(msg)
        if m:
            for die in m:
                self.dice.append(Die(die))

    def get_roll_totals(self) -> None:
        for die in self.dice:
            print(die.name)
            self.roll_totals.append(die.roll())

    def get_formatted_total_strings(self) -> str:
        total_string = ""
        die_count = 0
        for total in self.roll_totals:
            total_string += f"Roll {die_count + 1}: {total}"
            die = self.dice[die_count]
            if self.sassy:
                list = []
                if total > (die.amount * die.sides) * 0.667:
                    list = TOTAL_STRINGS_POSITIVE
                else:
                    list = TOTAL_STRINGS_NEGATIVE
                    
                string = list[secrets.randbelow(len(list))]
                string = re.sub("result", str(total), string)
                
                total_string += "\n" + string
                
            if die_count < len(self.roll_totals) - 1:
                total_string += "\n"
                
            die_count += 1

        return total_string


r = roller(is_sassy=True)
r.get_dice(test_msg)
r.get_roll_totals()
print(r.get_formatted_total_strings())
