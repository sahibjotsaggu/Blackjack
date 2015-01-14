from graphics import *
from random import *
import os, time

class PlayerBank:
    __bet_amount = 0

    def __init__(self, money):
        self.money = money

    def get_balance(self):
        return self.money

    def lose_money(self, amount):
        self.money -= amount

    def add_money(self, amount):
        self.money += amount

    def bet_amount(self, amount):
        PlayerBank.__bet_amount += amount

    def get_bet_amt(self):
        return PlayerBank.__bet_amount

    def bet_reset(self):
        PlayerBank.__bet_amount = 0

# CREATE A STATUS CLASS
class Status:
    def __init__(self, statTxt):
        self.statTxt = statTxt

# initialize player object with an initial amount
player = PlayerBank(2000)

def main():
    try:
        win = GraphWin("Blackjack", 600, 450)
        #win.setBackground(color_rgb(35,158,17))
        win.setBackground(color_rgb(75,196,45))

        statusBar = Rectangle(Point(8,420), Point(595,445))
        statusBar.setFill(color_rgb(255, 255, 255))
        statusBar.draw(win)
        status = Text(Point(302,433), "Bet an amount by clicking the appropriate token(s).")
        status.draw(win)

        # makes the card at the top-right corner, for design
        cornerCard(win)

        token_positions, token_values, token_colours = tokens(win)
        token_circle(win)
        start_button = Rectangle(Point(490,365), Point(590,390))
        start_button.setFill(color_rgb(75,164,55))
        start_button.draw(win)
        start_button_txt = Text(Point(540,378), "Deal")
        start_button_txt.setStyle('bold')
        start_button_txt.draw(win)

        # show player amount on screen
        player_amount_txt = Text(Point(65,240), "Player: $ " + str(player.get_balance()))
        player_amount_txt.setStyle('bold')
        player_amount_txt.draw(win)

        player_bet_amt_txt = Text(Point(65, 30), "Bet: $0")
        player_bet_amt_txt.setStyle('bold')
        player_bet_amt_txt.draw(win)


        # place bet amount by choosing tokens...
        choose_bet(win, token_positions, token_values, token_colours, player_amount_txt, player_bet_amt_txt, status)
        start_button_txt.undraw()
        start_button.undraw()

        # all betting and initializing stuff is over, so start the actual game..
        startGame(win, status, player_bet_amt_txt, player_amount_txt)


        win.getMouse()
        win.close()
    # this try-except statement takes care of the user closing the window at any time
    # during the operation of this program
    except GraphicsError:
        win.close()


def startGame(win, status, player_bet_amt_txt, player_amount_txt):
    # drawing the  'Hit' button
    hit_button = Rectangle(Point(490,365), Point(590,390))
    hit_button.setFill(color_rgb(75,164,55))
    hit_button.draw(win)
    hit_button_txt = Text(Point(540,378), "Hit")
    hit_button_txt.setStyle('bold')
    hit_button_txt.draw(win)

    # drawing the 'Stand' button
    stand_button = Rectangle(Point(388,365), Point(488,390))
    stand_button.setFill(color_rgb(255,0,0))
    stand_button.draw(win)
    stand_button_txt = Text(Point(438,378), "Stand")
    stand_button_txt.setStyle('bold')
    stand_button_txt.draw(win)


    # this is where all the cards that have been dealt out go into
    # after each game is over, these cards will be put back into 'cards_list'
    temp_card_list, playerCVal, dealerCVal, dealer_card_2_val, player_x, dealer_x, cards_list, pVal_txt, dVal_txt = deal_initial_cards(win)
    winner_val = blackjack_check(playerCVal, dealerCVal + dealer_card_2_val)
    # if the player got blackjack
    if winner_val == 0:
        print("Player got Blackjack!")
        dealing = show_dealer_cards(win, temp_card_list, cards_list, player_x, pVal_txt, "player")
        # if the player has decided to deal again
        if dealing:
            # player wins the bet
            p_gets_money_or_no(player_bet_amt_txt, player_amount_txt, "yes")
            # close the window and start it again for the next hand
            win.close()
            # this is where the use of classes and objects comes in handy:
            #   without using OOP, I would have to reintialize all the variables
            #   that keep track of the player's betting and total money and then
            #   find a way perhaps through the use of files to save them so when
            #   the window closes, i don't lose that info.
            #   Using classes helps because even though the window is closed,
            #   the 'blackjack.py' program is still running (closing the window)
            #   was just an instruction given to the program to reset it
            main()
        else:
            win.close()
            end_game(True)

    # if the dealer got blackjack
    elif winner_val == 1:
        dealing = show_dealer_cards(win, temp_card_list, cards_list, dealer_x, dVal_txt, "dealer")
        if dealing:
            print("DEALING AGAIN!")
            # dealer wins the bet
            p_gets_money_or_no(player_bet_amt_txt, player_amount_txt, "no")
            win.close()
            main()
        else:
            win.close()
            end_game(False)

    # if no one got blackjack
    else:
        if playerCVal == dealerCVal + dealer_card_2_val:
            push_game(win, dVal_txt, dealerCVal + dealer_card_2_val, temp_card_list, cards_list, dealer_x, status)
        else:
            print("No one got Blackjack!")

