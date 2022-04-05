#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import time
from datetime import *
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
import aioschedule
import config
from aiogram import Bot, Dispatcher, executor, types
import functions

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

chosenNum = -1
gotQuestion = []

users = functions.updateUsers()
print(users)

theText = ""

blacklist = []
reactionEnabled = False


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if functions.userBlocked(message.from_user.id):
        await message.delete()
        await bot.send_message(message.from_user.id, "Вы заблокированы на некоторое время!")
    else:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton(text="✍️ Подписка на уведомления"))
        keyboard.add(KeyboardButton(text="❌ Отписаться от уведомлении"))
        keyboard.add(KeyboardButton(text="🙋‍♂️Задать вопрос"))
        keyboard.add(KeyboardButton(text="ℹ️Актуальные вопросы"))
        await message.answer("Привет, вот список доступных команд: ", reply_markup=keyboard)
    return



@dp.message_handler(commands=["cancel"])
async def cancel(message: types.Message):
    functions.setStatus(message.from_user.id, "None")

    await message.reply("Задача отменена")
    return


@dp.message_handler(text=["🙋‍♂️Задать вопрос"])
async def question(message: types.Message):
    if functions.userBlocked(message.from_user.id):
        await message.delete()
        await bot.send_message(message.from_user.id, "Вы заблокированы на некоторое время!")
    else:
        functions.setStatus(message.from_user.id, "question")
        await message.reply("Напишите Ваш вопрос либо отмените свое действие /cancel")
    return



@dp.message_handler(commands=["birthday"])
async def birthday(message: types.Message):
    if functions.userBlocked(message.from_user.id):
        await message.delete()
        await bot.send_message(message.from_user.id, "Вы заблокированы на некоторое время!")
    else:
        userData = functions.getUser(message.from_user.id)
        if userData[3] != None:
            await message.reply(f"Здравствуйте, {userData[2]}, "
                                f"Вы уже внесли свой день рождения ({userData[3]}) в базу данных! "
                                f"Для того чтобы изменить ее, напишите @yeapit")
        else:
            await message.reply("Укажите Вашу дату рождения в формате день/месяц/год (7/3/2000 : 7 марта 2000 года)")
            functions.setStatus(message.from_user.id, "birthday")
    return


@dp.message_handler(commands=['answers'])
async def answers(message: types.Message):
    if functions.userBlocked(message.from_user.id):
        await message.delete()
        await bot.send_message(message.from_user.id, "Вы заблокированы на некоторое время!")
    else:
        await message.answer("Актуальные вопросы - /interesting\n"
                             "Ваши вопросы - /myQuestions")
    return


@dp.message_handler(text=["ℹ️Актуальные вопросы"])
async def actualQuestions(message: types.Message):
    if functions.userBlocked(message.from_user.id):
        await message.delete()
        await bot.send_message(message.from_user.id, "Вы заблокированы на некоторое время!")
    else:
        questions = functions.getInteresting()
        s = "АКТУАЛЬНЫЕ ВОПРОСЫ:\n"
        for question in questions:
            s += "---------------------------\n" \
                 "Вопрос номер " + str(question[4]) + ":\n" \
                                                      "Вопрос: " + question[0] + "\n" \
                                                                                 "Ответ: " + question[1] + "\n"
        await message.answer(s)
    return


@dp.message_handler(commands=['myQuestions'])
async def myQuestions(message: types.Message):
    if functions.userBlocked(message.from_user.id):
        await message.delete()
        await bot.send_message(message.from_user.id, "Вы заблокированы на некоторое время!")
    else:
        questions = functions.getMyQuestions(message.from_user.id)

        s = "МОИ ВОПРОСЫ:\n"
        for question in questions:
            s += "--------------------------------\n" \
                 "Вопрос номер " + str(question[4]) + ":\n" \
                                                      "Вопрос: " + question[0] + "\n" \
                                                                                 "Ответ: " + question[1] + "\n"
        await message.answer(s)
    return


@dp.message_handler(text=['⌨️Команды'])
async def help(message: types.Message):
    if functions.userBlocked(message.from_user.id):
        await message.delete()
        await bot.send_message(message.from_user.id, "Вы заблокированы на некоторое время!")
    else:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(KeyboardButton(text="✍️ Подписка на уведомления"))
        keyboard.add(KeyboardButton(text="❌ Отписаться от уведомлении"))
        keyboard.add(KeyboardButton(text="🙋‍♂️Задать вопрос"))
        keyboard.add(KeyboardButton(text="ℹ️Актуальные вопросы"))
        await bot.send_message(message.from_user.id, "Вот список доступных команд: ", reply_markup=keyboard)
    return


