from sqlalchemy import (Column, DateTime, ForeignKey, Index, Integer, String,
                        create_engine, func)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()


class Player(Base):
    """
    Модель игрока.

    Атрибуты:
        id (int): Уникальный идентификатор игрока.
        username (str): Имя пользователя игрока.
        first_login (datetime): Дата и время первого входа.
        points (int): Количество очков игрока.
        boosts (relationship): Список бустов, связанных с игроком.
    """

    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False, index=True)
    first_login = Column(DateTime, nullable=False, default=func.now())
    points = Column(Integer, default=0)

    boosts = relationship(
        'PlayerBoost', back_populates='player', lazy='dynamic')

    def add_points(self, amount):
        """
        Добавляет очки игроку.

        Аргументы:
            amount (int): Количество очков для добавления.
        """
        if amount > 0:
            self.points += amount

    def add_boost(self, boost, level=1):
        """
        Добавляет буст игроку, если у него еще нет этого буста.

        Аргументы:
            boost (Boost): Объект буста для добавления.
            level (int, optional): Уровень буста. По умолчанию 1.
        """
        if not self.boosts.filter_by(boost_id=boost.id).first():
            player_boost = PlayerBoost(
                player_id=self.id, boost_id=boost.id, level=level)
            self.boosts.append(player_boost)


class Boost(Base):
    """
    Модель буста.

    Атрибуты:
        id (int): Уникальный идентификатор буста.
        name (str): Имя буста.
        description (str): Описание буста.
        boost_type (str): Тип буста.
        players (relationship): Список игроков, связанных с бустом.
    """

    __tablename__ = 'boosts'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String)
    boost_type = Column(String)

    players = relationship(
        'PlayerBoost', back_populates='boost', lazy='dynamic')


class PlayerBoost(Base):
    """
    Связывающая модель для отношений многие ко многим между Player и Boost.

    Атрибуты:
        id (int): Уникальный идентификатор записи.
        player_id (int): Идентификатор игрока.
        boost_id (int): Идентификатор буста.
        level (int): Уровень буста.
        player (relationship): Связанный игрок.
        boost (relationship): Связанный буст.
    """

    __tablename__ = 'player_boosts'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    boost_id = Column(Integer, ForeignKey('boosts.id'))
    level = Column(Integer, default=1)

    player = relationship('Player', back_populates='boosts')
    boost = relationship('Boost', back_populates='players')

    __table_args__ = (
        Index('ix_player_boost', 'player_id', 'boost_id', unique=True),
    )


# Создание движка и сессии
engine = create_engine('sqlite:///:memory:', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

# Создание таблиц в базе данных
Base.metadata.create_all(engine)

# Пример использования
new_player = Player(username="player1")
new_boost = Boost(
    name="Speed Boost", description="Increases speed by 20%",
    boost_type="Speed")

# Добавление объектов в сессию
session.add(new_player)
session.add(new_boost)
session.commit()

# Проверка данных перед добавлением буста
print(f"До добавления буста: {new_player.boosts.count()} бустов у игрока")

# Добавление буста и проверка
new_player.add_boost(new_boost, level=2)
session.commit()

print(f"После добавления буста: {new_player.boosts.count()} бустов у игрока")
for player_boost in new_player.boosts:
    print(f"Буст: {player_boost.boost.name}, Уровень: {player_boost.level}")

# Начисление очков за вход и проверка
new_player.add_points(10)
session.commit()

player_from_db = session.query(Player).filter_by(username="player1").first()
print(f"Игрок {player_from_db.username} имеет {player_from_db.points} очков")
