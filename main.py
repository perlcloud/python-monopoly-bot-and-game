import uuid
import random
import landings


class Dice:
    """Dice class for executing and tracking a players rolls"""

    jail_roll_count = 0  # Number of times player has attempted to roll a double to leave jail

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

    # Landings for which no action is needed on landing
    NO_ACTION = [
        GO,
        JAIL,
        FREE_PARKING,
    ]

    # Options for ways to leave jail
    LEAVE_JAIL_USE_CARD = "card"
    LEAVE_JAIL_PAY = "pay"
    LEAVE_JAIL_ROLL = "roll"

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

    def get_cards_by_owner(self, player):
        chance_cards = [c for c in self.chance.cards if c.owner and c.owner.id == player.id]
        community_chest_cards = [c for c in self.community_chest.cards if c.owner and c.owner.id == player.id]
        return chance_cards + community_chest_cards


class PlayerBase:
    """Base Class for a Monopoly player"""

    id = None
    position = (0, Board.landings[0])
    name = None
    dice = Dice()
    cash = None
    in_jail = False

    def __init__(self, name, game):
        self.id = uuid.uuid4()
        self.name = name
        self.game = game
        self.cash = self.game.bank.withdraw(1500)

    @property
    def get_out_of_jail_free_cards(self):
        cards = self.game.board.get_cards_by_owner(self)
        cards = [
            c for c in cards
            if c.deck_code_name == "community_chest"
               and c.id == landings.CommunityChest.GET_OUT_OF_JAIL_FREE
            or c.deck_code_name == "chance"
               and c.id == landings.Chance.GET_OUT_OF_JAIL_FREE
        ]
        return cards

    def leave_jail_option(self):
        """Extend this method to return one of the 3 LEAVE_JAIL_OPTIONS to choose how you want to leave jail"""
        raise NotImplementedError

    def withdraw(self, amount):
        """
        Attempt to withdraw money from the users cash
        Returns None if the player does not have the cash on hand
        """
        value = amount if amount <= self.cash else None
        if value:
            self.cash -= amount

        return value


class DefaultPlayer(PlayerBase):
    """Default implementation of a monopoly player, making obvious choices"""

    def leave_jail_option(self):
        if len(self.get_out_of_jail_free_cards) > 0:
            return game.board.LEAVE_JAIL_USE_CARD
        elif self.cash >= 1000:
            return game.board.LEAVE_JAIL_PAY
        else:
            return game.board.LEAVE_JAIL_ROLL


class Bank:
    """Bank object for tracking cash-flow, houses, and hotels"""

    def __init__(self):
        self.cash = 20580

    def withdraw(self, amount):
        """Withdraw money from the bank"""
        self.cash -= amount
        return amount

    def deposit(self, amount):
        """Deposit money in the bank"""
        self.cash += amount