@dp.message_handler(text=["✍️ Подписка на уведомления"])
async def func(message: types.Message):
    if functions.userBlocked(message.from_user.id):
        await message.delete()
        await bot.send_message(message.from_user.id, "Вы заблокированы на некоторое время!")
    else:
        user = functions.getUser(message.from_user.id)
        if user is None or user[2] == 'None':
            functions.deleteStudent(message.from_user.id)
            functions.addStudent(message.from_user.id, message.from_user.username, "None")
            await message.answer("Напишите свое имя на английском языке(Example: Sugurov Khamza)")
            functions.setStatus(message.from_user.id, "theName")
        else:
            await message.answer("Вы уже подписаны!")
    return


@dp.message_handler(text=["❌ Отписаться от уведомлении"])
async def unsubscribe(message: types.Message):
    if functions.userBlocked(message.from_user.id):
        await message.delete()
        await bot.send_message(message.from_user.id, "Вы заблокированы на некоторое время!")
    else:
        user = functions.getUser(message.from_user.id)
        if user is not None:
            functions.deleteStudent(message.from_user.id)
            await message.answer("Вы успешно отписались от уведомлений!")
            await bot.send_message(347821020, message.from_user.username + " отписался от уведомлении!")
        else:
            await message.answer("Вы не подписаны!")
    return



# ADMIN

@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    if message.from_user.id == 347821020 and message.chat.type == 'private':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton(text="Рассылка для всех"))
        keyboard.add(KeyboardButton(text="Рассылка для определенных людей"))
        keyboard.add(KeyboardButton(text="Заданные вопросы"))
        keyboard.add(KeyboardButton(text="Поместить в актуальные"))
        keyboard.add(KeyboardButton(text="Удалить из актуальных"))
        keyboard.add(KeyboardButton(text="Удалить вопросы"))
        keyboard.add(KeyboardButton(text="Управление курсами"))
        keyboard.add(KeyboardButton(text="/users"))
        keyboard.add(KeyboardButton(text="/update"))
        keyboard.add(KeyboardButton(text="/remove_from_bd"))
        keyboard.add(KeyboardButton(text="/block"))
        keyboard.add(KeyboardButton(text="/unblock"))
        await message.answer("Привет, Хамзеке, вот доступные функции", reply_markup=keyboard)
    else:
        await message.reply("Функция недоступна в беседе либо у Вас недостаточно прав!")
    return


@dp.message_handler(commands=['disable', 'enable'])
async def switchReaction(message: types.Message):
    global reactionEnabled
    if message.from_user.id == 347821020:
        msg = message.text.replace("/", '').strip()
        if msg == 'disable':
            reactionEnabled = False
        if msg == 'enable':
            reactionEnabled = True

        return
    else:
        await message.reply("У Вас недостаточно прав!")
    return


@dp.message_handler(commands=['users'])
async def showUsers(message: types.Message):
    if message.from_user.id == 347821020 and message.chat.type == 'private':
        t = ""
        for id in users:
            t += str(id) + " " + users[id] + "\n"
        await message.reply("Список пользователей:\n" + t)
    else:
        await message.reply("У Вас недостаточно прав либо функция недоступна в беседе!")
    return

@dp.message_handler(text=['Заданные вопросы'])
async def questions(message: types.Message):
    if message.from_user.id == 347821020 and message.chat.type == 'private':
        await message.answer("Вопросы без ответа /notAnswered\n"
                             "Все вопросы /allQuestions")
    else:
        await message.reply("Функция недоступна в беседе либо у Вас недостаточно прав!")
    return

@dp.message_handler(text=['Управление курсами'])
async def courses(message: types.Message):
    if message.from_user.id == config.ADMIN:
        await message.answer("Команда для добавления /ac courseName,courseId")
        text, list = functions.getCoursesMenu()
        await message.answer(text)
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(*list)
        if text != "Нет зарегистрированых курсов!":
            await message.answer("Введите ID курса",reply_markup=keyboard)
            functions.setStatus(message.from_user.id, "Courses")
    else:
        await message.answer("Нет доступа!")



