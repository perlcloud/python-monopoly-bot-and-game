import random
import landings


class Dice:
    """Dice class for executing and tracking a players rolls"""

    def roll(self):
        """Roll 2 Dice"""
        dice = [random.randint(1, 6), random.randint(1, 6)]
        return {
            0: dice[0],
            1: dice[1],
            "total": dice[0] + dice[1],
            "same": dice[0] == dice[1],
        }


class Board:
    """Class representing the Monopoly board with helpful gameplay functions"""

    GO = 0
    MEDITIRANEAN_AVE = 1
    COMMUNITY_CHEST_1 = 2
    BALTIC_AVE = 3
    INCOME_TAX = 4
    READING_RAILROAD = 5
    ORIENTAL_AVE = 6
    CHANCE_1 = 7
    VERMONT_AVE = 8
    CONNECTICUT_AVE = 9
    JAIL = 10
    ST_CHARLES_PLACE = 11
    ELECTRIC_COMPANY = 12
    STATES_AVE = 13
    VIRGINIA_AVE = 14
    PENNSYLVANIA_RAILROAD = 15
    ST_JAMES_PLACE = 16
    COMMUNITY_CHEST_2 = 17
    TENNESSEE_AVE = 18
    NEW_YORK_AVE = 19
    FREE_PARKING = 20
    KENTUCKY_AVE = 21
    CHANCE_2 = 22
    INDIANA_AVE = 23
    ILLINOIS_AVE = 24
    BO_RAILROAD = 25
    ATLTLANTIC_AVE = 26
    VENTNOR_AVE = 27
    WATER_WORKS = 28
    MARVIN_GARDENS = 29
    GO_TO_JAIL = 30
    PACIFIC_AVE = 31
    NORTH_CAROLINA_AVE = 32
    COMMUNITY_CHEST_3 = 33
    PENNSYLVANIA_AVE = 34
    SHORTLINE = 35
    CHANCE_3 = 36
    PARK_PLACE = 37
    LUXERY_TAX = 38
    BOARDWALK = 39

    chance = landings.Chance()
    community_chest = landings.CommunityChest()
    landings = {
        GO: landings.Go(),
        MEDITIRANEAN_AVE: landings.MediterRaneanAvenue(),
        COMMUNITY_CHEST_1: landings.CommunityChest(),
        BALTIC_AVE: landings.BalticAvenue(),
        INCOME_TAX: landings.IncomeTax(),
        READING_RAILROAD: landings.ReadingRailroad(),
        ORIENTAL_AVE: landings.OrientalAvenue(),
        CHANCE_1: chance,
        VERMONT_AVE: landings.VermontAvenue(),
        CONNECTICUT_AVE: landings.ConnecticutAvenue(),
        JAIL: landings.Jail(),
        ST_CHARLES_PLACE: landings.StCharlesPlace(),
        ELECTRIC_COMPANY: landings.ElectricCompany(),
        STATES_AVE: landings.StatesAvenue(),
        VIRGINIA_AVE: landings.VirginiaAvenue(),
        PENNSYLVANIA_RAILROAD: landings.PennsylvaniaRailroad(),
        ST_JAMES_PLACE: landings.StJamesPlace(),
        COMMUNITY_CHEST_2: community_chest,
        TENNESSEE_AVE: landings.TennesseeAvenue(),
        NEW_YORK_AVE: landings.NewYorkAvenue(),
        FREE_PARKING: landings.FreeParking(),
        KENTUCKY_AVE: landings.KentuckyAvenue(),
        CHANCE_2: chance,
        INDIANA_AVE: landings.IndianaAvenue(),
        ILLINOIS_AVE: landings.IllinoisAvenue(),
        BO_RAILROAD: landings.BORailroad(),
        ATLTLANTIC_AVE: landings.AtlanticAvenue(),
        VENTNOR_AVE: landings.VentnorAvenue(),
        WATER_WORKS: landings.WaterWorks(),
        MARVIN_GARDENS: landings.MarvinGardens(),
        GO_TO_JAIL: landings.GoToJail(),
        PACIFIC_AVE: landings.PacificAvenue(),
        NORTH_CAROLINA_AVE: landings.NorthCarolinaAvenue(),
        COMMUNITY_CHEST_3: community_chest,
        PENNSYLVANIA_AVE: landings.PennsylvaniaAvenue(),
        SHORTLINE: landings.ShortLine(),
        CHANCE_3: chance,
        PARK_PLACE: landings.ParkPlace(),
        LUXERY_TAX: landings.LuxuryTax(),
        BOARDWALK: landings.Boardwalk(),
    }
    bord_len = len(landings) - 1

    def advance(self, current_position, roll_value):
        """Calculate the players new position based on their dice roll"""
        if not 2 <= roll_value <= 12:
            raise ValueError(
                f"You cannot roll a value of {roll_value}. Only 2-12 are valid values."
            )

        passed_go = False
        next_position = current_position + roll_value
        if next_position > self.bord_len:
            passed_go = True
            next_position = next_position - self.bord_len - 1

        return (next_position, self.landings[next_position]), passed_go

    def next_utility(self, position):
        """Return the next utility after the players current position"""
        if (
            self.GO <= position <= self.ST_CHARLES_PLACE
            or self.MARVIN_GARDENS <= position <= self.BOARDWALK
        ):
            return self.ELECTRIC_COMPANY
        elif self.ELECTRIC_COMPANY <= position <= self.VENTNOR_AVE:
            return self.WATER_WORKS

    def next_railroad(self, position):
        """Return the next railroad after the players current position"""
        if (
            self.GO <= position <= self.INCOME_TAX
            or self.CHANCE_3 <= position <= self.BOARDWALK
        ):
            return self.READING_RAILROAD
        elif self.READING_RAILROAD <= position <= self.VIRGINIA_AVE:
            return self.PENNSYLVANIA_RAILROAD
        elif self.PENNSYLVANIA_RAILROAD <= position <= self.ILLINOIS_AVE:
            return self.BO_RAILROAD
        elif self.BO_RAILROAD <= position <= self.PENNSYLVANIA_AVE:
            return self.SHORTLINE


