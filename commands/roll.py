import inspect
import json
import random
import re
import sys
import time
from datetime import datetime, timedelta

import discord
from discord import app_commands

from bot import ModerationBot
from commands.ban import TempBanCommand
from commands.base import Command
from commands.dm import DMCommand
from commands.mute import timeoutCommand
from helpers.embed_builder import EmbedBuilder
from helpers.emoji_parser import parse_emotes
from helpers.misc_functions import (
    author_is_mod,
    is_integer,
    is_valid_duration,
    parse_duration,
)
from helpers.random_roller import roller
from helpers.userid_parser import parse_userid


class RollCommand(Command):
    def __init__(self, client_instance: ModerationBot) -> None:
        self.cmd = None
        self.client = client_instance

    def get_slash_commands(self) -> list:
        @app_commands.command(name="roll", description="roll dice")
        async def roll_command(interaction: discord.Interaction, die: str) -> None:
            r: roller = roller(True)
            r.get_dice(die)
            r.get_roll_totals()
            await interaction.response.send_message(
                f"yoooooooo im like. a wip lol but heres your totals:\n{r.get_formatted_total_string()}",
                ephemeral=True,
            )

        return [roll_command]


classes = [("RollCommand", RollCommand)]

"""
class RollCommandBak(Command):
    def __init__(self, client_instance: ModerationBot) -> None:
        self.cmd = None
        self.client = client_instance
        self.storage = client_instance.storage
        self.usage = f"Usage: {self.client.prefix}roll"
        self.roll_counter = 0  # Counter to track the number of rolls

    def get_custom_emoji(self, name):
        #Fetch the bot's custom emoji by name.
        for emoji in self.client.emojis:
            if emoji.name == name:
                return str(emoji)
        return f":{name}:"  # Fallback in case the emoji is not found

    def get_forced_roll(self):
        #Force a roll of 1 or 20 based on a condition.
        # Alternate between forcing 1 or 20
        return 1 if self.roll_counter % 2 == 0 else 20

    def d20_roll(self):
        # Every 10th roll, force a 1 or 20
        if self.roll_counter % 10 == 0:
            return self.get_forced_roll()
        return random.randint(1, 20)

    def custom_roll(self, num_dice, dice_size):
        rolls = [random.randint(1, dice_size) for _ in range(num_dice)]
        return sum(rolls)

    def get_slash_commands(self) -> list:
        @app_commands.command(name="roll", description="roll some dice")
        @app_commands.describe(dice="roll a die, in XdY format (ie, 2d20)")
        @app_commands.describe(coin="flip a coin; takes no arguments")
        async def roll_command(
            interaction: discord.Interaction,
            dice: str | None = None,
            sassy: bool | None = False,
        ) -> None:
            response = ""
            roll = None
            r = roller(is_sassy=sassy)

            r.get_dice(str(dice))

            if not r.dice:
                await interaction.response.send_message("Use XdY Format! (2d6, 1d20)")
                return

            for die in r.dice:
                if die.amount == 0 and die.sides == 0:
                    await interaction.response.send_message(
                        f"{die.name}: Why are you making me do this?"
                    )
                    return
                if die.amount == 0:
                    await interaction.response.send_message(f"{die.name} Just.. why?")
                    return
                if die.amount < 0:
                    await interaction.response.send_message(
                        f"{die.name}: Are you trying make reality collapse into itself, rolling negative amount of dice?!"
                    )
                    return
                elif die.amount > 100:
                    await interaction.response.send_message(
                        f"{die.name}: These are far too many dice you are trying to roll here, 100 at maximum should suffice!"
                    )
                    return
                elif die.sides <= 0:
                    await interaction.response.send_message(
                        f"{die.name}: I don't know what you are rolling but its not dice."
                    )
                    return
                elif die.sides == 1:
                    await interaction.response.send_message(
                        f"{die.name}: Might as well just count how many dice you have."
                    )
                    return
                elif die.sides > 1000:
                    await interaction.response.send_message(
                        f"{die.name}: Anything above 1000 sides are far too much. Those are real chonkers, some real badonkas!"
                    )
                    return

            roll = self.custom_roll(len(r.dice), dice_size)

            # reset counter on natural crits to avoid back-to-back extremes by forced rolls
            if roll == 1 or roll == 20:
                self.roll_counter = 1

            user_id = interaction.user.id

            # Predefined rolls for specific users
            if user_id == 504374276334288896:
                roll = 1
                response = f"{self.get_custom_emoji('HaPoint')} you rolled a 1, critical simosas fail!"
            elif user_id == 219060288106921985:
                roll = 20
                response = f"{self.get_custom_emoji('pogcat')} Critical success! You dropped this Snesh: {self.get_custom_emoji('crown')}"
            elif user_id == 722476157714563073:
                roll = 1
                response = (
                    f"{self.get_custom_emoji('satanstarege')} you rolled a 1, loser!"
                )

            if not response and not coin:
                # Get the emotes
                PointNLaugh = self.get_custom_emoji("PointNLaugh")
                pogowo = self.get_custom_emoji("pogowo")
                happynathyjump = self.get_custom_emoji("happynathyjump")
                hap = self.get_custom_emoji("hap")
                HaPoint = self.get_custom_emoji("HaPoint")
                fishap = self.get_custom_emoji("fishap")
                hapwiggle = self.get_custom_emoji("hapwiggle")
                pogcat = self.get_custom_emoji("pogcat")
                crown = self.get_custom_emoji("crown")
                pausecham = self.get_custom_emoji("pausecham")

                # Different outcomes based on the roll
                max_roll = len(r.dice) * dice_size if dice else 20

                if roll == 69:
                    response = "Nice"
                elif roll == 420:
                    response = "Blaze it!"
                elif roll > 9000:
                    response = f"Its over 9000!"
                elif roll == 1:
                    response = f"{PointNLaugh} you rolled a 1, critical fail!"
                elif roll == 20 and not dice:
                    response = f"{pogowo} Critical success! You dropped this: {crown}"
                elif roll == max_roll:
                    response = (
                        f"{pogowo} Perfect roll! You hit the absolute limit: {crown}"
                    )
                else:
                    percent = roll / max_roll

                    if percent <= 0.10:
                        response = f"{PointNLaugh} Oof."
                    elif percent <= 0.30:
                        response = f"{hap} rough, not your best moment."
                    elif percent < 0.50:
                        response = (
                            f"{pausecham} could've gone worse, but probably better."
                        )
                    elif percent == 0.50:
                        response = f"Straight center. I have no strong feelings one way or the other."
                    elif percent <= 0.70:
                        response = f"{happynathyjump} not too bad! Probably passed that ability check!"
                    elif percent <= 0.90:
                        response = f"{pogowo} strong roll!"
                    else:
                        response = f"{crown} nice roll, almost had it!"

                await interaction.response.send_message(response)

        return [roll_command]
"""