@dp.message_handler(text=['Поместить в актуальные'])
async def makeInteresting(message: types.Message):
    if message.from_user.id == 347821020 and message.chat.type == 'private':
        questions = functions.getAnswered()
        s = "Отвеченные вопросы:\n "
        for question in questions:
            s += str(question[4]) + ". " + question[0] + "\n"

        await message.answer(s)
        await message.answer(
            "Введите id вопросов, которые хотите поместить в актуальные через запятую. Например (1, 2, 3..)")
        functions.setStatus(message.from_user.id, "makeInteresting")
    else:
        await message.reply("Функция недоступна в беседе либо у Вас недостаточно прав!")
    return


@dp.message_handler(text=['Удалить из актуальных'])
async def removeInteresting(message: types.Message):
    if message.from_user.id == 347821020 and message.chat.type == 'private':
        questions = functions.getInteresting()
        s = "Актуальные вопросы:\n"
        for question in questions:
            s += str(question[4]) + ". " + question[0] + "\n"

        await message.answer(s)
        await message.answer(
            "Введите id вопросов, которые хотите удалить из актуальных через запятую. Например (1, 2, 3..)")
        functions.setStatus(message.from_user.id, "removeInteresting")
    else:
        await message.reply("Функция недоступна в беседе либо у Вас недостаточно прав!")
    return


@dp.message_handler(commands=['notAnswered'])
async def notAnswered(message: types.Message):
    if message.from_user.id == 347821020 and message.chat.type == 'private':
        questions = functions.getNotAnswered()
        await message.answer("Введите id вопроса чтобы ответить, либо /cancel")
        s = ""
        for question in questions:
            s += str(question[4]) + ". " + question[0] + "\n"
        await message.answer(s)
        functions.setStatus(message.from_user.id, "questionNum")
    else:
        await message.reply("Функция недоступна в беседе либо у Вас недостаточно прав!")
    return


@dp.message_handler(commands=['allQuestions'])
async def allQuestions(message: types.Message):
    if message.from_user.id == 347821020 and message.chat.type == 'private':
        questions = functions.getQuestions()
        await message.answer("Введите id вопроса чтобы изменить, либо /cancel")
        s = ""
        for question in questions:
            s += str(question[4]) + ". " + question[0] + " :" + question[1] + "\n"
        await message.answer(s)
        functions.setStatus(message.from_user.id, "questionNum")
    else:
        await message.reply("Функция недоступна в беседе либо у Вас недостаточно прав!")
    return


@dp.message_handler(commands=['changeQuestion'])
async def changeQuestion(message: types.Message):
    if (functions.getStatus(message.from_user.id))[0] == 'gotQuestionNum':
        await message.reply("Введите вопрос!")
        functions.setStatus(message.from_user.id, "setNewQuestion")
        return


@dp.message_handler(commands=['sendAnswer'])
async def changeQuestion(message: types.Message):
    if (functions.getStatus(message.from_user.id))[0] == 'gotQuestionNum':
        await message.reply("Введите ответ:")
        functions.setStatus(message.from_user.id, "setAnswer")
        return


@dp.message_handler(commands=["block"])
async def blockUser(message: types.Message):
    if message.from_user.id == 347821020:
        userId = int(message.text.replace("/block ", ""))
        functions.setStatus(userId, 'Blocked')
        await message.answer("Пользователь заблокирован!")


@dp.message_handler(commands=["unblock"])
async def blockUser(message: types.Message):
    if message.from_user.id == 347821020:
        userId = int(message.text.replace("/unblock ", ""))
        functions.setStatus(userId, 'None')
        await message.answer("Пользователь разблокирован!")


@dp.message_handler(commands=["remove_from_bd"])
async def removeFromBd(message: types.Message):
    if message.from_user.id == 347821020 and message.chat.type == 'private':
        functions.setStatus(347821020, "removeFromBd")
        s = ""
        c = 1
        for u in functions.data:
            s += str(c) + ". " + u[1] + "\n"
            c += 1
        await message.reply("Введите ID людей через запятую с пробелом:\n" + s)
    else:
        await message.reply("Функция недоступна в беседе либо у Вас недостаточно прав!")
    return


@dp.message_handler(commands=['update'])
async def updateData(message: types.Message):
    global users
    if message.from_user.id == 347821020 and message.chat.type == 'private':
        users = functions.updateUsers()
        await message.answer("Updated!")
    else:
        await message.reply("Функция недоступна в беседе либо у Вас недостаточно прав!")

