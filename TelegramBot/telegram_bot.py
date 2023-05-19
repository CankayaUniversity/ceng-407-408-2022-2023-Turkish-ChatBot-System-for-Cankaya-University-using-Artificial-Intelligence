#pip install requests python-telegram-bot==12.8 google-cloud-speech pydub

import requests
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

# Set your bot token here
BOT_TOKEN = "Set your bot token here"
BACKEND_URL = "http://localhost:5000"  # Replace with your backend URL if needed

LOGIN_FEATURE = 0 # Set to 1 to enable login, set to 0 to disable login

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

from google.cloud import speech_v1p1beta1 as speech
import io
from google.oauth2 import service_account

# Set the path to your Google Cloud key file
GOOGLE_APPLICATION_CREDENTIALS = "google_cloud_api.json"

def transcribe_audio_file(file_path):
    # Convert audio file to 16-bit samples
    audio = AudioSegment.from_file(file_path)
    audio = audio.set_sample_width(2)
    audio.export("converted_audio.wav", format="wav")
    file_path = "converted_audio.wav"

    # Set up Google Cloud Speech-to-Text API client
    credentials = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)
    client = speech.SpeechClient(credentials=credentials)

    # Configure API request
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="tr-TR",
    )

    with open(file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    response = client.recognize(config=config, audio=audio)

    # Clean up the temporary file
    os.remove("converted_audio.wav")

    # Process the API response
    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript

    return transcript

import os
import tempfile
from pydub import AudioSegment

def process_audio(update: Update, context: CallbackContext):
    if LOGIN_FEATURE and ("authenticated" not in context.user_data or not context.user_data["authenticated"]):
        update.effective_message.reply_text("You must log in first using /login <username> <password>")
        return

    audio = update.effective_message.voice or update.effective_message.audio

    if audio is None:
        update.effective_message.reply_text("Please send a voice message or an audio file.")
        return

    with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as temp_file:
        temp_file_path = temp_file.name
    audio_file = audio.get_file()
    audio_file.download(temp_file_path)

    try:
        # Convert the audio file to WAV format
        audio_segment = AudioSegment.from_file(temp_file_path)
        audio_segment = audio_segment.set_frame_rate(16000).set_channels(1)
        wav_file_path = os.path.splitext(temp_file_path)[0] + ".wav"
        audio_segment.export(wav_file_path, format="wav")

        # Transcribe the audio file
        text = transcribe_audio_file(wav_file_path)
        print(f"Transcribed text: {text}")  # Debugging print statement
        if text:
            update.effective_message.reply_text(f"Transcribed text: {text}")
            # Call the process_message function with the transcribed text
            process_message(update, context, str(text))
        else:
            update.effective_message.reply_text("Sorry, I couldn't understand the audio.")
    finally:
        os.remove(temp_file_path)
        os.remove(wav_file_path)


def start(update: Update, context: CallbackContext):
    if LOGIN_FEATURE and ("authenticated" not in context.user_data or not context.user_data["authenticated"]):
        update.effective_message.reply_text("You must log in first using /login <username> <password>")
        return
    context.user_data["welcome_sent"] = True
    keyboard = [
        [
            InlineKeyboardButton("GPT-3", callback_data="gpt3"),
            InlineKeyboardButton("BERT", callback_data="bert"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.effective_message.reply_text("Please choose a model:", reply_markup=reply_markup)

def login(update: Update, context: CallbackContext):
    if len(context.args) != 2:
        update.effective_message.reply_text("Please provide a username and password. Usage: /login <username> <password>")
        return

    username, password = context.args
    correct_username = "ceng408_2"
    correct_password = "ceng408_2"

    if username == correct_username and password == correct_password:
        context.user_data["authenticated"] = True
        update.effective_message.reply_text("Login successful. You can now use the bot with \"/start\".")
    else:
        update.effective_message.reply_text("Invalid credentials. Please try again.")

def button(update: Update, context: CallbackContext):
    if LOGIN_FEATURE and ("authenticated" not in context.user_data or not context.user_data["authenticated"]):
        update.effective_message.reply_text("You must log in first using /login <username> <password>")
        return

    query = update.callback_query
    model = query.data
    query.answer()

    context.user_data["model"] = model
    query.edit_message_text(text=f"Selected model: {model}\nSend your question to get a response.")

def process_message(update: Update, context: CallbackContext, message_text=None):
    if "welcome_sent" not in context.user_data:
        if LOGIN_FEATURE:
            update.effective_message.reply_text("You must log in first using /login <username> <password>")
        else:
            update.effective_message.reply_text("Welcome to the bot! Please type /start to begin.")
        context.user_data["welcome_sent"] = True
        return

    if "model" not in context.user_data:
        update.effective_message.reply_text("Please choose a model using /start")
        return

    model = context.user_data["model"]
    message = message_text if message_text is not None else update.effective_message.text

    try:
        if model == "gpt3":
            response = requests.post(f"{BACKEND_URL}/generate-response-gpt3", json={"message": message})
        elif model == "bert":
            response = requests.post(f"{BACKEND_URL}/generate-response-bert", json={"message": message})
        else:
            raise ValueError("Invalid model")

        response.raise_for_status()
        result = response.json()["text"]
        update.effective_message.reply_text(result)
    except Exception as e:
        logger.exception(e)
        update.effective_message.reply_text("Error generating response")

def help_command(update: Update, context: CallbackContext):
    help_text = "List of available commands:\n\n"
    help_text += "/start - Choose a model (GPT-3 or BERT)\n"

    if LOGIN_FEATURE:
        help_text += "/login <username> <password> - Log in to the bot\n"

    help_text += "/help - Show this list of commands"

    update.effective_message.reply_text(help_text)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, process_message))
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("login", login, pass_args=True))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.voice | Filters.audio, process_audio))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
