import datetime
import sys

import aiosqlite
import asyncio


number_dict = {
    "1": "one",
    "2": "two",
    "3": "three",
    "4": "four",
    "5": "five",
    "6": "six",
    "7": "seven",
    "8": "eight",
}


def process_input(input_string):
    if input_string == "ta":
        return "Teacher Advisory"
    else:
        try:
            x = number_dict[str(input_string)].title()
        except KeyError:
            x = input_string
        return "Stinger " + x


async def main():
    database = await aiosqlite.connect('./Scheduler/database.db')
    cursor = await database.cursor()
    date = datetime.datetime.now() + datetime.timedelta(days=1)
    days = (date - datetime.datetime(2021, 9, 1)).days
    while True:
        first_half = input(f"What is the first half of the stinger's name? [{date}] : ")
        if first_half in ["skip", "s"]:
            days += 2
            date += datetime.timedelta(days=2)
            continue
        elif first_half in ["quit", "q", "exit", "e", "x"]:
            break
        first_half = process_input(first_half)
        second_half = process_input(input(f"What is the second half of the stinger's name? [{date}] : "))
        await cursor.execute("INSERT INTO stingers_first_half VALUES (?, ?)", (days, first_half))
        await cursor.execute(f"INSERT INTO stingers_second_half VALUES (?, ?)", (days, second_half))
        days += 2
        date += datetime.timedelta(days=2)
        await database.commit()
        print("added")
    await database.close()


async def add_columns_to_database():
    database = await aiosqlite.connect('./Scheduler/database.db')
    cursor = await database.cursor()
    await cursor.execute(
        "CREATE TABLE stingers_first_half (days integer, stinger text)")
    await cursor.execute(
        "CREATE TABLE stingers_second_half (days integer, stinger text)")
    await database.commit()
    await database.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
