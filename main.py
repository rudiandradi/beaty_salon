import telebot
import config
from DB import createUser, create_feedback, add_mailing
import Keyboards
import logging
import big_messages
from DynamicKeyboards import create_services, create_staff_markup
import uuid


rate = 0
bot = telebot.TeleBot(config.token)
logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'bot.log')
logger = logging.getLogger('bot.log')


# Обработчик старта
@bot.message_handler(commands=['start'])
def name(message):
    msg = 'Привет! Я бот салона красоты Юлия. Для начала скажи,' \
          ' как могу к тебе обращаться?'
    send = bot.send_message(message.chat.id, msg, parse_mode='html')
    bot.register_next_step_handler(send, first)
# Приём контакта
def welcome(message):
    send = bot.send_message(message.chat.id, f'Отлично, {message.text}! Теперь мне нужно знать твой номер телефона',
                         reply_markup=Keyboards.contact_keyboard)
    bot.register_next_step_handler(send, first)
def first(message):
    createUser(message) # Добавляем пользователя в DB
    msg = 'Выбери опцию: используй клавиатуру, чтобы посмотреть информацию об услугах, записаться к нам или подписаться на рассылку'
    send = bot.send_message(message.chat.id, msg, parse_mode='html', reply_markup=Keyboards.about_markup)
    bot.register_next_step_handler(send, main)
def ask_feedback(chat_id, message_id):
    msg = 'Введите, пожалуйста, отзыв. '
    send = bot.edit_message_text(chat_id=chat_id, text=msg, message_id=message_id,
                          parse_mode='html', reply_markup=Keyboards.ask_feedback_markup)
    bot.register_next_step_handler(send, feedback_write)
def mark_write(chat, message_id):
    # with open("feedbacks.txt", "a+") as fout:
    #     fout.write(f'User: {chat}, Mark: {rate}\n\n')
    # fout.close()
    create_feedback(user_id=uuid.uuid4(),chat_id=chat, rate=rate)
    msg = 'Спасибо!\nВаше мнение очень важно для нас!\nВыберите опцию'
    send = bot.edit_message_text(chat_id=chat, text=msg, message_id=message_id,
                          parse_mode='html', reply_markup=Keyboards.ask_feedback_markup)
    bot.register_next_step_handler(send, main)
def feedback_write(message):
    feedback = message.text
    # with open("feedbacks.txt", "a+") as fout:
    #     fout.write(f'User: {message.from_user.id}, Mark: {rate}, Text: {feedback}\n\n')
    # fout.close()
    create_feedback(user_id=uuid.uuid4(), chat_id=message.from_user.id, rate=rate, comment=feedback)
    msg = 'Спасибо! Отзыв записан!'
    send = bot.send_message(message.chat.id, msg, parse_mode='html', reply_markup=Keyboards.about_markup)
    bot.register_next_step_handler(send, main)

def main(message):
    if message.text == 'О нас':
        msg = big_messages.about_us
        photo = 'https://mir-s3-cdn-cf.behance.net/project_modules/2800_opt_1/09d3c436328513.5717d4d80e7a6.png'
        send=bot.send_photo(chat_id=message.chat.id, caption=msg, photo=photo,parse_mode='html', reply_markup=Keyboards.about_markup)
        #send = bot.send_message(message.chat.id, msg, parse_mode='html', reply_markup=Keyboards.about_markup)
        bot.register_next_step_handler(send, main)
    elif message.text == 'Услуги':
        msg = 'Выбери услугу'
        bot.send_message(message.chat.id, msg, parse_mode='html', reply_markup=create_services(page=1))
    elif message.text == 'Отзывы':
        msg = 'Выберите опцию'
        bot.send_message(message.chat.id, msg, parse_mode='html', reply_markup=Keyboards.fb_markup)
    elif message.text == 'Контакты':
        msg = big_messages.contact
        send = bot.send_message(message.chat.id, msg, parse_mode='html', reply_markup=Keyboards.about_markup)
        bot.register_next_step_handler(send, main)
    elif message.text == 'Подписаться на рассылку':
        msg = 'Вы успешно подписались на рассылку!'
        add_mailing(message.chat.id)
        send = bot.send_message(message.chat.id, msg, parse_mode='html', reply_markup=Keyboards.about_markup)
        bot.register_next_step_handler(send, main)
    elif message.text == 'Акции':
        msg = 'Акций пока нет. Они обязательно появятся после интеграции с YClients'
        send = bot.send_message(message.chat.id, msg, parse_mode='html', reply_markup=Keyboards.about_markup)
        bot.register_next_step_handler(send, main)
    elif message.text == 'Специалисты':
        msg='Выберите специалиста'
        bot.send_message(message.chat.id, msg, parse_mode='html', reply_markup=create_staff_markup(page=1))




