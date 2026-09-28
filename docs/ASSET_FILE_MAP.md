# Карта ресурсов Clash of Clans

Репозиторий: `Wega918/34tm49`  
Проверено: 2026-09-22

## Главный вывод

Для вывода здания, юнита или эффекта недостаточно преобразовать каждый файл отдельно в JSON. Нужна единая база связей:

```text
игровой объект / запись данных
  -> логическое имя и вариант/уровень
  -> export/symbol внутри .sc
  -> геометрия, кадры, матрицы и таймлайн из .sc
  -> одна или несколько текстур *_N.sctx
  -> VFX, звук, снаряд, тень и 3D-ресурсы
```

Итоговый каталог `asset-manifest.json` должен быть точкой входа для браузерного движка.

## Что найдено в `assets/sc`

Всего 553 файла: 307 `.sc` и 246 `.sctx`.

| Группа | Примеры | Назначение |
|---|---|---|
| Здания | `buildings.sc`, `buildings2.sc`, `buildings_cc.sc`, `building_bases.sc` | Части, варианты, уровни и анимации зданий |
| Юниты | `chr_barbarian.sc`, `chr_archer.sc`, `chr_dragon.sc` | Персонажи, направления и действия |
| Общие персонажи | `characters.sc` | Совместно используемые элементы персонажей |
| Герои | `hero_bk_default.sc`, `hero_aq_default.sc` | Внешность и визуальные состояния героев |
| Эффекты | `vfx_character.sc`, `vfx_env.sc`, `vfx_spells.sc` | Эффекты персонажей, окружения и заклинаний |
| Окружение | `background_*.sc`, `map.sc`, `clouds.sc` | Поле, фоны, карты и окружение |
| Декорации | `decos2.sc`, `decos_cc.sc` | Декоративные объекты |
| Интерфейс | `ui.sc`, `hud.sc`, `overlay.sc`, `health_bar.sc` | UI и HUD |
| Инфоэкраны | `info_*.sc` | Карточки информации; не основной боевой спрайт |
| События | `events.sc`, `shop.sc`, `tutorial*.sc` | Экраны и специализированный контент |

## Связь `.sc` и `.sctx`

Обычно базовое имя образует пакет:

```text
chr_barbarian.sc + chr_barbarian_0.sctx
buildings.sc + buildings_0.sctx ... buildings_70.sctx
vfx_spells.sc + vfx_spells_0.sctx ... vfx_spells_4.sctx
```

- `.sc` хранит exports/symbols, shapes, вершины и UV, таймлайны, кадры, матрицы, цвета и ссылки на страницы текстур.
- `.sctx` — текстурная страница/атлас; `_N` — номер страницы одного пакета.
- Один `.sc` может использовать много `.sctx`.
- Отсутствие соседнего `.sctx` нельзя толковать только по имени: текстура может быть общей, внешней, встроенной либо файл может быть служебным.

Крупные пакеты: `buildings` — 71 страница, `characters` — 12, `buildings_cc` — 11, `vfx_character` — 11, `vfx_env` — 7, `vfx_spells` — 5.

## `assets/csv` — не обычные текстовые CSV

В папке 26 файлов. Они бинарные/закодированные и не читаются как UTF-8 CSV. Простое переименование или обычный CSV-парсер не подойдут.

| Файл | Роль для будущей проверки после декодирования |
|---|---|
| `animations.csv` | Имена и настройки анимаций |
| `animation_transitions.csv` | Переходы состояний |
| `assets.csv` | Реестр/настройки ресурсов |
| `3d.csv`, `3d_building.csv`, `3d_environment.csv` | 3D-ресурсы |
| `particle_effects_3d.csv` | 3D-частицы |
| `skin_projectile_vis.csv` | Визуальные варианты снарядов |
| `preview_scenarios.csv` | Сценарии предпросмотра |
| `resource_packs.csv` | Пакеты ресурсов |
| `assets_logic.scindex` | Индекс логических ресурсов |
| `particle_emitters_logic.scindex` | Индекс логики эмиттеров |

Не все CSV относятся к бою: там также есть биллинг, чат, подсказки, события и служебная конфигурация.

## Другие ключевые индексы

| Файл | Роль |
|---|---|
| `assets/data/assetdata.scindex` | Индекс и метаданные ресурсов |
| `assets/data/assetdependencies.flat` | Граф зависимостей ресурсов |
| `assets/data/particle_emitters_3d.zflex` | Данные 3D-эмиттеров |
| `assets/assets.scdb` | База ресурсов, формат требует исследования |
| `assets/fingerprint.json` | Контрольный список/хеши версии |
| `assets/game_assets.txt` | Список путей, но не смысл и не анимации |
| `assets/all_files.txt` | Общий список файлов |

## Что преобразовывать

1. `.sctx` — декодировать в PNG/WebP или GPU-совместимый формат.
2. `.sc` — разобрать в JSON/компактный runtime-формат: exports, shapes, texture page, UV, vertices, movie clips, FPS, frames, matrices, colors и вложенные symbols.
3. Декодировать относящиеся к рендеру таблицы и индексы.
4. Построить общий `asset-manifest.json`.

Не надо превращать абсолютно всё в JSON: медиа остаются медиафайлами, а большие числовые массивы выгоднее хранить бинарно. JSON-копии без разрешённых связей полной картины не дадут.

## Предлагаемая структура

```text
decoded/
  manifest/
    asset-manifest.json
    aliases.json
    dependencies.json
    unresolved.json
  sc/
  textures/
  tables/
  audio/
  reports/
    decode-report.json
    collisions.json
```

Пример записи manifest:

```json
{
  "id": "building:cannon:level_1",
  "kind": "building",
  "source": { "table": null, "row": null },
  "visual": {
    "sc": "sc/buildings.json",
    "export": null,
    "texturePages": []
  },
  "states": { "idle": null, "attack": null, "destroyed": null },
  "attachments": { "projectile": null, "impactVfx": null, "audio": [] },
  "confidence": "unresolved"
}
```

`null` заполняется только после чтения exports и индексов; это нельзя надёжно угадать по имени файла.

## Как система должна искать пушку

1. Найти cannon в декодированных игровых таблицах/индексах.
2. Получить уровень, визуальный вариант и имя ресурса/export.
3. Через manifest найти пакет (`buildings` или другой).
4. Загрузить нужный SC runtime и только требуемые texture pages.
5. Выбрать состояние idle/aim/attack/damaged/destroyed.
6. Подключить projectile/VFX/audio через dependency graph.
7. Проигрывать исходный таймлайн с FPS, матрицами, слоями и событиями кадров.

## План полной карты

- [x] Посчитать `.sc` и `.sctx`.
- [x] Разделить основные семейства.
- [x] Зафиксировать правило пар по базовому имени.
- [ ] Извлечь exports из каждого `.sc`.
- [ ] Связать exports -> shapes -> texture pages.
- [ ] Определить контейнер/сжатие бинарных `.csv`.
- [ ] Декодировать `assetdata.scindex`, `assetdependencies.flat`, `assets_logic.scindex`.
- [ ] Связать игровые записи с exports.
- [ ] Связать здания/юнитов со снарядами, VFX и звуками.
- [ ] Генерировать единый `asset-manifest.json`.
- [ ] Проверить по одному объекту каждого класса: юнит, здание, герой, заклинание.

## Достоверность связей

Каждая связь получает статус:

- `exact` — прочитана из SC/таблицы/индекса;
- `derived` — однозначно выведена из структуры и пары имён;
- `heuristic` — предположение по имени;
- `unresolved` — ещё не установлена.

Так система не примет информационный экран или догадку за боевой ресурс.