def end_game(winner):
    win = GraphWin("Blackjack - End Game", 300, 160)
    win.setBackground(color_rgb(75,196,45))
    farewell_msg1 = Text(Point(150,40), "It was a great pleasure")
    farewell_msg2 = Text(Point(150,70), "playing with you!")
    farewell_msg1.setSize(18)
    farewell_msg2.setSize(18)
    farewell_msg1.setStyle('bold')
    farewell_msg2.setStyle('bold')
    farewell_msg1.draw(win)
    farewell_msg2.draw(win)
    if winner:
        tot_earn = Text(Point(150,120), "Total Earnings: ${0}".format(player.get_balance() + (player.get_bet_amt()*2)))
    else:
        tot_earn = Text(Point(150,120), "Total Earnings: ${0}".format(player.get_balance()))
    tot_earn.setSize(15)
    tot_earn.draw(win)
    win.getMouse()
    win.close()

# the variable 'pgmon' means 'player gets money or not?'
def p_gets_money_or_no(player_bet_amt_txt, player_amount_txt, pgmon):
    if pgmon == "yes":
        # adding two times the bet amount for the player because the player won
        player.add_money(player.get_bet_amt() * 2)
        player_amount_txt.setText("Player: $ " + str(player.get_balance()))

        # making the bet amount of the player equal to $0 in preperation for the next hand
        player.bet_reset()
        player_bet_amt_txt.setText("Bet: $ " + str(player.get_bet_amt()))
    else:
        # making the bet amount of the player equal to $0 in preperation for the next hand
        player.bet_reset()
        player_bet_amt_txt.setText("Bet: $ " + str(player.get_bet_amt()))
        # NOTE: the player's money doesn't change because:
        #   it had already been taken when betting and now that the player has lost
        #   their bet, they don't get it back

def show_dealer_cards(win, temp_card_list, cards_list, dealer_x, dVal_txt, winner):
    Image(Point(dealer_x-20, 100), "Cards/"+temp_card_list[3]).draw(win)
    dVal_txt.setText("21")
    deal_again = deal_again_dialog(winner)
    return deal_again

def deal_again_dialog(winner):
    win = GraphWin("Deal Again?", height=90)
    if winner == "dealer":
        show_txt1 = Text(Point(100,20), "The dealer has won.")
        show_txt2 = Text(Point(100,35), "You lose the game.")
    else:
        show_txt1 = Text(Point(100,20), "Congratulations!")
        show_txt2 = Text(Point(100,35), "You win this hand!")
    show_txt1.setSize(10)
    show_txt2.setSize(10)
    show_txt1.draw(win)
    show_txt2.draw(win)

    # play again button
    deal_again_txt1 = Text(Point(50, 60), "Deal")
    deal_again_txt2 = Text(Point(50, 75), "Again")
    deal_again_txt1.setSize(10)
    deal_again_txt2.setSize(10)
    deal_button = Rectangle(Point(5,50), Point(95,85))
    deal_button.setFill(color_rgb(89,255,0))
    deal_button.draw(win)
    deal_again_txt1.draw(win)
    deal_again_txt2.draw(win)
    # close button
    close_txt = Text(Point(150, 67.5), "End Game")
    close_txt.setSize(10)
    close_button = Rectangle(Point(105,50), Point(195,85))
    close_button.setFill(color_rgb(255,63,0))
    close_button.draw(win)
    close_txt.draw(win)
    get_choice = win.getMouse()
    get_choiceX = get_choice.getX()
    get_choiceY = get_choice.getY()
    if get_choiceX > 105 and get_choiceX < 195 and get_choiceY > 50 and get_choiceY < 85:
        win.close()
    else:
        win.close()
        return True

def push_game(win, dVal_txt, dealer_total_val, temp_card_list, cards_list, dealer_x, status):
    status.setText("The game has been pushed! No one wins.")
    if dealer_total_val == 21:
        dVal_txt.setText("21")
        Image(Point(dealer_x-20, 100), "Cards/"+temp_card_list[3]).draw(win)
        player.add_money(player.get_bet_amt())
        player.bet_reset()
    else:
        dVal_txt.setText(str(dealer_total_val))
        Image(Point(dealer_x-20, 100), "Cards/"+temp_card_list[3]).draw(win)
        player.add_money(player.get_bet_amt())
        player.bet_reset()
    temp_cards_to_main_card_lst(temp_card_list, cards_list)
    shuffle_deck(cards_list)

