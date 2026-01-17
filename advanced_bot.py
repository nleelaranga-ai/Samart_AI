import json
import logging
import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from deep_translator import GoogleTranslator

# --- 1. CONFIGURATION ---
# ⚠️ REPLACE THIS WITH YOUR REAL TOKEN
TOKEN = "8529547844:AAGcE-LTQIS5pVsQlUa-hxgBM1WeGus-_9M" 

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- 2. LOAD DATABASE ---
# Loads the 15 Verified Schemes you built earlier
try:
    with open('scholarships.json', 'r', encoding='utf-8') as f:
        SCHOLARSHIPS = json.load(f)
    print(f"✅ Database Loaded: {len(SCHOLARSHIPS)} Schemes Ready.")
except Exception as e:
    print(f"❌ Error loading database: {e}")
    SCHOLARSHIPS = []

# --- 3. MULTILINGUAL SETUP ---
TRANSLATION_CACHE = {} 
USER_LANG = {}
USER_STATE = {}

BASE_TEXTS = {
    'welcome': "🙏 **Namaste! Welcome to SamartAI.**\n\nI can guide you in your own language. Please select one:",
    'menu': "🏠 **Main Menu**\nHow can I help you today?",
    'btn_search': "🔍 Find Scholarships",
    'btn_check': "✅ Check Eligibility",
    'btn_help': "📞 Help / Support",
    'ask_caste': "👤 **Select Your Category:**",
    'ask_income': "💰 **Please type your Annual Income:**\n(Example: 50000)",
    'eligible': "✅ **You are Eligible!**\nBased on income ₹{}, you can apply for:",
    'not_eligible': "❌ **Not Eligible.**\nYour income ₹{} is above the limit (₹{}).",
    'no_results': "⚠️ No schemes found for this category.",
    'found_header': "🎉 **Found Schemes for {}:**",
    'more_langs': "🌐 More Languages..."
}

# --- 4. TRANSLATION ENGINE ---
async def get_text(key, lang_code, format_args=None):
    """Smart translation with caching"""
    text = BASE_TEXTS.get(key, "")
    
    if lang_code == 'en':
        return text.format(*format_args) if format_args else text

    cache_key = f"{lang_code}_{key}"
    if cache_key in TRANSLATION_CACHE:
        translated_text = TRANSLATION_CACHE[cache_key]
    else:
        loop = asyncio.get_running_loop()
        translated_text = await loop.run_in_executor(
            None, 
            lambda: GoogleTranslator(source='auto', target=lang_code).translate(text)
        )
        TRANSLATION_CACHE[cache_key] = translated_text

    return translated_text.format(*format_args) if format_args else translated_text

async def translate_dynamic(text, lang_code):
    """Translates database content on the fly"""
    if lang_code == 'en': return text
    loop = asyncio.get_running_loop()
    try:
        return await loop.run_in_executor(
            None, 
            lambda: GoogleTranslator(source='auto', target=lang_code).translate(text)
        )
    except:
        return text

