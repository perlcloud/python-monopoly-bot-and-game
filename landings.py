import random


class LandingsBase:
    """Base class for a Monopoly Board Position"""

    name = None
    is_utility = False
    is_railroad = False

    def __str__(self):
        return f"<{self.name}>"


class CardBase(LandingsBase):
    """Base class for Monopoly card sets"""

    name = None
    cards = []

    def __init__(self, scramble=True):
        if scramble:
            # We don't scramble cards when we reload an old game.
            self.cards = sorted(self.cards, key=lambda x: random.random())

    def _get_top_card(self):
        """Returns the card on top of the pile"""
        return self.cards.pop()

    def _place_card_at_bottom(self, card):
        """Place a card at the bottom of the pile"""
        self.cards.insert(0, card)

    def select_card(self):
        """Selects a card, placing the card at the bottom of the pile if the player does no keep the card"""
        card = self._get_top_card()
        print(f"Chance card selected: {card}")

        if not card[0] == self.GET_OUT_OF_JAIL_FREE:
            self._place_card_at_bottom(card)

        return card


class Chance(CardBase):
    """Class representing the Chance set of cards"""

    ADVANCE_TO_GO = 0
    ADVANCE_TO_ILLINOIS = 1
    ADVANCE_TO_ST_CHARLES_PLACE = 2
    ADVANCE_TO_NEAREST_UTILITY = 3
    ADVANCE_TO_NEAREST_RAILROAD = 4
    BANKS_PAYS_DIVIDEND = 5
    GET_OUT_OF_JAIL_FREE = 6
    GO_BACK_THREE = 7
    GO_TO_JAIL = 8
    GENERAL_REPAIRS = 9
    POOR_TAX = 10
    TRIP_TO_READING_RAILROAD = 11
    TRIP_TO_BOARDWALK = 12
    CHAIRMAN_OF_THE_BOARD = 13
    BUILDING_LOAN_LOAN = 14
    WON_CROSSWORD_COMPETITION = 15

    name = "Chance"
    cards = [
        (ADVANCE_TO_GO, 'Advance to "Go". (Collect $200).'),
        (ADVANCE_TO_ILLINOIS, "Advance to Illinois Ave. If you pass Go, collect $200."),
        (
            ADVANCE_TO_ST_CHARLES_PLACE,
            "Advance to St. Charles Place. If you pass Go, collect $200.",
        ),
        (
            ADVANCE_TO_NEAREST_UTILITY,
            "Advance token to nearest Utility. If unowned, you may buy it from the Bank. "
            "If owned, throw dice and pay owner a total 10 times the amount thrown.",
        ),
        (
            ADVANCE_TO_NEAREST_RAILROAD,
            "Advance token to the nearest Railroad and pay owner twice the rental to which "
            "he/she is otherwise entitled. If Railroad is unowned, you may buy it from the Bank.",
        ),
        (BANKS_PAYS_DIVIDEND, "Bank pays you dividend of $50."),
        (
            GET_OUT_OF_JAIL_FREE,
            "Get out of Jail Free. This card may be kept until needed, or traded/sold.",
        ),
        (GO_BACK_THREE, "Go Back Three Spaces."),
        (
            GO_TO_JAIL,
            "Go to Jail. Go directly to Jail. Do not pass GO, do not collect $200.",
        ),
        (
            GENERAL_REPAIRS,
            "Make general repairs on all your property: For each house pay $25, For each hotel pay $100.",
        ),
        (POOR_TAX, "Pay poor tax of $15"),
        (
            TRIP_TO_READING_RAILROAD,
            "Take a trip to Reading Railroad. If you pass Go, collect $200.",
        ),
        (
            TRIP_TO_BOARDWALK,
            "Take a walk on the Boardwalk. Advance token to Boardwalk.",
        ),
        (
            CHAIRMAN_OF_THE_BOARD,
            "You have been elected Chairman of the Board. Pay each player $50.",
        ),
        (BUILDING_LOAN_LOAN, "Your building loan matures. Receive $150."),
        (
            WON_CROSSWORD_COMPETITION,
            "You have won a crossword competition. Collect $100.",
        ),
    ]


