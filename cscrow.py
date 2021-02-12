import threading
import schedule
import sched, time
from decimal import getcontext, Decimal
import datetime
import pprint
import json
import sqlite3
from telepot.helper import Editor
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ForceReply, ReplyKeyboardRemove
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from commonregex import CommonRegex
from coinbase.wallet.client import Client
import time
import telepot
from telepot.loop import MessageLoop
from telepot.delegate import pave_event_space, per_chat_id, create_open, include_callback_query_chat_id

conn = sqlite3.connect('trading.db')
cur = conn.cursor()

api_key = 'YB3b7ksR1CUMpe0Q'
api_secret = 'mduoq77vHOAgIzIykD3OKJNXIzriI2iU'

client = Client(api_key, api_secret)

ad = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="I want to BUY Bitcoin")],
    [KeyboardButton(text="I want to SELL Bitcoin")],
    [KeyboardButton(text="Cancel")],

], resize_keyboard=True)

badvert = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="BankTransfer (Buy)"), KeyboardButton(text="CashDeposit (Buy)")],
    [KeyboardButton(text="iTunesGiftCards (Buy)"), KeyboardButton(text="PerfectMoney (Buy)")],
    [KeyboardButton(text="AdvancedCash (Buy)"), KeyboardButton(text="Neteller (Buy)")],
    [KeyboardButton(text="Payza (Buy)"), KeyboardButton(text="OKPay (Buy)")],
    [KeyboardButton(text="Skrill (Buy)"), KeyboardButton(text="Webmoney (Buy)")],
    [KeyboardButton(text="Alipay (Buy)"), KeyboardButton(text="AmazonGiftCards (Buy)")],
    [KeyboardButton(text="WesternUnion (Buy)"), KeyboardButton(text="MoneyGram (Buy)")],
    [KeyboardButton(text="back↩")],
])

sadvert = ReplyKeyboardMarkup(keyboard=[

    [KeyboardButton(text="BankTransfer (Sell)"), KeyboardButton(text="CashDeposit (Sell)")],
    [KeyboardButton(text="iTunesGiftCards (Sell)"), KeyboardButton(text="PerfectMoney (Sell)")],
    [KeyboardButton(text="AdvancedCash (Sell)"), KeyboardButton(text="Neteller (Sell)")],
    [KeyboardButton(text="Payza (Sell)"), KeyboardButton(text="OKPay (Sell)")],
    [KeyboardButton(text="Skrill (Sell)"), KeyboardButton(text="Webmoney (Sell)")],
    [KeyboardButton(text="Alipay (Sell)"), KeyboardButton(text="AmazonGiftCards (Sell)")],
    [KeyboardButton(text="WesternUnion (Sell)"), KeyboardButton(text="MoneyGram (Sell)")],
    [KeyboardButton(text="back↩")],
])

payment = InlineKeyboardMarkup(inline_keyboard=[

    [InlineKeyboardButton(text='BankTransfer', callback_data='BankTransfer bst')],
    [InlineKeyboardButton(text='CashDeposit', callback_data='CashDeposit bst')],
    [InlineKeyboardButton(text='iTunesGiftCards', callback_data='iTunesGiftCards bst')],
    [InlineKeyboardButton(text='PerfectMoney', callback_data='PerfectMoney bst')],
    [InlineKeyboardButton(text='AdvancedCash', callback_data='AdvancedCash bst')],
    [InlineKeyboardButton(text='Neteller', callback_data='Neteller bst')],
    [InlineKeyboardButton(text='Payza', callback_data='Payza bst')],
    [InlineKeyboardButton(text='Cancel', callback_data='main'),
     InlineKeyboardButton(text='Next', callback_data='next')],
])

payment1 = InlineKeyboardMarkup(inline_keyboard=[

    [InlineKeyboardButton(text='OKPay', callback_data='OKPay bst')],
    [InlineKeyboardButton(text='Skrill', callback_data='Skrill bst')],
    [InlineKeyboardButton(text='WebMoney', callback_data='WebMoney bst')],
    [InlineKeyboardButton(text='Alipay', callback_data='Alipay bst')],
    [InlineKeyboardButton(text='AmazonGiftCards', callback_data='AmazonGiftCards bst')],
    [InlineKeyboardButton(text='WesternUnion', callback_data='WesternUnion bst')],
    [InlineKeyboardButton(text='MoneyGram', callback_data='MoneyGram bst')],
    [InlineKeyboardButton(text='Cancel', callback_data='main'),
     InlineKeyboardButton(text='Previous', callback_data='prev')],
])

paysell = InlineKeyboardMarkup(inline_keyboard=[

    [InlineKeyboardButton(text='BankTransfer', callback_data='BankTransfer tq')],
    [InlineKeyboardButton(text='CashDeposit', callback_data='CashDeposit tq')],
    [InlineKeyboardButton(text='iTunesGiftCards', callback_data='iTunesGiftCards tq')],
    [InlineKeyboardButton(text='PerfectMoney', callback_data='PerfectMoney tq')],
    [InlineKeyboardButton(text='AdvancedCash', callback_data='AdvancedCash tq')],
    [InlineKeyboardButton(text='Neteller', callback_data='Neteller tq')],
    [InlineKeyboardButton(text='Payza', callback_data='Payza tq')],
    [InlineKeyboardButton(text='Cancel', callback_data='main'), InlineKeyboardButton(text='Next', callback_data='nxt')],
])

paysell1 = InlineKeyboardMarkup(inline_keyboard=[

    [InlineKeyboardButton(text='OKPay', callback_data='OKPay tq')],
    [InlineKeyboardButton(text='Skrill', callback_data='Skrill tq')],
    [InlineKeyboardButton(text='WebMoney', callback_data='WebMoney tq')],
    [InlineKeyboardButton(text='Alipay', callback_data='Alipay tq')],
    [InlineKeyboardButton(text='AmazonGiftCards', callback_data='AmazonGiftCards tq')],
    [InlineKeyboardButton(text='WesternUnion', callback_data='WesternUnion tq')],
    [InlineKeyboardButton(text='MoneyGram', callback_data='MoneyGram tq')],
    [InlineKeyboardButton(text='Cancel', callback_data='main'),
     InlineKeyboardButton(text='Previous', callback_data='prv')],
])

curency = InlineKeyboardMarkup(inline_keyboard=[

    [InlineKeyboardButton(text='USD', callback_data='USD z'), InlineKeyboardButton(text='GBP', callback_data='GBP z'),
     InlineKeyboardButton(text='EUR', callback_data='EUR z'), InlineKeyboardButton(text='CNY', callback_data='CNY z')],
    [InlineKeyboardButton(text='RUB', callback_data='RUB z'), InlineKeyboardButton(text='BRL', callback_data='BRL z'),
     InlineKeyboardButton(text='MYR', callback_data='MYR z'), InlineKeyboardButton(text='UAH', callback_data='UAH z')],
    [InlineKeyboardButton(text='UZS', callback_data='UZS z'), InlineKeyboardButton(text='BYR', callback_data='BYR z'),
     InlineKeyboardButton(text='NGN', callback_data='NGN z'), InlineKeyboardButton(text='TRY', callback_data='TRY z')],
    [InlineKeyboardButton(text='VND', callback_data='VND z'), InlineKeyboardButton(text='AUD', callback_data='AUD z'),
     InlineKeyboardButton(text='ARS', callback_data='ARS z'), InlineKeyboardButton(text='CAD', callback_data='CAD z')],
    [InlineKeyboardButton(text='HTG', callback_data='HTG z'), InlineKeyboardButton(text='MXN', callback_data='MXN z'),
     InlineKeyboardButton(text='NZD', callback_data='NZD z'), InlineKeyboardButton(text='SEK', callback_data='SEK z')],
    [InlineKeyboardButton(text='IDR', callback_data='IDR z'), InlineKeyboardButton(text='IRR', callback_data='IRR z'),
     InlineKeyboardButton(text='AFN', callback_data='AFN z'), InlineKeyboardButton(text='INR', callback_data='INR z')],
    [InlineKeyboardButton(text='KZT', callback_data='KZT z'), InlineKeyboardButton(text='AMD', callback_data='AMD z'),
     InlineKeyboardButton(text='KES', callback_data='KES z'), InlineKeyboardButton(text='CLP', callback_data='CLP z')],
    [InlineKeyboardButton(text='⬅Back', callback_data='bck')],
])
changeafter = InlineKeyboardMarkup(inline_keyboard=[

    [InlineKeyboardButton(text='💵Change your currency', callback_data='currency')],
    [InlineKeyboardButton(text='🔬Verification', callback_data='verify')],
    [InlineKeyboardButton(text='📱Add Contact', callback_data='contact')],
])

after = InlineKeyboardMarkup(inline_keyboard=[

    [InlineKeyboardButton(text='💵Select currency', callback_data='currency')],
    [InlineKeyboardButton(text='📈Buy Bitcoin', callback_data='buy'),
     InlineKeyboardButton(text='📉Sell Bitcoin', callback_data='seller')],
])
open_deal = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔓Open deal', callback_data='dealing')],
])
close_deal = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔓Open deal', callback_data='dealout')],
])

start_deal = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Yes', callback_data='yes'), InlineKeyboardButton(text='No', callback_data='no')],
])
user_deal = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Yes', callback_data='yup'), InlineKeyboardButton(text='No', callback_data='nope')],
])

more_info = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Affilliate👨‍👨‍👦', callback_data='aff'),
     InlineKeyboardButton(text='Community🌐', callback_data='comm')],
    [InlineKeyboardButton(text='Terms📋', callback_data='terms'),
     InlineKeyboardButton(text='Support📞', callback_data='support')],
])

check_info = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='I have received the funds', callback_data='donefund')],

])

check_info1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='I have received the funds', callback_data='donefund')],
    [InlineKeyboardButton(text='Dispute', callback_data='meditate')],
])

check_receive = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='I have sent the funds', callback_data='checkdone')],
])
check_receive1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='I have sent the funds', callback_data='checkdone')],
    [InlineKeyboardButton(text='Dispute', callback_data='meditate')],
])

markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Wallet💼"), KeyboardButton(text="Buy/Sell BTC📊")],
    [KeyboardButton(text="About📱"), KeyboardButton(text="Settings⚙")],
], resize_keyboard=True)

back = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀back")]], resize_keyboard=True)

go = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="back")]], resize_keyboard=True)

test = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='✅I Agree')]], resize_keyboard=True)

dw = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Deposit⏫', callback_data='dep'),
     InlineKeyboardButton(text='Withdraw⏬', callback_data='with')],
    [InlineKeyboardButton(text='Reports📋', callback_data='rep')],
])

buymes = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Send Message', callback_data='buymes')],

])
sellmes = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Send Message', callback_data='sellmes')],

])

chang1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Margin💲', callback_data='marg'),
     InlineKeyboardButton(text='Limits↔️', callback_data='limit'),
     InlineKeyboardButton(text='Deactivate❌', callback_data='deactivate')],
    [InlineKeyboardButton(text='Terms', callback_data='term_s')],
    [InlineKeyboardButton(text='Delete Ad🗑', callback_data='delad')],
])
chang2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Margin💲', callback_data='marg'),
     InlineKeyboardButton(text='Limits↔️', callback_data='limit'),
     InlineKeyboardButton(text='Activate✅', callback_data='activate')],
    [InlineKeyboardButton(text='Terms', callback_data='term_s')],
    [InlineKeyboardButton(text='Delete Ad🗑', callback_data='delad')],
])

buse = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Buy📈', callback_data='buy'),
     InlineKeyboardButton(text='Sell📉', callback_data='seller')],
    [InlineKeyboardButton(text='Select Currency💵', callback_data='currency')],
    [InlineKeyboardButton(text='My adverts', callback_data='myadvert')],

    [InlineKeyboardButton(text='Add an Advert📋', callback_data='advert')],
])

markup_set = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Edit Withdraw Address")],

    [KeyboardButton(text="back🏠")],
], resize_keyboard=True)

admin = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Message User"), KeyboardButton(text="Search User")],
    [KeyboardButton(text="Ban User"), KeyboardButton(text="Verify User")],

], resize_keyboard=True)