# --- 5. HANDLERS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles /start, 'Hi', and Restart Button"""
    
    # 1. The Language Menu
    keyboard = [
        [InlineKeyboardButton("🇬🇧 English", callback_data='lang_en')],
        [InlineKeyboardButton("🇮🇳 తెలుగు (Telugu)", callback_data='lang_te')],
        [InlineKeyboardButton("🌐 More / ఇతర భాషలు...", callback_data='lang_menu_more')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # 2. Logic: Button vs Text
    if update.callback_query:
        # If clicked "Restart", edit the existing message (Fixes the crash)
        await update.callback_query.edit_message_text(
            text=BASE_TEXTS['welcome'], 
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    else:
        # If typed "Hi" or "/start", send a NEW message
        await update.message.reply_text(
            text=BASE_TEXTS['welcome'], 
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id
    
    # --- A. LANGUAGE SELECTION ---
    if data == 'lang_menu_more':
        keyboard = [
            [InlineKeyboardButton("🇮🇳 Hindi", callback_data='lang_hi'), InlineKeyboardButton("🇮🇳 Tamil", callback_data='lang_ta')],
            [InlineKeyboardButton("🇮🇳 Kannada", callback_data='lang_kn'), InlineKeyboardButton("🇮🇳 Malayalam", callback_data='lang_ml')],
            [InlineKeyboardButton("🔙 Back", callback_data='restart')]
        ]
        await query.edit_message_text("🌎 **Select your local language:**", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
        return

    if data.startswith('lang_') and 'menu' not in data:
        lang = data.split('_')[1]
        USER_LANG[user_id] = lang
        await show_main_menu(query, lang)
        return

    if data == 'restart':
        await start(update, context) # Calls the robust start function
        return

    # --- B. MENU NAVIGATION ---
    lang = USER_LANG.get(user_id, 'en') # Default English

    if data == 'main_menu':
        await show_main_menu(query, lang)

    elif data == 'menu_search':
        btn_text = await get_text('ask_caste', lang)
        # Expanded Categories based on your new data
        keyboard = [
            [InlineKeyboardButton("SC", callback_data='caste_SC'), InlineKeyboardButton("ST", callback_data='caste_ST')],
            [InlineKeyboardButton("BC", callback_data='caste_BC'), InlineKeyboardButton("Brahmin", callback_data='caste_Brahmin')],
            [InlineKeyboardButton("Kapu / EBC", callback_data='caste_Kapu'), InlineKeyboardButton("Minority", callback_data='caste_Minority')],
            [InlineKeyboardButton("Disabled / Workers", callback_data='caste_Special')],
            [InlineKeyboardButton("🔙 Back", callback_data='main_menu')]
        ]
        await query.edit_message_text(btn_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif data == 'menu_check':
        USER_STATE[user_id] = 'WAITING_INCOME'
        msg = await get_text('ask_income', lang)
        await query.edit_message_text(msg, parse_mode='Markdown')

    elif data.startswith('caste_'):
        caste = data.split('_')[1]
        
        # SMART FILTERING: Matches Caste OR Keywords in your new DB
        results = []
        for s in SCHOLARSHIPS:
            # Check if category matches or if "All" is present
            cat_match = caste.lower() in s['category'].lower() or "all" in s['category'].lower()
            
            # Special handling for "Special" button (Disabled/Workers)
            if caste == "Special" and ("differently" in s['category'].lower() or "worker" in s['category'].lower()):
                cat_match = True
                
            if cat_match:
                results.append(s)
        
        if results:
            header = await get_text('found_header', lang, [caste])
            response = f"{header}\n\n"
            
            for s in results:
                name_tr = await translate_dynamic(s['name'], lang)
                desc_tr = await translate_dynamic(s['description'], lang)
                response += f"🏛 **{name_tr}**\n💰 ₹{s['income_limit']}\n📝 {desc_tr}\n🔗 [Link]({s['link']})\n\n"
        else:
            response = await get_text('no_results', lang)

        keyboard = [[InlineKeyboardButton("🔙 Menu", callback_data='main_menu')]]
        await query.edit_message_text(response, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def show_main_menu(query, lang):
    t_menu = await get_text('menu', lang)
    t_search = await get_text('btn_search', lang)
    t_check = await get_text('btn_check', lang)
    t_help = await get_text('btn_help', lang)
    
    keyboard = [
        [InlineKeyboardButton(t_search, callback_data='menu_search')],
        [InlineKeyboardButton(t_check, callback_data='menu_check')],
        [InlineKeyboardButton(t_help, callback_data='menu_help')],
        [InlineKeyboardButton("⚙️ Language / భాష", callback_data='restart')]
    ]
    await query.edit_message_text(t_menu, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles Income Input AND Greetings (Hi/Hello)"""
    user_text = update.message.text.lower()
    
    # 1. Check for Greetings
    greetings = ["hi", "hello", "hey", "namaste", "hola", "start"]
    if any(greet in user_text for greet in greetings):
        await start(update, context) # Trigger the Start Menu
        return

    # 2. Check for Income Input (if waiting)
    user_id = update.effective_user.id
    state = USER_STATE.get(user_id)
    lang = USER_LANG.get(user_id, 'en')

    if state == 'WAITING_INCOME':
        try:
            # Extract number from text (e.g. "my income is 50000")
            import re
            numbers = re.findall(r'\d+', user_text)
            if not numbers:
                raise ValueError
            
            income = int(numbers[0])
            limit = 300000 # Using 3L as standard for new DB
            
            if income <= limit:
                msg = await get_text('eligible', lang, [income])
            else:
                msg = await get_text('not_eligible', lang, [income, limit])
            
            await update.message.reply_text(msg, parse_mode='Markdown')
            USER_STATE[user_id] = None # Reset
        except:
            await update.message.reply_text("⚠️ Please type just the number (e.g., 60000)")

# --- 6. MAIN EXECUTION ---
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler("start", start))
    
    # Button Clicks
    app.add_handler(CallbackQueryHandler(button_handler))
    
    # Text Messages (Handles "Hi" and "Income")
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
    
    print("🚀 SamartAI Final Bot is Running...")
    app.run_polling()