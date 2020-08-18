import pytest
from unittest import mock

import main
import landings


def test_dice_return_dict():
    """Verify the dice roll returns expected values"""
    dice = main.Dice()
    roll = dice.roll()

    assert type(roll) == dict, "Returned array is not a dictionary"

    for key in [0, 1, "total", "same"]:
        assert key in roll.keys(), f"key '{key}' missing"


def test_dice_correct_total():
    """Verify the dice roll total value is correct"""
    dice = main.Dice()
    roll = dice.roll()

    assert (
        roll[0] + roll[1] == roll["total"]
    ), "The 'total' value for the dice roll does not match the value rolled"


@mock.patch("main.random.randint")
def test_dice_matching_values(mock_randint):
    """Verify the return values from a dice roll when the dice values are the same"""
    mock_randint.side_effect = [5, 5]

    dice = main.Dice()
    roll = dice.roll()

    assert roll[0] == roll[1]
    assert roll["same"] is True


@mock.patch("main.random.randint")
def test_dice_non_matching_values(mock_randint):
    """Verify the return values from a dice roll when the dice values are not the same"""
    mock_randint.side_effect = [5, 6]

    dice = main.Dice()
    roll = dice.roll()

    assert roll[0] != roll[1]
    assert roll["same"] is False


def test_board_len():
    """Verify the board length is 40, with a zero index"""
    board = main.Board()
    assert board.bord_len == 40 - 1


def test_board_advance_roll_value_error():
    """Verify that the advance function will throw an error if a bad dice value is passed"""
    board = main.Board()
    with pytest.raises(ValueError):
        board.advance(0, 1)
    with pytest.raises(ValueError):
        board.advance(0, 13)


def test_board_advance_passed_go():
    """Verify that appropriate moves are considered 'Passing Go'"""
    board = main.Board()

    # Landing on Go is considered 'Passing Go'
    position, passed_go = board.advance(board.LUXERY_TAX, 2)
    assert passed_go is True

    # Moving from Go to another location is not considered 'Passing Go'
    position, passed_go = board.advance(board.GO, 2)
    assert passed_go is not True

    # Advancing passed Go is considered 'Passing Go'
    position, passed_go = board.advance(board.BOARDWALK, 2)
    assert passed_go is True


def test_board_advance_end_of_board():
    """Verify a roll that passes go is calculated correctly"""
    board = main.Board()

    # Land on Go
    position, passed_go = board.advance(board.PARK_PLACE, 4)
    assert position[0] == board.MEDITIRANEAN_AVE


def test_board_advance_return_tuple_value():
    """Verify the return value from the advance function is formatted correctly"""
    board = main.Board()

    # Land on Go
    position, passed_go = board.advance(board.GO, 5)
    assert position[0] == board.READING_RAILROAD
    assert position[1] == board.landings[board.READING_RAILROAD]


def test_board_advance_next_utility():
    """Verify the next_utility() function returns the right utility"""
    board = main.Board()
    assert board.next_utility(board.BALTIC_AVE) == board.ELECTRIC_COMPANY
    assert board.next_utility(board.VIRGINIA_AVE) == board.WATER_WORKS
    assert board.next_utility(board.PARK_PLACE) == board.ELECTRIC_COMPANY


def test_board_advance_next_railroad():
    """Verify the next_railroad() function returns the right railroad"""
    board = main.Board()
    assert board.next_railroad(board.BALTIC_AVE) == board.READING_RAILROAD
    assert board.next_railroad(board.VERMONT_AVE) == board.PENNSYLVANIA_RAILROAD
    assert board.next_railroad(board.TENNESSEE_AVE) == board.BO_RAILROAD
    assert board.next_railroad(board.WATER_WORKS) == board.SHORTLINE
    assert board.next_railroad(board.PARK_PLACE) == board.READING_RAILROAD