def shuffle_deck(cards_list):
    for shuffling in range(500):
        shuffle(cards_list)

def temp_cards_to_main_card_lst(temp_card_list, cards_list):
    for card_num in range(len(temp_card_list)):
        cards_list.insert(0, temp_card_list[card_num])
    print(temp_card_list)
    print(cards_list)

def blackjack_check(playerCVal, dealerCVal):
    # if both have blackjack, then it is a 'push'
    if playerCVal == dealerCVal and playerCVal== 21:
        return 2
    else:
        # if the player got blackjack
        if playerCVal == 21:
            return 0
        # if the dealer for blackjack
        elif dealerCVal == 21:
            return 1
        # if no one got blackjack
        else:
            return 2

def deal_initial_cards(win):
    temp_card_list = []
    cards_list = get_cards_list()
    player_x, player_y = 300, 300
    dealer_x, dealer_y = 300, 100
    for init_deal in range(1,5):
        # this makes sure to deal the cards alternating from player to dealer
        if init_deal%2 == 0:
            if init_deal == 4:
                Image(Point(dealer_x, dealer_y), "Cards/cDown.gif").draw(win)
                dealer_x += 20
                temp_card_list.append(cards_list[0])
                del cards_list[0]
            else:
                Image(Point(dealer_x, dealer_y), "Cards/"+cards_list[0]).draw(win)
                dealer_x += 20
                temp_card_list.append(cards_list[0])
                del cards_list[0]
        else:
            Image(Point(player_x, player_y), "Cards/"+cards_list[0]).draw(win)
            player_x += 20
            temp_card_list.append(cards_list[0])
            del cards_list[0]
        time.sleep(0.25)

    # the following four lines get the value from the start of the
    # picture filename to the 'o' in ...'of'...
    pCard1 = temp_card_list[0][:temp_card_list[0].index('o')]
    pCard2 = temp_card_list[2][:temp_card_list[2].index('o')]
    dCard1 = temp_card_list[1][:temp_card_list[1].index('o')]
    dCard2 = temp_card_list[3][:temp_card_list[3].index('o')]

    dealer_card_2_val = get_sec_card_val(dCard2)

    playerCVal = count_initial_card_value(pCard1, pCard2)
    dealerCVal = count_initial_card_value(dCard1, dCard2) - dealer_card_2_val
    # the value of the dealer's second card is being removed because the dealer's
    # second card is face down in the beginning
    pVal_txt, dVal_txt = draw_value(win, playerCVal, dealerCVal)
    return temp_card_list, playerCVal, dealerCVal, dealer_card_2_val, player_x, dealer_x, cards_list, pVal_txt, dVal_txt

# returns the value of the dealer's second card so it can be removed from
# the initial total while still being saved for later use
def get_sec_card_val(dCard2):
    dealer_card_2 = 0
    # check to see if the card is a number or letter
    # if number...
    if dCard2.isnumeric():
        dealer_card_2 += int(dCard2)
    # if letter..
    else:
        # special case if card is 'ace'
        if dCard2 == "A":
            dealer_card_2 += 11
        else:
            dealer_card_2 += 10
    return dealer_card_2

def draw_value(win, playerCVal, dealerCVal):
    pVal_Box = Rectangle(Point(233,285), Point(263,315))
    pVal_Box.setFill(color_rgb(255,255,255))
    pVal_Box.draw(win)

    dVal_Box = Rectangle(Point(233,85), Point(263,115))
    dVal_Box.setFill(color_rgb(255,255,255))
    dVal_Box.draw(win)

    pVal_txt = Text(Point(248,300), str(playerCVal))
    dVal_txt = Text(Point(248,100), str(dealerCVal))
    pVal_txt.setStyle('bold')
    dVal_txt.setStyle('bold')
    pVal_txt.draw(win)
    dVal_txt.draw(win)
    return pVal_txt, dVal_txt

# count the value of the initial two cards
def count_initial_card_value(card_one, card_two):
    card_total = 0
    # card 1
    # check to see if the card is a number or letter
    # if number...
    if card_one.isnumeric():
        card_total += int(card_one)
    # if letter..
    else:
        # special case if card is 'ace'
        if card_one == "A":
            card_total += 11
        else:
            card_total += 10
    # card 2
    # check to see if the card is a number or letter
    # if number...
    if card_two.isnumeric():
        card_total += int(card_two)
    # if letter..
    else:
        # special case if card is 'ace'
        if card_one == "A" and card_two == "A":
            card_total += 1
        elif card_two == "A": # this is only true if card_one is not 'A'
            card_total += 11
        else:
            card_total += 10
    return card_total

