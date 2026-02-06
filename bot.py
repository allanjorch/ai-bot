import logging
import os
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL = os.getenv('OLLAMA_MODEL', 'phi3:mini')
OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')

async def handle_message(update: Update, context):
    text = update.message.text
    logger.info(f'Message: {text}')
    
    await update.message.reply_text('🤔 Thinking...', 
        reply_to_message_id=update.message.message_id)
    
    try:
        response = requests.post(f'{OLLAMA_URL}/api/chat', json={
            'model': MODEL,
            'messages': [{'role': 'user', 'content': text}],
            'stream': False
        }, timeout=30)
        response.raise_for_status()
        result = response.json()
        await update.message.reply_text(result['message']['content'],
            reply_to_message_id=update.message.message_id)
        logger.info('✅ Replied successfully')
    except Exception as e:
        logger.error(f'❌ Error: {e}')
        await update.message.reply_text('❌ AI brain error - try again!')

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