def test_board_get_cards_by_owner():
    """Verify the func returns the right cards"""
    game = main.Game()
    game.add_player("TestPlayer1", main.DefaultPlayer)
    game.add_player("TestPlayer2", main.DefaultPlayer)
    game.current_player = game.players[0]

    # Get card examples
    chance_jail_card = [
        c
        for c in game.board.chance.cards
        if c.id == game.board.chance.GET_OUT_OF_JAIL_FREE
    ][0]
    community_chest_jail_card = [
        c
        for c in game.board.community_chest.cards
        if c.id == game.board.community_chest.GET_OUT_OF_JAIL_FREE
    ][0]

    # Give each card to a player
    chance_jail_card.owner = game.current_player
    community_chest_jail_card.owner = game.players[1]

    # Verify the one card we gave to the current player comes back
    # but the 2nd one we gave to the other player does not
    assert [chance_jail_card] == game.board.get_cards_by_owner(game.current_player)


def test_game_advance_position():
    """Tests that the game-play functionality for moving a player according to dice roll works"""
    game = main.Game()
    game.add_player("TestPlayer", main.PlayerBase)
    game.current_player = game.players[0]

    passed_go = game._advance_position(2)

    assert passed_go is False
    assert game.current_player.position[0] == main.Board.COMMUNITY_CHEST_1


def test_game_move_position_forward():
    """Tests that the game-play functionality for moving a player forward to a set position works"""
    game = main.Game()
    game.add_player("TestPlayer", main.PlayerBase)
    game.current_player = game.players[0]
    game.current_player.position = (
        game.board.COMMUNITY_CHEST_2,
        game.board.landings[game.board.COMMUNITY_CHEST_2],
    )

    passed_go = game._move_position(game.board.ST_CHARLES_PLACE)

    assert passed_go is True
    assert game.current_player.position[0] == main.Board.ST_CHARLES_PLACE


def test_game_move_position_backwards():
    """Tests that the game-play functionality for moving a player forward to a set position works"""
    game = main.Game()
    game.add_player("TestPlayer", main.PlayerBase)
    game.current_player = game.players[0]
    game.current_player.position = (
        game.board.MEDITIRANEAN_AVE,
        game.board.landings[game.board.MEDITIRANEAN_AVE],
    )

    passed_go = game._move_position(game.board.LUXERY_TAX)

    assert passed_go is False
    assert game.current_player.position[0] == main.Board.LUXERY_TAX


def test_game_bank_collect():
    """Verify money collected from the bank is handled correctly"""
    game = main.Game()
    game.add_player("TestPlayer", main.PlayerBase)
    game.current_player = game.players[0]

    bank_cash_old = game.bank.cash
    player_cash_old = game.current_player.cash
    amount = 50

    game._bank_collect(amount)

    bank_cash_new = game.bank.cash
    player_cash_new = game.current_player.cash

    assert (
        bank_cash_new == bank_cash_old - amount
    ), f"Cash not withdrawn from the bank correctly. {bank_cash_new} == ({bank_cash_old} - {amount})"
    assert (
        player_cash_new == player_cash_old + amount
    ), f"Cash not added to the user correctly. {bank_cash_new} == ({bank_cash_old} - {amount})"


def test_bank_withdraw():
    """Verify the behavior of the withdraw() function in the Bank"""
    game = main.Game()
    bank_cash_old = game.bank.cash

    main.PlayerBase("TestPlayer", game)

    assert game.bank.cash == bank_cash_old - 1500


def test_bank_deposit():
    """Verify the behavior of the deposit() function in the Bank"""
    game = main.Game()
    bank_cash_old = game.bank.cash

    game.bank.deposit(50)

    assert bank_cash_old == game.bank.cash - 50


def test_chance_scramble():
    """Verify the order of the cards is different on loading when scramble == True"""
    chance1 = landings.Chance(scramble=True)
    chance2 = landings.Chance(scramble=True)

    assert chance1.cards != chance2.cards


def test_chance_select_and_place_card():
    """Verify the card selected is placed at the bottom"""
    chance = landings.Chance()
    second_to_last_card = chance.cards[0]

    # Find a non "Get out of jail free" card for the test
    # "Get out of jail free" cards are not placed back into the stack
    selected_card = chance.select_card()
    while selected_card.id == chance.GET_OUT_OF_JAIL_FREE:
        selected_card = chance.select_card()

    last_card = chance.cards[0]  # Manually get the card at the bottom of the stack
    assert last_card == selected_card
    assert second_to_last_card != selected_card


