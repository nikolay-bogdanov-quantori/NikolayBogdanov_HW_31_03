from __init__ import Heroes, Motos, Stories, Battles, get_sqlalchemy_engine, get_console_error_logger_handler
from sqlalchemy.orm import sessionmaker
import argparse
import random
import logging


def add_hero(**kwargs):
    logger_hero = logging.getLogger("scripts.add_hero")
    logger_hero.addHandler(get_console_error_logger_handler())

    engine = get_sqlalchemy_engine()
    Session = sessionmaker(bind=engine)
    hero_to_add = Heroes(**kwargs)
    try:
        if kwargs["power"] <= 0:
            raise ValueError("power value must be >= 1!")

        with Session() as session:
            logger_hero.info("adding hero: name=%s, side=%s, birthdate=%s, power=%s",
                             hero_to_add.name, hero_to_add.side, hero_to_add.birthdate, hero_to_add.power)
            session.add(hero_to_add)
            session.commit()
    except Exception as ex:
        logger_hero.error(ex.args[0].replace("\n", " "))

    for handler in logger_hero.handlers:
        handler.close()
        logger_hero.removeHandler(handler)


def add_moto(**kwargs):
    logger_moto = logging.getLogger("scripts.add_moto")
    logger_moto.addHandler(get_console_error_logger_handler())

    engine = get_sqlalchemy_engine()
    Session = sessionmaker(bind=engine)
    try:
        with Session() as session:
            moto_id = session.query(Motos.id).where(Motos.hero_id == kwargs["hero_id"]).count() + 1
            moto_to_add = Motos(**kwargs, moto_id=moto_id)
            logger_moto.info("adding moto for hero_id=%s, moto_id=%s, moto=%s",
                             moto_to_add.hero_id, moto_to_add.moto_id, moto_to_add.moto)
            session.add(moto_to_add)
            session.commit()
    except Exception as ex:
        logger_moto.error(ex.args[0].replace("\n", " "))

    for handler in logger_moto.handlers:
        handler.close()
        logger_moto.removeHandler(handler)


def add_battle(**kwargs):
    def battle_log_filter(record):
        return not record.getMessage().startswith('Draw')

    logger_battle = logging.getLogger("scripts.add_battle")

    formatter = logging.Formatter("%(asctime)s - %(message)s")
    handler = logging.FileHandler(filename="logs/battle.log")
    handler.setFormatter(formatter)
    logger_battle.addHandler(handler)
    logger_battle.addFilter(battle_log_filter)

    logger_battle.info("Battle begins..")
    engine = get_sqlalchemy_engine()
    Session = sessionmaker(bind=engine)
    with Session() as session:
        all_sides = [side[0] for side in session.query(Heroes.side).distinct().all()]
        side1, side2 = random.sample(all_sides, 2)
        hero1 = random.choice(
            session.query(Heroes.id, Motos.id, Heroes.power, Heroes.name, Motos.moto).join(Heroes.motos).where(
                Heroes.side == side1).all())
        hero2 = random.choice(
            session.query(Heroes.id, Motos.id, Heroes.power, Heroes.name, Motos.moto).join(Heroes.motos).where(
                Heroes.side == side2).all())

    logger_battle.info("%s against %s", side1, side2)
    logger_battle.info("%s (power = %s) says: %s", hero1[3], hero1[2], hero1[4])
    logger_battle.info("%s (power = %s) says: %s", hero2[3], hero2[2], hero2[4])
    # вероятность победы высчитывается так:
    # случайно выбирается целое число из отрезка [1, 2, ... , power1+power2] результаты: 1 и power1+1  считаются ничьей
    # (небольшое преимушество первого иили второго героя соответственно), выпадание [2, ...,power1] - победа героя 1
    # [power1+2, ...,power2] -победа героя 2
    power1 = hero1[2]
    power2 = hero2[2]
    dices = range(1, power1 + power2 + 1)
    roll = random.choice(dices)
    if roll == 1 or roll == power1 + 1:
        outcome = 0
        logger_battle.info("Draw!")
    elif roll <= power1:
        outcome = 1
        logger_battle.info("Victory of %s", hero1[3])
    else:
        outcome = 2
        logger_battle.info("Victory of %s", hero2[3])

    logger_battle.info("Battle ends..")
    battle_to_add = {"hero_1_id": hero1[0],
                     "hero_1_moto_id": hero1[1],
                     "hero_2_id": hero2[0],
                     "hero_2_moto_id": hero2[1],
                     "winner": outcome}
    with engine.connect() as connection:
        connection.execute(Battles.insert().values(battle_to_add))

    for handler in logger_battle.handlers:
        handler.close()
        logger_battle.removeHandler(handler)