class CommunityChest(CardBase):
    """Class representing the Community Chest set of cards"""

    ADVANCE_TO_GO = 0
    BANK_ERROR = 1
    DOCTOR_FEE = 2
    STOCK_SALE = 3
    GET_OUT_OF_JAIL_FREE = 4
    GO_TO_JAIL = 5
    OPERA_NIGHT = 6
    HOLIDAY_FUND = 7
    TAX_REFUND = 8
    BIRTHDAY = 9
    LIFE_INSURANCE = 10
    HOSPITAL_FEES = 11
    SCHOOL_FEES = 12
    CONSULT = 13
    STREET_REPAIRS = 14
    BEAUTY_CONTEST = 15
    INHERITANCE = 16

    name = "Community Chest"
    cards = [
        (ADVANCE_TO_GO, "Advance to 'Go'. (Collect $200)"),
        (BANK_ERROR, "Bank error in your favor. Collect $200."),
        (DOCTOR_FEE, "Doctor's fees. Pay $50."),
        (STOCK_SALE, "From sale of stock you get $50."),
        (GET_OUT_OF_JAIL_FREE, "Get Out of Jail Free."),
        (GO_TO_JAIL, "Go to Jail."),
        (
            OPERA_NIGHT,
            "Grand Opera Night. Collect $50 from every player for opening night seats.",
        ),
        (HOLIDAY_FUND, "Holiday {Xmas} Fund matures. Receive {Collect} $100."),
        (TAX_REFUND, "Income tax refund. Collect $20."),
        (BIRTHDAY, "It is your birthday. Collect $10 from every player."),
        (LIFE_INSURANCE, "Life insurance matures – Collect $100"),
        (HOSPITAL_FEES, "Hospital Fees. Pay $50."),
        (SCHOOL_FEES, "School fees. Pay $50."),
        (CONSULT, "Receive $25 consultancy fee."),
        (
            STREET_REPAIRS,
            "You are assessed for street repairs: Pay $40 per house and $115 per hotel you own.",
        ),
        (BEAUTY_CONTEST, "You have won second prize in a beauty contest. Collect $10."),
        (INHERITANCE, "You inherit $100."),
    ]


class Go(LandingsBase):
    name = "Go"


class MediterRaneanAvenue(LandingsBase):
    name = "Mediter-Ranean Avenue"


class BalticAvenue(LandingsBase):
    name = "Baltic Avenue"


class IncomeTax(LandingsBase):
    name = "Income Tax"


class ReadingRailroad(LandingsBase):
    name = "Reading Railroad"
    is_railroad = True


class OrientalAvenue(LandingsBase):
    name = "Oriental Avenue"


class VermontAvenue(LandingsBase):
    name = "Vermont Avenue"


class ConnecticutAvenue(LandingsBase):
    name = "Connecticut Avenue"


class Jail(LandingsBase):
    name = "Jail"


class StCharlesPlace(LandingsBase):
    name = "St. Charles Place"


class ElectricCompany(LandingsBase):
    name = "Electric Company"
    is_utility = True


class StatesAvenue(LandingsBase):
    name = "States Avenue"


class VirginiaAvenue(LandingsBase):
    name = "Virginia Avenue"


class PennsylvaniaRailroad(LandingsBase):
    name = "Pennsylvania Railroad"
    is_railroad = True


class StJamesPlace(LandingsBase):
    name = "St. James Place"


class TennesseeAvenue(LandingsBase):
    name = "Tennessee Avenue"


class NewYorkAvenue(LandingsBase):
    name = "New York Avenue"


class FreeParking(LandingsBase):
    name = "Free Parking"


class KentuckyAvenue(LandingsBase):
    name = "Kentucky Avenue"


class IndianaAvenue(LandingsBase):
    name = "Indiana Avenue"


class IllinoisAvenue(LandingsBase):
    name = "Illinois Avenue"


class BORailroad(LandingsBase):
    name = "B&O Railroad"
    is_railroad = True


class AtlanticAvenue(LandingsBase):
    name = "Atlantic Avenue"


class VentnorAvenue(LandingsBase):
    name = "Ventnor Avenue"


class WaterWorks(LandingsBase):
    name = "Water Works"
    is_utility = True


class MarvinGardens(LandingsBase):
    name = "Marvin Gardens"


class GoToJail(LandingsBase):
    name = "Go To Jail"


class PacificAvenue(LandingsBase):
    name = "Pacific Avenue"


class NorthCarolinaAvenue(LandingsBase):
    name = "North Carolina Avenue"


class PennsylvaniaAvenue(LandingsBase):
    name = "Pennsylvania Avenue"


class ShortLine(LandingsBase):
    name = "Short Line"
    is_railroad = True


class ParkPlace(LandingsBase):
    name = "Park Place"


class LuxuryTax(LandingsBase):
    name = "Luxury Tax"


class Boardwalk(LandingsBase):
    name = "Boardwalk"
