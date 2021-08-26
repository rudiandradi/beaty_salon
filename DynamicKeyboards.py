from telebot import types


def create_services(page):
    services_markup = types.InlineKeyboardMarkup(row_width=1)
    if page == 1:
        key1 = types.InlineKeyboardButton('Парикмахер', callback_data='haircut')
        key2 = types.InlineKeyboardButton('Макияж', callback_data='makiyazh')
        key3 = types.InlineKeyboardButton('Маникюр', callback_data='manikur')
        key4 = types.InlineKeyboardButton('Покраска', callback_data='pokraska')
        key5 = types.InlineKeyboardButton('1', callback_data='services')
        key6 = types.InlineKeyboardButton('2', callback_data='services_2')
        key7 = types.InlineKeyboardButton('3', callback_data='services_3')
        services_markup.add(key1).add(key2).add(key3).add(key4).row(key5,key6,key7)

    elif page == 2:
        key1 = types.InlineKeyboardButton('Педикюр', callback_data='pedikur')
        key2 = types.InlineKeyboardButton('Татуаж',callback_data='tatuazh')
        key3 = types.InlineKeyboardButton('Наращивание', callback_data='narashivanie')
        key4 = types.InlineKeyboardButton('Чистка лица', callback_data='chistka')
        key5 = types.InlineKeyboardButton('1', callback_data='services')
        key6 = types.InlineKeyboardButton('2', callback_data='services_2')
        key7 = types.InlineKeyboardButton('3', callback_data='services_3')
        services_markup.add(key1).add(key2).add(key3).add(key4).row(key5,key6,key7)

    elif page == 3:
        key1 = types.InlineKeyboardButton('Обёртывание', callback_data='obert')
        key2 = types.InlineKeyboardButton('Массаж', callback_data='massazh')
        key3 = types.InlineKeyboardButton('Пилинг', callback_data='piling')
        key4 = types.InlineKeyboardButton('1', callback_data='services')
        key5 = types.InlineKeyboardButton('2', callback_data='services_2')
        key6 = types.InlineKeyboardButton('3', callback_data='services_3')
        services_markup.add(key1).add(key2).add(key3).row(key4, key5, key6)

    key_exit = types.InlineKeyboardButton('Главное меню', callback_data='exit')
    services_markup.add(key_exit)

    return services_markup

def create_staff_markup(page):
    staff_markup = types.InlineKeyboardMarkup()
    if page == 1:
        key1 = types.InlineKeyboardButton('Алексей', callback_data='staf_alex')
        key2 = types.InlineKeyboardButton('Егор', callback_data='staf_egor')
        key3 = types.InlineKeyboardButton('Иван', callback_data='staf_ivan')
        key4 = types.InlineKeyboardButton('1', callback_data='staf_1')
        key5 = types.InlineKeyboardButton('2', callback_data='staf_2')
        staff_markup.add(key1).add(key2).add(key3).row(key4, key5)
    elif page == 2:
        key1 = types.InlineKeyboardButton('Светлана', callback_data='staf_sveta')
        key2 = types.InlineKeyboardButton('Инга', callback_data='staf_inga')
        key3 = types.InlineKeyboardButton('Вика', callback_data='staf_vika')
        key4 = types.InlineKeyboardButton('1', callback_data='staf_1')
        key5 = types.InlineKeyboardButton('2', callback_data='staf_2')
        staff_markup.add(key1).add(key2).add(key3).row(key4, key5)

    return staff_markup
