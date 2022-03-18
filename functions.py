#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

import psycopg2

import config

connection = psycopg2.connect(config.URL)
cursor = connection.cursor()

data = []
users = {}

def getMainMenu():
    s = "Подписаться на уведомления - /subscribe\n" \
        "Отписаться от уведомлении - /unsubscribe\n" \
        "Задать вопрос - /question\n" \
        "Актуальные вопросы - /answers"
    return s


def updateUsers():
    global data
    global users
    sql = "SELECT id, name FROM public.students;"
    cursor.execute(sql)
    data = cursor.fetchall()
    for id in data:
        users[id[0]] = id[1]
    return users


def rollBack():
    cursor.execute("ROLLBACK")


def getStatus(id):
    sql = "SELECT status FROM public.students where id = " + str(id)
    cursor = connection.cursor()
    cursor.execute(sql)
    status = cursor.fetchone()
    return status


def setStatus(id, status):
    sql = f"UPDATE public.students SET status='{status}' WHERE id={id};"
    cursor.execute(sql)
    connection.commit()


def getUser(id):
    sql = "SELECT id, username, name, birthday FROM public.students where id = " + str(id)
    cursor = connection.cursor()
    cursor.execute(sql)
    user = cursor.fetchone()
    return user


def deleteStudent(id):
    new_sql = "DELETE FROM public.students WHERE id = " + str(id) + ";"
    cursor.execute(new_sql)
    connection.commit()


def addStudent(id, username, name):
    new_sql = "INSERT INTO public.students(id, username, name) VALUES (" + str(id) + ", " \
                                                                                     "'" + username + "', '" + name + "');"
    cursor.execute(new_sql)
    connection.commit()


def updateStudent(id, name):
    new_sql = f"UPDATE public.students SET name='{name}' WHERE id={id};"
    cursor.execute(new_sql)
    connection.commit()



def addQuestion(id, question):
    new_sql = f"INSERT INTO public.questions(question, answer, answered, user_id) VALUES ('{question}','None', {False}, {id});"
    cursor.execute(new_sql)
    connection.commit()


def getNotAnswered():
    new_sql = "SELECT question, answer, answered, user_id, question_id FROM public.questions where answered = 'False'"
    cursor.execute(new_sql)
    questions = cursor.fetchall()
    return questions

def getAnswered():
    new_sql = "SELECT question, answer, answered, user_id, question_id FROM public.questions where answered = 'True'"
    cursor.execute(new_sql)
    questions = cursor.fetchall()
    return questions


def getInteresting():
    new_sql = "SELECT question, answer, answered, user_id, question_id FROM public.questions where interesting=True"
    cursor.execute(new_sql)
    questions = cursor.fetchall()
    return questions

def getMyQuestions(id):
    new_sql = f"SELECT question, answer, answered, user_id, question_id FROM public.questions where user_id={id}"
    cursor.execute(new_sql)
    questions = cursor.fetchall()
    return questions

def getQuestions():
    new_sql = "SELECT question, answer, answered, user_id, question_id FROM public.questions"
    cursor.execute(new_sql)
    questions = cursor.fetchall()
    return questions


def getQuestion(id):
    new_sql = f"SELECT question, answer, answered, user_id, question_id FROM public.questions where question_id = {id}"
    cursor.execute(new_sql)
    question = cursor.fetchone()
    return question


def setAnswer(question_id, answer):
    sql = f"UPDATE public.questions SET answer='{answer}', answered={True} WHERE question_id={question_id};"
    cursor.execute(sql)
    connection.commit()


def setQuestion(question_id, question):
    sql = f"UPDATE public.questions	SET question='{question}' WHERE question_id={question_id};"
    cursor.execute(sql)
    connection.commit()

def setInteresting(question_id):
    sql = f"UPDATE public.questions SET interesting={True} WHERE question_id = {question_id};"
    cursor.execute(sql)
    connection.commit()

def removeInteresting(question_id):
    sql = f"UPDATE public.questions SET interesting={False} WHERE question_id = {question_id};"
    cursor.execute(sql)
    connection.commit()

def deleteUser(user_id):
    sql = f"DELETE FROM public.students	WHERE id={user_id}"
    cursor.execute(sql)
    connection.commit()


def setUserBirthday(user_id, date):
    sql = f"UPDATE public.students SET birthday='{date}' WHERE id={user_id};"
    cursor.execute(sql)
    connection.commit()


def getBirthdayUsers(id):
    today = datetime.date.today()
    user = getUser(id)
    newDate = datetime.date(today.year, user[3].month, user[3].day)
    print((newDate-today).days)
    return (newDate-today).days

def userBlocked(id):
    if getStatus(id) is None:
        return False
    if getStatus(id)[0] == "Blocked":
        return True
    return False

def setBirthdayStatus(userId, donaterId, sum):
    sql = f"INSERT INTO public.birthdaytable(student_id, donater_id, donat_sum)VALUES ({userId}, {donaterId}, {sum});"
    cursor.execute(sql)
    connection.commit()

def updateBirthdayStatus(donaterId, sum):
    sql = f"UPDATE public.birthdaytable SET donat_sum={sum} WHERE donater_id={donaterId};"
    cursor.execute(sql)
    connection.commit()

def clearBirthdayStatuses():
    sql = "DELETE FROM public.birthdaytable	WHERE donat_sum=-1"
    cursor.execute(sql)
    connection.commit()

def cashSent(donaterId, userId):
    sql = f"SELECT * FROM public.birthdaytable where donater_id={donaterId} and student_id={userId}"
    cursor.execute(sql)
    return cursor.fetchone()