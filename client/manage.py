from __init__ import Base, Heroes, Motos, Stories, Battles, get_sqlalchemy_engine
from sqlalchemy.orm import sessionmaker
import argparse
import logging
import psycopg2
import os


def create_and_fill_db_if_not_exists():
    logger_create_db_if_not_exists = logging.getLogger("manage.create_db_if_not_exists")
    try:
        logger_create_db_if_not_exists.info("checking if DB exists")
        psycopg2.connect(os.getenv("DATABASE_URL"))
    except:
        logger_create_db_if_not_exists.info("DB not found, trying to create")
        create_db()
        fill_db()
    else:
        logger_create_db_if_not_exists.info("Connected to existing DB")


def create_db():
    logger_create_db = logging.getLogger("manage.create_db")
    logger_create_db.info("creating DB")
    engine = get_sqlalchemy_engine()
    Base.metadata.create_all(engine)
    logger_create_db.info("DB was created")


def fill_db():
    logger_fill_db = logging.getLogger("manage.fill_db")
    logger_fill_db.info("adding predefined data to tables")
    engine = get_sqlalchemy_engine()
    heroes = [
        Heroes(name="Abaddon the Despoiler", side="Chaos", birthdate=None, power=9),
        Heroes(name="Lucius the Eternal", side="Chaos", birthdate=None, power=7),
        Heroes(name="Kharn the Betrayer", side="Chaos", birthdate=None, power=7),
        Heroes(name="Ahzek Ahriman", side="Chaos", birthdate=None, power=5),
        Heroes(name="Constantin Valdor", side="Imperium of Man", birthdate=None, power=9),
        Heroes(name="Bjorn the Fell-Handed", side="Imperium of Man", birthdate=None, power=7),
        Heroes(name="Nathaniel Garro", side="Imperium of Man", birthdate=None, power=6),
        Heroes(name="Sigismund", side="Imperium of Man", birthdate=None, power=8)
    ]
    motos = [
        Motos(hero_id=1, moto="I am the Arch-fiend, the Despoiler of Worlds, and by my hands shall the false Emperor fall."),
        Motos(hero_id=1, moto="Horus was weak. Horus was a fool. He had the whole galaxy within his grasp and he let it slip away."),
        Motos(hero_id=2, moto="Brothers! Welcome to the feast! Tell me, which among you will be the first course?"),
        Motos(hero_id=3, moto="Kill! Maim! Burn! Kill! Maim! Burn! Kill! Maim! Burn! Kill! Maim! Burn! Kill! Maim! Burn! Kill! Maim! Burn! Kill! Maim! Burn!."),
        Motos(hero_id=4, moto="Please forgive me the horror we both know you will make me put you through."),
        Motos(hero_id=4, moto="The only good is knowledge and the only evil is ignorance."),
        Motos(hero_id=4, moto="If the path to salvation leads through the halls of purgatory, then so be it."),
        Motos(hero_id=5, moto="There are no bystanders in the war of life and death, no place the battle cannot reach; so fight it without remorse or relenting, for death will surely do the same."),
        Motos(hero_id=6, moto="God-Emperor? Calling him a god was how all this mess started."),
        Motos(hero_id=6, moto="There's no turning back... Triumph or oblivion."),
        Motos(hero_id=7, moto="My name is Nathaniel Garro, and I am a Legion of One."),
        Motos(hero_id=8, moto="Nothing worthwhile is done without challenge, best to overcome it before plans are enacted."),
        Motos(hero_id=8, moto="Zeal makes all things possible, duty makes all things simple.")
    ]

    battles = [
        {"hero_1_id": 1, "hero_1_moto_id": 1, "hero_2_id": 8, "hero_2_moto_id": 12, "winner": 1},
        {"hero_1_id": 2, "hero_1_moto_id": 3, "hero_2_id": 6, "hero_2_moto_id": 9, "winner": 0}
    ]

    stories = [
        Stories(
            hero_id=1,
            story=
            """Abaddon is now infamous for leading Black Crusades, the terrible military campaigns during which the normally fractious forces of Chaos unite under his leadership and launch a massive attack against the Imperium from within the Eye of Terror. The most recent of these attacks, the 13th Black Crusade in 999.M41, led to the fall of the vital Imperial Fortress World of Cadia, the birth of the Great Rift that divided the galaxy in half and the start of the Noctis Aeterna and the Era Indomitus. The name of Abaddon, the Warmaster of Chaos, has become a bitter curse within the Imperium. During the Great Crusade, Abaddon rose to become Captain of the 1st Company of what was then called the Luna Wolves Legion. When the Horus Heresy came to a head, it was clear that Abaddon's loyalty lay with his primarch."""
        ),
        Stories(
            hero_id=2,
            story=
            """Many millennia ago, Lucius was a proud Space Marine of the Emperor's Children Legion, following his Primarch, Fulgrim, across the galaxy in the name of the Emperor. Forsaking all experience other than the art of close combat with the sword, Lucius bore the scars of battle with pride and, over time, he began to equate pain with success. By the time the Emperor's Children had been seduced by Horus' rebellion, Lucius had cut deep lines across his face, head and chest, linking his scars in a maze of irregular patterns that distorted and deformed his features. Lucius slowly descended into madness. He was compelled by the whispers in his mind to commit ever more extreme acts, furthering an intense obsession with being the perfect swordsman."""
        ),
        Stories(
            hero_id=3,
            story=
            """For all his qualities as a warrior, Kharn was neither patient nor particularly subtle, nor a great orator, and, instead of guiding and tempering his primarch's words and decisions with wisdom, he often was second into the thickest of the fray right behind Angron, slaying anything which had escaped Angron's twin chainaxes. Any words of tempering he might have uttered were quickly forgotten in the rush of battle. In the shadow of Angron, Kharn began to change, becoming more aggressive and unstable, reckless traits he had long kept in check rising to the surface. Angron's use of the Butcher's Nails, cybernetic skull implants designed to heighten aggression, only accelerated Kharn's descent into madness."""
        ),
        Stories(
            hero_id=4,
            story=
            """Before the Horus Heresy began, Ahriman had risen to the powerful position of Chief Librarian of the Thousand Sons Legion, the captain of its 1st Fellowship and the leader of the Sekhmet or Scarab Occult who served as the elite Veterans of the Legion and deployed in Terminator Armour. Ahriman was also one of the leaders of the Thousand Sons' most powerful sorcerous cult, the Corvidae, who were skilled in the psychic discipline of precognition, which was the ability to determine the likely probabilities of future events. They served as the Legion's seers, warning their battle-brothers of dangers before they materialised. The Corvidae Cult also helped guide the Thousand Sons Legion along the lines of Fate during times of conflict and in pursuit of their overall psychic and material growth as a Legion, as well as serving as the Legion's primary strategic planners. Ahriman had come to share his primarch's obsession with the pursuit and preservation of arcane knowledge and the unraveling of the mysteries of the Warp."""
        ),
        Stories(
            hero_id=5,
            story=
            """Constantin Valdor, known as "The First of the Ten Thousand" and "The Shield of the Emperor," was the first Chief Custodian and Captain-General of the ancient Legio Custodes, the elite bodyguard of the Emperor of Mankind. Under Valdor's peerless leadership during the Wars of Unification to reunite Terra and the subsequent Great Crusade launched to reclaim the lost colony worlds of Humanity, the Legio Custodes was an unstoppable force, and its warriors covered themselves in glory for Terran years uncounted."""
        ),
        Stories(
            hero_id=6,
            story=
            """Bjorn the Fell-Handed, also known as "the Eldest," "Trueclaw," "Revered One," and "Last from the Company of Russ," is a Venerable Mars Pattern Mark V Dreadnought and former Great Wolf of the Space Wolves Chapter. He is also the oldest living Space Marine in the Imperium of Man, for in his mortal life he fought beside the Emperor and his Primarch Leman Russ during the Great Crusade and the bitter wars of the Horus Heresy.More than ten thousand Terran years have passed since that age of legends, yet Bjorn remains a living link to the Chapter's distant past -- it is little wonder that his counsel is sought by many within the Space Wolves when they gird for war. Despite his extreme age, Bjorn is a steadfast warrior and lumbers into battle entombed within the sacred sarcophagus of his Dreadnought. A venerable hero of immense power, Bjorn has masterminded many of the Space Wolves' greatest victories, and by his hand have some of the Imperium's most heinous adversaries been slain. Always eager to crush the foes of the Allfather, Bjorn continues to fight amongst his Chapter's ranks as he has done for millennia."""
        ),
        Stories(
            hero_id=7,
            story=
            """Nathaniel Garro was originally the battle-captain of the Death Guard Legion's 7th Great Company and later became the leader or Agentia Primus of a band of Space Marines gathered from all the Legions known as the Knights-Errant who remained loyal to the Emperor of Mankind and were directed on missions chosen by Malcador the Sigillite, the Regent of Terra. Kyril Sindermann would later claim that Garro became the first true martyr of the Church of the God-Emperor. Garro was also the leader of "The Seventy," the 70 surviving Loyalist Astartes who alone of the Death Guard Legion escaped the massacre of Loyalists at Isstvan III aboard the frigate Eisenstein to bring word of the Warmaster Horus' betrayal of the Emperor to Terra. Garro held to the original tenets of his Legion when many of his battle-brothers chose to follow Horus, their traitorous Primarch Mortarion, and First Captain Calas Typhon's decision to serve Chaos and overthrow the Emperor, installing Horus as the new emperor to rule over the Imperium of Man."""
        ),
        Stories(
            hero_id=8,
            story=
            """Sigismund was the first captain of the Imperial Fists Legion during the Great Crusade and the Horus Heresy eras. Sigismund was a name that echoed through the Great Crusade even before the darkness of the Horus Heresy made him the stuff of legends. Born on Terra and raised to the Legiones Astartes as the Great Crusade was at its height, he ascended in rank and renown thanks to a simple fact: he was a warrior of unparalleled lethality and ability. Beneath the primarchs there has perhaps never been a more skilled warrior in combat. Across the battlefields of hundreds of worlds and the duelling floors of every Legion he was never defeated except on one occasion, and only through treachery, when he received a headbutt to the face from the Night Lords' infamous First Captain Jago Sevatarion."""
        )
    ]
    Session = sessionmaker(bind=engine)
    with Session() as session:
        for hero in heroes:
            session.add(hero)
        session.commit()

    with Session() as session:
        for moto in motos:
            moto.moto_id = session.query(Motos.id).where(Motos.hero_id == moto.hero_id).count() + 1
            session.add(moto)
        session.commit()

    with Session() as session:
        for story in stories:
            session.add(story)
        session.commit()

    with engine.connect() as connection:
        result = connection.execute(Battles.insert().values(battles))

    logger_fill_db.info("data was added")


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(title='subcommands', metavar='command',
                                   description='valid subcommands', help='description')
#
db_check_parser = subparsers.add_parser('check_and_fill',
                                        help='checks if DB exists, if not, creates it and fills with predefined data')
db_check_parser.set_defaults(func=create_and_fill_db_if_not_exists)

create_parser = subparsers.add_parser('create_db',  help='create new db')
create_parser.set_defaults(func=create_db)
#
fill_parser = subparsers.add_parser('fill_db',  help='fill existing DB with predefined data')
fill_parser.set_defaults(func=fill_db)


if __name__ == '__main__':
    args = parser.parse_args()
    if not vars(args):
        parser.print_usage()
    else:
        args.func()
