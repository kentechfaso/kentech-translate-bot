from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from googletrans import Translator
import os

TOKEN = os.getenv("BOT_TOKEN")

translator = Translator()
user_languages = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌍 Bienvenue sur Kentech Translate Bot\n\n"
        "Commandes disponibles :\n"
        "/langues\n"
        "/traduire fr\n"
        "/traduire en\n"
        "/aide"
    )

async def langues(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌍 Langues disponibles\n\n"
        "fr = Français\n"
        "en = Anglais\n"
        "es = Espagnol\n"
        "de = Allemand\n"
        "ar = Arabe\n"
        "it = Italien\n"
        "pt = Portugais"
    )

async def traduire(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Exemple : /traduire en"
        )
        return

    langue = context.args[0]
    user_languages[update.effective_user.id] = langue

    await update.message.reply_text(
        f"✅ Traduction activée vers {langue}"
    )

async def aide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Utilisez /langues pour voir les langues disponibles.\n"
        "Puis utilisez /traduire <code>."
    )

async def translate_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texte = update.message.text
    langue = user_languages.get(update.effective_user.id, "fr")

    try:
        resultat = translator.translate(texte, dest=langue)

        await update.message.reply_text(
            f"🌍 Traduction :\n\n{resultat.text}"
        )
    except Exception:
        await update.message.reply_text(
            "❌ Erreur de traduction."
        )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("langues", langues))
app.add_handler(CommandHandler("traduire", traduire))
app.add_handler(CommandHandler("aide", aide))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        translate_text
    )
)

app.run_polling()
``
