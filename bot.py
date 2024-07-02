import logging
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from multiprocessing import Process
import check_New_News  # Assuming these modules are implemented correctly
import update_All_News  # Assuming these modules are implemented correctly
import json
import asyncio
from telegram.error import BadRequest, Forbidden, BadRequest


from PIL import Image
import requests
from io import BytesIO

# Set up logging to provide detailed debug information
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Replace with your actual bot tokens
BOT_TOKEN_1 = "YOUR_TELEGRAM_BOT_TOKEN"


# Define the /start command handler for the first bot

# Define the /start command handler for the second bot

try:
    with open("database/telegramID.json", "r") as f:
        user_data = json.load(f)
except FileNotFoundError:
    user_data = {}


async def start_bot1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    user_username = update.effective_user.username

    # Check if the user already exists in our data
    existing_user = next(
        (user for user in user_data if user.get("id") == user_id), None
    )

    if existing_user is None:
        # If not, add the new user as an object to the list
        new_user = {"id": user_id, "name": user_name, "username": user_username}
        user_data.append(new_user)

        # Update the JSON file
        with open("database/telegramID.json", "w") as f:
            json.dump(user_data, f, indent=4)

    image_path = "src/Clogo.jpg"

    # Sending the photo with a caption

    button = InlineKeyboardButton(text="Main Chanel ", url="https://t.me/nsdevspace")
    reply_markup = InlineKeyboardMarkup([[button]])

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open(image_path, "rb"),
        caption=(
            f"Hi {update.effective_user.mention_html()},  Welcome ! 😊 \nLive Hiru News Update Bot Yenuli  ✅ \n\nActivated Successfully 📡 \nNews Updates Will Send You Automatically\n\n 🇱🇰 "
        ),
        reply_markup=reply_markup,
        parse_mode="HTML",  # Ensure HTML parsing mode is set for the mention_html method
    )


async def send_news_updates(application, news):
    for news_item in news:
        message = news_item["Title"]
        IMAGE_URL = news_item["Image"]
        Link = news_item["Link"]
        news_content = news_item["Paragraph"]

        button = InlineKeyboardButton(text="See more", url=Link)
        reply_markup = InlineKeyboardMarkup([[button]])

        try:
            # Load the main image from the URL
            image_url = IMAGE_URL
            response = requests.get(image_url)
            response.raise_for_status()
            main_image = Image.open(BytesIO(response.content))

            # Load the logo
            logo = Image.open("src/logo.png")

            # Calculate the desired width of the logo (30% of the main image width)
            logo_width = int(main_image.width * 0.15)

            # Resize the logo proportionally based on the calculated width
            logo_height = int(logo.height * (logo_width / logo.width))
            logo = logo.resize((logo_width, logo_height))

            # Calculate the position to place the logo (bottom-left corner)
            main_width, main_height = main_image.size
            position = (0, main_height - logo_height)

            # Paste the logo onto the main image
            main_image.paste(logo, position, logo)

            # Save the resulting image
            main_image.save("src/a_with_logo.jpg")

            print("Image saved as a_with_logo.jpg")

        except Exception as e:
            print(f"An error occurred: {e}")
            continue

        with open("database/telegramID.json", "r") as f:
            user_data = json.load(f)

        for user in user_data:
            user_id = user["id"]
            try:
                await application.bot.send_photo(
                    chat_id=user_id,
                    photo="src/a_with_logo.jpg",
                    parse_mode="Markdown",
                    caption=" 🟢 "
                    + "*"
                    + message
                    + "*"
                    + " 🟢 "
                    + "\n\n"
                    + news_content
                    + "\n\n"
                    + "@NsDevSpace",
                    reply_markup=reply_markup,
                )

            except Forbidden:
                print(f"Bot was blocked by user ID {user_id}. Skipping.")
                # Optionally, log this information or take other actions
            except BadRequest as e:
                if str(e) == "Chat not found":
                    print(f"Chat not found for user ID {user_id}. Skipping.")
                    # Optionally, log this information or take other actions
                else:
                    raise


# Main function to handle the updating and sending of news
async def main():
    application = ApplicationBuilder().token(BOT_TOKEN_1).build()

    while True:
        update_All_News.run_scraper()
        check_New_News.get_and_save_latest_news()
        with open("database/Latest_News.json", "r", encoding="utf-8") as file:
            latest_news = json.load(file)

        await send_news_updates(application, latest_news)

        await asyncio.sleep(320)


# Function to start the first bot
def run_bot1():
    application1 = ApplicationBuilder().token(BOT_TOKEN_1).build()
    application1.add_handler(CommandHandler("start", start_bot1))
    application1.run_polling()


# Function to start the second bot
def run_bot2():
    asyncio.run(main())


if __name__ == "__main__":
    # Create separate processes for each bot
    process1 = Process(target=run_bot1)
    process2 = Process(target=run_bot2)

    # Start both processes
    process1.start()
    process2.start()

    # Join both processes to the main process
