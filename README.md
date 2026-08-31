# SOEmu

Эмулятор сервера и компактный архив скриптов клиента Stalker Online 0.6.5.3
для анализа протокола BigWorld Engine 2.0.1.

В репозитории находятся:

- `server/` — LoginApp/BaseApp-эмулятор, MariaDB-хранилище, схема и тесты;
- `packs/res/scripts/**/*.pyc` — оригинальный Python 2.6 bytecode клиента;
- `packs/res/scripts/**/*.pyc_dis` — читаемые декомпиляции bytecode;
- `packs/res/scripts/entity_defs/` — `.def`, `alias.xml` и описания сущностей;
- небольшие JSON/XML-конфиги, необходимые для понимания скриптов.

Модели, текстуры, карты, звук, игровой EXE/DLL, логи и крупные игровые данные
сюда намеренно не загружаются.

## Запуск сервера

Требуются Python 3, MariaDB на `127.0.0.1:3307` и зависимости из
`requirements.txt`. Запустите `RUN_EMULATOR.bat`. Пароль MariaDB запрашивается
в консоли или передаётся только локально через `SOEMU_DB_PASSWORD`.

Подробности настройки базы находятся в `DATABASE.md`.
