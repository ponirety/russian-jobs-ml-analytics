# 💼 Vacancy Salary Predictor

ML-сервис для предсказания рыночной заработной платы по описанию вакансии на основе данных с hh.ru.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?logo=fastapi)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3+-orange?logo=scikit-learn)

## 🎯 О проекте

HR-менеджерам, рекрутерам и соискателям часто сложно понять, насколько предлагаемая зарплата соответствует рынку. Этот проект решает задачу автоматического предсказания справедливой заработной платы на основе ключевых параметров вакансии: опыта, региона, категории, формата работы и названия.

Сервис принимает описание вакансии через REST API и возвращает прогнозируемую зарплату в рублях.

## 🛠 Технологический стек

| Слой                 | Технологии                   |
| -------------------- | ---------------------------- |
| Обработка данных     | Python, Pandas, NumPy        |
| Машинное обучение    | Scikit-learn (Random Forest) |
| Бэкенд / API         | FastAPI, Pydantic, Uvicorn   |
| Сериализация моделей | Joblib                       |
| Визуализация         | Matplotlib, Seaborn, Jupyter |

## 🏗 Архитектура проекта

```
vacancy-analytics/
├── notebooks/          # Исследовательские ноутбуки (EDA, обучение)
│   ├── 01_data_inspection.ipynb
│   ├── 02_data_preprocessing.ipynb
│   ├── 03_feature_engineering.ipynb
│   └── 04_model_training.ipynb
├── src/                # Логика инференса модели
│   └── predictor.py
├── app/                # FastAPI веб-сервис
│   └── main.py
├── models/             # Сохранённые артефакты (.joblib)
├── data/
│   ├── raw/            # Исходные данные
│   └── processed/      # Очищенные датасеты
├── requirements.txt
├── .gitignore
└── README.md
```

## 🔄 ML-пайплайн

1. **Загрузка данных** — 129 464 вакансий с hh.ru (июль 2026).
2. **Очистка** — удаление строк без указания зарплаты (потеря ~20%), создание целевой переменной `target_salary` как среднего/единственного значения `from`/`to`.
3. **Feature Engineering**:
   - Булевы признаки (`is_remote`, `is_hybrid` и т.д.) → `int`
   - Порядковое кодирование `experience` (0–3)
   - Извлечение признаков из `name`: длина, флаги `is_senior`, `is_junior`
   - One-Hot Encoding для городов, категорий и форм занятости
4. **Отбор признаков** — топ-100 по важности Random Forest (убрали шум из 746 колонок).
5. **Обучение** — `RandomForestRegressor` с `train_test_split(test_size=0.2, random_state=42)`.
6. **Деплой** — модель и список признаков сериализованы через `joblib`, обёрнуты в FastAPI.

## 📊 Результаты модели

| Метрика                         | Значение        |
| ------------------------------- | --------------- |
| R² (коэффициент детерминации)   | **0.34**        |
| MAE (средняя абсолютная ошибка) | **~33 000 ₽**   |
| Количество признаков            | 100             |
| Размер тестовой выборки         | 20 630 вакансий |

### Топ-5 самых важных признаков

| Признак                               | Важность |
| ------------------------------------- | -------- |
| `name_length`                         | 26.7%    |
| `experience`                          | 13.8%    |
| `employment_form_Полная занятость`    | 7.5%     |
| `employment_form_Частичная занятость` | 5.1%     |
| `accept_labor_contract`               | 5.0%     |

## 🚀 Как запустить локально

### 1. Клонировать репозиторий

```bash
git clone https://github.com/ponirety/vacancy-analytics.git
cd vacancy-analytics
```

### 2. Установить зависимости

```bash
pip install -r requirements.txt
```

### 3. Получить артефакты модели

Файлы `models/rf_model_100.joblib` и `models/feature_names.joblib` не включены в репозиторий из-за размера.
Скачайте их по ссылке: **[https://drive.google.com/drive/folders/1r5BR8iNvxC7kZh-ar-IYDP4yhDHJ6bKX?hl=ru]** и положите в папку `models/`.

> Либо обучите модель заново, пройдя по ноутбукам в папке `notebooks/`.

### 4. Запустить API-сервер

```bash
python -m uvicorn app.main:app --reload
```

### 5. Открыть документацию

Перейдите по адресу: **http://127.0.0.1:8000/docs**

Там вы увидите интерактивный Swagger UI для тестирования API.

## 📡 Пример API-запроса

### Запрос

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "experience": 3,
       "name_length": 35,
       "is_senior": 1,
       "area_name_Москва": 1,
       "employment_form_Полная занятость": 1,
       "category_Высший и средний менеджмент": 1
     }'
```

### Ответ

```json
{
  "predicted_salary": 560283
}
```

## 📄 Лицензия

MIT License

## 👤 Автор

**<Бабушкин Дмитрий>**  
[https://github.com/ponirety](#) · [@peble7](#)
