# Encrypted File Sharing

Учебный проект для передачи файлов по локальной сети с шифрованием AES и обменом ключами Диффи — Хеллмана. Сервер выступает ретранслятором между клиентами.

## Настройка окружения

Откройте терминал в корне проекта — папке с `requirements.txt`.

### 1. Создайте виртуальное окружение

```bash
python -m venv .venv
```

Если окружение `.venv` уже создано, переходите к активации.

### 2. Активируйте окружение

**Windows, PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows, командная строка (cmd):**

```bat
.venv\Scripts\activate.bat
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

### 3. Установите зависимости

```bash
python -m pip install -r requirements.txt
```

В VS Code выберите интерпретатор из `.venv`: `Ctrl+Shift+P` → `Python: Select Interpreter`.

После обновления `requirements.txt` повторите команду установки в активированном окружении. Папка `.venv` создаётся локально и не добавляется в Git.

## Структура проекта

```text
encrypted-file-sharing/
    client/
        __init__.py
        application.py       # Связь интерфейса, сети и шифрования
        GUI.py               # Графический интерфейс
        network.py           # Подключение и обмен данными
    crypto/
        __init__.py
        aes.py               # Шифрование и расшифрование AES
        diffie_hellman.py     # Обмен ключами Диффи — Хеллмана
    server/
        __init__.py
        relay.py             # Сервер-ретранслятор
        relay_test.py        # Тесты сервера
    docs/
        source/              # Исходники и настройки Sphinx
        build/               # Результат сборки документации
        make.bat
        Makefile
    main_client.py           # Точка входа клиента
    main_server.py           # Точка входа сервера
    protocol.py              # Общий формат сетевых сообщений
    requirements.txt         # Зависимости проекта
    .gitignore               # Исключения для Git
    README.md
```

Файлы `__init__.py` обозначают Python-пакеты. Локальная `.venv` и служебные каталоги кэша в схеме не показаны.
