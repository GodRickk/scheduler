# Scheduler - планировщик рабочего времени

## Описание проекта

Scheduler - это Python-библиотека для управления графиком занятости работников. 

Она позволяет:
- находить свободные временные слоты
- находить занятые слоты
- проверять доступность времени для встреч
- подбирать подходящее время для заявок определенной продолжительности. 
    

Библиотека получает данные о расписании через REST API.


## Установка и запуск тестов

### 1. Клонирование репозитория

```bash
git clone https://github.com/GodRickk/scheduler.git
cd scheduler
```

### 2. Создание виртуального окружения
```bash
# Windows
python -m venv .venv
```

```bash
# Linux/MacOS
python3 -m venv .venv
```


###  3. Активация виртуального окружения
```bash
# Windows
.venv\Scripts\activate
```

```bash
# Linux/MacOS
source .venv/bin/activate
```

### 4. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 5. Запуск тестов

```bash
pytest
```