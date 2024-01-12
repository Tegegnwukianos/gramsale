import telebot
from telebot import types
from config import TOKEN
import sqlite3
# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = telebot.TeleBot(TOKEN)

class BalanceManager:
    def __init__(self, db_filename='user_balances.db'):
        self.db_filename = db_filename

    def init_database(self):
        conn = sqlite3.connect(self.db_filename)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS balances (
                user_id INTEGER PRIMARY KEY,
                balance REAL DEFAULT 0.0
            )
        ''')
        conn.commit()
        conn.close()

    def get_balance(self, user_id):
        conn = sqlite3.connect(self.db_filename)
        cursor = conn.cursor()
        cursor.execute('SELECT balance FROM balances WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0.0

    def update_balance(self, user_id, amount):
        conn = sqlite3.connect(self.db_filename)
        cursor = conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO balances (user_id) VALUES (?)', (user_id,))
        cursor.execute('UPDATE balances SET balance = balance + ? WHERE user_id = ?', (amount, user_id))
        conn.commit()
        conn.close()

    def decrease_balance(self, user_id, amount):
        conn = sqlite3.connect(self.db_filename)
        cursor = conn.cursor()
        cursor.execute('UPDATE balances SET balance = balance - ? WHERE user_id = ?', (amount, user_id))
        conn.commit()
        conn.close()

# Initialize the BalanceManager
balance_manager = BalanceManager()
balance_manager.init_database()


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    # Check if the user is already in the database
    if balance_manager.get_balance(user_id) == 0.0:
        # If not, add the user with an initial balance of 0.00
        balance_manager.update_balance(user_id, 0.0)


    # Create inline keyboard
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    my_account_button = types.InlineKeyboardButton("My Account", callback_data='my_account')
    new_order_button = types.InlineKeyboardButton("New Order", callback_data='new_order')
    services_button = types.InlineKeyboardButton("Services", callback_data='services')
    contact_us_button = types.InlineKeyboardButton("Contact Us", callback_data='contact_us')

    keyboard.add(my_account_button, new_order_button, services_button, contact_us_button)

    # Send the start message with inline keyboard
    bot.send_message(848696652, f"user started {message.from_user.username}")
    #bot.send_sticker(user_id, "CAACAgUAAxkBAAJYMGWhelXozxMMGM289NEVkvAOyfALAAJlBAACmuxYVLwYAAGolBvU_jQE")
    bot.send_message(user_id, f"""Hi, {message.from_user.first_name}
        
Welcome to Gramsale.
Gramsale is the Most Reliable growth Panel on the market with 90 million orders processed successfully! Promote your social profiles right now!""", reply_markup=keyboard)

# Handler for inline keyboard button clicks
@bot.callback_query_handler(func=lambda call: True)
def handle_inline_query(call):
    user_id = call.from_user.id

    if call.data == 'my_account':
        # Get user balance (replace with your database logic)
        balance = balance_manager.get_balance(user_id)

        # Create an inline keyboard for account information
        account_keyboard = types.InlineKeyboardMarkup(row_width=1)
        deposit_button = types.InlineKeyboardButton("Deposit", callback_data='deposit')

        # Display user account information along with the balance and a "Deposit" button
        account_keyboard.add(types.InlineKeyboardButton(f"Balance: {balance}$", callback_data='dummy'), deposit_button)

        # Send the account information message
        bot.send_message(
            user_id,
            f"Your Account Information:\nName: {call.from_user.first_name}\nUsername: @{call.from_user.username}\nUser ID: {user_id}\n",
            reply_markup=account_keyboard
        )

    elif call.data == 'new_order':
        # Create an inline keyboard for choosing services
        services_keyboard = types.InlineKeyboardMarkup(row_width=2)
        telegram_button = types.InlineKeyboardButton("Telegram", callback_data='service_telegram')
        facebook_button = types.InlineKeyboardButton("Facebook", callback_data='service_facebook')
        instagram_button = types.InlineKeyboardButton("Instagram", callback_data='service_instagram')
        youtube_button = types.InlineKeyboardButton("YouTube", callback_data='service_youtube')
        tiktok_button = types.InlineKeyboardButton("TikTok", callback_data='service_tiktok')

        services_keyboard.add(telegram_button, facebook_button, instagram_button, youtube_button, tiktok_button)
        bot.send_message(user_id, "Choose a service:", reply_markup=services_keyboard)


    elif call.data == 'services':
        # Logic for 'Services'
        bot.send_message(user_id, "View available services.")

    elif call.data == 'contact_us':
        # Logic for 'Contact Us'
        bot.send_message(user_id, "Contact us for support or inquiries.")

    elif call.data == 'deposit':
        # Inline keyboard for choosing payment provider
        payment_provider_keyboard = types.InlineKeyboardMarkup(row_width=1)
        mpesa_button = types.InlineKeyboardButton("MPESA", callback_data='mpesa')
        pesapal_button = types.InlineKeyboardButton("Pesapal", callback_data='pesapal')
        flutterwave_button = types.InlineKeyboardButton("Flutterwave", callback_data='flutterwave')
        coinbase_button = types.InlineKeyboardButton("Coinbase", callback_data='coinbase')
        binance_pay_button = types.InlineKeyboardButton("Binance Pay", callback_data='binance_pay')

        payment_provider_keyboard.add(mpesa_button, pesapal_button, flutterwave_button, coinbase_button, binance_pay_button)

        # Send the payment provider options
        #balance = balance_manager.update_balance(user_id, 50)
        bot.send_message(user_id, "Choose a payment provider:", reply_markup=payment_provider_keyboard)

    # Handle the chosen payment provider
    elif call.data in ['mpesa', 'pesapal', 'flutterwave', 'coinbase', 'binance_pay']:
        # Logic for handling the chosen payment provider
        bot.send_message(user_id, f"You chose {call.data}. Follow the instructions provided for {call.data} payment.")


     # Handle the chosen service
    elif call.data == 'service_telegram':
        # Create an inline keyboard for Telegram sub-services
        telegram_sub_services_keyboard = types.InlineKeyboardMarkup(row_width=2)

        telegram_sub_services_keyboard.add(types.InlineKeyboardButton("Telegram Subscribers (0.4$ per 1k)", callback_data='telegram_subscribers'))
        telegram_sub_services_keyboard.add(types.InlineKeyboardButton("Telegram Negative Reactions (0.3$ per 1k)", callback_data='telegram_negative_reactions')) 
        telegram_sub_services_keyboard.add(types.InlineKeyboardButton("Telegram Positive Reactions (0.3$ per 1k)", callback_data='telegram_positive_reactions'))

        # Send the Telegram sub-services options
        bot.send_message(user_id, "Choose a sub-service for Telegram:", reply_markup=telegram_sub_services_keyboard)

    elif call.data == 'service_facebook':
        # Logic for 'Facebook' service
        bot.send_message(user_id, "You chose Facebook. Implement logic for processing Facebook services.")

    elif call.data == 'service_instagram':
    # Creating InlineKeyboardMarkup
        instagram_services_keyboard = types.InlineKeyboardMarkup(row_width=2)

        # Adding InlineKeyboardButton with 'text' argument
        followers_button = types.InlineKeyboardButton(text="Instagram Followers (0.6$ per 1k)", callback_data='instagram_followers')
        
        # Adding the button to the keyboard
        instagram_services_keyboard.add(followers_button)

        # Logic for 'Instagram' service
        bot.send_message(user_id, "Choose a service for Instagram:", reply_markup=instagram_services_keyboard)


    elif call.data == 'service_youtube':
        # Logic for 'YouTube' service
        bot.send_message(user_id, "You chose YouTube. Implement logic for processing YouTube services.")

    elif call.data == 'service_tiktok':
        # Logic for 'TikTok' service
        bot.send_message(user_id, "You chose TikTok. Implement logic for processing TikTok services.")

    # Handle the chosen sub-service
    elif call.data == 'sub_service_telegram_views':
        # Logic for handling Telegram Views sub-service
        bot.send_message(user_id, "You chose Telegram Views. Implement logic for processing this sub-service.")

    elif call.data == 'sub_service_telegram_other':
        # Logic for handling Other Telegram Sub-Service
        bot.send_message(user_id, "You chose Other Telegram Sub-Service. Implement logic for processing this sub-service.")
    elif call.data == 'telegram_subscribers':
        bot.send_message(user_id, "enter ammount you want to order it costs 0.5 per 1k")
         # Register a handler for the next step
        bot.register_next_step_handler(call.message, process_telegram_subscribers_amount)

    # Answer the callback query to remove the "loading" status
    bot.answer_callback_query(callback_query_id=call.id)


def process_telegram_subscribers_amount(message):
    user_id = message.from_user.id

    try:
        # Convert the entered amount to a float
        amount = float(message.text)

        # Validate the amount (you can customize the min and max values)
        if 1 <= amount <= 1000:  # Example: min 1, max 1000
            # Calculate the cost per subscriber
            cost_per_subscriber = 0.0005
            total_cost = amount * cost_per_subscriber

            # Ask for confirmation
            confirmation_text = f"Confirm your order:\n\nAmount: {amount} subscribers\nTotal Cost: {total_cost}$"
            confirmation_keyboard = types.InlineKeyboardMarkup(row_width=2)
            confirm_button = types.InlineKeyboardButton("Confirm", callback_data='confirm_order')
            cancel_button = types.InlineKeyboardButton("Cancel", callback_data='cancel_order')
            confirmation_keyboard.add(confirm_button, cancel_button)

            # Send confirmation message with buttons
            bot.send_message(user_id, confirmation_text, reply_markup=confirmation_keyboard)

        else:
            # Invalid amount
            bot.send_message(user_id, "Invalid amount. Please enter a value between 1 and 1000.")

    except ValueError:
        # Handle invalid input
        bot.send_message(user_id, "Invalid input. Please enter a valid numeric value.")










    

# Start the bot
bot.polling()
