import csv
from datetime import date

from django.db import transaction
from django.db.models import Prefetch

from .models import LevelPrize, PlayerLevel


def assign_prize_to_player(player_id, level_id, prize_id):
    """
    Присваивает игроку приз за прохождение уровня.

    Аргументы:
        player_id (int): Идентификатор игрока.
        level_id (int): Идентификатор уровня.
        prize_id (int): Идентификатор приза.
    """
    try:
        with transaction.atomic():
            # Получаем объект PlayerLevel
            player_level = PlayerLevel.objects.get(
                player_id=player_id, level_id=level_id)

            if player_level.is_completed:
                # Проверяем, если игрок уже получил приз за этот уровень
                level_prize, created = LevelPrize.objects.get_or_create(
                    level_id=level_id,
                    prize_id=prize_id,
                    defaults={'received': date.today()}
                )

                if not created:
                    print(f"Приз уже был присвоен за этот уровень.")
                else:
                    print(
                        f"Приз {level_prize.prize.title} "
                        f"присвоен игроку за "
                        f"уровень {player_level.level.title}.")
            else:
                print(f"Уровень еще не пройден.")
    except PlayerLevel.DoesNotExist:
        print("Игрок или уровень не найдены.")


def export_player_data_to_csv(file_path):
    """
    Экспортирует данные игрока в CSV-файл. Включает ID игрока, название уровня,
    статус прохождения уровня, и полученный приз за уровень.

    Аргументы:
        file_path (str): Путь к файлу для сохранения CSV.
    """
    # Используем Prefetch для оптимизации запросов к связанным моделям
    player_levels = PlayerLevel.objects.prefetch_related(
        Prefetch('level'),
        Prefetch('player'),
        Prefetch(
            'level__levelprize_set',
            queryset=LevelPrize.objects.select_related('prize'))
    ).iterator()

    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            ['Player ID', 'Level Title', 'Level Completed', 'Prize Title'])

        for player_level in player_levels:
            prize = player_level.level.levelprize_set.first()
            prize_title = prize.prize.title if prize else 'No prize'
            writer.writerow(
                [
                    player_level.player.player_id,
                    player_level.level.title,
                    player_level.is_completed,
                    prize_title
                ])