class PlayerBase:
    """Base Class for a Monopoly player"""

    position = (0, Board.landings[0])
    name = None
    dice = Dice()
    cash = 1500
    get_out_of_jail_free_cards = 0
    in_jail = False

    def __init__(self, name):
        self.name = name


class Game:
    """Gameplay class handling player turns"""

    players = []
    board = Board()
    current_player = None

    def _advance_position(self, roll_value):
        """Advances a players position based on a spin of the dice"""
        self.current_player.position, passed_go = game.board.advance(
            self.current_player.position[0], roll_value
        )
        return passed_go

    def _move_position(self, position_id, backwards_movement=False):
        """Changes a player to a new position specified"""
        passed_go = (
            True
            if self.current_player.position[0] > position_id
            and not backwards_movement
            or position_id == 0
            else False
        )
        self.current_player.position = (position_id, game.board.landings[position_id])
        return passed_go

    def _bank_collect(self, amount):
        """Collects money from the Bank"""
        self.current_player.cash += amount
        # TODO remove from bank

    def add_player(self, player):
        """Adds a player to the game"""
        self.players.append(player)

    def run_turn(self):
        """Runs the run_turn for the current player"""
        print(
            f"Player {self.current_player.name} is on {self.current_player.position[1]}"
        )

        # roll dice
        roll = self.current_player.dice.roll()
        print(f"Player {self.current_player.name} rolled {roll['total']}")

        # move players piece
        passed_go = self._advance_position(roll["total"])
        print(
            f"Player {self.current_player.name} is now on {self.current_player.position[1]}"
        )

        if passed_go:
            self._bank_collect(200)

        # take action based on where the player landed
        position_id, position = self.current_player.position

        if isinstance(position, landings.Chance):
            # PlayerBase landed on Chance, pick a card and act on its instructions
            card_id, card_text = position.select_card()

            if card_id == landings.Chance.ADVANCE_TO_GO:
                self._move_position(Board.GO)
                self._bank_collect(200)
                print(
                    f"Player {self.current_player.name} has been moved to {self.current_player.position[1]} and got $200"
                )

            elif card_id == landings.Chance.ADVANCE_TO_ILLINOIS:
                passed_go = self._move_position(Board.ILLINOIS_AVE)
                if passed_go:
                    self._bank_collect(200)

            elif card_id == landings.Chance.ADVANCE_TO_ST_CHARLES_PLACE:
                passed_go = self._move_position(Board.ST_CHARLES_PLACE)
                if passed_go:
                    self._bank_collect(200)

            elif card_id == landings.Chance.ADVANCE_TO_NEAREST_UTILITY:
                nearest_utility = game.board.next_utility(position_id)
                passed_go = self._move_position(nearest_utility)
                if passed_go:
                    self._bank_collect(200)

            elif card_id == landings.Chance.ADVANCE_TO_NEAREST_RAILROAD:
                nearest_railroad = game.board.next_railroad(position_id)
                passed_go = self._move_position(nearest_railroad)
                if passed_go:
                    self._bank_collect(200)

            elif card_id == landings.Chance.BANKS_PAYS_DIVIDEND:
                self._bank_collect(50)

            elif card_id == landings.Chance.GET_OUT_OF_JAIL_FREE:
                self.current_player.get_out_of_jail_free_cards += 1

            elif card_id == landings.Chance.GO_BACK_THREE:
                go_back_to = (
                    position_id - 3
                    if position_id >= 3
                    else 49
                    if position_id == 2
                    else 48
                    if position_id == 1
                    else 47
                )
                self._move_position(go_back_to, backwards_movement=True)

            elif card_id == landings.Chance.GO_TO_JAIL:
                self.current_player.position = 10, self._move_position(Board.JAIL)
                self.current_player.in_jail = True
                # TODO write Jail code

            elif card_id == landings.Chance.GENERAL_REPAIRS:
                pass
                # TODO write code to remove value from user based on houses/hotels

            elif card_id == landings.Chance.POOR_TAX:
                self._bank_collect(15)

            elif card_id == landings.Chance.TRIP_TO_READING_RAILROAD:
                passed_go = self._move_position(Board.READING_RAILROAD)
                if passed_go:
                    self._bank_collect(200)

            elif card_id == landings.Chance.TRIP_TO_BOARDWALK:
                self._move_position(Board.BOARDWALK)

            elif card_id == landings.Chance.CHAIRMAN_OF_THE_BOARD:
                pass
                # TODO pay each player 50

            elif card_id == landings.Chance.BUILDING_LOAN_LOAN:
                self._bank_collect(150)

            elif card_id == landings.Chance.WON_CROSSWORD_COMPETITION:
                self._bank_collect(100)

        elif isinstance(position, landings.CommunityChest):
            # PlayerBase landed on Community Chest, pick a card and act on its instructions
            card_id, card_text = position.select_card()

            if card_id == landings.CommunityChest.ADVANCE_TO_GO:
                self._move_position(Board.GO)
                self._bank_collect(200)
                print(
                    f"Player {self.current_player.name} has been moved to {self.current_player.position[1]} and got $200"
                )

            elif card_id == landings.CommunityChest.BANK_ERROR:
                pass

            elif card_id == landings.CommunityChest.DOCTOR_FEE:
                pass

            elif card_id == landings.CommunityChest.STOCK_SALE:
                pass

            elif card_id == landings.CommunityChest.GET_OUT_OF_JAIL_FREE:
                pass

            elif card_id == landings.CommunityChest.GO_TO_JAIL:
                pass

            elif card_id == landings.CommunityChest.OPERA_NIGHT:
                pass

            elif card_id == landings.CommunityChest.HOLIDAY_FUND:
                pass

            elif card_id == landings.CommunityChest.TAX_REFUND:
                pass

            elif card_id == landings.CommunityChest.BIRTHDAY:
                pass

            elif card_id == landings.CommunityChest.LIFE_INSURANCE:
                pass

            elif card_id == landings.CommunityChest.HOSPITAL_FEES:
                pass

            elif card_id == landings.CommunityChest.SCHOOL_FEES:
                pass

            elif card_id == landings.CommunityChest.CONSULT:
                pass

            elif card_id == landings.CommunityChest.STREET_REPAIRS:
                pass

            elif card_id == landings.CommunityChest.BEAUTY_CONTEST:
                pass

            elif card_id == landings.CommunityChest.INHERITANCE:
                pass

        # take actions
        if passed_go:
            print(f"Player {self.current_player.name} passed Go!!!")

    def play(self):
        """Runs the Monopoly game"""
        first_round = True
        while first_round or input("\tDo you want to take another round? ").lower() in [
            "yes",
            "y",
            "",
        ]:
            first_round = False

            for player in self.players:
                self.current_player = player
                # player.run_turn()
                self.run_turn()


if __name__ == "__main__":
    game = Game()
    game.add_player(PlayerBase("Avi"))
    game.add_player(PlayerBase("Avrohom"))

    game.play()
