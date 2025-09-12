import os
import logging
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update
from dotenv import load_dotenv
from otp_scraper import get_new_otp
from utils.otp_filter import OTPFilter

# Load .env
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROUP_ID = os.getenv("TELEGRAM_GROUP_ID")

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

otp_filter = OTPFilter()

# ================= Commands =================
def start(update: Update, context: CallbackContext):
    update.message.reply_text("🚀 Bot aktif!\nGunakan /status, /test, /check")

def status(update: Update, context: CallbackContext):
    update.message.reply_text("✅ Bot sedang online dan siap jalan.")

def test(update: Update, context: CallbackContext):
    update.message.reply_text("🧪 Test command berhasil!")

def check(update: Update, context: CallbackContext):
    otp_data = get_new_otp()
    if otp_data:
        if otp_filter.is_duplicate(otp_data):
            update.message.reply_text("⚠️ OTP duplikat.")
        else:
            otp_filter.add_otp(otp_data)
            context.bot.send_message(chat_id=GROUP_ID, text=f"🔑 OTP baru: {otp_data}")
    else:
        update.message.reply_text("🕒 Belum ada OTP baru.")

# ================= Main =================
def main():
    if not TOKEN or not GROUP_ID:
        logger.error("❌ TELEGRAM_BOT_TOKEN atau TELEGRAM_GROUP_ID belum di-set di .env")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("test", test))
    dp.add_handler(CommandHandler("check", check))

    updater.start_polling()
    logger.info("🚀 Bot started polling...")
    updater.idle()

if __name__ == "__main__":
    main()
