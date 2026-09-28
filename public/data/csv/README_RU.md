# CSV Runtime Pack

Это готовые данные для использования в игре.

- Исходных CSV внутри нет.
- Base64-копий, SHA-256 и lossless-обёрток нет.
- Пустые значения удалены.
- `TRUE/FALSE` преобразованы в `true/false`.
- Числа преобразованы из строк в JSON numbers.
- Названия колонок преобразованы в lowerCamelCase.
- Строки-продолжения сохранены в `rows`, чтобы связанные значения не потеряли соответствие друг другу.
- Все именованные записи доступны напрямую по имени, без перебора массива.

## Обычные таблицы

```js
const cannon = table.entries["нужное имя"];
```

Пример структуры:

```json
{
  "format": "runtime-table-v1",
  "table": "animation_transitions",
  "entries": {
    "DebrisTowerAnimTransitions": {
      "from": "activate",
      "to": "attack",
      "condition": "isAnimationOver()&&!isConstructing()",
      "rows": [
        {
          "from": "activate",
          "to": "upgrade",
          "condition": "isConstructing()"
        }
      ]
    }
  }
}
```

`rows` — дополнительные строки той же именованной записи. Их нельзя было слить с основной строкой без потери связи между колонками.

## Анимации

```js
const variants = animations.groups.Barbarian.actions.attack;
const firstAttack = variants[0];
console.log(firstAttack.exportName);
console.log(firstAttack.swf);
```

У каждого действия массив вариантов, поскольку одно действие может иметь несколько исходных анимаций с весами выбора.

## manifest.json

Содержит список всех таблиц, имена файлов и количество основных записей.

## Не включено

`assets_logic.scindex.json` и `particle_emitters_logic.scindex.json` не включены: в предоставленном архиве они были только Base64-копиями исходных бинарников, а не семантически декодированными данными. Такие файлы пока нельзя нормально использовать в игровом коде.