class TradingBot(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(TradingBot, self).__init__(*args, **kwargs)
        global currentDate
        global counter, counter1, counter2
        self.counter = 0
        self.counter1 = 0
        self.counter2 = 0

    def order_type(self, ordertype):
        global order
        if ordertype == 'buy':
            order = 'buy'
        elif ordertype == 'sell':
            order = 'sell'
        elif ordertype == 'exb':
            order = 'exb'
        elif ordertype == 'exs':
            order = 'exs'

    def advert_type(self, adverttype):
        global advertt
        self.advertt = adverttype

    def gateway_type(self, gate_way):
        global gateway
        gateway = gate_way

    def fixed_price(self, fixed):
        global price_tag
        price_tag = fixed

    def margin_percent(self, percent):
        global margin
        self.margin = percent

    def currency(self, chatid):

        self.conn = sqlite3.connect('trading.db')
        self.cur = self.conn.cursor()
        from exchanges.coindesk import CoinDesk
        currency_cod = self.cur.execute('SELECT currency FROM Investor WHERE investor=(?)', (chatid,))
        self.bal = currency_cod.fetchone()[0]
        t = CoinDesk().get_current_price(currency="{}".format(self.bal))
        mult_price = (round(float(t), 2))

        self.conn.commit()
        # self.cur.close()
        return mult_price

    def current(self, currency):
        from exchanges.coindesk import CoinDesk
        t = CoinDesk().get_current_price(currency="{}".format(currency))
        mult_price = (round(t, 2))
        self.conn.commit()
        return mult_price

    def currency_code(self, chatid):
        self.conn = sqlite3.connect('trading.db')
        self.cur = self.conn.cursor()
        currency_cod = self.cur.execute('SELECT currency FROM Investor WHERE investor=(?)', (chatid,))
        bal = currency_cod.fetchone()[0]

        self.conn.commit()
        # self.cur.close()
        return bal

    def currency_update(self, currencycode, chatid):
        self.conn = sqlite3.connect('trading.db')
        self.cur = self.conn.cursor()
        self.cur.execute('UPDATE Investor SET currency =(?) WHERE investor=(?)',
                         (currencycode, chatid))
        self.conn.commit()
        # self.cur.close()

    def on_chat_message(self, msg):
        global chat_id
        global banned
        content_type, chat_type, chat_id = telepot.glance(msg)
        self.conn = sqlite3.connect('trading.db')
        self.cur = self.conn.cursor()

        # from pprint import pprint
        # pprint(msg)

        global command
        try:
            command = msg['text']
        except Exception:
            command = 'nothing'
            banned = 0

        try:
            cmdphoto = msg['photo']
            for i in cmdphoto:
                print(i)
            global photoverify
            photoverify = (i.get('file_id'))

        except Exception:
            pass

        try:

            checkban = self.cur.execute('SELECT ban FROM Investor WHERE investor=(?)', (self.chat_id,))
            banned = checkban.fetchone()[0]
        except Exception:
            pass

        try:
            global cmd
            cmd = msg['reply_to_message']['text']

        except Exception:
            pass

        try:
            if command == '/mainmenu':
                self.sender.sendMessage("Main Menu", reply_markup=markup)

            else:
                if cmd == 'Please upload photo for verification':
                    # if command != '/menu':
                    try:
                        bot.sendPhoto('234578692', photoverify)

                        yty = self.chat_id
                        bot.sendMessage(yty,
                                        "Photo was successfully sent\nIf you are verified your account status will change to verified",
                                        reply_markup=markup)
                        bot.sendMessage('234578692', "To verify this user press /verify {}".format(yty))

                    except Exception:
                        pass


        except Exception:
            pass
        global checkers

        # =====================================================================================================================================


        # =====================================================================================================================================

        if command.startswith('/start') or command == '/start' and banned == 0:  # Message (incoming) 1 sent by user
            self.user = bot.getChat(self.chat_id)
            firstname = self.user.get('first_name')
            user_name = self.user.get('username')
            now = datetime.date.today()
            self.cur.execute(
                'INSERT OR IGNORE INTO Investor (investor,username,balance,newbalance, deposit,withdraw,out,commission,newcommission,ncommission,cout,date,currency,deal,worth,verification,goodreviews,badreviews,done,ban,contact) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                (
                    self.chat_id, firstname, 0.0, 0.0, 'none', 'none', 0, 0, 0, 0, 0, now, 'USD', 0, 0, "❌", 0, 0, 0, 0,
                    0))
            self.conn.commit()
            self.sender.sendMessage(
                """Welcome to Cryptoscrow Bot, please confirm that you have read and agreed to *Terms of Service*\n""",
                parse_mode='Markdown', reply_markup=test)
            self.sender.sendDocument('BQADBAADiAIAAtB74FBh_9SPlj_RJQI')
            self.sender.sendDocument('BQADBAADEgMAAuVRWFC3RITtJ9-HuwI')
            self.sender.sendDocument('BQADBAADhwIAAtB74FCZfdx6gh0g8AI')

            try:
                with_i = self.cur.execute('SELECT ref FROM Affiliate ', )
                with_n = with_i.fetchall()
                aft = []
                for record in with_n:
                    for i in record:
                        aft.append(i)
                if self.chat_id in aft:
                    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
                else:
                    self.cur.execute('INSERT OR IGNORE INTO Affiliate (owner,ref) VALUES (?,?)',
                                     (command.split()[1], self.chat_id))
                    self.conn.commit()
            except Exception:
                print("User is under no one")
            print("User:", self.chat_id, "initiated the BOT")

        elif command == 'nothing':
            print("====================================================")
        elif command == '/mainmenu':
            print("====================================================")
        elif command == '/menu':
            self.sender.sendMessage("Main menu", reply_markup=markup)
        elif command == '/admin NJS-%HJHB515_bJK':
            self.sender.sendMessage("Welcome to the admin section.Here you can change some things about the bot",
                                    reply_markup=admin)

        elif command == ("Message User"):
            self.sender.sendMessage(
                "To send a message to a specific user through the bot press /send userid text\nTo send a message to all users press /send all text ")
        elif command == ("Ban User"):
            self.sender.sendMessage("To ban a user press /ban userid and to unban user press /unban userid")

        elif command == ("Verify User"):
            self.sender.sendMessage(
                "To verify a user press /verify userid and to remove verification user press /unverify userid")

        # =========================================================================================================================================================================

        elif command == '/redeem':
            newbala = self.cur.execute('SELECT newbalance FROM Investor WHERE investor=(?)', (self.chat_id,))
            newbl = newbala.fetchone()[0]
            com = self.cur.execute('SELECT commission FROM Investor WHERE investor=(?)', (self.chat_id,))
            com_ission = com.fetchone()[0]
            if float(com_ission) > 0.0000001:
                pricing = round((float(com_ission) + float(newbl)), 8)
                self.cur.execute('UPDATE Investor SET newbalance =(?) WHERE investor=(?)',
                                 ('{}'.format(pricing), self.chat_id))
                self.conn.commit()
                self.cur.execute('UPDATE Investor SET commission =(?) WHERE investor=(?)', (0.0, self.chat_id))
                self.conn.commit()
                self.sender.sendMessage("Your commission has been added to the balance and its ready for withdrawal")
            else:
                self.sender.sendMessage("Your dont have any commission to withdraw")

        elif banned != 1 and command == 'Wallet💼':
            user = bot.getChat(self.chat_id)

            firstname = user.get('first_name')
            user_name = user.get('username')

            self.cur.execute('UPDATE Investor SET username =(?) WHERE investor=(?)', (firstname, self.chat_id))
            self.conn.commit()

            deal = self.cur.execute('SELECT deal FROM Investor WHERE investor=(?)', (self.chat_id,))
            dl = deal.fetchone()[0]
            worth = self.cur.execute('SELECT worth FROM Investor WHERE investor=(?)', (self.chat_id,))
            wt = worth.fetchone()[0]
            verify = self.cur.execute('SELECT verification FROM Investor WHERE investor=(?)', (self.chat_id,))
            vf = verify.fetchone()[0]
            goodreview = self.cur.execute('SELECT goodreviews FROM Investor WHERE investor=(?)', (self.chat_id,))
            good = goodreview.fetchone()[0]
            badreview = self.cur.execute('SELECT badreviews FROM Investor WHERE investor=(?)', (self.chat_id,))
            bad = badreview.fetchone()[0]
            bala = self.cur.execute('SELECT balance FROM Investor WHERE investor=(?)', (self.chat_id,))
            bal = bala.fetchone()[0]
            item_d = self.cur.execute('SELECT deposit FROM Investor WHERE investor=(?)', (self.chat_id,))

            dep_addr = item_d.fetchone()[0]

            newbala = self.cur.execute('SELECT newbalance FROM Investor WHERE investor=(?)', (self.chat_id,))
            newbl = newbala.fetchone()[0]

            dat = self.cur.execute('SELECT date FROM Investor WHERE investor=(?)', (self.chat_id,))
            date_d = dat.fetchone()[0]

            comn = self.cur.execute('SELECT commission FROM Investor WHERE investor=(?)', (self.chat_id,))
            commi = comn.fetchone()[0]

            now = datetime.date.today()

            currentDate = datetime.datetime.strptime(date_d, '%Y-%m-%d').date()
            diff = now - currentDate
            dif = str(diff)
            days = dif.split()[0]

            if bal < (0.000001) and (len(dep_addr) > 26 and len(dep_addr) < 36):
                depp = self.cur.execute('SELECT deposit FROM Investor WHERE investor=(?)', (self.chat_id,))
                dep_o = depp.fetchone()[0]
                # trans = client.get_address_transactions("495d62e2-c289-5caf-abc0-bf147af57cda", '{}'.format(dep_o))
                trans = client.get_address_transactions("495d62e2-c289-5caf-abc0-bf147af57cda",
                                                        '1DRXecSHCQL8JkrpeXp7udSmVpFAjEpbkd')

                for tx in trans.data:

                    tr = tx.amount

                    true = '{}'.format(tr).split()[1]
                    self.cur.execute('UPDATE Investor SET balance =(?) WHERE investor=(?)',
                                     (true, self.chat_id))

                    bala = self.cur.execute('SELECT balance FROM Investor WHERE investor=(?)', (self.chat_id,))
                    bal = bala.fetchone()[0]

                    newbala = self.cur.execute('SELECT newbalance FROM Investor WHERE investor=(?)', (self.chat_id,))
                    newbl = newbala.fetchone()[0]
                    pricing = round((float(true) + float(newbl)), 8)

                    appendMe = '\n{} :  + Deposit: {} BTC '.format(currentDate, true)
                    appendFile = open('{}.txt'.format(self.chat_id), 'a')
                    appendFile.write(appendMe)
                    appendFile.close()
                    self.cur.execute('UPDATE Investor SET newbalance =(?) WHERE investor=(?)',
                                     ('{}'.format(pricing), self.chat_id))
                    self.conn.commit()

                    if float(true) >= 0.0000002:
                        self.cur.execute('UPDATE Investor SET balance =(?) WHERE investor=(?)',
                                         (0.0, self.chat_id))
                        self.conn.commit()

                        self.cur.execute('UPDATE Investor SET deposit =(?) WHERE investor=(?)',
                                         ('none', self.chat_id))
                        self.conn.commit()
                    else:
                        print('New deposit not yet updated')
                newbala = self.cur.execute('SELECT newbalance FROM Investor WHERE investor=(?)', (self.chat_id,))
                newbl = newbala.fetchone()[0]
                comn = self.cur.execute('SELECT commission FROM Investor WHERE investor=(?)', (self.chat_id,))
                commi = comn.fetchone()[0]

                if days == '0:00:00':
                    d = round(Decimal(commi), 8)
                    message = '''💼 *Bitcoin wallet*\n\n_Balance_: *{} BTC*\n_Equivalent_: *{:,} {}*\n_Aff.Commission_: *{} BTC*\n\nIn the past *{} day(s)* you have made *{} deals* of *{} BTC* in total.\n\nReviews: ({})👍 ({})👎'''.format(
                        round(Decimal(newbl), 8).normalize(), round((newbl * float(self.currency(self.chat_id))), 2),
                        self.currency_code(self.chat_id),
                        d.normalize(),

                        0, dl, round(wt, 8), good,
                        bad)
                    self.sender.sendMessage(message, parse_mode='Markdown', reply_markup=dw)
                else:
                    d = round(Decimal(commi), 8)
                    message = '''💼 *Bitcoin wallet*\n\n_Balance_: *{} BTC*\n_Equivalent_: *{:,} {}*\n_Aff.Commission_: *{} BTC*\n\nIn the past *{} day(s)* you have made *{} deals* of *{} BTC* in total.\n\nReviews: ({})👍 ({})👎'''.format(
                        round(Decimal(newbl), 8).normalize(), round((newbl * float(self.currency(self.chat_id))), 2),
                        self.currency_code(self.chat_id),
                        d.normalize(),

                        days, dl, round(wt, 8), good,
                        bad)
                    self.sender.sendMessage(message, parse_mode='Markdown', reply_markup=dw)
            else:
                if days == '0:00:00':
                    d = round(Decimal(commi), 8)
                    message = '''💼 *Bitcoin wallet*\n\n_Balance_: *{} BTC*\n_Equivalent_: *{:,} {}*\n_Aff.Commission_: *{} BTC*\n\nIn the past *{} day(s)* you have made *{} deals* of *{} BTC* in total.\n\nReviews: ({})👍 ({})👎'''.format(
                        round(Decimal(newbl), 8).normalize(), round((newbl * float(self.currency(self.chat_id))), 2),
                        self.currency_code(self.chat_id),
                        d.normalize(),

                        0, dl, round(wt, 8), good,
                        bad)
                    self.sender.sendMessage(message, parse_mode='Markdown', reply_markup=dw)
                else:
                    d = round(Decimal(commi), 8)
                    message = '''💼 *Bitcoin wallet*\n\n_Balance_: *{} BTC*\n_Equivalent_: *{:,} {}*\n_Aff.Commission_: *{} BTC*\n\nIn the past *{} day(s)* you have made *{} deals* of *{} BTC* in total.\n\nReviews: ({})👍 ({})👎'''.format(
                        round(Decimal(newbl), 8).normalize(),
                        round((float(newbl) * float(self.currency(self.chat_id))), 2),
                        self.currency_code(self.chat_id),
                        d.normalize(),

                        days, dl, round(wt, 8), good,
                        bad)
                    self.sender.sendMessage(message, parse_mode='Markdown', reply_markup=dw)

                    # ============================================================================================================

        elif banned != 1 and command == '◀back':
            self.sender.sendMessage('Choose your payment method', reply_markup=badvert)

        elif banned != 1 and command == '✅I Agree':
            user = bot.getChat(self.chat_id)

            firstname = user.get('first_name')
            user_name = user.get('username')

            self.cur.execute('UPDATE Investor SET username =(?) WHERE investor=(?)', (firstname, self.chat_id))
            self.conn.commit()
            self.sender.sendMessage(
                """*Hello {}!*\n\nThis is a fast and free wallet along with the decentralized BTC (Bitcoin) exchange service and an escrow service.""".format(
                    firstname), parse_mode='Markdown',
                reply_markup=markup)

            self.sender.sendMessage(
                'If you have any questions please contact [Support](https://t.me/CryptoscrowHelp_bot/)',
                parse_mode="Markdown", reply_markup=after)

        # elif banned != 1 and len(command) > 29 and len(command) < 36:



        elif banned != 1 and command.endswith('BTC') or command.endswith('Btc') or command.endswith('btc'):
            newbala = self.cur.execute('SELECT newbalance FROM Investor WHERE investor=(?)', (self.chat_id,))
            newbl = newbala.fetchone()[0]
            dony = self.cur.execute('SELECT done FROM Investor WHERE investor=(?)', (self.chat_id,))
            done = dony.fetchone()[0]

            if done == 0:
                if newbl >= 0.002 and float(command.split()[0]) <= newbl:
                    self.cur.execute('UPDATE Investor SET out =(?) WHERE investor=(?)',
                                     ((command.split()[0]), self.chat_id))
                    with_i = self.cur.execute('SELECT out FROM Investor WHERE investor=(?)', (self.chat_id,))
                    with_n = with_i.fetchone()[0]
                    items = self.cur.execute('SELECT withdraw FROM Investor WHERE investor=(?)', (self.chat_id,))
                    itmm = items.fetchone()[0]
                    new_profit = newbl - with_n
                    # primary_account = client.get_primary_account()
                    # primary_account.send_money(to=itmm, amount=with_n, currency='BTC',
                    #                          description='Trading_bot_user:{}'.format(self.chat_id))
                    self.cur.execute('UPDATE Investor SET newbalance =(?) WHERE investor=(?)',
                                     ('{}'.format(new_profit), self.chat_id))
                    self.conn.commit()
                    currentDate = datetime.datetime.strptime(date_d, '%Y-%m-%d').date()
                    appendMe = '\n{} :  -Withdraw {} BTC '.format(
                        currentDate, self.chat_id, with_n)
                    appendFile = open('{}.txt'.format(self.chat_id), 'a')
                    appendFile.write(appendMe)
                    appendFile.close()
                    messag_w = '''Your withdrawal request of {}BTC has being processed kindly wait for at least 1 hour to receive it to your withdrawal address'''.format(
                        with_n)
                    self.sender.sendMessage(messag_w)
                    print("Withdrawal request sent of: ", with_n, "has been sent by", self.chat_id)
                else:

                    self.sender.sendMessage("Error:You don't have enough money to withdraw such an amount")
            else:
                self.sender.sendMessage('*!Your funds have been locked until the transaction is done!*',
                                        parse_mode='Markdown')
        elif banned != 1 and command == 'Buy/Sell BTC📊':  # Message (incoming) 1 sent by user
            message = '''Here you can deal with buyers/sellers while the bot act as an escrow for guaranteed safety.\n\n*Market rate*: {:,} {}/BTC'''.format(
                self.currency(self.chat_id), self.currency_code(self.chat_id))

            buysell = self.sender.sendMessage(message, parse_mode='Markdown', reply_markup=buse)

            self.editorbs = telepot.helper.Editor(self.bot, buysell)
            self.edit_msg = telepot.message_identifier(buysell)

        elif banned != 1 and command == 'I want to BUY Bitcoin':
            self.order_type('buy')
            message = '''💸 Payment method\n\nIf you can't find required payment method in the list below, probably you already have one editable advert for this method.\n\nPlease send a request to [Support](https://t.me/CryptoscrowHelp_bot//) to add new method or currency.'''
            self.sender.sendMessage(message, parse_mode='Markdown', reply_markup=badvert)

        elif banned != 1 and command == 'I want to SELL Bitcoin':
            self.order_type('sell')
            message = '''💸 Payment method\nIf you can't find required payment method in the list below, probably you already have one editable advert for this method.\n\nPlease send a request to [Support](https://t.me/CryptoscrowHelp_bot/) to add new method or currency.'''

            self.sender.sendMessage(message, parse_mode='Markdown', reply_markup=sadvert)

        elif banned != 1 and command.endswith('(Buy)'):
            yy = command.split()[0]
            tt = yy.strip().lower()

            note = self.currency_code(self.chat_id)

            with_i = self.cur.execute('SELECT processor FROM Buy WHERE identifier=(?) AND currency=(?)',
                                      (self.chat_id, note))
            with_n = with_i.fetchall()
            dct = []
            for record in with_n:
                for i in record:
                    dct.append(i)

            if tt in dct:
                self.sender.sendMessage("*You have a {} Advertisement that already exists *".format(yy),
                                        parse_mode="Markdown")
            else:
                checkers = '(Buy)'
                self.gateway_type(command.split()[0])
                message = '''📊 Rate BTC\n\n*1 BTC = {:,} {}*.\n\nTo set your price margin press input your percentage (must end with %). For example: 2 %'''.format(
                    self.currency(self.chat_id), self.currency_code(self.chat_id), self.currency(self.chat_id))

                self.sender.sendMessage(message, parse_mode='Markdown', reply_markup=back)

        elif banned != 1 and command.endswith('(Sell)'):
            yy = command.split()[0]
            tt = yy.strip().lower()

            note = self.currency_code(self.chat_id)

            with_i = self.cur.execute('SELECT processor FROM Sell WHERE identifier=(?) AND currency=(?)',
                                      (self.chat_id, note))
            with_n = with_i.fetchall()
            dct = []
            for record in with_n:
                for i in record:
                    dct.append(i)

            if tt in dct:
                self.sender.sendMessage("*You have a {} Advertisement that already exists. *".format(yy),
                                        parse_mode="Markdown")
            else:
                checkers = '(Sell)'
                self.gateway_type(command.split()[0])
                message = '''📊 Rate BTC\n\n*1 BTC = {:,} {}*.\n\nTo set your price margin press input your percentage (must end with %). For example: 2 %'''.format(
                    self.currency(self.chat_id), self.currency_code(self.chat_id), self.currency(self.chat_id))

                self.sender.sendMessage(message, parse_mode='Markdown', reply_markup=back)

        elif banned != 1 and command.startswith('/destination'):
            global destin
            global destin1

            idt = command.split()[1:]
            if self.advertt == 'buy':

                bot.sendMessage(myid,
                                'Here is the Destination address where you should send the money: *{}*'.format(
                                    " ".join(idt)),
                                parse_mode='Markdown')
                buys = bot.sendMessage(myid,
                                       '*Press the button below only after you have sent the funds\n\nYou can initiate a dispute after one hour by contacting* [Support](https://t.me/CryptoscrowHelp_bot/) ',
                                       parse_mode='Markdown', reply_markup=check_receive1)
                destin = telepot.message_identifier(buys)
                self.sender.sendMessage('Destination address sent')
                print('destin')
            elif self.advertt == 'sell':

                bot.sendMessage(useridentify,
                                'Here is the Destination address where you should send the money: *{}*'.format(
                                    " ".join(idt)),
                                parse_mode='Markdown')
                bys = bot.sendMessage(useridentify,
                                      '*Press the button below only after you have sent the funds\n\nYou can initiate a dispute after one hour by contacting* [Support](https://t.me/CryptoscrowHelp_bot/)',
                                      parse_mode='Markdown', reply_markup=check_receive1)
                destin1 = telepot.message_identifier(bys)
                self.sender.sendMessage('Destination address sent')
                print('destin1')



        elif banned != 1 and command.endswith('%'):
            try:
                if order == 'exb':
                    price = float(command.split()[0])
                    # self.fixed_price(price)
                    self.cur.execute('UPDATE Buy SET price=(?) WHERE ROWID=(?)',
                                     (price, exb))
                    self.sender.sendMessage("Margin has been updated")
                elif order == 'exs':
                    price = float(command.split()[0])
                    # self.fixed_price(price)
                    self.cur.execute('UPDATE Sell SET price=(?) WHERE ROWID=(?)',
                                     (price, exs))
                    self.sender.sendMessage("Margin has been updated")

                else:
                    price = float(command.split()[0])
                    self.fixed_price(price)
                    # store in the database
                    message = '''Limits \nWrite min. and max. limits in {}.For example: *1 to 1000000*'''.format(
                        self.currency_code(self.chat_id))
                    self.sender.sendMessage(message, parse_mode='Markdown')
            except Exception:
                self.sender.sendMessage(
                    'Error : Make sure there is space between the number and the percentage sign eg 25 %')


        elif banned != 1 and 'to' in command:

            if order == 'buy':
                user = bot.getChat(self.chat_id)

                firstname = user.get('first_name')
                user_name = user.get('username')
                min = command.split()[0]
                max = command.split()[2]
                y = self.currency_code(self.chat_id)

                self.cur.execute(
                    "INSERT INTO Buy(Identifier,username,processor,price,margin,auto,min,max,currency,status,terms) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    (self.chat_id, firstname, gateway.strip().lower(), price_tag, 0, 0, min, max, y, 0, 'No Terms'))
                self.conn.commit()

                self.sender.sendMessage('''📰 *Advert created!*''', parse_mode='Markdown', reply_markup=markup)
                self.sender.sendMessage(
                    '''You can edit your advert by pressing _My Adverts_ button under Buy/Sell ''',
                    parse_mode='Markdown')
            elif order == 'sell':
                user = bot.getChat(self.chat_id)

                firstname = user.get('first_name')
                user_name = user.get('username')
                min = command.split()[0]
                max = command.split()[2]
                x = self.currency_code(self.chat_id)
                self.cur.execute(
                    'INSERT INTO Sell (Identifier,username,processor,price,margin,auto,min,max,currency,status,terms) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                    (self.chat_id, firstname, gateway.strip().lower(), price_tag, 0, 0, min, max, x, 0, 'No Terms'))
                self.conn.commit()

                self.sender.sendMessage('''📰 *Advert created!*''', parse_mode='Markdown', reply_markup=markup)
                self.sender.sendMessage(
                    '''You can edit your advert by pressing _My Adverts_ button under Buy/Sell ''',
                    parse_mode='Markdown')
            elif order == 'exb':
                min = command.split()[0]
                max = command.split()[2]
                self.cur.execute('UPDATE Buy SET min =(?),max=(?) WHERE ROWID=(?)',
                                 (min, max, exb))
                self.sender.sendMessage("Limits have been updated")
            elif order == 'exs':
                min = command.split()[0]
                max = command.split()[2]
                self.cur.execute('UPDATE Sell SET min =(?),max=(?) WHERE ROWID=(?)',
                                 (min, max, exs))
                self.sender.sendMessage("Limits have been updated")



        elif banned != 1 and command.strip().lower() == 'good' :

            if self.advertt == 'buy' and self.chat_id == myid:
                worth = self.cur.execute('SELECT goodreviews FROM Investor WHERE investor=(?)', (useridentity,))
                worthly = worth.fetchone()[0]
                self.sender.sendMessage('_You have rated the user service as : {}_'.format(command),
                                        parse_mode='Markdown')

                self.cur.execute('UPDATE Investor SET goodreviews =(?) WHERE investor=(?)',
                                 ('{}'.format(worthly + 1), useridentity))
            elif self.advertt == 'buy' and self.chat_id == useridentity:
                worth = self.cur.execute('SELECT goodreviews FROM Investor WHERE investor=(?)', (myid,))
                worthly = worth.fetchone()[0]
                self.sender.sendMessage('_You have rated the user service as : {}_'.format(command),
                                        parse_mode='Markdown')

                self.cur.execute('UPDATE Investor SET goodreviews =(?) WHERE investor=(?)',
                                 ('{}'.format(worthly + 1), myid))
            elif self.advertt == 'sell' and self.chat_id == useridentify:
                worth = self.cur.execute('SELECT goodreviews FROM Investor WHERE investor=(?)', (myid,))
                worthly = worth.fetchone()[0]
                self.sender.sendMessage('_You have rated the user service as : {}_'.format(command),
                                        parse_mode='Markdown')

                self.cur.execute('UPDATE Investor SET goodreviews =(?) WHERE investor=(?)',
                                 ('{}'.format(worthly + 1), myid))
            elif self.advertt == 'sell' and self.chat_id == myid:
                worth = self.cur.execute('SELECT goodreviews FROM Investor WHERE investor=(?)', (useridentify,))
                worthly = worth.fetchone()[0]
                self.sender.sendMessage('_You have rated the user service as : {}_'.format(command),
                                        parse_mode='Markdown')

                self.cur.execute('UPDATE Investor SET goodreviews =(?) WHERE investor=(?)',
                                 ('{}'.format(worthly + 1), useridentify))


        elif banned != 1 and command.strip().lower() == 'bad' :

            if self.advertt == 'buy' and self.chat_id == useridentity:
                worth = self.cur.execute('SELECT badreviews FROM Investor WHERE investor=(?)', (myid,))
                worthly = worth.fetchone()[0]
                self.sender.sendMessage('_You have rated the user service as : {}_'.format(command),
                                        parse_mode='Markdown')

                self.cur.execute('UPDATE Investor SET badreviews =(?) WHERE investor=(?)',
                                 ('{}'.format(worthly + 1), myid))
            elif self.advertt == 'buy' and self.chat_id == myid:
                worth = self.cur.execute('SELECT badreviews FROM Investor WHERE investor=(?)', (useridentity,))
                worthly = worth.fetchone()[0]
                self.sender.sendMessage('_You have rated the user service as : {}_'.format(command),
                                        parse_mode='Markdown')

                self.cur.execute('UPDATE Investor SET badreviews =(?) WHERE investor=(?)',
                                 ('{}'.format(worthly + 1), useridentity))


            elif self.advertt == 'sell' and self.chat_id == useridentify:
                worth = self.cur.execute('SELECT badreviews FROM Investor WHERE investor=(?)', (myid,))
                worthly = worth.fetchone()[0]
                self.sender.sendMessage('_You have rated the user service as : {}_'.format(command),
                                        parse_mode='Markdown')

                self.cur.execute('UPDATE Investor SET badreviews =(?) WHERE investor=(?)',
                                 ('{}'.format(worthly + 1), myid))
            elif self.advertt == 'sell' and self.chat_id == myid:
                worth = self.cur.execute('SELECT badreviews FROM Investor WHERE investor=(?)', (useridentity,))
                worthly = worth.fetchone()[0]
                self.sender.sendMessage('_You have rated the user service as : {}_'.format(command),
                                        parse_mode='Markdown')

                self.cur.execute('UPDATE Investor SET badreviews =(?) WHERE investor=(?)',
                                 ('{}'.format(worthly + 1), useridentity))


        elif command.startswith("/ban"):
            try:
                t = command.split()[1]
                self.cur.execute('UPDATE Investor SET ban =(?) WHERE investor=(?)',
                                 (1, t))

                self.sender.sendMessage('You have banned : {}'.format(t))

            except Exception:
                self.sender.sendMessage("Make sure there you have included the userId of the person you want to ban")

        elif command.startswith("/unban"):
            try:
                t = command.split()[1]
                self.cur.execute('UPDATE Investor SET ban =(?) WHERE investor=(?)', (0, t))

                self.sender.sendMessage('You have unbanned : {}'.format(t))

            except Exception:
                self.sender.sendMessage("Make sure there you have included the userId of the person you want to unban")

        elif command.startswith("/verify"):
            try:
                t = command.split()[1]
                self.cur.execute('UPDATE Investor SET verification =(?) WHERE investor=(?)',
                                 ("✅", t))

                self.sender.sendMessage('You have  verified : {}'.format(t))
                bot.sendMessage(t, 'Hello,Your Account has been successfully verified')
            except Exception:
                self.sender.sendMessage("Make sure there you have included the userId of the person you want to verify")

        elif command.startswith("/unverify"):
            try:
                t = command.split()[1]
                self.cur.execute('UPDATE Investor SET verification =(?) WHERE investor=(?)',
                                 ("❌", t))

                self.sender.sendMessage('You have unverified : {}'.format(t))

            except Exception:
                self.sender.sendMessage(
                    "Make sure there you have included the userId of the person you want to unverify")
        elif command == '/photo':
            print("Incoming photo")
        elif command == 'Search User':
            bot.sendMessage(self.chat_id,
                            "To search for user and get his/her details based on username press */search username*\n\n *Example : /search forever* \n\n*Note : If the user doesn't have a username you cant use this command*\nTo get all users press /search all",
                            parse_mode='Markdown')
        elif command.startswith('/search'):
            if command.split()[1] == 'all':
                bala = self.cur.execute('SELECT username,investor,newbalance,date,verification FROM Investor ', )
                lst = bala.fetchall()

                bal = []
                for items in lst:
                    bot.sendMessage(self.chat_id,
                                    '''_Name_ :*{}*\n*Userid* : _{}_\n*Current balance* : _{}_ BTC\n*Joined on* : _{}_\n*Verified* : {} '''.format(
                                        items[0], items[1], round(float(items[2]), 8), items[3], items[4]),
                                    parse_mode='Markdown')
            else:
                try:
                    bala = self.cur.execute(
                        'SELECT username,investor,newbalance,date,verification FROM Investor WHERE username=(?)',
                        (command.split()[1],))
                    lst = bala.fetchall()

                    bal = []
                    for items in lst:
                        for records in items:
                            bal.append(records)

                    bot.sendMessage(self.chat_id,
                                    '''_Name_ :*{}*\n*Userid* : _{}_\n*Current balance* : _{}_ BTC\n*Joined on* : _{}_\n*Verified* : {} '''.format(
                                        bal[0], bal[1], round(bal[2], 8), bal[3], bal[4]), parse_mode='Markdown')
                except Exception:
                    self.sender.sendMessage("Either the user doesnt exist or you missed the Caps on the username")




        elif command.startswith('/send'):
            try:
                t = command.split()[1]
                if t == 'all' or t == 'All':
                    mes = command.split()[2:]
                    mess = ' '.join(mes)
                    grp = self.cur.execute('SELECT * FROM Investor', )
                    group = grp.fetchall()
                    for users in group:
                        bot.sendMessage('{}'.format(users[0]), mess)
                    self.sender.sendMessage("The above message has been sent to all users.")
                else:
                    mes = command.split()[2:]
                    mess = ' '.join(mes)
                    bot.sendMessage('{}'.format(t), mess)
                    self.sender.sendMessage("The above message has been sent to user: {}.".format(t))
            except Exception:
                self.sender.sendMessage("Make sure you have added the user id the message is directed to")


        elif banned != 1 and command == 'back↩':
            self.sender.sendMessage('Select the advertisement type below', reply_markup=ad)

        elif banned != 1 and command == 'About📱':

            self.sender.sendMessage("""This is a fast and free wallet along with the decentralized BTC (Bitcoin) exchange service and an escrow service.
        """, reply_markup=more_info)
        elif banned != 1 and command == 'Settings⚙':

            self.sender.sendMessage('You can change whatever you want here', reply_markup=changeafter)
            # ==========================================================================================================
        elif banned != 1 and command == 'Cancel':
            self.sender.sendMessage('You have decided not to create an advert', reply_markup=markup)
        elif banned != 1 and command == '/here':
            self.sender.sendMessage("Write your message below", reply_markup=ForceReply())
        elif banned == 1:
            self.sender.sendMessage(
                "Sorry my friend you have been banned from using our services\n\n[Support](https://t.me/CryptoscrowHelp_bot/) ",
                parse_mode="Markdown")

        elif 'cmd' in locals() or 'cmd' in globals():
            if cmd == "Add your contact number here for potential buyers/sellers to contact you when you're offline":
                self.cur.execute('UPDATE Investor SET contact =(?) WHERE investor=(?)', (command, self.chat_id))
                self.conn.commit()
                self.sender.sendMessage("Contact saved successfully", reply_markup=markup)
            elif cmd == '''📤 Withdraw Bitcoin

Please enter the address of the external BTC wallet.''':
                try:
                    parsed_text = CommonRegex(command)
                    self.validation = (parsed_text.btc_addresses)[0]
                    self.cur.execute('UPDATE Investor SET withdraw =(?) WHERE investor=(?)', (command, self.chat_id))
                    items = self.cur.execute('SELECT withdraw FROM Investor WHERE investor=(?)', (self.chat_id,))
                    itmm = items.fetchone()[0]
                    newbala = self.cur.execute('SELECT newbalance FROM Investor WHERE investor=(?)', (self.chat_id,))
                    newbl = newbala.fetchone()[0]
                    message = '''Your withdrawal address is : *{}* \n\nPlease specify the amount of BTC to withdraw. (*Must end with BTC*)
                \n_❕ Average network fee is 0.001 BTC and it will charged from the residual balance._
                \n_Min. amount_: *0.002 BTC*.\n_Available_: *{} BTC*'''.format(itmm, newbl)
                    self.sender.sendMessage(message, parse_mode='Markdown', reply_markup=markup)
                except Exception:
                    self.sender.sendMessage("Invalid Bitcoin Address", reply_markup=markup)
            elif cmd == 'Type your message below' and (command.strip().lower() != 'good' or command.strip().lower() != 'bad'):
                global system_mess
                system_mess = 'buymes'
                self.sender.sendMessage("Message sent")

                bot.sendMessage(myid, "{}\n\nPress /here to reply".format(command))

            elif cmd == "Input your message below" and (command.strip().lower() != 'good' or command.strip().lower() != 'bad'):
                system_mess = 'sellmes'
                self.sender.sendMessage("Message sent")

                bot.sendMessage(myid, "{}\n\nPress /here to reply".format(command))

            elif cmd == 'Write your message below' and (command.strip().lower() != 'good' or command.strip().lower() != 'bad'):
                if system_mess == 'buymes':
                    bot.sendMessage(useridentity, "{}".format(command), reply_markup=buymes)
                    self.sender.sendMessage("Message sent")
                elif system_mess == 'sellmes':
                    bot.sendMessage(useridentify, "{}".format(command), reply_markup=sellmes)
                    self.sender.sendMessage("Message sent")



            elif cmd == 'Please add your terms below' and (command.strip().lower() != 'good' or command.strip().lower() != 'bad'):
                if order == 'exb':

                    self.cur.execute('UPDATE Buy SET terms =(?) WHERE ROWID=(?)',
                                     (command, exb))
                    self.sender.sendMessage("Your terms have been updated")
                elif order == 'exs':
                    self.cur.execute('UPDATE Sell SET terms =(?) WHERE ROWID=(?)', (command, exs))
                    self.sender.sendMessage("Your terms have been updated")

            elif cmd == 'Input the amount below' and command !='/menu' and command !="/mainmenu" and (command.strip().lower() != 'good' or command.strip().lower() != 'bad'):
                global great
                global refferal

                refferal = self.chat_id
                great = float(command)
                dony = self.cur.execute('SELECT done FROM Investor WHERE investor=(?)', (self.chat_id,))
                done = dony.fetchone()[0]

                if self.advertt == 'buy':

                    from_cash = float(sell_info[1])
                    to_cash = float(sell_info[2])

                    newbala = self.cur.execute('SELECT newbalance FROM Investor WHERE investor=(?)', (useridentity,))
                    newbl = newbala.fetchone()[0]

                    blah = round((Decimal(great) / Decimal(sell_xx)), 8)
                    cv = self.currency(self.chat_id)
                    deduct = float(newbl) * 0.02

                    cxv = round(float(newbl - deduct) * float(cv), 2)

                    if cxv >= from_cash:
                        if cxv > to_cash:
                            if float(great) >= from_cash and float(great) <= to_cash:
                                global officialb
                                officialb = round((float(great) / float(sell_xx)), 8)

                                t = (Decimal(officialb * 0.004))
                                txt = round(t, 8)
                                jj = (Decimal(officialb * 0.002))
                                global sherlockb
                                sherlockb = round(jj, 8)

                                global endchargeb
                                endchargeb = round(Decimal(officialb), 8) - txt

                                message = '''Are you sure you want to buy *{} BTC* for *{:,} {}* with rate *{:,} {}*?.\n\n❕ You also agree with the terms of the service and the ad policy. After a deal, the service charges a *fixed fee {} BTC*.'''.format(
                                    round(Decimal(officialb), 8), great, nlm_all, sell_xx, nlm_all, txt)

                                buysure = self.sender.sendMessage(message, parse_mode='Markdown',
                                                                  reply_markup=start_deal)
                                self.bsure = telepot.helper.Editor(self.bot, buysure)
                                self.bedit_msg_ident = telepot.message_identifier(buysure)

                            else:
                                self.sender.sendMessage(
                                    '*Please input an amount between {:,} {} - {:,} {}!*'.format(from_cash, nlm_all,
                                                                                                 to_cash, nlm_all),
                                    parse_mode='Markdown')
                                self.sender.sendMessage("Input the amount below", reply_markup=ForceReply())

                        else:
                            if float(great) >= from_cash and float(great) <= cxv:

                                officialb = round((float(great) / float(sell_xx)), 8)

                                t = (Decimal(officialb * 0.004))
                                txt = round(t, 8)
                                jj = (Decimal(officialb * 0.002))

                                sherlockb = round(jj, 8)
                                endchargeb = round(Decimal(officialb), 8) - txt
                                # \n\n❕ You also agree with the terms of the service and the ad policy. After a deal, the service charges a *fixed fee {} BTC
                                message = '''Are you sure you want to buy *{} BTC* for *{:,} {}* with rate *{:,} {}*?.\n\n❕ You also agree with the terms of the service and the ad policy. After a deal, the service charges a *fixed fee {} BTC*.'''.format(
                                    round(Decimal(officialb), 8), great, nlm_all, sell_xx, nlm_all, txt)
                                buysure = self.sender.sendMessage(message, parse_mode='Markdown',
                                                                  reply_markup=start_deal)
                                self.bsure = telepot.helper.Editor(self.bot, buysure)
                                self.bedit_msg_ident = telepot.message_identifier(buysure)

                            else:
                                self.sender.sendMessage(
                                    '*Please input an amount between {:,} {} - {:,} {}!*'.format(from_cash, nlm_all,
                                                                                                 cxv, nlm_all),
                                    parse_mode='Markdown')
                                self.sender.sendMessage("Input the amount below", reply_markup=ForceReply())
                    else:
                        self.sender.sendMessage('*Seller is unavailable or has low volume*', parse_mode='Markdown')

                elif self.advertt == 'sell':

                    global officials
                    fromcash = float(buy_info[1])
                    tocash = float(buy_info[2])
                    '''price=tests[5],currency=tests[6],from=tests[7] to tests[9]'''
                    newbala = self.cur.execute('SELECT newbalance FROM Investor WHERE investor=(?)', (self.chat_id,))
                    newbl = newbala.fetchone()[0]

                    if float(great) >= fromcash and float(great) <= tocash:

                        officials = round((float(great) / float(buy_xx)), 8)

                        t = (Decimal(officials * 0.004))
                        txt = round(t, 8)
                        jj = (Decimal(officials * 0.002))
                        global sherlocks
                        sherlocks = round(jj, 8)
                        global endcharges
                        endcharges = round(Decimal(officials), 8) - txt
                        if newbl >= 0.00002 and officials < newbl:
                            message = '''Are you sure you want to sell *{} BTC* for *{:,} {}* with rate *{:,} {}*?\n\n❕ You also agree with the terms of the service and the ad policy. After a deal, the service charges a *fixed fee {} BTC*.'''.format(
                                round(Decimal(officials), 8), great, nlm_all, buy_xx, nlm_all, txt)
                            sellsure = self.sender.sendMessage(message, parse_mode='Markdown', reply_markup=start_deal)
                            self.csure = telepot.helper.Editor(self.bot, sellsure)
                            self.b_edit_msg_ident = telepot.message_identifier(sellsure)

                        else:
                            self.sender.sendMessage(
                                "*Your Bitcoin balance is insufficient* please topup to continue with your trade",
                                parse_mode="Markdown")
                    else:
                        self.sender.sendMessage(
                            '*Please input an amount between {:,} {} - {:,} {}!*'.format(fromcash, nlm_all,
                                                                                         tocash,
                                                                                         nlm_all),
                            parse_mode='Markdown')
                        self.sender.sendMessage("Input the amount below", reply_markup=ForceReply())


        else:
            self.sender.sendMessage('Error:Invalid Input!!!')

        self.conn.commit()
        self.cur.close()

    # =====================================================================================================
    def on_callback_query(self, msg):
        query_id, from_id, data = telepot.glance(msg, flavor='callback_query')

        self.conn = sqlite3.connect('trading.db')
        self.cur = self.conn.cursor()
        global finger
        global disput

        global chekbuy
        global cheksell
        global exb
        global exs
        global test
        global tests
        global medit
        global medit1
        global nlm_all
        global buy_info
        global sell_info
        global sell_xx
        global buy_xx

        if data == 'advert':
            self.sender.sendMessage('Select the advertisement type below.', reply_markup=ad)

        elif data == 'buy':
            try:
                try:
                    self.editorbs.deleteMessage()
                except Exception:
                    self.editor_b.deleteMessage()
            except Exception:
                pass

            dony = self.cur.execute('SELECT ncommission FROM Investor WHERE investor=(?)', (self.chat_id,))
            still_open = dony.fetchone()[0]
            if still_open != 5:

                self.advert_type(data)
                sent = self.sender.sendMessage(
                    '''📈 *Buy*\n\nPlease select payment method. The best rate and count of adverts are listed next.\n\nMarket rate: {:,} {}/BTC'''.format(
                        self.currency(from_id), self.currency_code(from_id)), parse_mode='Markdown',
                    reply_markup=payment)

                self.b_editor = telepot.helper.Editor(self.bot, sent)
                self.b_edit_msg_ident = telepot.message_identifier(sent)
            else:
                self.sender.sendMessage("*You cannot access this section until you have completed your transaction*",
                                        parse_mode="Markdown")

        elif data == 'main':
            try:
                self.b_editor.deleteMessage()
            except Exception:
                try:
                    self._editor.deleteMessage()
                except Exception:
                    pass
            message = '''Here you can deal with buyers/sellers while the bot act as an escrow for guaranteed safety.\n\nMarket rate: {:,} {}/BTC'''.format(
                self.currency(from_id), self.currency_code(from_id))
            sent = self.sender.sendMessage(message, reply_markup=buse)
            self.editor_b = telepot.helper.Editor(self.bot, sent)
            self.edit_msg_ident_b = telepot.message_identifier(sent)


        elif data == 'bck':
            try:
                self.editor_c.deleteMessage()
            except Exception:
                pass
            message = '''Here you can deal with buyers/sellers while the bot act as an escrow for guaranteed safety.\n\n*Market rate*: {:,} {}/BTC'''.format(
                self.currency(from_id), self.currency_code(from_id))

            buysell = self.sender.sendMessage(message, parse_mode='Markdown', reply_markup=buse)
        elif data == 'badbk':
            message = '''💸 Payment method

                If you can't find required payment method in the list bellow, probably you already have one editable advert for this method.

                Please make a request on [help desk](https://changebot.freshdesk.com/) to add new method or currency.'''
            self.sender.sendMessage(message, parse_mode='Markdown', reply_markup=badvert)

        elif data == 'currency':

            try:
                self.editorbs.deleteMessage()
            except Exception:
                try:
                    try:
                        self.editorbs.deleteMessage()
                    except Exception:
                        self.editor_b.deleteMessage()
                except Exception:
                    pass

            sent = self.sender.sendMessage(
                '''💵 Currency\n\nSelect a currency. This filter affects the viewing and creating adverts.\nCurrently «*{}*» is being used.'''.format(
                    self.currency_code(from_id)), parse_mode='Markdown', reply_markup=curency)
            self.editor_c = telepot.helper.Editor(self.bot, sent)
            self._edit_msg_ident = telepot.message_identifier(sent)

        elif data == 'seller':
            try:
                try:
                    self.editorbs.deleteMessage()
                except Exception:
                    self.editor_b.deleteMessage()
            except Exception:
                pass
            dony = self.cur.execute('SELECT ncommission FROM Investor WHERE investor=(?)', (self.chat_id,))
            still_open = dony.fetchone()[0]
            if still_open != 5:

                self.advert_type('sell')
                message = '''📉 *Sell*\n\nPlease select payment method. The best rate and count of adverts are listed next.\n\nMarket rate: {:,} {}/BTC'''.format(
                    self.currency(from_id), self.currency_code(from_id))
                sent = self.sender.sendMessage(message, parse_mode='Markdown', reply_markup=paysell)
                self._editor = telepot.helper.Editor(self.bot, sent)
                self._edit_msg_ident = telepot.message_identifier(sent)
            else:
                self.sender.sendMessage("*You cannot access this section until you have completed your transaction*",
                                        parse_mode="Markdown")

        elif data == 'dep':
            item_d = self.cur.execute('SELECT deposit FROM Investor WHERE investor=(?)', (from_id,))

            dep_addr = item_d.fetchone()[0]

            bala = self.cur.execute('SELECT balance FROM Investor WHERE investor=(?)', (from_id,))
            bal = bala.fetchone()[0]

            if bal < 0.00001 and len(dep_addr) < 25:
                self.cur.execute(
                    "UPDATE Investor SET balance =(?) WHERE investor=(?)", (0, from_id)
                )
                self.conn.commit()
                address = client.create_address("495d62e2-c289-5caf-abc0-bf147af57cda")

                jsontopy = json.loads(str(address))

                btc_address = jsontopy.get('address')

                self.cur.execute('UPDATE Investor SET deposit =(?) WHERE investor=(?)', (btc_address, from_id))

                item_d = self.cur.execute('SELECT deposit FROM Investor WHERE investor=(?)', (from_id,))

                dep_add = item_d.fetchone()[0]

                depo = "{}".format(dep_add)

                message = '''📥 *Deposit Bitcoin*\n\nUse the one time address below to deposit BTC from an external wallet.\n\n_❕ You should deposit coins on address below first. After that you can sell coins._\n\nFunds will come after one network's confirmation.'''
                self.sender.sendMessage(message, parse_mode='Markdown', reply_markup=markup)
                self.sender.sendMessage('''*{}*'''.format(depo), parse_mode='Markdown',
                                        reply_markup=markup)

            else:
                message = '''📥 *Deposit Bitcoin*\n\nUse the one time address below to deposit BTC from an external wallet.\n\n_❕ You should deposit coins on address below first. After that you can sell coins._\n\nFunds will come after 3 network's confirmation.'''
                self.sender.sendMessage(message, parse_mode='Markdown', reply_markup=markup)
                self.sender.sendMessage('''*{}*'''.format(dep_addr), parse_mode='Markdown',
                                        reply_markup=markup)

        elif data.endswith("z"):
            try:
                self.editor_c.deleteMessage()
            except Exception:
                pass

            self.currency_update(data.split()[0], from_id)
            message = '''Here you can deal with buyers/sellers while the bot act as an escrow for guaranteed safety.\n\n*Market rate*: {:,} {}/BTC'''.format(
                self.currency(from_id), self.currency_code(from_id))
            self.sender.sendMessage(message, parse_mode='Markdown', reply_markup=buse)

        elif data == 'with':
            self.sender.sendMessage('To go back to Main Menu >> /menu')
            message = '''📤 *Withdraw Bitcoin*\n\nPlease enter the address of the external BTC wallet.'''
            self.sender.sendMessage(message, parse_mode='Markdown', reply_markup=ForceReply())




        elif data.endswith('bst'):
            global processing
            u = data.split()[0]
            processing = '{}'.format(u.strip().lower())

            note = self.currency_code(from_id)
            selld = self.cur.execute(
                'SELECT COUNT(Identifier) FROM Sell WHERE processor=(?) AND currency=(?) AND status=(?)',
                (processing, note, 0))
            fili = selld.fetchone()[0]

            if int(fili) > 0:
                message = '''📈 Buy\n\nThere is a list of {} sellers available for {}. Please select a seller and open a deal.\n\n⚠*{}* *ONLY!*! Ignoring of this condition can lead to cancellation of the deal.'''.format(
                    fili,
                    processing,
                    processing.strip().upper())
                # self.sender.sendMessage(message,parse_mode='Markdown')
                self.conn.commit()

                fech = self.cur.execute(
                    'SELECT ROWID,username,price,min,max FROM Sell WHERE processor=(?) AND currency=(?) AND status=(?)',
                    (processing, note, 0))
                tech = fech.fetchall()

                global L
                L = []
                for records in tech:
                    price = float(self.currency(from_id))
                    nlm = self.currency_code(from_id)
                    x = float(records[2]) + 100
                    xx = round(((x / 100) * price), 2)
                    L.append(
                        '📩 ' + str(records[0]) + " " + str(records[1]) + ' - price - ' + str(xx) + ' {} '.format(
                            nlm) + str(
                            records[3]) + ' to ' + str(records[4]))

                buyat = self.sender.sendMessage(message, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=list((map(
                        lambda c: [InlineKeyboardButton(text=str(c), callback_data=str('📩 ' + c.split()[1]))], L)))))
                self.listing = telepot.helper.Editor(self.bot, buyat)
                self.b_edit_msg_ident = telepot.message_identifier(buyat)
            else:
                self.sender.sendMessage("No Adverts in this section yet!!")

        elif data.endswith('tq'):
            global processing_s
            t = data.split()[0]
            processing_s = '{}'.format(t.strip().lower())
            note = self.currency_code(from_id)
            selld = self.cur.execute(
                'SELECT COUNT(Identifier) FROM Buy WHERE processor=(?) AND currency=(?) AND status=(?)',
                (processing_s, note, 0))
            fili = selld.fetchone()[0]

            if int(fili) > 0:
                message = '''📉 Sell\n\nThere is a list of {} buyers available for {}. Please select a buyer and open a deal.\n\n⚠️*{}* *ONLY*! Ignoring of this condition can lead to cancellation of the deal.'''.format(
                    fili,
                    processing_s,
                    processing_s.strip().upper())
                # self.sender.sendMessage(message,parse_mode='Markdown')
                self.conn.commit()

                fech = self.cur.execute(
                    'SELECT ROWID,username,price,min,max  FROM Buy WHERE processor=(?) AND currency=(?) AND status=(?)',
                    (processing_s, note, 0))
                teach = fech.fetchall()

                global R
                R = []
                for records in teach:
                    price = float(self.currency(from_id))
                    nlm = self.currency_code(from_id)
                    x = float(records[2]) + 100
                    xx = round(((x / 100) * price), 2)
                    R.append(
                        '📨 ' + str(records[0]) + " " + str(records[1]) + ' - price - ' + str(xx) + ' {} '.format(
                            nlm) + str(
                            records[3]) + ' to ' + str(records[4]))

                buyat = self.sender.sendMessage(message, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=list(
                        (map(lambda c: [InlineKeyboardButton(text=str(c), callback_data=str('📨 ' + c.split()[1]))],
                             R)))))
                self.listing1 = telepot.helper.Editor(self.bot, buyat)
                self.b_edit_msg_ident = telepot.message_identifier(buyat)
            else:
                self.sender.sendMessage("No Adverts in this section yet!!")

                # else:
                #     self.sender.sendMessage( 'You want to sell Bitcoin but you have *insufficient funds*',
                #                     parse_mode='Markdown')


        elif data.startswith('📩'):
            try:
                try:
                    self.listing.deleteMessage()
                except Exception:
                    self.listing1.deleteMessage()
            except Exception:
                pass
            tests = data.split()

            # try:
            global useridentity
            identit = self.cur.execute('SELECT identifier FROM Sell WHERE ROWID=(?)', (tests[1],))
            identy = identit.fetchone()[0]
            useridentity = int(identy)

            deal = self.cur.execute('SELECT deal FROM Investor WHERE investor=(?)', (useridentity,))
            dl = deal.fetchone()[0]
            worth = self.cur.execute('SELECT worth FROM Investor WHERE investor=(?)', (useridentity,))
            wt = worth.fetchone()[0]
            verify = self.cur.execute('SELECT verification FROM Investor WHERE investor=(?)', (useridentity,))
            vf = verify.fetchone()[0]
            goodreview = self.cur.execute('SELECT goodreviews FROM Investor WHERE investor=(?)', (useridentity,))
            good = goodreview.fetchone()[0]
            badreview = self.cur.execute('SELECT badreviews FROM Investor WHERE investor=(?)', (useridentity,))
            bad = badreview.fetchone()[0]
            dat = self.cur.execute('SELECT date FROM Investor WHERE investor=(?)', (useridentity,))
            date_d = dat.fetchone()[0]
            user = self.cur.execute('SELECT username FROM Investor WHERE investor=(?)', (useridentity,))
            name_user = user.fetchone()[0]
            sellinfo = self.cur.execute('SELECT price,min,max,terms FROM Sell WHERE ROWID=(?)', (tests[1],))
            sell_info = sellinfo.fetchall()[0]

            now = datetime.date.today()
            currentDate = datetime.datetime.strptime(date_d, '%Y-%m-%d').date()
            diff = now - currentDate
            dif = str(diff)
            days = dif.split()[0]
            price = float(self.currency(from_id))
            nlm_all = self.currency_code(from_id)
            x = float(sell_info[0]) + 100
            sell_xx = round(((x / 100) * price), 2)
            message = '''📈 Buy ({})\n\nIn the past {} day(s) {} made {} deal(s) of {} BTC in total.\n\nReviews: ({})👍 ({})👎\nVerified: {}\n\nTerms of trade:\n{}\n\nThis advert allow to buy BTC with rate {:,} {} of amount from {:,} {} to {:,} {}.'''.format(
                processing, days, name_user, dl, round(wt, 8), good, bad, vf, sell_info[3], sell_xx, nlm_all,
                sell_info[1], nlm_all,
                sell_info[2], nlm_all)
            buyat = self.sender.sendMessage(message, reply_markup=open_deal)
            self.opendeal = telepot.helper.Editor(self.bot, buyat)
            self.b_edit_msg_ident = telepot.message_identifier(buyat)
        elif data.startswith('📨'):
            try:
                try:
                    self.listing.deleteMessage()
                except Exception:
                    self.listing1.deleteMessage()
            except Exception:
                pass
            test = data.split()

            # try:
            global useridentify
            identify = self.cur.execute('SELECT identifier FROM Buy WHERE ROWID=(?)', (test[1],))
            ident = identify.fetchone()[0]
            useridentify = int(ident)

            deal = self.cur.execute('SELECT deal FROM Investor WHERE investor=(?)', (useridentify,))
            dl = deal.fetchone()[0]
            worth = self.cur.execute('SELECT worth FROM Investor WHERE investor=(?)', (useridentify,))
            wt = worth.fetchone()[0]
            verify = self.cur.execute('SELECT verification FROM Investor WHERE investor=(?)', (useridentify,))
            vf = verify.fetchone()[0]
            goodreview = self.cur.execute('SELECT goodreviews FROM Investor WHERE investor=(?)', (useridentify,))
            good = goodreview.fetchone()[0]
            badreview = self.cur.execute('SELECT badreviews FROM Investor WHERE investor=(?)', (useridentify,))
            bad = badreview.fetchone()[0]
            dat = self.cur.execute('SELECT date FROM Investor WHERE investor=(?)', (useridentify,))
            date_d = dat.fetchone()[0]
            user = self.cur.execute('SELECT username FROM Investor WHERE investor=(?)', (useridentify,))
            name_user = user.fetchone()[0]
            buyinfo = self.cur.execute('SELECT price,min,max,terms FROM Buy WHERE ROWID=(?)', (test[1],))
            buy_info = buyinfo.fetchall()[0]
            now = datetime.date.today()
            currentDate = datetime.datetime.strptime(date_d, '%Y-%m-%d').date()
            diff = now - currentDate
            dif = str(diff)
            days = dif.split()[0]
            price = float(self.currency(from_id))
            nlm_all = self.currency_code(from_id)
            x = float(buy_info[0]) + 100
            buy_xx = round(((x / 100) * price), 2)
            message = '''📉 Sell ({})\n\nIn the past {} days(s) {} made {} deal(s) of {} BTC in total.\n\nReviews: ({})👍 ({})👎\nVerified: {}\n\nTerms of trade:\n{}\n\nThis advert allow you to sell BTC with rate {:,} {} on amount from {:,} {} to {:,} {}.'''.format(
                processing_s, days, name_user, dl, round(wt, 8), good, bad, vf, buy_info[3], buy_xx, nlm_all,
                buy_info[1], nlm_all,
                buy_info[2], nlm_all)

            buyat = self.sender.sendMessage(message, reply_markup=close_deal)
            self.closedeal = telepot.helper.Editor(self.bot, buyat)
            self.b_edit_msg_ident = telepot.message_identifier(buyat)

        elif data == 'dealing':
            try:
                self.opendeal.deleteMessage()
            except Exception:
                self.closedeal.deleteMessage()
            try:
                try:
                    self._editor.deleteMessage()
                except Exception:
                    self.b_editor.deleteMessage()
            except Exception:
                pass
            if self.chat_id == useridentity:
                self.sender.sendMessage('*You cannot open a deal with yourself*', parse_mode='Markdown')
            else:

                message = '''💵 Input the buying amount\n\nPlease input an amount between *{:,} {}* and *{:,} {}*.'''.format(
                    sell_info[1], nlm_all, sell_info[2], nlm_all)
                self.sender.sendMessage(message, parse_mode='Markdown')
                self.sender.sendMessage("Input the amount below", reply_markup=ForceReply())
        elif data == 'dealout':
            try:
                self.opendeal.deleteMessage()
            except Exception:
                self.closedeal.deleteMessage()
            try:
                try:
                    self._editor.deleteMessage()
                except Exception:
                    self.b_editor.deleteMessage()
            except Exception:
                pass
            if self.chat_id == useridentify:
                self.sender.sendMessage('*You cannot open a deal with yourself*', parse_mode='Markdown')
            else:

                message = '''💵 Input the selling amount\n\nPlease input an amount between *{:,} {}* and *{:,} {}*.'''.format(
                    buy_info[1], nlm_all, buy_info[2], nlm_all)
                self.sender.sendMessage(message, parse_mode='Markdown')
                self.sender.sendMessage("Input the amount below", reply_markup=ForceReply())
        elif data == 'yes':

            global myid
            myid = from_id
            # firstname = user.get('first_name')

            if self.advertt == 'buy':
                try:
                    self.csure.deleteMessage()
                except Exception:
                    self.bsure.deleteMessage()
                global noreply
                global pytype
                global lotime

                pytype = 'buy'

                user = bot.getChat(from_id)
                firstname = user.get('first_name')
                global btotalcharge
                btotalcharge = round((officialb * 0.004), 8) + round(officialb, 8)

                # endchargeb = round(float(btotalcharge), 8) - round((officialb * 0.008), 8)
                newbala = self.cur.execute('SELECT newbalance FROM Investor WHERE investor=(?)', (useridentity,))
                newbl = newbala.fetchone()[0]
                userr = self.cur.execute('SELECT username FROM Investor WHERE investor=(?)', (useridentity,))
                ruser = userr.fetchone()[0]

                if btotalcharge < float(newbl):
                    message = '''Waiting for {}. If user doesn't appear within 30 minutes, the deal will be automatically cancelled.'''.format(
                        ruser)

                    buyat = self.sender.sendMessage(message, reply_markup=markup)
                    self.byat = telepot.helper.Editor(self.bot, buyat)
                    self.b_edit_msg_ident = telepot.message_identifier(buyat)
                    lotime = 0
                    noreply = 0

                    n = self.cur.execute('SELECT contact FROM Investor WHERE investor=(?)', (useridentity,))
                    neb = n.fetchone()[0]

                    if len(neb) > 5:
                        self.sender.sendMessage(
                            "*You can message/call seller at : {} if the seller takes too long to respond*".format(neb),
                            parse_mode="Markdown")

                    bot.sendMessage(useridentity, "You can send buyer a message", reply_markup=buymes)
                    t = (Decimal(officialb * 0.004))
                    txt = round(t, 8)

                    self.cur.execute('UPDATE Investor SET ncommission =(?) WHERE investor=(?)', (5, self.chat_id))
                    self.conn.commit()

                    buyset1 = bot.sendMessage(useridentity,
                                              "{} wants to buy bitcoins worth {} from you.\nTotal charges(service charge incl) : {}\n\nDo you want to proceed?".format(
                                                  firstname, round(Decimal(officialb), 8),
                                                  txt),
                                              reply_markup=user_deal)
                    global buyest
                    buyest = telepot.message_identifier(buyset1)
                    print(lotime)

                    def job():
                        self.conn = sqlite3.connect('trading.db')
                        self.cur = self.conn.cursor()
                        if lotime != 1:
                            try:
                                try:
                                    bot.deleteMessage(buyest)
                                except Exception:
                                    bot.deleteMessage(sellsett)
                            except Exception:
                                pass
                            self.sender.sendMessage('_Deal cancelled_', parse_mode='Markdown')
                            self.cur.execute('UPDATE Investor SET ncommission =(?) WHERE investor=(?)',
                                             (0, self.chat_id))
                            self.conn.commit()
                            bot.sendMessage(useridentity, '_Deal cancelled_', parse_mode='Markdown')
                            # except Exception:
                            #
                            #     bot.sendMessage(useridentify, '_Deal cancelled_', parse_mode='Markdown')
                            schedule.clear('check{}'.format(self.chat_id))
                        self.conn.commit()
                        self.cur.close()

                    def run_threaded(job_func):
                        job_thread = threading.Thread(target=job_func)
                        job_thread.start()

                    schedule.every(900).seconds.do(run_threaded, job).tag('check{}'.format(self.chat_id))


                else:
                    self.sender.sendMessage("*Seller is unavailable or has low volume*", parse_mode="Markdown")


            elif self.advertt == 'sell':
                try:
                    self.csure.deleteMessage()
                except Exception:
                    self.bsure.deleteMessage()
                pytype = 'sell'

                user = bot.getChat(useridentify)
                firstname = user.get('first_name')
                global stotalcharge
                stotalcharge = round((officials * 0.004), 8) + round(officials, 8)

                userr = self.cur.execute('SELECT username FROM Investor WHERE investor=(?)', (useridentify,))
                ruser = userr.fetchone()[0]
                # endcharges = round(float(stotalcharge), 8) - round((officials * 0.008), 8)

                message = '''Waiting for {}. If user doesn't appear within 30 minutes, the deal will be automatically cancelled.'''.format(
                    ruser)

                sellyat = self.sender.sendMessage(message, reply_markup=markup)
                self.sellat = telepot.helper.Editor(self.bot, sellyat)
                self.edit_msg = telepot.message_identifier(sellyat)
                n = self.cur.execute('SELECT contact FROM Investor WHERE investor =(?)', (useridentify,))
                neb = n.fetchone()[0]
                lotime = 0
                if len(neb) > 5:
                    self.sender.sendMessage(
                        "*You can message/call buyer at : {} if the buyer takes too long to respond*".format(neb),
                        parse_mode="Markdown")
                noreply = 0
                t = (Decimal(officials * 0.004))
                txt = round(t, 8)
                self.cur.execute('UPDATE Investor SET ncommission =(?) WHERE investor=(?)', (5, self.chat_id))
                self.conn.commit()
                sett2 = bot.sendMessage(useridentify,
                                        "{} wants to sell bitcoins worth {} to you.\nTotal charges(service charge incl) : {}\n\nDo you want to proceed?".format(
                                            firstname, round(Decimal(officials), 8), txt),
                                        reply_markup=user_deal)

                bot.sendMessage(useridentify, "You can send buyer a message", reply_markup=sellmes)
                global sellsett
                sellsett = telepot.message_identifier(sett2)

                def job():
                    self.conn = sqlite3.connect('trading.db')
                    self.cur = self.conn.cursor()
                    if lotime != 1:
                        try:
                            try:
                                bot.deleteMessage(buyest)
                            except Exception:
                                bot.deleteMessage(sellsett)
                        except Exception:
                            pass
                        self.sender.sendMessage('_Deal cancelled_', parse_mode='Markdown')
                        self.cur.execute('UPDATE Investor SET ncommission =(?) WHERE investor=(?)', (0, self.chat_id))
                        self.conn.commit()
                        bot.sendMessage(useridentify, '_Deal cancelled_', parse_mode='Markdown')
                        # except Exception:
                        #
                        #     bot.sendMessage(useridentity, '_Deal cancelled_', parse_mode='Markdown')
                        schedule.clear('checker{}'.format(self.chat_id))

                    self.conn.commit()
                    self.cur.close()

                def run_threaded(job_func):
                    job_thread = threading.Thread(target=job_func)
                    job_thread.start()

                schedule.every(900).seconds.do(run_threaded, job).tag('checker{}'.format(self.chat_id))
        elif data == 'buymes':
            self.sender.sendMessage("Type your message below", reply_markup=ForceReply())
        elif data == 'sellmes':
            self.sender.sendMessage("Input your message below", reply_markup=ForceReply())
        elif data == 'no':
            try:
                try:
                    bot.deleteMessage(buyest)
                except Exception:
                    bot.deleteMessage(sellsett)
            except Exception:
                pass
            self.sender.sendMessage("Your deal has been cancelled.", reply_markup=markup)

        elif data == 'verify':
            self.sender.sendMessage('''Please send us a photo of your *identity card* and *selfie (photo of your face)* near *identity card*.

1) _Restricted to use any image editor._ 
2) _Required information should be clearly visible._ 
3) _We do not guarantee that we will mark your account as "verified" or contact you_
''', parse_mode='Markdown')
            self.sender.sendMessage('To go back to Main Menu >> /menu')
            self.sender.sendMessage("*Please upload photo for verification*", parse_mode="Markdown",
                                    reply_markup=ForceReply())
        elif data == 'yup':
            try:
                bot.deleteMessage(buyest)
            except Exception:
                bot.deleteMessage(sellsett)
            noreply = 1
            lotime = 1
            self.advert_type(pytype)

            if self.advertt == 'buy':

                newbala = self.cur.execute('SELECT newbalance FROM Investor WHERE investor=(?)', (from_id,))
                newbl = newbala.fetchone()[0]

                if btotalcharge < float(newbl):

                    self.cur.execute('UPDATE Investor SET done =(?) WHERE investor=(?)',
                                     (1, from_id))
                    currentDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.cur.execute(
                        "INSERT INTO transactions(buyer,seller,amount,date) VALUES (?,?,?,?)",
                        (from_id, myid, round(btotalcharge, 8), currentDate))
                    self.conn.commit()
                    self.cur.execute('UPDATE Investor SET ncommission =(?) WHERE investor=(?)', (5, myid))
                    self.conn.commit()
                    self.cur.execute('UPDATE Investor SET ncommission =(?) WHERE investor=(?)', (5, self.chat_id))
                    self.conn.commit()
                    bot.sendMessage(useridentity,
                                    'Send your _money destination(account/email/id)_ to the buyer by pressing /destination followed by _money destination_ where the fund will be sent.',
                                    parse_mode='Markdown')
                    self.sender.sendMessage('*!Your funds have been locked until the transaction is done!*',
                                            parse_mode='Markdown')

                    bot.sendMessage(myid,
                                    '_Transaction initiated. Please wait for the address where you should send money to _',
                                    parse_mode='Markdown')

                else:
                    self.sender.sendMessage("Insufficient funds to proceed with the transaction")

            elif self.advertt == 'sell':

                self.advert_type(pytype)
                newbal = self.cur.execute('SELECT newbalance FROM Investor WHERE investor=(?)', (useridentify,))
                newsl = newbal.fetchone()[0]

                self.cur.execute('UPDATE Investor SET done =(?) WHERE investor=(?)',
                                 (1, myid))
                currentDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.cur.execute(
                    "INSERT INTO transactions(buyer,seller,amount,date) VALUES (?,?,?,?)",
                    (from_id, myid, round(stotalcharge, 8), currentDate))
                self.conn.commit()
                self.cur.execute('UPDATE Investor SET ncommission =(?) WHERE investor=(?)', (5, myid))
                self.conn.commit()
                self.cur.execute('UPDATE Investor SET ncommission =(?) WHERE investor=(?)', (5, self.chat_id))
                self.conn.commit()

                bot.sendMessage(myid,
                                'Send your _money destination(account/email/id)_ to the buyer by pressing /destination followed by _money destination_ where the fund will be sent.',
                                parse_mode='Markdown')
                bot.sendMessage(myid, '*!Your funds have been locked until the transaction is done!*',
                                parse_mode='Markdown')

                self.sender.sendMessage(
                    '_Transaction initiated. Please wait for the address where the money should be sent to_',
                    parse_mode='Markdown')

        elif data == 'unlock':
            try:
                try:
                    bot.deleteMessage(medit1)

                except Exception:
                    bot.deleteMessage(medit)

            except Exception:
                pass

            try:
                try:
                    bot.deleteMessage(chekbuy)
                except Exception:
                    bot.deleteMessage(cheksell)
            except Exception:
                pass
            self.advert_type(pytype)

            if self.advertt == 'buy':
                self.cur.execute('UPDATE Investor SET ncommission =(?) WHERE investor=(?)', (0, useridentity))
                self.conn.commit()

                self.cur.execute('UPDATE Investor SET ncommission =(?) WHERE investor=(?)', (0, myid))
                self.conn.commit()
                self.cur.execute('UPDATE Investor SET done =(?) WHERE investor=(?)',
                                 (0, useridentity))
                self.sender.sendMessage(
                    "You have resolved the dispute and unlocked {} funds".format(useridentity),
                    parse_mode="Markdown")
                bot.sendMessage(myid,
                                "*Dispute solved*",
                                parse_mode="Markdown")
                bot.sendMessage(useridentity,
                                "Your funds have been unlocked",
                                parse_mode="Markdown")


            elif self.advertt == 'sell':
                self.cur.execute('UPDATE Investor SET ncommission =(?) WHERE investor=(?)', (0, useridentify))
                self.conn.commit()

                self.cur.execute('UPDATE Investor SET ncommission =(?) WHERE investor=(?)', (0, myid))
                self.conn.commit()
                self.cur.execute('UPDATE Investor SET done =(?) WHERE investor=(?)',
                                 (0, myid))

                self.sender.sendMessage(
                    "You have resolved the dispute and unlocked {} funds".format(myid),
                    parse_mode="Markdown")
                bot.sendMessage(useridentify,
                                "*Dispute solved*",
                                parse_mode="Markdown")
                bot.sendMessage(myid,
                                "Your funds have been unlocked",
                                parse_mode="Markdown")


        elif data == 'donefund':  # i have received funds
            self.advert_type(pytype)
            # self.counter += 1
            # print(self.counter)

            # if self.counter < 2:
            self.cur.execute('UPDATE Investor SET ncommission =(?) WHERE investor=(?)', (0, self.chat_id))
            self.conn.commit()
            try:
                try:
                    bot.deleteMessage(medit1)

                except Exception:
                    bot.deleteMessage(medit)

            except Exception:
                pass

            try:
                try:
                    bot.deleteMessage(chekbuy)
                except Exception:
                    bot.deleteMessage(cheksell)
            except Exception:
                pass

            if self.advertt == 'buy':
                self.cur.execute('UPDATE Investor SET ncommission =(?) WHERE investor=(?)', (0, useridentity))
                self.conn.commit()

                self.cur.execute('UPDATE Investor SET ncommission =(?) WHERE investor=(?)', (0, myid))
                self.conn.commit()
                worthla = self.cur.execute('SELECT worth FROM Investor WHERE investor=(?)', (useridentity,))
                worthy = worthla.fetchone()[0]

                worth = self.cur.execute('SELECT worth FROM Investor WHERE investor=(?)', (myid,))
                worthly = worth.fetchone()[0]

                newbala = self.cur.execute('SELECT newbalance FROM Investor WHERE investor=(?)', (useridentity,))
                newbl = newbala.fetchone()[0]

                nwbala = self.cur.execute('SELECT newbalance FROM Investor WHERE investor=(?)', (myid,))
                nwbl = nwbala.fetchone()[0]

                mydeal = self.cur.execute('SELECT deal FROM Investor WHERE investor=(?)', (useridentity,))
                dealmine = mydeal.fetchone()[0]

                hisdeal = self.cur.execute('SELECT deal FROM Investor WHERE investor=(?)', (myid,))
                dealhis = hisdeal.fetchone()[0]

                try:
                    aff = self.cur.execute('SELECT owner FROM Affiliate WHERE ref= (?)', (refferal,))
                    affiliat = aff.fetchone()[0]

                    nbl = self.cur.execute('SELECT commission FROM Investor WHERE investor=(?)', (affiliat,))
                    nebly = nbl.fetchone()[0]

                    rr = (Decimal(nebly) + Decimal(sherlockb))

                    rtt = round(rr, 8)

                    self.cur.execute('UPDATE Investor SET commission =(?) WHERE investor=(?)',
                                     (float(rtt), int(affiliat)))
                    currentDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    appendMe = '\n{} : + commission : {} BTC '.format(currentDate, round(Decimal(sherlockb), 8))
                    appendFile = open('{}.txt'.format(affiliat), 'a')
                    appendFile.write(appendMe)
                    appendFile.close()
                    self.conn.commit()
                except Exception:
                    print("No affiliate to profit")

                currentDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.cur.execute('UPDATE Investor SET newbalance =(?) WHERE investor=(?)',
                                 ('{}'.format(newbl - btotalcharge), useridentity))
                appendMe = '\n{} :  - Trade complete: {} '.format(currentDate, endchargeb)
                appendFile = open('{}.txt'.format(useridentity), 'a')
                appendFile.write(appendMe)
                appendFile.close()
                appendM = '\n{} :  + Trade complete: {} '.format(currentDate, endchargeb)
                appendFile = open('{}.txt'.format(myid), 'a')
                appendFile.write(appendM)
                appendFile.close()

                if 'disput' in globals():
                    print('disput', ' ', disput)
                    if disput == 0:
                        self.cur.execute('UPDATE Investor SET ncommission =(?) WHERE investor=(?)', (0, useridentity))
                        self.conn.commit()

                        self.cur.execute('UPDATE Investor SET ncommission =(?) WHERE investor=(?)', (0, myid))
                        self.conn.commit()
                        self.sender.sendMessage(
                            "You have resolved the dispute and marked the transaction as complete.",
                            parse_mode="Markdown")
                        bot.sendMessage(myid,
                                        "You have received *{} BTC*.".format(
                                            endchargeb),
                                        parse_mode="Markdown")
                        bot.sendMessage(useridentity,
                                        "Dispute resolved.",
                                        parse_mode="Markdown")
                    else:
                        self.sender.sendMessage(
                            "You have marked the transaction as complete.\n\nRate the seller by typing _good_ or _bad_",
                            parse_mode="Markdown")
                        bot.sendMessage(myid,
                                        "You have received *{} BTC*.\n\nRate the seller by typing _good_ or _bad_".format(
                                            endchargeb),
                                        parse_mode="Markdown")
                else:
                    self.sender.sendMessage(
                        "You have marked the transaction as complete.\n\nRate the seller by typing _good_ or _bad_",
                        parse_mode="Markdown")
                    bot.sendMessage(myid,
                                    "You have received *{} BTC*.\n\nRate the seller by typing _good_ or _bad_".format(
                                        endchargeb),
                                    parse_mode="Markdown")

                self.cur.execute('UPDATE Investor SET done =(?) WHERE investor=(?)',
                                 (0, useridentity))

                self.cur.execute('UPDATE Investor SET newbalance =(?) WHERE investor=(?)',
                                 ('{}'.format(nwbl + round(float(endchargeb), 8)), myid))

                self.cur.execute('UPDATE Investor SET deal =(?) WHERE investor=(?)',
                                 ('{}'.format(dealmine + 1), useridentity))
                self.cur.execute('UPDATE Investor SET deal =(?) WHERE investor=(?)',
                                 ('{}'.format(dealhis + 1), myid))
                self.cur.execute('UPDATE Investor SET worth =(?) WHERE investor=(?)',
                                 ('{}'.format(worthy + float(officialb)), useridentity))
                self.cur.execute('UPDATE Investor SET worth =(?) WHERE investor=(?)',
                                 ('{}'.format(worthly + float(officialb)), myid))
                self.cur.execute('UPDATE Investor SET done =(?) WHERE investor=(?)', (0, useridentity))
                disput = 1

            elif self.advertt == 'sell':
                self.cur.execute('UPDATE Investor SET ncommission =(?) WHERE investor=(?)', (0, useridentify))
                self.conn.commit()
                self.cur.execute('UPDATE Investor SET ncommission =(?) WHERE investor=(?)', (0, myid))
                self.conn.commit()
                worthla = self.cur.execute('SELECT worth FROM Investor WHERE investor=(?)', (myid,))
                worthy = worthla.fetchone()[0]

                worth = self.cur.execute('SELECT worth FROM Investor WHERE investor=(?)', (useridentify,))
                worthly = worth.fetchone()[0]

                mydeal = self.cur.execute('SELECT deal FROM Investor WHERE investor=(?)', (myid,))
                dealmine = mydeal.fetchone()[0]

                hisdeal = self.cur.execute('SELECT deal FROM Investor WHERE investor=(?)', (useridentify,))
                dealhis = hisdeal.fetchone()[0]

                newbala = self.cur.execute('SELECT newbalance FROM Investor WHERE investor=(?)', (myid,))
                newbl = newbala.fetchone()[0]

                nwbala = self.cur.execute('SELECT newbalance FROM Investor WHERE investor=(?)', (useridentify,))
                nwbl = nwbala.fetchone()[0]

                try:
                    aff = self.cur.execute('SELECT owner FROM Affiliate WHERE ref= (?)', (refferal,))
                    affiliat = aff.fetchone()[0]

                    nbl = self.cur.execute('SELECT commission FROM Investor WHERE investor=(?)', (affiliat,))
                    nebly = nbl.fetchone()[0]

                    rr = (Decimal(nebly) + Decimal(sherlocks))

                    rtt = round(rr, 8)

                    self.cur.execute('UPDATE Investor SET commission =(?) WHERE investor=(?)',
                                     (float(rtt), int(affiliat)))
                    currentDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    appendMe = '\n{} : + commission : {} BTC '.format(currentDate, round(Decimal(sherlocks), 8))
                    appendFile = open('{}.txt'.format(affiliat), 'a')
                    appendFile.write(appendMe)
                    appendFile.close()
                    self.conn.commit()
                except Exception:
                    print("No affiliate to profit")

                self.cur.execute('UPDATE Investor SET newbalance =(?) WHERE investor=(?)',
                                 ('{}'.format(newbl - stotalcharge), myid))
                currentDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                appendMe = '\n{} :  - Trade complete: {} BTC '.format(
                    currentDate, endcharges)
                appendFile = open('{}.txt'.format(myid), 'a')
                appendFile.write(appendMe)
                appendFile.close()
                appendM = '\n {} :  + Trade complete: {} BTC '.format(
                    currentDate, endcharges)
                appendFile = open('{}.txt'.format(useridentify), 'a')
                appendFile.write(appendM)
                appendFile.close()
                if 'disput' in globals():
                    if disput == 0:
                        self.cur.execute('UPDATE Investor SET ncommission =(?) WHERE investor=(?)', (0, useridentify))
                        self.conn.commit()

                        self.cur.execute('UPDATE Investor SET ncommission =(?) WHERE investor=(?)', (0, myid))
                        self.conn.commit()
                        self.sender.sendMessage(
                            "You have resolved the dispute and marked the transaction as complete.",
                            parse_mode="Markdown")
                        bot.sendMessage(useridentify,
                                        "You have received *{} BTC*.".format(
                                            endcharges),
                                        parse_mode="Markdown")
                        bot.sendMessage(myid,
                                        "Dispute resolved.",
                                        parse_mode="Markdown")
                    else:
                        self.sender.sendMessage(
                            "You have marked the transaction as complete.\n\nRate the seller by typing _good_ or _bad_",
                            parse_mode="Markdown")
                        bot.sendMessage(useridentify,
                                        "You have received *{} BTC*.\n\nRate the seller by typing _good_ or _bad_".format(
                                            endcharges),
                                        parse_mode="Markdown")

                else:
                    self.sender.sendMessage(
                        "You have marked the transaction as complete.\n\nRate the seller by typing _good_ or _bad_",
                        parse_mode="Markdown")
                    bot.sendMessage(useridentify,
                                    "You have received *{} BTC*.\n\nRate the seller by typing _good_ or _bad_".format(
                                        endcharges),
                                    parse_mode="Markdown")

                self.cur.execute('UPDATE Investor SET done =(?) WHERE investor=(?)',
                                 (0, myid))
                self.cur.execute('UPDATE Investor SET newbalance =(?) WHERE investor=(?)',
                                 ('{}'.format(nwbl + round(float(endcharges), 8)), useridentify))

                self.cur.execute('UPDATE Investor SET deal =(?) WHERE investor=(?)',
                                 ('{}'.format(dealmine + 1), myid))
                self.cur.execute('UPDATE Investor SET deal =(?) WHERE investor=(?)',
                                 ('{}'.format(dealhis + 1), useridentify))

                self.cur.execute('UPDATE Investor SET worth =(?) WHERE investor=(?)',
                                 ('{}'.format(worthy + float(officials)), myid))
                self.cur.execute('UPDATE Investor SET worth =(?) WHERE investor=(?)',
                                 ('{}'.format(worthly + float(officials)), useridentify))
                self.cur.execute('UPDATE Investor SET done =(?) WHERE investor=(?)', (0, myid))
                disput = 1
                # subtract total charge from balance

                # else:
                #     self.counter = 0
                #     print(self.counter)




        elif data == 'meditate':
            try:
                try:
                    bot.deleteMessage(cheksell)
                except Exception:
                    bot.deleteMessage(chekbuy)
            except Exception:
                pass
            # self.counter2 += 1
            # print(self.counter2)

            # if self.counter2 < 2:
            dspt = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Release the funds ', callback_data='donefund')],
                [InlineKeyboardButton(text='Unlock funds', callback_data='unlock')],
            ])

            disput = 0
            try:
                user = bot.getChat(useridentity)
                first1 = user.get('first_name')
                user = bot.getChat(myid)
                first2 = user.get('first_name')

                bot.sendMessage(useridentity,
                                "Dispute process initiated contact [Support](https://t.me/CryptoscrowHelp_bot/) to solve issue",
                                parse_mode='Markdown', reply_markup=markup)
                bot.sendMessage(myid,
                                "Dispute process initiated contact [Support](https://t.me/CryptoscrowHelp_bot/) to solve issue",
                                parse_mode='Markdown', reply_markup=markup)
                real = '234578692'
                med1 = bot.sendMessage('234578692',
                                       "{}={} has an issue with his trade with {}={} :PRICE => {}".format(
                                           useridentity,
                                           first1, myid,
                                           first2,
                                           round(
                                               Decimal(
                                                   btotalcharge),
                                               8)),
                                       reply_markup=dspt)

                medit = telepot.message_identifier(med1)

                self.counter1 = 0
            except Exception:
                user = bot.getChat(useridentify)
                first1 = user.get('first_name')
                user = bot.getChat(myid)
                first2 = user.get('first_name')

                bot.sendMessage(useridentify,
                                "Dispute process initiated contact [Support](https://t.me/CryptoscrowHelp_bot/) to solve issue",
                                parse_mode='Markdown', reply_markup=markup)
                bot.sendMessage(myid,
                                "Dispute process initiated contact [Support](https://t.me/CryptoscrowHelp_bot/) to solve issue",
                                parse_mode='Markdown', reply_markup=markup)
                med2 = bot.sendMessage('234578692',
                                       "{}={} has an issue with his trade with {}={} :PRICE => {}".format(myid,
                                                                                                          first2,
                                                                                                          useridentify,
                                                                                                          first1,
                                                                                                          round(
                                                                                                              Decimal(
                                                                                                                  stotalcharge),
                                                                                                              8)),
                                       reply_markup=dspt)

                medit1 = telepot.message_identifier(med2)

                # self.counter1 = 0
                # else:
                #     self.counter2 = 0

        elif data == 'checkdone':  # i have sent funds
            try:
                try:
                    bot.deleteMessage(destin)
                except Exception:
                    bot.deleteMessage(destin1)
            except Exception:
                pass
            # self.counter1 += 1
            # print(self.counter1)

            # if self.counter1 < 2:
            if self.advertt == 'buy':

                self.sender.sendMessage('_Message sent_', parse_mode="Markdown")
                buys = bot.sendMessage(useridentity,
                                       '_Buyer has verified he has sent payment to the destination address you sent him_',
                                       parse_mode="Markdown", reply_markup=check_info1)

                chekbuy = telepot.message_identifier(buys)
                self.counter1 = 0
            elif self.advertt == 'sell':

                self.sender.sendMessage('_Message sent_', parse_mode='Markdown')
                bus = bot.sendMessage(myid,
                                      '_Buyer has verified he has sent payment to the destination address you sent him_',
                                      parse_mode='Markdown', reply_markup=check_info1)
                cheksell = telepot.message_identifier(bus)
                self.counter1 = 0

        elif data == 'myadvert':

            note = self.currency_code(from_id)

            fech = self.cur.execute('SELECT ROWID,price,min,max FROM Buy WHERE identifier=(?) AND currency=(?)',
                                    (from_id, note))
            teach = fech.fetchall()

            fe = self.cur.execute('SELECT ROWID,price,min,max FROM Sell WHERE identifier=(?) AND currency=(?)',
                                  (from_id, note))
            tea = fe.fetchall()

            if bool(tea) or bool(teach):
                global Q
                Q = []
                for records in teach:
                    Q.append(
                        '👉🏻 ' + str(records[0]) + ' - margin - ' + str(records[1]) + " % " +
                        str(records[2]) + ' to ' + str(records[3]))

                message = '_Here you can edit your adverts_'

                buys = self.sender.sendMessage(message, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=list(
                        (map(lambda c: [InlineKeyboardButton(text=str(c), callback_data=str(c))], Q)))))
                self.editing = telepot.helper.Editor(self.bot, buys)
                self.edit_msg = telepot.message_identifier(buys)
                try:
                    for records in tea:
                        Q.append(
                            '👈🏻 ' + str(records[0]) + ' - margin - ' + str(records[1]) + " % " + str(
                                records[2]) + ' to ' + str(records[3]))

                    self.editing.editMessageReplyMarkup(reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=list(
                            (map(lambda c: [InlineKeyboardButton(text=str(c), callback_data=str(c))], Q)))))
                except Exception:
                    pass
            else:
                self.sender.sendMessage("*You don't have an Advert in this section*", parse_mode='Markdown')

        elif data == 'aff':
            message = '''*Earn Passive Income Via our Affiliate Program:*

Invite new users and earn 💵 passive income 💵.

Commission >> 0.2%

For example: if your affiliate referral make a transaction of 2 BTC, you will earn 0.004 BTC of dividends credited to your wallet each time your referral(s) make make transactions.

Affiliate program is perpetual; it has no limits for invitations and you can act immediately to start earning.

Keep in mind, for good results you should select right category of buyers/sellers who want to buy or sell BTC.

Invite users via the link below.'''

            mess_link = 'https://t.me/Cryptoscrow_bot?start={}'.format(from_id)
            self.sender.sendMessage(message, parse_mode='Markdown')
            self.sender.sendMessage(mess_link)

            # owner == command  #==ref from_id
            # so ref was brought in under owner
            # we should check if refs were stored under kush
            affiliate = self.cur.execute('SELECT DISTINCT ref FROM Affiliate WHERE owner=(?) AND owner!= ref',
                                         (from_id,))
            fili = affiliate.fetchall()
            if bool(fili):
                noda = '''Below 👇 is a list of your referral(s)'''

                self.sender.sendMessage(noda, reply_markup=markup)
                for i in fili:
                    for me in i:
                        user = bot.getChat(me)
                        first = user.get('first_name')

                        self.sender.sendMessage("{}".format(first))

                self.conn.commit()
                self.sender.sendMessage("Press /redeem to get your commission ready for withdrawal")
            else:
                self.sender.semdMessage("You dont have anybody under you")
        elif data.startswith('👉🏻'):
            finger = 'b'
            note = self.currency_code(from_id)
            exb = data.split()[1]
            self.order_type('exb')
            fe = self.cur.execute('SELECT processor,price,min,max FROM Buy WHERE ROWID=(?) AND currency=(?)',
                                  (exb, note))
            tea = fe.fetchone()
            sent = self.sender.sendMessage(
                '''📰 My ads\n\n*Payment method*: _{}_\n*BTC Margin*: _{}%_\n*Min. value*: _{:,} {}_\n*Max. value*: _{:,} {}_\n*Status*: _Active_'''.format(
                    tea[0], tea[1], tea[2], note, tea[3], note), parse_mode='Markdown', reply_markup=chang1)
            self.edb = telepot.helper.Editor(self.bot, sent)
            self.edit_msg = telepot.message_identifier(sent)


        elif data.startswith('👈🏻'):
            finger = 's'
            note = self.currency_code(from_id)
            exs = data.split()[1]
            self.order_type('exs')
            fe = self.cur.execute('SELECT processor,price,min,max FROM Sell WHERE ROWID=(?) AND currency=(?)',
                                  (exs, note))
            tea = fe.fetchone()
            sent = self.sender.sendMessage(
                '''📰 My ads\n\n*Payment method*: _{}_\n*BTC Margin*: _{}%_\n*Min. value*: _{:,} {}_\n*Max. value*: _{:,} {}_\n*Status*: _Active_'''.format(
                    tea[0], tea[1], tea[2], note, tea[3], note), parse_mode='Markdown', reply_markup=chang1)
            self.eds = telepot.helper.Editor(self.bot, sent)
            self.edit_msg = telepot.message_identifier(sent)

        elif data == 'contact':
            marku = ForceReply()
            self.sender.sendMessage('To go back to Main Menu >> /menu')
            self.sender.sendMessage(
                "Add your contact number here for potential buyers/sellers to contact you when you're offline",
                reply_markup=marku)
        elif data == 'term_s':
            self.sender.sendMessage("Please add your terms below", reply_markup=ForceReply())
        elif data == 'marg':
            self.sender.sendMessage(
                "🔗*Margin*\n\nTo edit the margin used for this ad input your number followed by percentage sign Example  2 %",
                parse_mode='Markdown')

        elif data == 'limit':
            self.sender.sendMessage(
                "📏*Limit*\n\nTo edit the limits.Write min. and max. limits in USD.For example: 1 to 1000000",
                parse_mode='Markdown')

        # ==================================================================================================================================
        # UPDATE NEEDS TO BE INCLUDED
        # ===================================================================================================================================

        elif data == "deactivate":
            note = self.currency_code(from_id)
            if finger == 'b':
                fe = self.cur.execute('SELECT processor,price,min,max FROM Buy WHERE ROWID=(?) AND currency=(?)',
                                      (exb, note))
                tea = fe.fetchall()[0]

                self.edb.editMessageText(
                    '''📰 My ads\n\n*Payment method*: _{}_\n*BTC Margin*: _{}%_\n*Min. value*: _{} USD_\n*Max. value*: _{} USD_\n*Status*: _Inactive_'''.format(
                        tea[0], tea[1], tea[2], tea[3]), parse_mode='Markdown', reply_markup=chang2)
                self.cur.execute('UPDATE Buy SET status =(?) WHERE ROWID=(?)',
                                 (1, exb))
                self.conn.commit()

            elif finger == 's':
                fe = self.cur.execute('SELECT processor,price,min,max FROM Sell WHERE ROWID=(?) AND currency=(?)',
                                      (exs, note))
                tea = fe.fetchall()[0]

                self.eds.editMessageText(
                    '''📰 My ads\n\n*Payment method*: _{}_\n*BTC Margin*: _{}%_\n*Min. value*: _{} USD_\n*Max. value*: _{} USD_\n*Status*: _Inactive_'''.format(
                        tea[0], tea[1], tea[2], tea[3]), parse_mode='Markdown', reply_markup=chang2)
                self.cur.execute('UPDATE Sell SET status =(?) WHERE ROWID=(?)',
                                 (1, exs))
                self.conn.commit()


        elif data == 'activate':
            note = self.currency_code(from_id)
            if finger == 'b':
                fe = self.cur.execute('SELECT processor,price,min,max FROM Buy WHERE ROWID=(?) AND currency=(?)',
                                      (exb, note))
                tea = fe.fetchall()[0]

                self.edb.editMessageText(
                    '''📰 My ads\n\n*Payment method*: _{}_\n*BTC Margin*: _{}%_\n*Min. value*: _{} USD_\n*Max. value*: _{} USD_\n*Status*: _Active_'''.format(
                        tea[0], tea[1], tea[2], tea[3]), parse_mode='Markdown', reply_markup=chang1)
                self.cur.execute('UPDATE Buy SET status =(?) WHERE ROWID=(?)',
                                 (0, exb))
                self.conn.commit()


            elif finger == 's':
                fe = self.cur.execute('SELECT processor,price,min,max FROM Sell WHERE ROWID=(?) AND currency=(?)',
                                      (exs, note))
                tea = fe.fetchall()[0]

                self.eds.editMessageText(
                    '''📰 My ads\n\n*Payment method*: _{}_\n*BTC Margin*: _{}%_\n*Min. value*: _{} USD_\n*Max. value*: _{} USD_\n*Status*: _Active_'''.format(
                        tea[0], tea[1], tea[2], tea[3]), parse_mode='Markdown', reply_markup=chang1)

                self.cur.execute('UPDATE Sell SET status =(?) WHERE ROWID=(?)',
                                 (0, exs))
                self.conn.commit()
        elif data == 'delad':
            note = self.currency_code(from_id)
            if finger == 'b':
                self.cur.execute('DELETE FROM Buy WHERE ROWID=(?)', (exb,))
                self.conn.commit()
                self.edb.deleteMessage()
                self.sender.sendMessage("Ad deleted")

            elif finger == 's':
                self.cur.execute('DELETE FROM Sell WHERE ROWID=(?)', (exs,))
                self.conn.commit()
                self.eds.deleteMessage()
                self.sender.sendMessage("Ad deleted")
        # =======================================================================================================================================

        # ======================================================================================================================================
        elif data == 'comm':
            message = "Join our channel >> @cryptoscrow_bot_channel"
            self.sender.sendMessage(message)
        elif data == 'rep':
            try:
                report= InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Next', callback_data='next1')],
                ])
                # readMe = open('{}.txt'.format(from_id), 'r').read()
                lines = []  # Declare an empty list named "lines"
                with open('{}.txt'.format(from_id), 'r') as in_file:  # Open file lorem.txt for reading of text data.
                    for line in in_file:  # For each line of text store in a string variable named "line", and
                        lines.append(line)  # add that line to our list of lines.
                lines.reverse()
                print(lines)
                liner = self.sender.sendMessage(" ".join(lines[0:30]), parse_mode='Markdown', reply_markup=report)
                self.liner = telepot.helper.Editor(self.bot, liner)

            except Exception:
                self.sender.sendMessage('*No recorded data found*', parse_mode='Markdown')

        elif data == 'next1':
            try:
                report= InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Next', callback_data='next2'),
                     InlineKeyboardButton(text='Back', callback_data='back2')],
                ])
                # readMe = open('{}.txt'.format(from_id), 'r').read()
                lines = []  # Declare an empty list named "lines"
                with open('{}.txt'.format(from_id), 'r') as in_file:  # Open file lorem.txt for reading of text data.
                    for line in in_file:  # For each line of text store in a string variable named "line", and
                        lines.append(line)  # add that line to our list of lines.
                lines.reverse()
                liner = self.liner.editMessageText(" ".join(lines[31:60]), parse_mode='Markdown', reply_markup=report)
                self.liner = telepot.helper.Editor(self.bot, liner)
            except Exception:
                self.sender.sendMessage("No more data to display")

        elif data == 'next2':
            try:
                report = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Next', callback_data='next3'),
                     InlineKeyboardButton(text='Back', callback_data='back3')],
                ])
                # readMe = open('{}.txt'.format(from_id), 'r').read()
                lines = []  # Declare an empty list named "lines"
                with open('{}.txt'.format(from_id), 'r') as in_file:  # Open file lorem.txt for reading of text data.
                    for line in in_file:  # For each line of text store in a string variable named "line", and
                        lines.append(line)  # add that line to our list of lines.
                lines.reverse()
                liner = self.liner.editMessageText(" ".join(lines[61:90]), parse_mode='Markdown', reply_markup=report)
                self.liner = telepot.helper.Editor(self.bot, liner)
            except Exception:
                self.sender.sendMessage("No more data to display")


        elif data == 'next3':
            try:
                report = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Next', callback_data='next4'),
                     InlineKeyboardButton(text='Back', callback_data='back4')],
                ])
                # readMe = open('{}.txt'.format(from_id), 'r').read()
                lines = []  # Declare an empty list named "lines"
                with open('{}.txt'.format(from_id), 'r') as in_file:  # Open file lorem.txt for reading of text data.
                    for line in in_file:  # For each line of text store in a string variable named "line", and
                        lines.append(line)  # add that line to our list of lines.
                lines.reverse()
                liner = self.liner.editMessageText(" ".join(lines[91:120]), parse_mode='Markdown', reply_markup=report)
                self.liner = telepot.helper.Editor(self.bot, liner)
            except Exception:
                self.sender.sendMessage("No more data to display")


        elif data == 'next4':
            try:
                report = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Back', callback_data='back5')],
                ])
                # readMe = open('{}.txt'.format(from_id), 'r').read()
                lines = []  # Declare an empty list named "lines"
                with open('{}.txt'.format(from_id), 'r') as in_file:  # Open file lorem.txt for reading of text data.
                    for line in in_file:  # For each line of text store in a string variable named "line", and
                        lines.append(line)  # add that line to our list of lines.

                lines.reverse()
                liner = self.liner.editMessageText(" ".join(lines[121:150]), parse_mode='Markdown',
                                                    reply_markup=report)
                self.liner = telepot.helper.Editor(self.bot, liner)
            except Exception:
                self.sender.sendMessage("No more data to display")

        elif data == 'back5':
            try:
                report = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Next', callback_data='next4'),
                     InlineKeyboardButton(text='Back', callback_data='back4')],
                ])
                # readMe = open('{}.txt'.format(from_id), 'r').read()
                lines = []  # Declare an empty list named "lines"
                with open('{}.txt'.format(from_id), 'r') as in_file:  # Open file lorem.txt for reading of text data.
                    for line in in_file:  # For each line of text store in a string variable named "line", and
                        lines.append(line)  # add that line to our list of lines.

                lines.reverse()
                liner = self.liner.editMessageText(" ".join(lines[91:120]), parse_mode='Markdown', reply_markup=report)
                self.liner = telepot.helper.Editor(self.bot, liner)
            except Exception:
                self.sender.sendMessage("No more data to display")

        elif data == 'back4':
            try:
                report = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Next', callback_data='next3'),
                     InlineKeyboardButton(text='Back', callback_data='back3')],
                ])
                # readMe = open('{}.txt'.format(from_id), 'r').read()
                lines = []  # Declare an empty list named "lines"
                with open('{}.txt'.format(from_id), 'r') as in_file:  # Open file lorem.txt for reading of text data.
                    for line in in_file:  # For each line of text store in a string variable named "line", and
                        lines.append(line)  # add that line to our list of lines.
                lines.reverse()
                liner = self.liner.editMessageText(" ".join(lines[61:90]), parse_mode='Markdown', reply_markup=report)
                self.liner = telepot.helper.Editor(self.bot, liner)
            except Exception:
                self.sender.sendMessage("No more data to display")

        elif data == 'back3':
            try:
                report = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Next', callback_data='next2'),
                     InlineKeyboardButton(text='Back', callback_data='back2')],
                ])
                # readMe = open('{}.txt'.format(from_id), 'r').read()
                lines = []  # Declare an empty list named "lines"
                with open('{}.txt'.format(from_id), 'r') as in_file:  # Open file lorem.txt for reading of text data.
                    for line in in_file:  # For each line of text store in a string variable named "line", and
                        lines.append(line)  # add that line to our list of lines.
                lines.reverse()
                liner = self.liner.editMessageText(" ".join(lines[31:60]), parse_mode='Markdown', reply_markup=report)
                self.liner = telepot.helper.Editor(self.bot, liner)
            except Exception:
                self.sender.sendMessage("No more data to display")

        elif data == 'back2':
            try:
                report = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Next', callback_data='next1'), ],
                ])
                # readMe = open('{}.txt'.format(from_id), 'r').read()
                lines = []  # Declare an empty list named "lines"
                with open('{}.txt'.format(from_id), 'r') as in_file:  # Open file lorem.txt for reading of text data.
                    for line in in_file:  # For each line of text store in a string variable named "line", and
                        lines.append(line)  # add that line to our list of lines.
                lines.reverse()
                liner = self.liner.editMessageText(" ".join(lines[0:30]), parse_mode='Markdown', reply_markup=report)
                self.liner = telepot.helper.Editor(self.bot, liner)
            except Exception:
                self.sender.sendMessage("No more data to display")





        elif data == 'terms':
            self.sender.sendMessage("*Here are the terms and conditions*", parse_mode='Markdown')
            self.sender.sendDocument('BQADBAADiAIAAtB74FBh_9SPlj_RJQI')
            self.sender.sendDocument('BQADBAADEgMAAuVRWFC3RITtJ9-HuwI')
            self.sender.sendDocument('BQADBAADhwIAAtB74FCZfdx6gh0g8AI')
        elif data == 'support':
            self.sender.sendMessage(
                "To contact support : [Support](https://t.me/CryptoscrowHelp_bot/) ",
                parse_mode='Markdown')

        elif data == 'nope':
            try:
                try:
                    bot.deleteMessage(buyest)
                except Exception:
                    bot.deleteMessage(sellsett)
            except Exception:
                pass
            self.sender.sendMessage('_Deal cancelled_', parse_mode='Markdown')
            try:
                bot.sendMessage(myid, '_Deal cancelled_', parse_mode='Markdown')
                self.cur.execute('UPDATE Investor SET ncommission =(?) WHERE investor=(?)', (0, myid))
                self.conn.commit()
            except Exception:
                self.cur.execute('UPDATE Investor SET ncommission =(?) WHERE investor=(?)', (0, myid))
                self.conn.commit()
                bot.sendMessage(useridentify, '_Deal cancelled_', parse_mode='Markdown')


        elif data == 'nxt':
            self._editor.editMessageReplyMarkup(reply_markup=paysell1)

        elif data == 'prv':
            self._editor.editMessageReplyMarkup(reply_markup=paysell)
        elif data == 'next':
            self.b_editor.editMessageReplyMarkup(reply_markup=payment1)

        elif data == 'prev':
            self.b_editor.editMessageReplyMarkup(reply_markup=payment)

        else:
            self.sender.sendMessage('Error wrong input.')
        self.conn.commit()
        self.cur.close()


# =====================================================================================================


TOKEN = '463856159:AAFAyFvNo7RzcHsSjnSvH2w7jbpvHLIwB1Y'  # get token from command-line

bot = telepot.DelegatorBot(TOKEN, [
    include_callback_query_chat_id(
        pave_event_space())(per_chat_id(), create_open, TradingBot, timeout=4000000),
])

MessageLoop(bot).run_as_thread()
print('Running....')

while 1:
    schedule.run_pending()
    time.sleep(10)




    # After you are done it will autosave but you have to rerun the bot by presssing here