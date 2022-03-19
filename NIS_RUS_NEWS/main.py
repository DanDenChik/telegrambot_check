from telegram import Update, Bot, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
from credits import bot_token
import os

CODE = 0
UNIT = 1
SAT = 2
WORK = 3
PHOTO = 4

STUDENT_CLASS = 0
STUDENT_CODE = 1
STUDENT_UNIT = 2


class_name = ""
code_name = ""
unit_name = ""
sat_name = ""
work_name = ""

stud_class_name = ""
stud_code_name = ""
stud_unit_name = ""
bot = Bot(token=bot_token)
updater = Updater(token=bot_token)
dispatcher = updater.dispatcher

def start(update, context):
    if str(update.message.from_user["username"] != "aidankakh"):
        reply_keyboard = [os.listdir(path="classes")]
        update.message.reply_text('Добрый день, введите ваш класс!', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return STUDENT_CLASS
    else:
        context.bot.send_message(update.effective_chat.id, text='Добрый день, Айдана Еркиновна!')

def addclass(update, context):
    if str(update.message.from_user["username"] == "DanDenChik" or update.message.from_user["username"] == "aidankakh"):
        if os.path.exists("classes/" + context.args[0]):
            context.bot.send_message(update.effective_chat.id, text='Класс уже существует.')
        else:
            os.mkdir("classes/"+context.args[0])
            context.bot.send_message(update.effective_chat.id, text='Класс был успешно добавлен.')
    else:
        context.bot.send_message(update.effective_chat.id, text='Вы не учитель!')
            
def addwork(update, context):
    if str(update.message.from_user["username"]) == "DanDenChik" or str(update.message.from_user["username"]) == "aidankakh" :
        reply_keyboard = [os.listdir(path="classes")]
        update.message.reply_text('Добрый день! Выберите класс для добавления работы', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return CODE
    else:
        context.bot.send_message(update.effective_chat.id, text='Вы не учитель!')
     
def code(update, context):
    global class_name
    class_name = update.message.text
    update.message.reply_text('Отлично! Теперь отправьте нам код ученика, мы заведем личную карточку или откроем существующую')
    
    return UNIT

def unit(update, context):
    global code_name
    code_name = str(update.message.text)
    path = os.path.join("classes", class_name, code_name)
    if os.path.exists(path):
        reply_keyboard = [["1 четверть","2 четверть"],["3 четверть","4 четверть"]]
        update.message.reply_text('Код уже зарегестрирован, выберите четверть:', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    else:
        os.mkdir(path)
        reply_keyboard = [["1 четверть","2 четверть"],["3 четверть","4 четверть"]]
        update.message.reply_text('Код зарегестрирован, выберите четверть:', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return SAT
    
def sat(update, context):
    global unit_name
    unit_name = str(update.message.text)
    path = os.path.join("classes", class_name, code_name, unit_name)
    if os.path.exists(path):
        reply_keyboard = [["СОР 1","СОР 2"],["СОЧ"]]
        update.message.reply_text('Хорошо! Теперь выберите, что вы хотите добавить', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    else:
        os.mkdir(path)
        reply_keyboard = [["СОР 1","СОР 2"],["СОЧ"]]
        update.message.reply_text('Хорошо! Теперь выберите, что вы хотите добавить', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return WORK
    
def work(update, context):
    global sat_name
    sat_name = str(update.message.text)
    path = os.path.join("classes", class_name, code_name, unit_name, sat_name)
    if os.path.exists(path):
        update.message.reply_text('Хорошо! Теперь отправьте файл с работой')
    else:
        os.mkdir(path)
        update.message.reply_text('Хорошо! Теперь отправьте файл с работой')
        
    
    return PHOTO

def photo(update, context):
    photo_file = update.message.document.get_file()
    path = os.path.join("classes", class_name, code_name, unit_name, sat_name)
    photo_file.download(path+"\work.jpeg")
    update.message.reply_text('Файл сохранен!')
    return ConversationHandler.END
   
def stud_class():
    global stud_class_name
    stud_class_name = update.message.text
    path = os.path.join("classes", stud_class_name)
    context.bot.send_message(update.effective_chat.id, text=path)
    if os.path.exists(path):
        update.message.reply_text('Отлично! Теперь отправьте нам ваш код.')
        return STUDENT_CODE
        
def stud_code():   
    global stud_code_name
    stud_code_name = update.message.text
    path = os.path.join("classes", stud_class_name, stud_code_name)
    stud_code_name = update.message.text
    if os.path.exists(path):
        reply_keyboard = [["1 четверть","2 четверть"],["3 четверть","4 четверть"]]
        update.message.reply_text('Отлично! Теперь выберите четверть.', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return STUDENT_UNIT

        
def stud_unit():   
    
    global stud_unit_name
    stud_unit_name = update.message.text
    path = os.path.join("classes", stud_class_name, stud_code_name, stud_unit_name)
    if os.path.exists(path):
        for filename in os.listdir(path):
            bot.send_document(message.chat.id, open(path+"/"+filename))
        return ConversationHandler.END
    
        

        
def cancel(update, context):
    update.message.reply_text('Отмена.')
    return ConversationHandler.END
     
start_handler = CommandHandler('start', start)
addclass_handler = CommandHandler('addclass', addclass)
addwork_handler = CommandHandler('addwork', addwork)
code_handler = MessageHandler(Filters.text & ~Filters.command, code)
unit_handler = MessageHandler(Filters.text & ~Filters.command, unit)
sat_handler = MessageHandler(Filters.regex('^(1 четверть|2 четверть|3 четверть|4 четверть)$'), sat)
work_handler = MessageHandler(Filters.regex('^(СОР 1|СОР 2|СОЧ)$'), work)
photo_handler = MessageHandler(Filters.document.category("image"), photo)
cancel_handler = CommandHandler('cancel', cancel)
stud_class_handler = MessageHandler(Filters.text & ~Filters.command, stud_class)
stud_code_handler = MessageHandler(Filters.text & ~Filters.command, stud_code)
stud_unit_handler = MessageHandler(Filters.text & ~Filters.command, stud_unit)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(addclass_handler)

conv_handler = ConversationHandler(
    entry_points=[addwork_handler],
    states={
        CODE: [code_handler],
        UNIT: [unit_handler],
        SAT: [sat_handler],
        WORK: [work_handler],
        PHOTO: [photo_handler]
    },fallbacks=[cancel_handler])
dispatcher.add_handler(conv_handler)

student_conv_handler = ConversationHandler(
    entry_points=[start_handler],
    states={
        STUDENT_CLASS: [stud_class_handler],
        STUDENT_CODE: [stud_code_handler],
        STUDENT_UNIT: [stud_unit_handler]
    },fallbacks=[cancel_handler])
dispatcher.add_handler(student_conv_handler)

updater.start_polling()
updater.idle()