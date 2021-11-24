from telegram.ext import *
import os
import core.core as core

bot = core.PizzaBot()


def start_command(update, context):
    update.message.reply_text('Введите /help для списка доступных команд')


def help_command(update, context):
    update.message.reply_text('Вы можете начать заказ введя /order и отменить его в любой момент введя /cancel')


def cancel_command(update, context):
    if bot.state != 'asleep':
        bot.cancel()
        bot.end()
        bot.set_size(None)
        bot.set_payment_method(None)
        update.message.reply_text('Заказ отменён')
    else:
        update.message.reply_text('Нечего отменять')


def order_command(update, context):
    bot.start()
    update.message.reply_text('Какую вы хотите пиццу? Большую или маленькую?')


def handle_message(update, context):
    text = str(update.message.text).lower()

    if bot.state == 'size_order':
        if text in ('большую' , 'маленькую'):
            bot.set_size(text)
            bot.next()
            update.message.reply_text('Как вы будете платить?')
        else:
            update.message.reply_text('Я не знаю такой пиццы. Только большую и маленькую')
    elif bot.state == 'payment_method':
        bot.set_payment_method(text)
        bot.next()
        update.message.reply_text(f'Вы хотите {bot.size} пиццу, оплата - {bot.payment_method}?')
    elif bot.state == 'confirmation':
        if text == "да":
            bot.confirm()
            bot.end()
            update.message.reply_text('Спасибо за заказ')
        elif text == "нет":
            bot.cancel()
            bot.end()
            update.message.reply_text('Хорошо, введите /start чтобы начать сначала')
        else:
            update.message.reply_text('Простите, Я вас не понимаю. Введите Да/Нет')
    else:
        update.message.reply_text('Простите, произошла ошибка')


def error(update, context):
    print(f"Update {update} caused error {context.error}")


def main():
    updater = Updater(os.environ.get('TOKEN'), use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("cancel", cancel_command))
    dp.add_handler(CommandHandler("order", order_command))

    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()
