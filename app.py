import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter


bot = telebot.TeleBot(TOKEN)




@bot.message_handler(commands = ['Start', 'Help'])
def Help(message: telebot.types.Message):
    text = 'Приветствую! Чтобы начать работу с ботом, введите команду в следующем формате: \n <Имя валюты,цену которой вы хотите узнать><Имя валюты, в которую хотите конвертировать первую валюту><Количество конвертируемой валюты>. \n \nНазвания валют должны быть введены на русском языке, в единственном числе через пробел. \n \n **Пример:** Рубль Доллар 23 \n Увидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands = ['values'])
def values(message: telebot.types.Message):
    text = 'Вернуться к началу: /Start \nДоступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3 :
            raise ConvertionException('Слишком много параметров!Повторите попытку.')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя!\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()