def test_chance_select_and_keep_card():
    """Verify the card selected is not placed at the bottom"""
    chance = landings.Chance()

    # Find a "Get out of jail free" card for the test
    # "Get out of jail free" cards are not placed back into the stack
    selected_card = chance.select_card()
    while selected_card.id != chance.GET_OUT_OF_JAIL_FREE:
        selected_card = chance.select_card()

    last_card = chance.cards[0]  # Manually get the card at the bottom of the stack
    assert last_card != selected_card


def test_community_chest_scramble():
    """Verify the order of the cards is different on loading when scramble == True"""
    community_chest1 = landings.Chance(scramble=True)
    community_chest2 = landings.Chance(scramble=True)

    assert community_chest1.cards != community_chest2.cards


def test_community_chest_select_and_place_card():
    """Verify the card selected is placed at the bottom"""
    community_chest = landings.CommunityChest()
    second_to_last_card = community_chest.cards[0]

    # Find a non "Get out of jail free" card for the test
    # "Get out of jail free" cards are not placed back into the stack
    selected_card = community_chest.select_card()
    while selected_card.id == community_chest.GET_OUT_OF_JAIL_FREE:
        selected_card = community_chest.select_card()

    last_card = community_chest.cards[
        0
    ]  # Manually get the card at the bottom of the stack
    assert last_card == selected_card
    assert second_to_last_card != selected_card


def test_community_chest_select_and_keep_card():
    """Verify the card selected is not placed at the bottom"""
    community_chest = landings.Chance()

    # Find a "Get out of jail free" card for the test
    # "Get out of jail free" cards are not placed back into the stack
    selected_card = community_chest.select_card()
    while selected_card.id != community_chest.GET_OUT_OF_JAIL_FREE:
        selected_card = community_chest.select_card()

    last_card = community_chest.cards[
        0
    ]  # Manually get the card at the bottom of the stack
    assert last_card != selected_card


def test_player_get_out_of_jail_free_cards():
    """Verify the get_out_of_jail_free_cards() func only returns the right type of cards"""
    game = main.Game()
    game.add_player("TestPlayer1", main.DefaultPlayer)
    game.current_player = game.players[0]

    # Get card examples
    chance_jail_card = [
        c
        for c in game.board.chance.cards
        if c.id == game.board.chance.GET_OUT_OF_JAIL_FREE
    ][0]
    community_chest_jail_card = [
        c
        for c in game.board.community_chest.cards
        if c.id == game.board.community_chest.GET_OUT_OF_JAIL_FREE
    ][0]
    chance_other_card = [
        c
        for c in game.board.chance.cards
        if c.id == game.board.chance.ADVANCE_TO_NEAREST_RAILROAD
    ][0]

    # Give the player cards including one that is not a jail card
    # which will be filtered out by the method we are testing
    chance_jail_card.owner = game.current_player
    community_chest_jail_card.owner = game.current_player
    # TODO replace with a card that makes sense like a property
    chance_other_card.owner = game.current_player

    player_jail_cards = game.current_player.get_out_of_jail_free_cards

    assert chance_other_card in game.board.get_cards_by_owner(game.current_player)
    assert chance_jail_card in player_jail_cards
    assert community_chest_jail_card in player_jail_cards


def test_player_withdraw_success():
    """
    Verify withdrawing money from the users bank removes the amount from their cash flow
    and returns the correct amount
    """
    game = main.Game()
    game.add_player("TestPlayer1", main.DefaultPlayer)
    game.current_player = game.players[0]

    cash = game.current_player.cash

    amount = 50
    returned_amount = game.current_player.withdraw(amount)

    assert returned_amount == amount
    assert cash - amount == game.current_player.cash


def test_player_withdraw_fail():
    """
    Verify withdrawing money from the users bank when they don't have enough money
    returns None and does not effect their cash flow
    """
    game = main.Game()
    game.add_player("TestPlayer1", main.DefaultPlayer)
    game.current_player = game.players[0]

    game.current_player.cash = 49
    cash = game.current_player.cash

    amount = 50
    returned_amount = game.current_player.withdraw(amount)

    assert returned_amount is None
    assert cash == game.current_player.cash