def get_cards_list():
    #path = "Cards/"
    #cards_list = os.listdir(path)
    #cards_list.remove("cDown.gif")
    # check to see if the 'Thumbs.db' file is in the cards_list and if it is,
    # it must be deleted because it is not a card that needs to be selected
    #if "Thumbs.db" in cards_list:
    #    cards_list.remove("Thumbs.db")
    cards_list = ['AofS.gif', 'AofD.gif', 'KofD.gif', '2ofC.gif']
    # shuffle the cards list 500 times
    #for shuffling in range(500):
    #    shuffle(cards_list)
    return cards_list


def choose_bet(win, token_positions, token_values, token_colours, player_amount_txt, player_bet_amt_txt, status):
    stop_betting = False
    while stop_betting == False:
        click = win.getMouse()
        clickX = click.getX()
        clickY = click.getY()
        for this_token in range(len(token_positions)):
            if clickX > token_positions[this_token][0] - 30 and clickX < token_positions[this_token][0] + 30 and clickY > token_positions[this_token][1] - 30 and clickY < token_positions[this_token][1] + 30:
                # if the player has more than $0 after betting (or equal to 0)
                if player.get_balance() - int(token_values[this_token]) >= 0:
                    # Empty the status bar of any error messages.
                    status.setText("")
                    # choosing random x and y values for the tokens to be randomly placed on the token circle
                    rand_x = randint(50,130)
                    rand_y = randint(90,170)
                    tok_pos = this_token
                    draw_token(win, token_values[this_token], rand_x, rand_y, token_colours, tok_pos)
                    # updating the player object's '__bet_amount' class variable and the
                    player.lose_money(int(token_values[this_token]))
                    player.bet_amount(int(token_values[this_token]))
                    player_bet_amt_txt.setText("Bet: $ " + str(player.get_bet_amt()))
                    player_amount_txt.setText("Player: $ " + str(player.get_balance()))
                else:
                    status.setText("You do not have enough money to bet more.")

            else:
                # when the user presses the 'Deal' button after betting
                if clickX > 490 and clickX < 590 and clickY > 365 and clickY < 390:
                    if player.get_bet_amt() != 0:
                        stop_betting = True
                    else:
                        status.setText("Please make a bet before starting the game.")

# drawing the selected token (for the betting) onto the
# token circle at a random coordinate inside it
def draw_token(win, token_value, x_coor, y_coor, token_colours, tok_pos):
    temp_token = Circle(Point(x_coor, y_coor), 30)
    temp_token.setFill(color_rgb(token_colours[tok_pos][0], token_colours[tok_pos][1], token_colours[tok_pos][2]))
    temp_token.draw(win)
    temp_token.setWidth(0)
    inner_temp_token = Circle(Point(x_coor, y_coor), 20)
    inner_temp_token.setFill(color_rgb(255,255,255))
    inner_temp_token.setOutline(color_rgb(255,255,255))
    inner_temp_token.draw(win)
    temp_token_txt = Text(Point(x_coor, y_coor), str(token_value))
    temp_token_txt.setStyle('bold')
    temp_token_txt.draw(win)

def token_circle(win):
    token_circle = Circle(Point(90,130), 80)
    token_circle.setWidth(3)
    token_circle.setFill(color_rgb(35,158,17))
    token_circle.setOutline(color_rgb(178,231,178))
    token_circle.draw(win)

def cornerCard(win):
    x,y = 580,20
    showCard = Image(Point(x,y), "Cards/cDown.gif")
    shadow = Rectangle(Point(x-40, y-53), Point(x+30, y+43))
    shadow.setFill(color_rgb(0,103,0))
    shadow.setOutline(color_rgb(0,103,0))
    shadow.draw(win)
    showCard.draw(win)

def tokens(win):
    token_positions = [[40,300],[110,300],[60,365],[130,365]] # this is the same as the token_inner_circles
    token_colours = [[204,51,102],[72,229,48],[0,102,204],[204,0,0]]
    token_outline_colour = [0,164,0]
    token_values = ["1", "5", "25", "100"]
    for index in range(len(token_positions)):
        temp_token = Circle(Point(token_positions[index][0], token_positions[index][1]), 30)
        temp_token.setFill(color_rgb(token_colours[index][0], token_colours[index][1], token_colours[index][2]))
        temp_token.draw(win)
        temp_token.setWidth(0)
        inner_temp_token = Circle(Point(token_positions[index][0], token_positions[index][1]), 20)
        inner_temp_token.setFill(color_rgb(255,255,255))
        inner_temp_token.setOutline(color_rgb(255,255,255))
        inner_temp_token.draw(win)
        temp_token_txt = Text(Point(token_positions[index][0], token_positions[index][1]), token_values[index])
        temp_token_txt.setStyle('bold')
        temp_token_txt.draw(win)

    return token_positions, token_values, token_colours

main()
