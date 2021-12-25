#!/usr/bin/env python
# -*- coding: utf-8 -*-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

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

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет, список доступных команд /commands\n"
                         "Подписка на бота /subscribe\n"
                         "Чтобы отменить любое действие, напишите 'отмена' либо /cancel")
    return


@dp.message_handler(commands=['update'])
async def updateData(message: types.Message):
    global users
    if message.from_user.id == 347821020:
        users = functions.updateUsers()

    await message.answer("Updated!")


@dp.message_handler(commands=['question'])
async def question(message: types.Message):
    functions.setStatus(message.from_user.id, "question")
    await message.answer("Напишите Ваш вопрос либо отмените свое действие /cancel")
    return


@dp.message_handler(commands=['questions', 'Заданные_вопросы'])
async def questions(message: types.Message):
    if message.from_user.id == 347821020:
        await message.answer("Вопросы без ответа /notAnswered\n"
                             "Все вопросы /allQuestions")
    return


@dp.message_handler(commands=['makeInteresting', 'Поместить_в_актуальные'])
async def makeInteresting(message: types.Message):
    if message.from_user.id == 347821020:
        questions = functions.getAnswered()
        s = "Отвеченные вопросы:\n "
        for question in questions:
            s+=str(question[4]) + ". " + question[0] + "\n"

        await message.answer(s)
        await message.answer("Введите id вопросов, которые хотите поместить в актуальные через запятую. Например (1, 2, 3..)")
        functions.setStatus(message.from_user.id, "makeInteresting")
    return


@dp.message_handler(commands=['removeInteresting', 'Удалить_из_актуальных'])
async def removeInteresting(message: types.Message):
    if message.from_user.id == 347821020:
        questions = functions.getInteresting()
        s = "Актуальные вопросы:\n"
        for question in questions:
            s += str(question[4]) + ". " + question[0] + "\n"

        await message.answer(s)
        await message.answer(
            "Введите id вопросов, которые хотите удалить их актуальных через запятую. Например (1, 2, 3..)")
        functions.setStatus(message.from_user.id, "removeInteresting")
    return

@dp.message_handler(commands=['notAnswered'])
async def notAnswered(message: types.Message):
    if message.from_user.id == 347821020:
        questions = functions.getNotAnswered()
        await message.answer("Введите id вопроса чтобы ответить, либо /cancel")
        s = ""
        for question in questions:
            s+=str(question[4])+". "+question[0] + "\n"
        await message.answer(s)
        functions.setStatus(message.from_user.id, "questionNum")
    return


@dp.message_handler(commands=['allQuestions'])
async def allQuestions(message: types.Message):
    if message.from_user.id == 347821020:
        questions = functions.getQuestions()
        await message.answer("Введите id вопроса чтобы изменить, либо /cancel")
        s = ""
        for question in questions:
            s+=str(question[4])+". "+question[0] + " :"+ question[1] +"\n"
        await message.answer(s)
        functions.setStatus(message.from_user.id, "questionNum")
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


@dp.message_handler(commands=['answers'])
async def answers(message: types.Message):
    await message.answer("Актуальные вопросы - /interesting\n"
                   "Ваши вопросы - /myQuestions")
    return

@dp.message_handler(commands=["interesting"])
async def actualQuestions(message: types.Message):
    questions = functions.getInteresting()
    s = "АКТУАЛЬНЫЕ ВОПРОСЫ:\n"
    for question in questions:
        s+= "---------------------------\n"\
            "Вопрос номер "+str(question[4])+":\n" \
            "Вопрос: " + question[0] + "\n" \
            "Ответ: " + question[1] +"\n" \

    await message.answer(s)
    return

@dp.message_handler(commands=['myQuestions'])
async def myQuestions(message: types.Message):
    questions = functions.getMyQuestions(message.from_user.id)

    s = "МОИ ВОПРОСЫ:\n"
    for question in questions:
        s+="--------------------------------\n"\
           "Вопрос номер "+str(question[4])+":\n" \
            "Вопрос: " + question[0] + "\n" \
            "Ответ: " + question[1] +"\n" \

    await message.answer(s)
    return

