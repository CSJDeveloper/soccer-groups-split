"""
This implementation is utilized to split players into different groups
based on their scores and behaviors.
"""

from collections import OrderedDict
from typing import List, Dict, Tuple
from typing import OrderedDict as OrderedDictType
import itertools
import datetime
import logging

import numpy as np


logging.basicConfig(level=logging.INFO)

# players waiting to be split
PlayersPool = (
    "CC",
    "C14",
    "Mark.Li",
    "Adam",
    "Chester",
    "HLJ",
    "Frank",
    "M.J",
    "Rifty",
    "YuYan",
    "ZhouYang",
    "Glass",
    "Fred",
    "Keven",
    "Torres",
    "37",
    "Leo",
    "Tiger",
)

# name of groups
GroupsName = ("A", "B")

# split groups before performing actual split
prior_groups_info = {"A": ["Mark.Li", "CC", "Frank"], "B": ["C14", "M.J"]}


def initialize_groups(groups_name: List[str]):
    """Initialize groups."""
    return OrderedDict({group_name: [] for group_name in groups_name})


def inject_prior_informaton(
    current_split_groups: OrderedDictType[str, List[str]],
    prior_split_info: Dict[str, List[str]],
):
    """Inject prior group split into the current split process."""
    current_split_groups.update(prior_split_info)
    return current_split_groups


def is_splitable_scenario(players_pool: Tuple[str], n_groups: int):
    """Whether current players can be split into `n_groups`."""
    n_players = len(players_pool)
    # players can be evenly split
    assert n_players % n_groups == 0


def print_split(current_groups_split: OrderedDictType[str, List[str]]):
    """Present the current groups split on the screen."""
    print_time_info = datetime.datetime.now()

    print_time_info = print_time_info.strftime("%Y-%m-%d %H:%M:%S")
    logging.info("  %s, the obtained groups split: \n", print_time_info)
    for group, players in current_groups_split.items():
        logging.info("  The group %s: %s \n", group, players)


def perform_groups_split(
    players_pool: Tuple[str], current_split_groups: OrderedDictType[str, List[str]]
):
    """Perform the group split."""
    n_groups = len(current_split_groups)
    n_players = len(players_pool)
    per_group_n_players = n_players // n_groups

    split_players = [players for _, players in current_split_groups.items()]
    split_players = list(itertools.chain(*split_players))

    left_players = [player for player in PlayersPool if player not in split_players]

    for group, playes in current_split_groups.items():
        group_n_players = len(playes)
        group_left_n_positions = per_group_n_players - group_n_players

        # randomly select `group_left_n_positions` from the left players pool
        selected_players = np.random.choice(
            left_players, size=group_left_n_positions, replace=False
        ).tolist()

        # added the selected players to the group split
        playes = playes + selected_players
        current_split_groups[group] = playes

        # remove the selected ones from left players pool
        left_players = [
            player for player in left_players if player not in selected_players
        ]

    return current_split_groups


def _main():
    # get how many groups are required to be split
    n_groups = len(GroupsName)

    # it is splitable
    is_splitable_scenario(players_pool=PlayersPool, n_groups=n_groups)

    split_groups = initialize_groups(groups_name=GroupsName)
    # update current split based on the prior split information
    split_groups = inject_prior_informaton(
        current_split_groups=split_groups, prior_split_info=prior_groups_info
    )

    # main process of
    # performing the group split
    split_groups = perform_groups_split(
        players_pool=PlayersPool, current_split_groups=split_groups
    )

    print_split(split_groups)


if __name__ == "__main__":
    _main()
