import telebot
from pymongo import MongoClient
from flask import Flask

def send_long_message(chat_id, message_text):
    max_message_length = 4096  # Telegram's maximum message length
    if len(message_text) <= max_message_length:
        bot.send_message(chat_id, message_text,  parse_mode="HTML",
                     disable_web_page_preview=True)
    else:
        # Splitting message into chunks
        chunks = [message_text[i:i + max_message_length] for i in range(0, len(message_text), max_message_length)]
        for chunk in chunks:
            bot.send_message(chat_id, chunk, parse_mode="HTML")
# Initialize the Telegram bot
bot = telebot.TeleBot('7061989308:AAEyIE9Sp6HgzyDf5VGldgP0WGXtaqOJFkQ')

# Connect to MongoDB
client = MongoClient(
    'mongodb+srv://tiwelap676:46hgscqQiHJ9HlNT@cluster0.fs4iwrf.mongodb.net/?retryWrites=true&w=majority')
db = client['test']
collection_users = db['users']
collection_call = db['calls']
collection_recentsearches = db['recentsearches']
# bot.send_message('995944815', "Successfully Deploy in PythonAnyWhere")
# bot.send_message('1098317745', "Successfully Deploy in PythonAnyWhere")


# Handle the '/start' command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_name = message.chat.first_name if message.chat.first_name else "Admin"
    message = f"Welcome, {user_name}.\nServer is running"
    bot.send_message(chat_id, message, parse_mode="HTML")


@bot.message_handler(commands=['call'])
def handle_call_command(message):
    chat_id = message.chat.id
    if str(chat_id) not in ["995944815", "1098317745"]:
        bot.send_message(chat_id, "Forbidden, Only Admins...")
        return
    try:
        isAdmin = collection_users.find_one({}, {"id": chat_id})
        if not isAdmin:
            bot.send_message(chat_id, "User not found")
            return
        bot.send_message(
            chat_id, "Send the Code The User For Adding More Call Points.")
        bot.register_next_step_handler(message, call_handle_user_code)
    except Exception as e:
        print("Error adding points:", e)
        bot.send_message(
            chat_id, "Sorry, an error occurred while adding points!")


# Function to handle user code
def call_handle_user_code(message):
    chat_id = message.chat.id
    code = message.text
    user = collection_call.find_one({"code": code})
    if not user:
        bot.send_message(chat_id, "User not found!")
        return
    bot.send_message(chat_id, "Enter the number of points for the user.")
    # Register a message handler for handling the points
    bot.register_next_step_handler(message, call_handle_points, user, code)

# Function to handle points


def call_handle_points(message, user, code):
    chat_id = message.chat.id
    points = message.text
    try:
        collection_call.update_one(
            {"code": code}, {"$set": {"points": int(points)}})
        bot.send_message(chat_id, f"Done, {user['code']} has {points} points now")
    except Exception as e:
        print("Error handling points:", e)
        bot.send_message(
            chat_id, "Sorry, an error occurred while updating points.")

# Command handler for /addpoints command


@bot.message_handler(commands=['addpoints'])
def handle_addpoints_command(message):
    chat_id = message.chat.id
    if str(chat_id) not in ["995944815", "1098317745"]:
        bot.send_message(chat_id, "Forbidden, Only Admins...")
        return
    try:
        isAdmin = collection_users.find_one({}, {"id": chat_id})
        if not isAdmin:
            bot.send_message(chat_id, "User not found")
            return
        bot.send_message(
            chat_id, "Send Id For Adding Points.")
        # Register a message handler for handling the code
        bot.register_next_step_handler(message, addpoints_handle_user_code)

    except Exception as e:
        print("Error adding points:", e)
        bot.send_message(
            chat_id, "Sorry, an error occurred while adding points!")

# Function to handle user code


def addpoints_handle_user_code(message):
    chat_id = message.chat.id
    idd = message.text
    user = collection_users.find_one({"id": idd})

    if not user:
        bot.send_message(chat_id, "User not found!")
        return
    bot.send_message(chat_id, "Enter Number Of Points!")

    # Register a message handler for handling the points
    bot.register_next_step_handler(
        message, addpoints_handle_points, user, idd)

# Function to handle points


def addpoints_handle_points(message, user, idd):
    chat_id = message.chat.id
    points = message.text

    try:
        collection_users.update_one(
            {"id": idd}, {"$set": {"points": int(points)}})
        bot.send_message(chat_id, f"Done, {user['id']} has { user['points']} now :)")
    except Exception as e:
        print("Error handling points:", e)
        bot.send_message(
            chat_id, "Sorry, an error occurred while updating points.")


@bot.message_handler(commands=['user'])
def handle_addpoints_command(message):
    chat_id = message.chat.id
    if str(chat_id) not in ["995944815", "1098317745"]:
        bot.send_message(chat_id, "Forbidden, Only Admins...")
        return
    try:
        isAdmin = collection_users.find_one({}, {"id": chat_id})
        if not isAdmin:
            bot.send_message(chat_id, "User not found")
            return
        bot.send_message(
            chat_id, "Send User Id")
        # Register a message handler for handling the code
        bot.register_next_step_handler(message, handle_user_details)

    except Exception as e:
        print("Error adding points:", e)
        bot.send_message(
            chat_id, "Sorry, an error occurred while adding points!")


def handle_user_details(message):
    chat_id = message.chat.id
    idd = message.text
    user = collection_users.find_one({"id": idd})
    recentsearches = collection_recentsearches.find_one({"id": idd})
    if not user:
        bot.send_message(chat_id, "User not found!")
        return
    urls = "\n".join(
        recentsearches["key"]) if recentsearches and "key" in recentsearches else "No Recent Searches"
    message = f"""
Id: {user['id']}
Code: {user['code']}
Points: {user['points']}\n
Recent Search:
{urls}
"""
    send_long_message(chat_id, message)


@bot.message_handler(commands=['delete'])
def handle_addpoints_command(message):
    chat_id = message.chat.id
    if str(chat_id) not in ["995944815", "1098317745"]:
        bot.send_message(chat_id, "Forbidden, Only Admins...")
        return
    try:
        isAdmin = collection_users.find_one({}, {"id": chat_id})
        if not isAdmin:
            bot.send_message(chat_id, "User not found")
            return
        bot.send_message(
            chat_id, "Send User Id whom you Want to Delete.")
        # Register a message handler for handling the code
        bot.register_next_step_handler(message, handle_user_delete)
    except Exception as e:
        print("Error adding points:", e)
        bot.send_message(
            chat_id, "Sorry, an error occurred while adding points!")


def handle_user_delete(message):
    chat_id = message.chat.id
    idd = message.text
    user = collection_users.find_one_and_delete({"id": idd})
    collection_recentsearches.find_one_and_delete({"id": idd})
    collection_call.find_one_and_delete({"id": idd})
    if not user:
        bot.send_message(chat_id, "User not found!")
        return

    message = f"User Deleted From Our App..."
    bot.send_message(chat_id, message,  parse_mode="HTML")


# Start the bot polling
bot.polling()

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello from Flask!'