@dp.message_handler(text=["Рассылка для определенных людей"])
async def msgs(message: types.Message):
    if message.from_user.id == 347821020 and message.chat.type == 'private':
        await bot.send_message(347821020, "Введите ваш текст:")
        functions.setStatus(message.from_user.id, "gotMsg")
    else:
        await message.reply("Функция недоступна в беседе либо у Вас недостаточно прав!")
    return


@dp.message_handler(text=["Рассылка для всех"])
async def forAllMsg(message: types.Message):
    if message.from_user.id == 347821020 and message.chat.type == 'private':
        await bot.send_message(347821020, "Введите ваш текст:")
        functions.setStatus(message.from_user.id, "gotMsgForAll")
    else:
        await message.reply("Функция недоступна в беседе либо у Вас недостаточно прав!")
    return

@dp.message_handler(text=['Удалить вопросы'])
async def delQuestions(message: types.Message):
    if message.from_user.id == 347821020 and message.chat.type == 'private':
        questions = functions.getQuestions()
        s = ""
        for question in questions:
            s += str(question[4]) + ". " + question[0] + " :" + question[1] + "\n"
        await bot.send_message(347821020, f"Все вопросы: \n{s}\nВведите id вопросов, которые хотите удалить "
                                          f"через запятую (пример: 1, 2, 3, 4...)")
        functions.setStatus(message.from_user.id, "delQuestions")
    else:
        await message.reply("Функция недоступна в беседе либо у Вас недостаточно прав!")
    return

