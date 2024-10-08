# Player Rewards System

## Описание

Player Rewards System — это Django-приложение для управления наградами игроков за прохождение уровней в игре. Приложение позволяет назначать призы за пройденные уровни и экспортировать данные о прохождении уровней и полученных призах в CSV-файл.

## Возможности

- **Назначение призов**: Автоматическое присвоение приза игроку при успешном завершении уровня.
- **Экспорт данных**: Экспорт данных об игроках, пройденных уровнях и полученных призах в CSV-файл. Оптимизирован для работы с большим количеством данных (100 000+ записей).
- **Модели данных**: Поддержка моделей для игроков, уровней, призов и связей между ними.

## Установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/yourusername/player_rewards_system.git
cd player_rewards_system
```

### 2. Установка зависимостей
Рекомендуется использовать виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate  # для Linux/MacOS
venv\Scripts\activate  # для Windows
```
#### Установите зависимости:

```bash
pip install -r requirements.txt
```

## Использование
#### - Присвоение приза игроку
Для присвоения приза игроку за завершение уровня используйте метод assign_prize_to_player из utils.py. Например:

```python
from game.utils import assign_prize_to_player

assign_prize_to_player(player_id=1, level_id=2, prize_id=3)
```
#### - Экспорт данных в CSV
Для экспорта данных в CSV-файл используйте метод export_player_data_to_csv из utils.py. Например:

```python
from game.utils import export_player_data_to_csv

export_player_data_to_csv('output.csv')
``` 
#### - Тестирование
Проект включает в себя тесты для проверки корректности работы функционала. Чтобы запустить тесты, выполните команду:

```bash
python manage.py test
```
#### Тесты проверяют следующие сценарии:

Успешное присвоение приза.
Проверка на повторное присвоение приза.
Экспорт данных в CSV при различных условиях.


### Task_1.py
Описание модели игрока и бустов с возможностью начислять игроку бусты за прохождение уровней или вручную.