@dp.message_handler(commands=['commands'])
async def help(message: types.Message):
    s = "Подписаться на уведомления - /subscribe\n" \
        "Отписаться от уведомлении - /unsubscribe\n" \
        "Задать вопрос - /question\n" \
        "Актуальные вопросы - /answers\n" \
        "Оставить запрос на аноним - /request\n" \
        "Ответить на сообщения анонимного пользователя - '/sa your message'\n" \
        "Написать сообщение от имени анонимного пользователя - /msg_to_user\n" \
        "Закончить сессию анонимного пользователя - /end_session"

    await message.answer(s)
    return


@dp.message_handler(commands=['subscribe'])
async def func(message: types.Message):
    user = functions.getUser(message.from_user.id)
    if user is None:
        functions.addStudent(message.from_user.id, message.from_user.username, "None")
        await message.answer("Напишите свое имя на английском языке(Example: Sugurov Khamza)")
        functions.setStatus(message.from_user.id, "theName")
    else:
        await message.answer("Вы уже подписаны! Чтобы отписаться нажмите /unsubscribe")
    return


@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    user = functions.getUser(message.from_user.id)
    if user is not None:
        functions.deleteStudent(message.from_user.id)
        await message.answer("Вы успешно отписались от уведомлений!")
        await bot.send_message(347821020, message.from_user.username + " отписался от уведомлении!")
    else:
        await message.answer("Вы не подписаны! Чтобы подписаться нажмите /subscribe")
    return


@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    if message.from_user.id == 347821020:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(KeyboardButton(text="Рассылка для всех"))
        keyboard.add(KeyboardButton(text="Рассылка для определенных людей"))
        keyboard.add(KeyboardButton(text="/Заданные_вопросы"))
        keyboard.add(KeyboardButton(text="/Поместить_в_актуальные"))
        keyboard.add(KeyboardButton(text="/Удалить_из_актуальных"))
        await message.answer("Привет, Хамзеке, вот доступные функции", reply_markup=keyboard)
    return


@dp.message_handler(text=["Рассылка для определенных людей"])
async def msgs(message: types.Message):
    if message.from_user.id == 347821020:
        await bot.send_message(347821020, "Введите ваш текст:")
        functions.setStatus(message.from_user.id, "gotMsg")
        return


@dp.message_handler(text=["Рассылка для всех"])
async def forAllMsg(message: types.Message):
    if message.from_user.id == 347821020:
        await bot.send_message(347821020, "Введите ваш текст:")
        functions.setStatus(message.from_user.id, "gotMsgForAll")
        return


@dp.message_handler(commands=["msg_to_user"])
async def msgToUser(message: types.Message):
    u = functions.getAnon()
    if u is not None:
        if message.from_user.id == u[0]:
            await message.answer("Введите ваш текст:")
            functions.setStatus(message.from_user.id, "gotMsgFromUser")
            return

    await message.answer("У вас нет доступа! Запросите доступ по команде /request")
    return


@dp.message_handler(commands=["request"])
async def request(message: types.Message):
    await bot.send_message(347821020, "Пользователь " + message.from_user.username + " просит анонимность! Чтобы "
                                                                                     "разрешить, отправь текст ниже!")
    await bot.send_message(347821020, "/make_anon " + str(message.from_user.id))

    u = functions.getAnon()
    if u is not None:
        await message.answer("На данный момент другой пользователь пользуется анонимкой, прошу подождать!")
        await bot.send_message(347821020, "На данный момент другой пользователь пользуется анонимкой, прошу подождать!")
    return


@dp.message_handler(commands=["end_session"])
async def endSession(message: types.Message):
    u = functions.getAnon()
    if u is not None:
        if message.from_user.id == u[0] or message.from_user.id == 347821020:
            functions.removeAnon()
            await bot.send_message(u[0], "Ваша сессия закончена!")
            await bot.send_message(347821020, "Пользователь " + str(u[0]) + " закончил сессию!")
        else:
            await message.answer("Вы не анонимный пользователь!")
    else:
        await message.answer("Анонимного пользователя нет!")
    return


@dp.message_handler(commands=["sa"])
async def msgToAnonim(message: types.Message):
    msg = message.text.replace("/sa ", "").strip()
    msg = message.from_user.username + ": " + msg
    u = functions.getAnon()
    if u is not None:
        if u[0] == message.from_user.id:
            await message.answer("Вы не можете отправлять сообщения самому себе!")
            return
        await bot.send_message(u[0], msg)
        await message.reply("Письмо анонимному пользователю отправлено!")
        await bot.send_message(347821020, "Пользователь " + msg)
        return
    await message.answer("Анонимный пользователь не назначен! ")
    return