@dp.message_handler(commands=['ac'])
async def addCourse(message: types.Message):
    if message.from_user.id == config.ADMIN:
        functions.setStatus(config.ADMIN, 'None')
        data = message.text.replace("/ac ","")
        course = data.split(",")
        functions.addCourse(course[0], course[1])
        await message.answer(f"Курс {course[1]}: {course[0]} успешно добавлен!")
    return

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('cash'))
async def cashSent(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    donater_id = callback_query.from_user.id
    if callback_query.data.startswith('cashSent'):
        userId = callback_query.data.replace("cashSent", "")
        print(userId)
        await bot.send_message(callback_query.from_user.id, "Сколько Вы скинули?")
        functions.setBirthdayStatus(int(userId), int(donater_id), -1)
        functions.setStatus(callback_query.from_user.id, "cashSent")
    elif callback_query.data.startswith('cashWontSent'):
        userId = callback_query.data.replace("cashWontSent", "")
        await bot.send_message(callback_query.from_user.id, "Напишите пожалуйста причину, если хотите.")
        functions.setBirthdayStatus(int(userId), int(donater_id), 0)
        functions.setStatus(callback_query.from_user.id, "cashWontSent")

    asyncio.create_task(wait(120, callback_query.from_user.id))


async def wait(seconds, userId):
    await asyncio.sleep(seconds)
    status = functions.getStatus(userId)
    if status[0] == "cashWontSent" or status[0] == "cashSent":
        await bot.send_message(userId, "Истекло время для ответа")
        functions.setStatus(userId, "None")
    functions.clearBirthdayStatuses()


@dp.message_handler()
async def getMsg(msg: types.Message):
    global users
    global theText
    global chosenNum
    global gotQuestion
    functions.rollBack()
    status = functions.getStatus(msg.from_user.id)
    if status is None and msg.chat.type == 'private':
        await msg.reply("Вы должны подписаться на бота, прежде чем использовать его функции.")
        return
    if functions.userBlocked(msg.from_user.id):
        await msg.delete()
        await bot.send_message(msg.from_user.id, "Вы заблокированы на некоторое время!")
    else:
        print(status)
        if msg.text.lower() == "отмена":
            await msg.reply("Задача отменена")
            functions.setStatus(msg.from_user.id, "None")
            return
        if status[0] == 'question':
            functions.addQuestion(msg.from_user.id, msg.text)
            await bot.send_message(347821020, "Задан новый вопрос, чтобы просмотреть /questions")
            await msg.reply("Вопрос отправлен, ожидайте ответ!")
            functions.setStatus(msg.from_user.id, "None")
            return
        if msg.text == "+":
            if reactionEnabled:
                await msg.reply("Принято!")
                await bot.send_message(347821020, msg.from_user.username + " согласился!")
            return
        if msg.text.lower() == "бот" and msg.from_user.id == 347821020:
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(KeyboardButton(text="⌨️Команды"))
            keyboard.add(KeyboardButton(text="ℹ️Актуальные вопросы"))
            await msg.reply("Что Вас интересует?", reply_markup=keyboard)
            return
        if msg.text == "-":
            if reactionEnabled:
                await msg.reply("Принято!")
                await bot.send_message(347821020, msg.from_user.username + " отказался от участия!")
            return
        if status[0] == 'theName':
            name = msg.text
            try:
                functions.updateStudent(msg.from_user.id, name)
                string = msg.from_user.username + " успешно подписался на Ваши уведомления! Его ID: " + str(
                    msg.from_user.id)
                await bot.send_message(347821020, string)
                await msg.answer("Вы успешно подписались на уведомления!\n"
                                 "По желанию Вы можете указать Вашу дату рождения /birthday")
            except:
                await msg.answer("Что то пошло не так")

            functions.setStatus(msg.from_user.id, "None")
            return
        if status[0] == 'birthday':
            functions.setStatus(msg.from_user.id, "None")
            dateString = msg.text
            dateFormatter = "%d/%m/%Y"
            birthday_date = datetime.strptime(dateString, dateFormatter)
            functions.setUserBirthday(msg.from_user.id, birthday_date)
            await bot.send_message(msg.from_user.id, str(birthday_date) + "- Ваша дата рождения! Если неверно ввели - "
                                                                          "/birthday")
            return
        if msg.chat.type == 'private':
            if msg.from_user.id == 347821020:
                if status[0] == 'gotMsg':
                    theText = msg.text
                    functions.setStatus(msg.from_user.id, 'None')
                    s = ""
                    c = 1
                    for u in functions.data:
                        s += str(c) + ". " + u[1] + "\n"
                        c += 1
                    await bot.send_message(347821020, "Введите ID людей через запятую с пробелом:\n" + s)
                    functions.setStatus(msg.from_user.id, 'forNA')
                    return
                if status[0] == 'removeFromBd':
                    ids = msg.text.split(', ')
                    for id in ids:
                        await msg.reply("Пользователь " + str(
                            functions.getUser(functions.data[int(id) - 1][0])) + " удалён из подписок!")
                        await bot.send_message(functions.data[int(id) - 1][0], "Вы удалены из подписок!")
                        functions.deleteUser(functions.data[int(id) - 1][0])

                    functions.setStatus(msg.from_user.id, "None")
                    return
                if status[0] == 'forNA':
                    ids = msg.text.split(', ')
                    for id in ids:
                        await bot.send_message(functions.data[int(id) - 1][0], theText)
                    functions.setStatus(msg.from_user.id, "None")
                    return
                if status[0] == 'gotMsgForAll':
                    theText = msg.text
                    functions.setStatus(msg.from_user.id, "None")
                    for user in functions.data:
                        await bot.send_message(user[0], theText)
                    return
                if status[0] == 'questionNum':
                    functions.setStatus(msg.from_user.id, "None")
                    gotQuestion = functions.getQuestion(int(msg.text))
                    await msg.answer("Если вы хотите исправить вопрос, то /changeQuestion\n"
                                     "Если вы хотите ответить на вопрос /sendAnswer")
                    functions.setStatus(msg.from_user.id, "gotQuestionNum")
                    return
                if status[0] == 'setAnswer':
                    functions.setStatus(msg.from_user.id, "None")
                    functions.setAnswer(gotQuestion[4], msg.text)
                    await msg.reply("Ответ отправлен!")
                    await bot.send_message(gotQuestion[3],
                                           "Вы получили ответ на свой вопрос, можете просмотреть их тут "
                                           "/answers")

                    return
                if status[0] == 'setNewQuestion':
                    functions.setStatus(msg.from_user.id, "None")
                    functions.setQuestion(gotQuestion[4], msg.text)
                    await msg.reply("Вопрос изменен!")
                    await bot.send_message(gotQuestion[3], "Ваш вопрос был изменен старостой! \n"
                                                           "Для того чтобы узнать причину, обратитесь к @yeapit")
                    return
                if status[0] == 'makeInteresting':
                    functions.setStatus(msg.from_user.id, "None")
                    ids = msg.text.split(', ')
                    for id in ids:
                        functions.setInteresting(id)
                    await msg.reply("Вопросы перемещены во вкладку актуальные!")
                    return
                if status[0] == 'removeInteresting':
                    functions.setStatus(msg.from_user.id, "None")
                    ids = msg.text.split(', ')
                    for id in ids:
                        functions.removeInteresting(id)
                    await msg.reply("Вопросы удалены со вкладки актуальных!")
                    return
                if status[0] == 'delQuestions':
                    functions.setStatus(msg.from_user.id, "None")
                    ids = msg.text.split(', ')
                    for id in ids:
                        functions.deleteQuestion(id)
                    await msg.reply("Вопросы удалены!")
                    return
                if status[0] == 'Courses':
                    if msg.text.isdigit():
                        id = int(msg.text)
                        course = functions.findCourse(id)
                        if not course:
                            await msg.answer("Курс не найден!")
                        else:
                            await msg.answer(course)
                    else:
                        functions.setStatus(config.ADMIN, 'None')
                        await msg.answer("Некорректное значение!")
                    return
            if status[0] == 'cashSent':
                if msg.text.isdigit():
                    if int(msg.text) < 1000:
                        await msg.reply("Нужно скинуть как минимум 1000")
                    else:
                        functions.updateBirthdayStatus(msg.from_user.id, int(msg.text))
                        functions.setStatus(msg.from_user.id, "None")
                        await bot.send_message(347821020, f"{msg.from_user.username} отправил {msg.text}")
                        await msg.reply("Отлично, Вас больше не будут беспокоить уведомления!")
                else:
                    await msg.reply("Введите сумму либо отмените ввод нажатием на /cancel")
                return
            if status[0] == 'cashWontSent':
                await bot.send_message(347821020, f"{msg.from_user.username} не закинет, пишет: {msg.text}")
                await msg.reply("Хорошо, Вас больше не будут беспокоить уведомления :(")
                functions.setStatus(msg.from_user.id, "None")
                return

            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(KeyboardButton(text="✍️ Подписка на уведомления"))
            keyboard.add(KeyboardButton(text="❌ Отписаться от уведомлении"))
            keyboard.add(KeyboardButton(text="🙋‍♂️Задать вопрос"))
            keyboard.add(KeyboardButton(text="ℹ️Актуальные вопросы"))
            await bot.send_message(msg.from_user.id, "Привет, не пиши мне без причины! Вот доступные команды: ",
                                   reply_markup=keyboard)

    return


async def birthdayNotification():
    global users
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
        if datetime.now().hour == 18 and datetime.now().minute == 0:
            for userId, name in users.items():
                button1 = InlineKeyboardButton('Скинул', callback_data='cashSent' + str(userId))
                button2 = InlineKeyboardButton('Я не скину', callback_data='cashWontSent' + str(userId))
                kb = InlineKeyboardMarkup(resize_keyboard=True).add(button1, button2)
                if 5 >= functions.getBirthdayUsers(userId) >= 1:
                    for u in users.keys():
                        if u != userId and functions.cashSent(u, userId) is None:
                            await bot.send_message(u,
                                                   f"У {name} день рождения через несколько дней! ({(functions.getUser(userId))[3]}). "
                                                   f"В связи с этим событием открыт сбор на каспи 87760156299 (1к+)",
                                                   reply_markup=kb)
                elif functions.getBirthdayUsers(userId) == 7:
                    for u in users.keys():
                        if u != userId and functions.cashSent(u, userId) is None:
                            await bot.send_message(u,
                                                   f"У {name} день рождения через неделю ({(functions.getUser(userId))[3]}). "
                                                   f"В связи с этим событием открываю сбор на каспи 87760156299 (1к+)",
                                                   reply_markup=kb)
                elif functions.getBirthdayUsers(userId) == 30 or functions.getBirthdayUsers(userId) == 31:
                    for u in users.keys():
                        if u != userId and functions.cashSent(u, userId) is None:
                            await bot.send_message(u,
                                                   f"У {name} день рождения через месяц ({(functions.getUser(userId))[3]}). "
                                                   f"В связи с этим событием прошу Вас отложить как минимум 1к на "
                                                   f"следующий месяц!",
                                                   reply_markup=kb)
                elif functions.getBirthdayUsers(userId) == 0:
                    await bot.send_message(userId, "С днём рождения!")
            await asyncio.sleep(60)

async def on_startup(_):
    asyncio.create_task(birthdayNotification())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
