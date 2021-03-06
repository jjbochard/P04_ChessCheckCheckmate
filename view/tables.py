from tabulate import tabulate
from tinydb import TinyDB


class TablesView:
    def __init__(
        self,
        tournament_table=TinyDB("db.json").table("tournament"),
        player_table=TinyDB("db.json").table("player"),
        round_table=TinyDB("db.json").table("round"),
        match_table=TinyDB("db.json").table("match"),
    ):
        self.tournament_table = tournament_table
        self.player_table = player_table
        self.round_table = round_table
        self.match_table = match_table

    def players_by_ranking(self, players):
        """ """
        players = sorted(players)
        print(
            tabulate(
                players,
                headers=[
                    "Ranking",
                    "Id",
                    "First name",
                    "Last name",
                    "Date of birth",
                    "Gender",
                ],
                tablefmt="fancy_grid",
            )
        )

    def players_by_alphabetical_order(self):
        """ """
        players = [
            [
                player["last_name"],
                player["first_name"],
                player["ranking"],
                player["date_of_birth"],
                player["gender"],
            ]
            for player in self.player_table
        ]
        players = sorted(players, key=lambda k: (k[0], k[1]))
        print(
            tabulate(
                players,
                headers=[
                    "First name",
                    "Last name",
                    "Ranking",
                    "Date of birth",
                    "Gender",
                ],
                tablefmt="fancy_grid",
            )
        )

    def players_by_id(self):
        """ """
        players = [
            [
                player.doc_id,
                player["last_name"],
                player["first_name"],
                player["ranking"],
                player["date_of_birth"],
                player["gender"],
            ]
            for player in self.player_table
        ]
        players = sorted(players)
        print(
            tabulate(
                players,
                headers=[
                    "Id",
                    "First name",
                    "Last name",
                    "Ranking",
                    "Date of birth",
                    "Gender",
                ],
                tablefmt="fancy_grid",
            )
        )

    def players_by_ranking_of_tournament(self, choice_tournament):
        choose_tournament = self.tournament_table.all()[int(choice_tournament) - 1]
        players_of_tournament = [
            self.player_table.all()[players - 1]
            for players in choose_tournament["players"]
        ]
        players_of_tournament_to_print = [
            [
                player["ranking"],
                player["last_name"],
                player["first_name"],
                player["date_of_birth"],
                player["gender"],
            ]
            for player in players_of_tournament
        ]
        players_of_tournament_to_print = sorted(players_of_tournament_to_print)
        print(
            tabulate(
                players_of_tournament_to_print,
                headers=[
                    "Ranking",
                    "First name",
                    "Last name",
                    "Date of birth",
                    "Gender",
                ],
                tablefmt="fancy_grid",
            )
        )

    def players_by_alphabetical_order_of_tournament(self, choice_tournament):
        choose_tournament = self.tournament_table.all()[int(choice_tournament) - 1]
        players_of_tournament = [
            self.player_table.all()[players - 1]
            for players in choose_tournament["players"]
        ]
        players_of_tournament_to_print = [
            [
                player["last_name"],
                player["first_name"],
                player["ranking"],
                player["date_of_birth"],
                player["gender"],
            ]
            for player in players_of_tournament
        ]
        players_of_tournament_to_print = sorted(
            players_of_tournament_to_print, key=lambda k: (k[0], k[1])
        )
        print(
            tabulate(
                players_of_tournament_to_print,
                headers=[
                    "First name",
                    "Last name",
                    "Ranking",
                    "Date of birth",
                    "Gender",
                ],
                tablefmt="fancy_grid",
            )
        )

    def rounds_of_tournament(self, choice_tournament):
        choose_tournament = self.tournament_table.all()[int(choice_tournament) - 1]
        rounds_of_tournament = []
        matchs_of_tournament = []
        for round in choose_tournament["rounds"]:
            rounds_of_tournament.append(self.round_table.all()[round - 1])
            for match in self.round_table.all()[round - 1]["list_of_match"]:
                matchs_of_tournament.append(self.match_table.all()[match - 1])

        rounds_of_tournament_to_print = []
        for i, round in enumerate(rounds_of_tournament):
            rounds_of_tournament_to_print.append(
                [
                    round["name"],
                    round["start_date"],
                    round["end_date"],
                ]
            )
            matchs_of_round = []
            for match in round["list_of_match"]:
                if (
                    matchs_of_tournament[match - 1]["score_player_1"] == 1.0
                    and matchs_of_tournament[match - 1]["score_player_2"] == 0.0
                ):
                    matchs_of_round.append(
                        self.player_table.get(
                            doc_id=matchs_of_tournament[match - 1]["player_1"]
                        )["first_name"]
                        + " "
                        + self.player_table.get(
                            doc_id=matchs_of_tournament[match - 1]["player_1"]
                        )["last_name"]
                        + " won against "
                        + self.player_table.get(
                            doc_id=matchs_of_tournament[match - 1]["player_2"]
                        )["first_name"]
                        + " "
                        + self.player_table.get(
                            doc_id=matchs_of_tournament[match - 1]["player_2"]
                        )["last_name"]
                        + "\n",
                    )
                elif (
                    matchs_of_tournament[match - 1]["score_player_1"] == 0.0
                    and matchs_of_tournament[match - 1]["score_player_2"] == 1.0
                ):
                    matchs_of_round.append(
                        self.player_table.get(
                            doc_id=matchs_of_tournament[match - 1]["player_2"]
                        )["first_name"]
                        + " "
                        + self.player_table.get(
                            doc_id=matchs_of_tournament[match - 1]["player_2"]
                        )["last_name"]
                        + " won against "
                        + self.player_table.get(
                            doc_id=matchs_of_tournament[match - 1]["player_1"]
                        )["first_name"]
                        + " "
                        + self.player_table.get(
                            doc_id=matchs_of_tournament[match - 1]["player_1"]
                        )["last_name"]
                        + "\n",
                    )
                elif (
                    matchs_of_tournament[match - 1]["score_player_1"] == 0.5
                    and matchs_of_tournament[match - 1]["score_player_2"] == 0.5
                ):
                    matchs_of_round.append(
                        self.player_table.get(
                            doc_id=matchs_of_tournament[match - 1]["player_2"]
                        )["first_name"]
                        + " "
                        + self.player_table.get(
                            doc_id=matchs_of_tournament[match - 1]["player_2"]
                        )["last_name"]
                        + " and "
                        + self.player_table.get(
                            doc_id=matchs_of_tournament[match - 1]["player_1"]
                        )["first_name"]
                        + " "
                        + self.player_table.get(
                            doc_id=matchs_of_tournament[match - 1]["player_1"]
                        )["last_name"]
                        + " drew\n",
                    )
            matchs = "".join(matchs_of_round)
            rounds_of_tournament_to_print[i].append(matchs)
        print(
            tabulate(
                rounds_of_tournament_to_print,
                headers=[
                    "Name",
                    "Start date",
                    "End date",
                    "Match",
                ],
                tablefmt="fancy_grid",
            )
        )

    def matchs_of_tournament(self, choice_tournament):
        choose_tournament = self.tournament_table.all()[int(choice_tournament) - 1]
        matchs_of_tournament = []
        for round in choose_tournament["rounds"]:
            for match in self.round_table.all()[round - 1]["list_of_match"]:
                matchs_of_tournament.append(self.match_table.all()[match - 1])
        matchs_of_tournament_to_print = []
        for match in matchs_of_tournament:
            if match["score_player_1"] == 1.0 and match["score_player_2"] == 0.0:
                matchs_of_tournament_to_print.append(
                    [
                        match.doc_id,
                        self.player_table.get(doc_id=match["player_1"])["first_name"]
                        + " "
                        + self.player_table.get(doc_id=match["player_1"])["last_name"]
                        + " won against "
                        + self.player_table.get(doc_id=match["player_2"])["first_name"]
                        + " "
                        + self.player_table.get(doc_id=match["player_2"])["last_name"],
                    ]
                )
            elif match["score_player_1"] == 0.0 and match["score_player_2"] == 1.0:
                matchs_of_tournament_to_print.append(
                    [
                        match.doc_id,
                        self.player_table.get(doc_id=match["player_2"])["first_name"]
                        + " "
                        + self.player_table.get(doc_id=match["player_2"])["last_name"]
                        + " won against "
                        + self.player_table.get(doc_id=match["player_1"])["first_name"]
                        + " "
                        + self.player_table.get(doc_id=match["player_1"])["last_name"],
                    ]
                )
            elif match["score_player_1"] == 0.5 and match["score_player_2"] == 0.5:
                matchs_of_tournament_to_print.append(
                    [
                        match.doc_id,
                        self.player_table.get(doc_id=match["player_2"])["first_name"]
                        + " "
                        + self.player_table.get(doc_id=match["player_2"])["last_name"]
                        + " and "
                        + self.player_table.get(doc_id=match["player_1"])["first_name"]
                        + " "
                        + self.player_table.get(doc_id=match["player_1"])["last_name"]
                        + " drew",
                    ]
                )

        print(
            tabulate(
                matchs_of_tournament_to_print,
                headers=["Id", "Match"],
                tablefmt="fancy_grid",
            )
        )

    def tournaments(self):
        """ """
        tournaments = [
            [
                tournament.doc_id,
                tournament["name"],
                tournament["place"],
                tournament["start_date"],
                tournament["end_date"],
                tournament["time_control"],
                tournament["description"],
            ]
            for tournament in self.tournament_table
        ]
        print(
            tabulate(
                tournaments,
                headers=[
                    "Id",
                    "Name",
                    "Place",
                    "Start date",
                    "End date",
                    "Time control",
                    "Description",
                ],
                tablefmt="fancy_grid",
            )
        )

    def matchs(self):
        matchs_of_round_to_print = []
        black_or_white_player = []
        matchs_of_round = [
            self.match_table.all()[match - 1]
            for match in self.round_table.all()[-1]["list_of_match"]
        ]
        for match in matchs_of_round:
            black_or_white_player.append(
                [
                    str(self.player_table.get(doc_id=match["player_1"])["first_name"])
                    + " "
                    + str(self.player_table.get(doc_id=match["player_1"])["last_name"]),
                    str(self.player_table.get(doc_id=match["player_2"])["first_name"])
                    + " "
                    + str(self.player_table.get(doc_id=match["player_2"])["last_name"]),
                ]
            )
            matchs_of_round_to_print.append(match)
        print(
            tabulate(
                black_or_white_player,
                headers=[
                    "Black",
                    "White",
                ],
                tablefmt="fancy_grid",
            )
        )

    def players_by_score(self):
        """ """
        players = [
            [
                self.player_table.all()[player - 1].doc_id,
                self.player_table.all()[player - 1]["score"],
                self.player_table.all()[player - 1]["ranking"],
                self.player_table.all()[player - 1]["last_name"],
                self.player_table.all()[player - 1]["first_name"],
                self.player_table.all()[player - 1]["date_of_birth"],
                self.player_table.all()[player - 1]["gender"],
            ]
            for player in self.tournament_table.all()[-1]["players"]
        ]
        players = sorted(
            players, key=lambda player: (player[1], -player[2]), reverse=True
        )
        print(
            tabulate(
                players,
                headers=[
                    "Id",
                    "Score",
                    "Ranking",
                    "First name",
                    "Last name",
                    "Date of birth",
                    "Gender",
                ],
                tablefmt="fancy_grid",
            )
        )

    def remaining_players(self, list_of_remaining_players):
        """ """
        players = [
            [
                player[0],
                player[1],
                player[2],
                player[3],
                player[4],
                player[5],
            ]
            for player in list_of_remaining_players
        ]
        players = sorted(players)
        print(
            tabulate(
                players,
                headers=[
                    "Id",
                    "First name",
                    "Last name",
                    "Ranking",
                    "Date of birth",
                    "Gender",
                ],
                tablefmt="fancy_grid",
            )
        )
