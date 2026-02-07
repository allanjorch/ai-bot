import logging
import os
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL = os.getenv('OLLAMA_MODEL', 'phi3:mini')
OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')
# SYSTEM_PROMPT = "You are a warm, thoughtful friend who's occasionally witty. You're intelligent but not arrogant, funny without trying too hard, and comfortable acknowledging when you don't know something. You bring positive energy while staying genuine, grounded, and self-aware."
SYSTEM_PROMPT = ""

async def handle_message(update: Update, context):
    text = update.message.text
    logger.info(f'Message: {text}')
    
    # await update.message.reply_text('🤔 Thinking...', 
    #     reply_to_message_id=update.message.message_id)
    
    try:
        response = requests.post(f'{OLLAMA_URL}/api/generate', json={
            'model': MODEL,
            'prompt': text,
            'system': SYSTEM_PROMPT,
            'options': {
                'temperature': 0.8,
                'num_ctx': 8192
            },
            'stream': False
        }, timeout=600)
        response.raise_for_status()
        result = response.json()
        formatted_response = f"""{result['response']}

_({MODEL})_"""

        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text=formatted_response,
            parse_mode='Markdown'
        )
        logger.info('✅ Replied successfully')
    except Exception as e:
        logger.error(f'❌ Error: {e}')
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text='❌ AI brain error - try again!'
        )

def main():
    token = os.getenv('TELEGRAM_TOKEN')
    if not token:
        logger.error('TELEGRAM_TOKEN not set')
        return
    
    app = Application.builder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info(f'🤖 Starting with model {MODEL}')
    
    # FIXED: Synchronous run_polling() - no asyncio.run() needed
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
