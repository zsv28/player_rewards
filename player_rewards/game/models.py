from datetime import date

from django.db import models


class Player(models.Model):
    player_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.player_id


class Level(models.Model):
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Prize(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class PlayerLevel(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    completed = models.DateField(default=date.today)
    is_completed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.player.player_id} - {self.level.title}'


class LevelPrize(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    received = models.DateField(default=date.today)

    def __str__(self):
        return f'{self.level.title} - {self.prize.title}'
