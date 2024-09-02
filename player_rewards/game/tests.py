import csv
import os
from datetime import date

from django.test import TestCase

from .models import Level, LevelPrize, Player, PlayerLevel, Prize
from .utils import assign_prize_to_player, export_player_data_to_csv


class PlayerPrizeTestCase(TestCase):
    def setUp(self):
        self.player = Player.objects.create(player_id="player_1")
        self.level = Level.objects.create(title="Level 1", order=1)
        self.level_2 = Level.objects.create(title="Level 2", order=2)
        self.prize = Prize.objects.create(title="Golden Trophy")
        self.prize_2 = Prize.objects.create(title="Silver Trophy")

        self.player_level = PlayerLevel.objects.create(
            player=self.player,
            level=self.level,
            completed=date.today(),
            is_completed=True,
            score=100
        )
        self.player_level_2 = PlayerLevel.objects.create(
            player=self.player,
            level=self.level_2,
            completed=date.today(),
            is_completed=False,
            score=50
        )

    def test_assign_prize_successful(self):
        """Тест успешного присвоения приза, когда уровень завершен."""
        assign_prize_to_player(self.player.id, self.level.id, self.prize.id)
        level_prize = LevelPrize.objects.filter(
            level=self.level, prize=self.prize).first()
        self.assertIsNotNone(level_prize)
        self.assertEqual(level_prize.prize.title, "Golden Trophy")

    def test_assign_prize_unsuccessful_level_not_completed(self):
        """Тест, что приз не присваивается, если уровень не завершен."""
        assign_prize_to_player(
            self.player.id, self.level_2.id, self.prize_2.id)
        level_prize = LevelPrize.objects.filter(
            level=self.level_2, prize=self.prize_2).first()
        self.assertIsNone(level_prize)

    def test_assign_prize_already_assigned(self):
        """Тест, что приз не присваивается повторно за тот же уровень."""
        assign_prize_to_player(self.player.id, self.level.id, self.prize.id)
        assign_prize_to_player(self.player.id, self.level.id, self.prize.id)
        level_prizes = LevelPrize.objects.filter(
            level=self.level, prize=self.prize)
        self.assertEqual(
            level_prizes.count(),
            1)  # Приз должен быть присвоен только один раз

    def test_export_to_csv_with_no_prize(self):
        """Тест, что экспорт работает правильно, даже если приз не был присвоен."""
        file_path = 'test_player_data.csv'
        export_player_data_to_csv(file_path)

        self.assertTrue(os.path.exists(file_path))

        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)
            self.assertEqual(
                len(rows), 3)  # Должно быть две строки данных и одна заголовка
            self.assertEqual(rows[1][0], self.player.player_id)
            self.assertEqual(rows[1][1], self.level.title)
            self.assertEqual(rows[1][2], 'True')
            self.assertEqual(rows[1][3], 'No prize')
            self.assertEqual(rows[2][0], self.player.player_id)
            self.assertEqual(rows[2][1], self.level_2.title)
            self.assertEqual(rows[2][2], 'False')
            self.assertEqual(rows[2][3], 'No prize')

        os.remove(file_path)

    def test_export_to_csv_with_multiple_prizes(self):
        """Тест, что экспорт работает правильно, если присвоены несколько призов."""
        assign_prize_to_player(self.player.id, self.level.id, self.prize.id)

        # Принудительно отметить второй уровень как завершенный, а затем назначить ему приз
        self.player_level_2.is_completed = True
        self.player_level_2.save()
        assign_prize_to_player(
            self.player.id, self.level_2.id, self.prize_2.id)

        file_path = 'test_player_data.csv'
        export_player_data_to_csv(file_path)

        self.assertTrue(os.path.exists(file_path))

        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)
            self.assertEqual(
                len(rows), 3)  # Должно быть две строки данных и одна заголовка
            self.assertEqual(rows[1][0], self.player.player_id)
            self.assertEqual(rows[1][1], self.level.title)
            self.assertEqual(rows[1][2], 'True')
            self.assertEqual(rows[1][3], self.prize.title)
            self.assertEqual(rows[2][0], self.player.player_id)
            self.assertEqual(rows[2][1], self.level_2.title)
            self.assertEqual(rows[2][2], 'True')
            self.assertEqual(rows[2][3], self.prize_2.title)

        os.remove(file_path)