def add_story(**kwargs):
    logger_story = logging.getLogger("scripts.add_story")
    logger_story.addHandler(get_console_error_logger_handler())

    engine = get_sqlalchemy_engine()
    Session = sessionmaker(bind=engine)
    story_to_add = Stories(**kwargs)
    try:
        with Session() as session:
            logger_story.info("adding story for hero_id=%s", story_to_add.hero_id)
            session.add(story_to_add)
            session.commit()
    except Exception as ex:
        logger_story.error(ex.args[0].replace("\n", " "))

    for handler in logger_story.handlers:
        handler.close()
        logger_story.removeHandler(handler)


def del_hero(**kwargs):
    logger_del_hero = logging.getLogger("scripts.del_hero")
    logger_del_hero.addHandler(get_console_error_logger_handler())

    engine = get_sqlalchemy_engine()
    Session = sessionmaker(bind=engine)
    hero_to_del_id = kwargs["hero_id"]
    try:
        with Session() as session:
            # получение имени удаляемого героя, нужно только для вывода в лог и проверки, что герой с таким id есть в БД
            hero_name = session.query(Heroes.name).where(Heroes.id == kwargs["hero_id"]).first()
            if hero_name is None:
                logger_del_hero.warning("deleting hero: hero_id=%s, hero is not present in DB!", hero_to_del_id)
            else:
                logger_del_hero.info("deleting hero: hero_id=%s, name=%s", hero_to_del_id, hero_name)

            session.query(Heroes).filter(Heroes.id == hero_to_del_id).delete()
            session.commit()
    except Exception as ex:
        logger_del_hero.error(ex.args[0].replace("\n", " "))

    for handler in logger_del_hero.handlers:
        handler.close()
        logger_del_hero.removeHandler(handler)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(title='subcommands', metavar='command',
                                   description='valid subcommands', help='description')

add_hero_parser = subparsers.add_parser('add_hero',  help='add new hero')
add_hero_parser.add_argument('-n', dest='name', type=str, required=True, help='(str) hero name')
add_hero_parser.add_argument('-s', dest='side', type=str, required=True, help='(str) hero side')
add_hero_parser.add_argument('-b', dest='birthdate', type=str, required=False, help='(str) hero birthdate')
add_hero_parser.add_argument('-p', dest='power', type=int, required=True, help='(int) hero power value')
add_hero_parser.set_defaults(func=add_hero)
#
add_moto_parser = subparsers.add_parser('add_moto', help='add new moto for hero')
add_moto_parser.add_argument('-hid', dest='hero_id', type=int, required=True, help='(int) id of hero to which the moto is added')
add_moto_parser.add_argument('-moto', dest='moto', type=str, required=True, help='(str) text of the moto')
add_moto_parser.set_defaults(func=add_moto)
#
add_battle_parser = subparsers.add_parser('add_battle',  help='add new battle between random heroes')
add_battle_parser.set_defaults(func=add_battle)
#
add_story_parser = subparsers.add_parser('add_story',  help='add the story to a hero')
add_story_parser.add_argument('-hid', dest='hero_id', type=int, required=True, help='(int) id of hero to which the story is added')
add_story_parser.add_argument('-s', dest='story', type=str, required=True, help='(str) text of the story')
add_story_parser.set_defaults(func=add_story)
#
del_hero_parser = subparsers.add_parser('del_hero',  help='delete hero by id')
del_hero_parser.add_argument('-hid', dest='hero_id', type=int, required=True, help='(int) id of hero to delete')
del_hero_parser.set_defaults(func=del_hero)

if __name__ == '__main__':
    args = parser.parse_args()
    if not vars(args):
        parser.print_usage()
    else:
        function_to_call = args.func
        keyword_args = vars(args)
        keyword_args.pop('func', None)  # удаление ненужного keyword аргумента
        function_to_call(**keyword_args)