@dp.message_handler(commands=["make_anon"])
async def makeAnon(message: types.Message):
    if message.from_user.id == 347821020:
        msg = message.text.replace("/make_anon ", '').strip()
        try:
            functions.setAnon(msg)
            await bot.send_message(msg, "Теперь вы можете писать от имени бота анонимно по команде /msg_to_user")
            await message.answer("Анонимный юзер установлен")
        except:
            await message.answer("Неправильный ID")
    return


@dp.message_handler(commands=["cancel"])
async def cancel(message: types.Message):
    functions.setStatus(message.from_user.id, "None")
    await message.reply("Задача отменена")
    return


@dp.message_handler()
async def getMsg(msg: types.Message):
    global users
    global theText
    global chosenNum
    global gotQuestion
    functions.rollBack()
    u = functions.getAnon()
    status = functions.getStatus(msg.from_user.id)
    print(status)
    if u is not None:
        if msg.from_user.id == u[0]:
            if status[0] == 'gotMsgFromUser':
                theText = msg.text
                theText = "Аноним: " + theText
                s = ""
                c = 1
                functions.setStatus(msg.from_user.id,'None')
                for u in functions.data:
                    s += str(c) + ". " + u[1] + "\n"
                    c += 1
                await msg.answer("Введи ID человека:\n" + s)
                functions.setStatus(msg.from_user.id,'forNAFromUser')
                return
            if status[0] == 'forNAFromUser':
                id = msg.text
                await bot.send_message(functions.data[int(id) - 1][0], theText)
                await bot.send_message(functions.data[int(id) - 1][0], "Чтобы ответить, наберите '/sa ваш ответ'")
                await bot.send_message(347821020, "(" + msg.from_user.username + ")" + theText)
                await msg.answer("Сообщение отправлено!")
                functions.setStatus(msg.from_user.id,'None')
                return
    if msg.text.lower() == "отмена":
        await msg.reply("Задача отменена")
        functions.setStatus(msg.from_user.id, "None")
        return
    if msg.from_user.id == 347821020:
        if status[0] == 'gotMsg':
            theText = msg.text
            functions.setStatus(msg.from_user.id,'None')
            s = ""
            c = 1
            for u in functions.data:
                s += str(c) + ". " + u[1] + "\n"
                c += 1
            await bot.send_message(347821020, "Введите ID людей через запятую с пробелом:\n" + s)
            functions.setStatus(msg.from_user.id, 'forNA')
            return
        if status[0] == 'forNA':
            ids = msg.text.split(', ')
            for id in ids:
                await bot.send_message(functions.data[int(id) - 1][0], theText)
                # await bot.send_message(functions.data[int(id) - 1][0], "Напиши мне '+', чтобы я знал что ты в курсе,"
                #                                             "но помни что отговорки по типу 'Я не читал' - не "
                #                                             "действительны!")
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
            await bot.send_message(gotQuestion[3], "Вы получили ответ на свой вопрос, можете просмотреть их тут "
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


    if status[0] == 'theName':
        name = msg.text
        try:
            functions.updateStudent(msg.from_user.id, name)
            string = msg.from_user.username + " успешно подписался на Ваши уведомления! Его ID: " + str(
                msg.from_user.id)
            await bot.send_message(347821020, string)
            await msg.answer("Вы успешно подписались на уведомления!")
        except:
            await msg.answer("Что то пошло не так")

        functions.setStatus(msg.from_user.id, "None")
        return
    if status[0] == 'question':
        functions.addQuestion(msg.from_user.id, msg.text)
        await bot.send_message(347821020, "Задан новый вопрос, чтобы просмотреть /questions")
        await msg.reply("Вопрос отправлен, ожидайте ответ!")
        functions.setStatus(msg.from_user.id, "None")
        return


    if msg.text == "+":
        await bot.send_message(347821020, msg.from_user.username + " в курсе последнего события!")
        return

    if msg.text == "-":
        await msg.reply("Принято!")
        await bot.send_message(347821020, msg.from_user.username + " отказался от участия!")
        return

    await bot.send_message(msg.from_user.id, "Привет, не пиши мне без причины! Вот доступные команды - /commands")
    return


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
