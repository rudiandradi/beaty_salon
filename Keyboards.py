from telebot import types


contact_keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
button_phone = types.KeyboardButton(text="Отправить телефон📞",
                                    request_contact=True)
contact_keyboard.add(button_phone)

### Основная клавиатура
about_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
key1 = types.KeyboardButton('О нас')
key2 = types.KeyboardButton('Услуги')
key3 = types.KeyboardButton('Специалисты')
key4 = types.KeyboardButton('Отзывы')
key5 = types.KeyboardButton('Контакты')
key6 = types.KeyboardButton('Подписаться на рассылку')
key7 = types.KeyboardButton('Акции')
about_markup.add(key1).row(key2,key3).row(key4,key5).add(key7).add(key6)

fb_markup = types.InlineKeyboardMarkup()
key1 = types.InlineKeyboardButton('Посмотреть отзывы', url='http://7yakooa7.plp7.ru/#reviews')
key2 = types.InlineKeyboardButton('Оставить отзыва', callback_data='send_rate')
fb_markup.add(key1).add(key2)


book_service = types.InlineKeyboardMarkup()
key1 = types.InlineKeyboardButton('Записаться', callback_data='booking')
key2 = types.InlineKeyboardButton('Выход', callback_data='exit')
book_service.add(key1).add(key2)

narashivanie_markup = types.InlineKeyboardMarkup(row_width=3)
key1 = types.InlineKeyboardButton('Наращивание ресниц', callback_data='n_resnic')
key2 = types.InlineKeyboardButton('Наращивание ногтей', callback_data='n_nails')
narashivanie_markup.add(key1).add(key2)

massazh_markup = types.InlineKeyboardMarkup(row_width=3)
key1 = types.InlineKeyboardButton('Массаж стоп', callback_data='m_stop')
key2 = types.InlineKeyboardButton('Массаж спины', callback_data='m_spina')
key3 = types.InlineKeyboardButton('Массаж лица', callback_data='m_face')
key4 = types.InlineKeyboardButton('Тайский', callback_data='m_tai')
massazh_markup.add(key1).add(key2).add(key3).add(key4)

rate_markup = types.InlineKeyboardMarkup(row_width=3)
key1 = types.InlineKeyboardButton('1', callback_data='rate_written_1')
key2 = types.InlineKeyboardButton('2', callback_data='rate_written_2')
key3 = types.InlineKeyboardButton('3', callback_data='rate_written_3')
key4 = types.InlineKeyboardButton('4', callback_data='rate_written_4')
key5 = types.InlineKeyboardButton('5', callback_data='rate_written_5')
key6 = types.InlineKeyboardButton('6', callback_data='rate_written_6')
key7 = types.InlineKeyboardButton('7', callback_data='rate_written_7')
key8 = types.InlineKeyboardButton('8', callback_data='rate_written_8')
key9 = types.InlineKeyboardButton('9', callback_data='rate_written_9')
key10 = types.InlineKeyboardButton('10', callback_data='rate_written_10')
rate_markup.row(key1,key2,key3,key4).row(key5,key6,key7,key8).row(key9,key10)

ask_feedback_markup = types.InlineKeyboardMarkup(row_width=3)
key1 = types.InlineKeyboardButton('Да', callback_data='want_send_feedback')
key2 = types.InlineKeyboardButton('Нет', callback_data='dont_want_send_feedback')
ask_feedback_markup.add(key1).add(key2)