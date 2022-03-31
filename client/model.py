from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey, Identity
from sqlalchemy.orm import declarative_base, relationship
TABLES_NAMES = tuple(("battles", "heroes", "motos", "stories"))

Base = declarative_base()

Battles = Table('battles', Base.metadata,
                Column('id', Integer, Identity(), primary_key=True),
                Column('hero_1_id', Integer, ForeignKey('heroes.id', ondelete="SET NULL")),
                Column('hero_1_moto_id', Integer, ForeignKey('motos.id', ondelete="SET NULL")),
                Column('hero_2_id', Integer, ForeignKey('heroes.id', ondelete="SET NULL")),
                Column('hero_2_moto_id', Integer, ForeignKey('motos.id', ondelete="SET NULL")),
                Column('winner', Integer),
                extend_existing=True
                )


class Heroes(Base):
    __tablename__ = "heroes"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    name = Column(String)
    side = Column(String)
    birthdate = Column(Date)
    power = Column(Integer)

    motos = relationship("Motos", back_populates="hero")
    opponents = relationship("Heroes", secondary=Battles,
                             primaryjoin=id == Battles.c.hero_1_id,
                             secondaryjoin=id == Battles.c.hero_2_id,
                             )
    story = relationship("Stories", back_populates="hero")


class Motos(Base):
    __tablename__ = "motos"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    hero_id = Column(Integer, ForeignKey('heroes.id', ondelete="CASCADE"))
    moto_id = Column(Integer)
    moto = Column(String)

    hero = relationship("Heroes", back_populates="motos")

    def __str__(self):
        return f"{self.id}, {self.moto}"


class Stories(Base):
    __tablename__ = "stories"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    hero_id = Column(Integer, ForeignKey('heroes.id', ondelete="CASCADE"), unique=True)  # unique чтобы на одного героя была строго одна история
    story = Column(String)

    hero = relationship("Heroes", back_populates="story")

    def __str__(self):
        return f"{self.id}, {self.moto}"