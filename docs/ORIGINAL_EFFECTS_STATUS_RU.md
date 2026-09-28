# Оригинальные эффекты юнитов

В браузерной демке запрещены процедурно нарисованные заменители снарядов и попаданий.

## Подключено из исходных SC

- Archer, Archer2, Barcher, Super Archer — `characters.sc:arrow_ammo_small`.
- Ice Wizard — `characters.sc:ice_wizard_projectile`.
- Lava Hound — `characters.sc:lavahound_projectile`.
- Ice Hound — `characters.sc:tiny_icehound_projectile`.
- Bowler — `characters.sc:slimeball_projectile`.
- Super Bowler — `characters.sc:slimeball_special`.
- Balloon и Hasty Balloon — `characters.sc:projectile_bomb`.
- Drop Ship — `characters.sc:projectile_bomb_lvl2`.
- Log Launcher — `characters.sc:logger_log_projectile_lvl1_3`.
- Wizard, Party Wizard, Super Wizard — исходные projectile/impact exports из `vfx_character.sc`.

Остальные юниты используют исходную анимацию атаки из собственного `chr_*.sc`. Если точная внешняя связь не подтверждена, дополнительный эффект не подставляется.

## Не является обычным SC MovieClip

Огонь Dragon/Baby Dragon и часть электрических/дымовых эффектов привязаны к именам из `particle_emitters_logic.scindex`, например:

- `dragonFire`, `dragonFireAdd`, `dragonSpark`;
- `BabyDragonSpitFire`, `BabyDragonSpitFireAdd`, `BabyDragonSpitFireEmbers1`;
- `electro_dragon_attack_01`, `electro_dragon_attack_02`.

Для них нужен отдельный runtime декодированных emitter-данных. Подмена похожим SC-эффектом намеренно не выполняется.