class Game:
    """Gameplay class handling player turns"""

    players = []
    board = Board()
    bank = Bank()
    current_player = None

    def _advance_position(self, roll_value):
        """Advances a players position based on a spin of the dice"""
        self.current_player.position, passed_go = self.board.advance(
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
        self.current_player.position = (position_id, self.board.landings[position_id])
        return passed_go

    def _bank_collect(self, amount):
        """Collects money from the Bank"""
        self.bank.withdraw(amount)
        self.current_player.cash += amount

    def add_player(self, name, player_obj):
        """Adds a player to the game"""
        self.players.append(player_obj(name, self))

    def run_turn(self):
        """Runs the run_turn for the current player"""
        # TODO split out this code and write tests for all of it

        print(
            f"Player {self.current_player.name} is on {self.current_player.position[1]}"
        )

        roll = None

        # If the player is in jail, attempt to leave
        if self.current_player.in_jail:
            # Player must now choose between paying $50, using a get out of jail free card, or trying to roll a double
            print(f"Player {self.current_player.name} is in Jail")
            selected_option = self.current_player.leave_jail_option()

            if selected_option == self.board.LEAVE_JAIL_USE_CARD:
                if len(self.current_player.get_out_of_jail_free_cards) > 0:
                    card = self.current_player.get_out_of_jail_free_cards.pop()
                    if card.deck_code_name == "community_chest":
                        self.board.community_chest.place_card_at_bottom(card)
                    if card.deck_code_name == "chance":
                        self.board.chance.place_card_at_bottom(card)
                    self.current_player.in_jail = False
                else:
                    raise ValueError("You cannot choose to use a card you don't have, cheater!")
            elif selected_option == self.board.LEAVE_JAIL_PAY:
                cash = self.current_player.withdraw(50)
                self.bank.deposit(cash)
                self.current_player.in_jail = False
            elif selected_option == self.board.LEAVE_JAIL_ROLL:
                roll = self.current_player.dice.roll()
                if not roll["same"]:
                    # The player did not roll a double and remains in jail
                    self.current_player.dice.jail_roll_count += 1
                    if self.current_player.dice.jail_roll_count == 3:
                        # If this is the 3rd try at rolling a double, player is forced to pay $50 and use the roll
                        cash = self.current_player.withdraw(50)
                        self.bank.deposit(cash)
                        self.current_player.dice.jail_roll_count = 0
                        self.current_player.in_jail = False
                    else:
                        return
                else:
                    self.current_player.dice.jail_roll_count = 0
                    self.current_player.in_jail = False

        # roll dice
        roll = self.current_player.dice.roll() if not roll else roll
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
            card = position.select_card()

            if card.id == landings.Chance.ADVANCE_TO_GO:
                self._move_position(Board.GO)
                self._bank_collect(200)
                print(
                    f"Player {self.current_player.name} has been moved to {self.current_player.position[1]} and got $200"
                )

            elif card.id == landings.Chance.ADVANCE_TO_ILLINOIS:
                passed_go = self._move_position(Board.ILLINOIS_AVE)
                if passed_go:
                    self._bank_collect(200)

            elif card.id == landings.Chance.ADVANCE_TO_ST_CHARLES_PLACE:
                passed_go = self._move_position(Board.ST_CHARLES_PLACE)
                if passed_go:
                    self._bank_collect(200)

            elif card.id == landings.Chance.ADVANCE_TO_NEAREST_UTILITY:
                nearest_utility = game.board.next_utility(position_id)
                passed_go = self._move_position(nearest_utility)
                if passed_go:
                    self._bank_collect(200)

            elif card.id == landings.Chance.ADVANCE_TO_NEAREST_RAILROAD:
                nearest_railroad = game.board.next_railroad(position_id)
                passed_go = self._move_position(nearest_railroad)
                if passed_go:
                    self._bank_collect(200)

            elif card.id == landings.Chance.BANKS_PAYS_DIVIDEND:
                self._bank_collect(50)

            elif card.id == landings.Chance.GET_OUT_OF_JAIL_FREE:
                card.owner = self.current_player

            elif card.id == landings.Chance.GO_BACK_THREE:
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

            elif card.id == landings.Chance.GO_TO_JAIL:
                self.current_player.position = 10, self._move_position(Board.JAIL)
                self.current_player.in_jail = True
                # TODO write Jail code

            elif card.id == landings.Chance.GENERAL_REPAIRS:
                pass
                # TODO write code to remove value from user based on houses/hotels

            elif card.id == landings.Chance.POOR_TAX:
                self._bank_collect(15)

            elif card.id == landings.Chance.TRIP_TO_READING_RAILROAD:
                passed_go = self._move_position(Board.READING_RAILROAD)
                if passed_go:
                    self._bank_collect(200)

            elif card.id == landings.Chance.TRIP_TO_BOARDWALK:
                self._move_position(Board.BOARDWALK)

            elif card.id == landings.Chance.CHAIRMAN_OF_THE_BOARD:
                pass
                # TODO pay each player 50

            elif card.id == landings.Chance.BUILDING_LOAN_LOAN:
                self._bank_collect(150)

            elif card.id == landings.Chance.WON_CROSSWORD_COMPETITION:
                self._bank_collect(100)

        elif isinstance(position, landings.CommunityChest):
            # PlayerBase landed on Community Chest, pick a card and act on its instructions
            card = position.select_card()

            if card.id == landings.CommunityChest.ADVANCE_TO_GO:
                self._move_position(Board.GO)
                self._bank_collect(200)
                print(
                    f"Player {self.current_player.name} has been moved to {self.current_player.position[1]} and got $200"
                )

            elif card.id == landings.CommunityChest.BANK_ERROR:
                pass

            elif card.id == landings.CommunityChest.DOCTOR_FEE:
                pass

            elif card.id == landings.CommunityChest.STOCK_SALE:
                pass

            elif card.id == landings.CommunityChest.GET_OUT_OF_JAIL_FREE:
                pass

            elif card.id == landings.CommunityChest.GO_TO_JAIL:
                pass

            elif card.id == landings.CommunityChest.OPERA_NIGHT:
                pass

            elif card.id == landings.CommunityChest.HOLIDAY_FUND:
                pass

            elif card.id == landings.CommunityChest.TAX_REFUND:
                pass

            elif card.id == landings.CommunityChest.BIRTHDAY:
                pass

            elif card.id == landings.CommunityChest.LIFE_INSURANCE:
                pass

            elif card.id == landings.CommunityChest.HOSPITAL_FEES:
                pass

            elif card.id == landings.CommunityChest.SCHOOL_FEES:
                pass

            elif card.id == landings.CommunityChest.CONSULT:
                pass

            elif card.id == landings.CommunityChest.STREET_REPAIRS:
                pass

            elif card.id == landings.CommunityChest.BEAUTY_CONTEST:
                pass

            elif card.id == landings.CommunityChest.INHERITANCE:
                pass

        elif isinstance(position, landings.GoToJail):
            # Player landed on "Go to jail", place player in jail and place them in jailed status
            _ = self._move_position(self.board.JAIL)
            self.current_player.in_jail = True

        # Take action based on where the player landed
        if position_id in self.board.NO_ACTION:
            pass

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
    game.add_player("Avi", DefaultPlayer)
    game.add_player("Sara", DefaultPlayer)

    game.play()