@bot.message_handler(content_types=['text'])
def message_handlers(message):
        if message.chat.type == 'private':
            if (str(message.text)).lower() == 'о нас':
                msg = big_messages.about_us
                photo = 'https://mir-s3-cdn-cf.behance.net/project_modules/2800_opt_1/09d3c436328513.5717d4d80e7a6.png'
                bot.send_photo(chat_id=message.chat.id, caption=msg, photo=photo,parse_mode='html', reply_markup=Keyboards.about_markup)
            elif (str(message.text)).lower() == 'услуги':
                msg = 'Выбери услугу'
                bot.send_message(message.chat.id, msg, parse_mode='html', reply_markup=create_services(page=1))
            elif (str(message.text)).lower() == 'отзывы':
                msg = 'Выберите опцию'
                bot.send_message(message.chat.id, msg, parse_mode='html', reply_markup=Keyboards.fb_markup)
            elif (str(message.text)).lower() == 'контакты':
                msg = big_messages.contact
                bot.send_message(message.chat.id, msg, parse_mode='html', reply_markup=Keyboards.about_markup)
                #bot.register_next_step_handler(send, main)
            elif (str(message.text)).lower() == 'подписаться на рассылку':
                msg = 'Вы успешно подписались на рассылку!'
                add_mailing(message.chat.id)
                bot.send_message(message.chat.id, msg, parse_mode='html', reply_markup=Keyboards.about_markup)
            elif (str(message.text)).lower() == 'акции':
                msg = 'Акций пока нет. Они обязательно появятся после интеграции с YClients'
                send = bot.send_message(message.chat.id, msg, parse_mode='html', reply_markup=Keyboards.about_markup)
                bot.register_next_step_handler(send, main)
            elif (str(message.text)).lower() == 'специалисты':
                msg = 'Выберите специалиста'
                bot.send_message(message.chat.id, msg, parse_mode='html', reply_markup=create_staff_markup(page=1))


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        global rate, triger
        triger = 0
        if call.message:

            # Меню переключения услуг
            if call.data == 'services':
                msg = 'Выбери услугу'
                triger = 1
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Переход на страницу 1.")
                bot.edit_message_text(chat_id=call.message.chat.id, text=msg, message_id=call.message.message_id,
                                          parse_mode='html', reply_markup=create_services(page=1))
            elif call.data == 'services_2':
                msg = 'Выбери услугу'
                triger = 1
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Переход на страницу 2.")
                bot.edit_message_text(chat_id=call.message.chat.id, text=msg, message_id=call.message.message_id,
                                          parse_mode='html', reply_markup=create_services(page=2))
            elif call.data == 'services_3':
                msg = 'Выбери услугу'
                triger = 1
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Переход на страницу 3.")
                bot.edit_message_text(chat_id=call.message.chat.id, text=msg, message_id=call.message.message_id,
                                          parse_mode='html', reply_markup=create_services(page=3))
            elif call.data == 'staf_1':
                msg = 'Выберите специалиста'
                triger = 1
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Переход на страницу 1.")
                bot.edit_message_text(chat_id=call.message.chat.id, text=msg, message_id=call.message.message_id,
                                          parse_mode='html', reply_markup=create_staff_markup(page=1))
            elif call.data == 'staf_2':
                msg = 'Выберите специалиста'
                triger = 1
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Переход на страницу 2.")
                bot.edit_message_text(chat_id=call.message.chat.id, text=msg, message_id=call.message.message_id,
                                          parse_mode='html', reply_markup=create_staff_markup(page=2))

            # Услуги
            elif call.data == 'haircut':
                photo = 'https://ratatum.com/wp-content/uploads/2020/04/Pricheska_s_nachesom-6.jpg'
                msg = big_messages.haircut_info
                bot.send_photo(call.message.chat.id, photo, caption=msg, reply_markup=Keyboards.book_service, parse_mode='html')
            elif call.data == 'makiyazh':
                photo = 'https://oir.mobi/uploads/posts/2019-12/1576016924_20-27.jpg'
                msg = big_messages.makiyazh_info
                bot.send_photo(call.message.chat.id, photo, caption=msg, reply_markup=Keyboards.book_service, parse_mode='html')
            elif call.data == 'manikur':
                photo = 'https://pix-feed.com/wp-content/uploads/2020/02/23-7.jpg'
                msg = big_messages.manikur_info
                bot.send_photo(call.message.chat.id, photo, caption=msg, reply_markup=Keyboards.book_service, parse_mode='html')
            elif call.data == 'pokraska':
                photo = 'https://krasotka.cc/wp-content/uploads/2017/11/23161345_1940347502950411_8868178262950412288_n.jpg'
                msg = big_messages.pokraska_info
                bot.send_photo(call.message.chat.id, photo, caption=msg, reply_markup=Keyboards.book_service, parse_mode='html')
            elif call.data == 'pedikur':
                photo = 'https://lisa.ru/images/cache/2019/4/23/resize_1080_1350_true_q90_515062_11cb0a8e85.jpeg'
                msg = big_messages.pedikur_info
                bot.send_photo(call.message.chat.id, photo, caption=msg, reply_markup=Keyboards.book_service, parse_mode='html')
            elif call.data == 'tatuazh':
                photo = 'https://www.anna-key.ru/upload/medialibrary/d75/d751a4ea75774d5f89d39f06bbcdeb23.jpg'
                msg = big_messages.tatuazh_info
                bot.send_photo(call.message.chat.id, photo, caption=msg, reply_markup=Keyboards.book_service, parse_mode='html')
            elif call.data == 'piling':
                photo = 'https://salonmagia.ru/upload/iblock/0ed/0eddd80ae09bf79c1e27a88220fa50e7.jpg'
                msg = big_messages.piling_info
                bot.send_photo(call.message.chat.id, photo, caption=msg, reply_markup=Keyboards.book_service, parse_mode='html')
            elif call.data == 'chistka':
                photo = 'https://101hairtips.com/wp-content/uploads/2/5/7/257d574e825803b49e1c5a80b704cc22.jpeg'
                msg = big_messages.chistka_info
                bot.send_photo(call.message.chat.id, photo, caption=msg, reply_markup=Keyboards.book_service, parse_mode='html')
            elif call.data == 'obert':
                photo = 'https://vseolady.ru/wp-content/uploads/2019/02/Antitsellyulitnye-obertyvaniya-2-1.jpg'
                msg = big_messages.obert_info
                bot.send_photo(call.message.chat.id, photo, caption=msg, reply_markup=Keyboards.book_service, parse_mode='html')
            elif call.data == 'narashivanie':
                photo = 'https://ratatum.com/wp-content/uploads/2020/04/Pricheska_s_nachesom-6.jpg'
                msg = big_messages.narashivanie_info
                bot.send_photo(call.message.chat.id, photo, caption=msg, reply_markup=Keyboards.narashivanie_markup, parse_mode='html')
            elif call.data == 'n_resnic':
                photo = 'https://alexgitara.ru/wp-content/uploads/effekt-kajli.jpg'
                msg = big_messages.n_resnic_info
                bot.send_photo(call.message.chat.id, photo, caption=msg, reply_markup=Keyboards.book_service, parse_mode='html')
            elif call.data == 'n_nails':
                photo = 'https://nail-trend.ru/uploads/posts/2017-12/1512923821_37.jpg'
                msg = big_messages.n_nails_info
                bot.send_photo(call.message.chat.id, photo, caption=msg, reply_markup=Keyboards.book_service, parse_mode='html')
            elif call.data == 'massazh':
                photo = 'https://ratatum.com/wp-content/uploads/2020/04/Pricheska_s_nachesom-6.jpg'
                msg = big_messages.massazh_info
                bot.send_photo(call.message.chat.id, photo, caption=msg, reply_markup=Keyboards.massazh_markup, parse_mode='html')
            elif call.data == 'm_stop':
                photo = 'https://ufa.klassmassazh.ru/media/pic_folder/service_main_photo/tehnika-massazha-v2.orig.jpg'
                msg = big_messages.m_stop_info
                bot.send_photo(call.message.chat.id, photo, caption=msg, reply_markup=Keyboards.book_service, parse_mode='html')
            elif call.data == 'm_spina':
                photo = 'https://ufa.klassmassazh.ru/media/pic_folder/service_main_photo/tehnika-massazha-v2.orig.jpg'
                msg = big_messages.m_spina_info
                bot.send_photo(call.message.chat.id, photo, caption=msg, reply_markup=Keyboards.book_service, parse_mode='html')
            elif call.data == 'm_face':
                photo = 'https://ufa.klassmassazh.ru/media/pic_folder/service_main_photo/tehnika-massazha-v2.orig.jpg'
                msg = big_messages.m_face_info
                bot.send_photo(call.message.chat.id, photo, caption=msg, reply_markup=Keyboards.book_service, parse_mode='html')
            elif call.data == 'm_tai':
                photo = 'https://ufa.klassmassazh.ru/media/pic_folder/service_main_photo/tehnika-massazha-v2.orig.jpg'
                msg = big_messages.m_tai_info
                bot.send_photo(call.message.chat.id, photo, caption=msg, reply_markup=Keyboards.book_service, parse_mode='html')
            elif call.data == 'booking':
                msg = 'Тут после интеграции с <a href="https://www.yclients.com">YClients</a> можно будет записаться'
                send = bot.send_message(call.message.chat.id, msg, parse_mode='html', reply_markup=Keyboards.about_markup)
                bot.register_next_step_handler(send, main)
            elif call.data == 'exit':
                msg = 'Выбери функцию'
                send = bot.send_message(call.message.chat.id, msg, parse_mode='html', reply_markup=Keyboards.about_markup)
                bot.register_next_step_handler(send, main)

            # Специалисты:
            elif call.data == 'staf_alex':
                photo = 'https://alterozoom.com/images/235772_DHmQpMf4iOKkppEbmUxEgg.jpeg'
                msg = big_messages.staf_alex_info
                bot.send_photo(call.message.chat.id, photo, caption=msg, reply_markup=Keyboards.book_service,
                               parse_mode='html')
            elif call.data == 'staf_egor':
                photo = 'https://alterozoom.com/images/235772_DHmQpMf4iOKkppEbmUxEgg.jpeg'
                msg = big_messages.staf_egor_info
                bot.send_photo(call.message.chat.id, photo, caption=msg, reply_markup=Keyboards.book_service,
                               parse_mode='html')
            elif call.data == 'staf_ivan':
                photo = 'https://alterozoom.com/images/235772_DHmQpMf4iOKkppEbmUxEgg.jpeg'
                msg = big_messages.staf_ivan_info
                bot.send_photo(call.message.chat.id, photo, caption=msg, reply_markup=Keyboards.book_service,
                               parse_mode='html')
            elif call.data == 'staf_sveta':
                photo = 'https://alterozoom.com/images/235772_DHmQpMf4iOKkppEbmUxEgg.jpeg'
                msg = big_messages.staf_sveta_info
                bot.send_photo(call.message.chat.id, photo, caption=msg, reply_markup=Keyboards.book_service,
                               parse_mode='html')
            elif call.data == 'staf_inga':
                photo = 'https://alterozoom.com/images/235772_DHmQpMf4iOKkppEbmUxEgg.jpeg'
                msg = big_messages.staf_inga_info
                bot.send_photo(call.message.chat.id, photo, caption=msg, reply_markup=Keyboards.book_service,
                               parse_mode='html')
            elif call.data == 'staf_vika':
                photo = 'https://alterozoom.com/images/235772_DHmQpMf4iOKkppEbmUxEgg.jpeg'
                msg = big_messages.staf_vika_info
                bot.send_photo(call.message.chat.id, photo, caption=msg, reply_markup=Keyboards.book_service,
                               parse_mode='html')

            # Отзывы:
            elif call.data == 'send_rate':
                msg = 'Пожалуйста, оцените наш салон'
                bot.send_message(call.message.chat.id, msg, reply_markup=Keyboards.rate_markup)
            elif call.data == 'rate_written_1':
                msg = 'Спасибо за оценку! Хотите ли написать комментарий?'
                triger = 1
                rate = 1
                bot.edit_message_text(chat_id=call.message.chat.id, text=msg, message_id=call.message.message_id,
                                      parse_mode='html', reply_markup=Keyboards.ask_feedback_markup)
            elif call.data == 'rate_written_2':
                msg = 'Спасибо за оценку! Хотите ли написать комментарий?'
                triger = 1
                rate = 2
                bot.edit_message_text(chat_id=call.message.chat.id, text=msg, message_id=call.message.message_id,
                                      parse_mode='html', reply_markup=Keyboards.ask_feedback_markup)
            elif call.data == 'rate_written_3':
                msg = 'Спасибо за оценку! Хотите ли написать комментарий?'
                triger = 1
                rate = 3
                bot.edit_message_text(chat_id=call.message.chat.id, text=msg, message_id=call.message.message_id,
                                      parse_mode='html', reply_markup=Keyboards.ask_feedback_markup)
            elif call.data == 'rate_written_4':
                msg = 'Спасибо за оценку! Хотите ли написать комментарий?'
                triger = 1
                rate = 4
                bot.edit_message_text(chat_id=call.message.chat.id, text=msg, message_id=call.message.message_id,
                                      parse_mode='html', reply_markup=Keyboards.ask_feedback_markup)
            elif call.data == 'rate_written_5':
                msg = 'Спасибо за оценку! Хотите ли написать комментарий?'
                triger = 1
                rate = 5
                bot.edit_message_text(chat_id=call.message.chat.id, text=msg, message_id=call.message.message_id,
                                      parse_mode='html', reply_markup=Keyboards.ask_feedback_markup)
            elif call.data == 'rate_written_6':
                msg = 'Спасибо за оценку! Хотите ли написать комментарий?'
                triger = 1
                rate = 6
                bot.edit_message_text(chat_id=call.message.chat.id, text=msg, message_id=call.message.message_id,
                                      parse_mode='html', reply_markup=Keyboards.ask_feedback_markup)
            elif call.data == 'rate_written_7':
                msg = 'Спасибо за оценку! Хотите ли написать комментарий?'
                triger = 1
                rate = 7
                bot.edit_message_text(chat_id=call.message.chat.id, text=msg, message_id=call.message.message_id,
                                      parse_mode='html', reply_markup=Keyboards.ask_feedback_markup)
            elif call.data == 'rate_written_8':
                msg = 'Спасибо за оценку! Хотите ли написать комментарий?'
                triger = 1
                rate = 8
                bot.edit_message_text(chat_id=call.message.chat.id, text=msg, message_id=call.message.message_id,
                                      parse_mode='html', reply_markup=Keyboards.ask_feedback_markup)
            elif call.data == 'rate_written_9':
                msg = 'Спасибо за оценку! Хотите ли написать комментарий?'
                triger = 1
                rate = 9
                bot.edit_message_text(chat_id=call.message.chat.id, text=msg, message_id=call.message.message_id,
                                      parse_mode='html', reply_markup=Keyboards.ask_feedback_markup)
            elif call.data == 'rate_written_10':
                msg = 'Спасибо за оценку! Хотите ли написать комментарий?'
                triger = 1
                rate = 10
                bot.edit_message_text(chat_id=call.message.chat.id, text=msg, message_id=call.message.message_id,
                                      parse_mode='html', reply_markup=Keyboards.ask_feedback_markup)
            elif call.data == 'want_send_feedback':
                ask_feedback(call.message.chat.id, call.message.message_id)
            elif call.data == 'dont_want_send_feedback':
                mark_write(call.message.chat.id, call.message.message_id)





        if triger == 0:
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

    except Exception as e:
        print(repr(e))

bot.polling(none_stop=True)