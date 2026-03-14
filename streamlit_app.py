import streamlit as st
from crewai import Agent, Task, Crew, Process

# Настройка страницы
st.set_page_config(page_title="Academic Debate AI (V13)", page_icon="🎓", layout="wide")

# Проверка API ключа в Secrets (для Streamlit Cloud) или в переменной окружения
import os

api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

st.title("🎓 Виртуальная симуляция дебатов ученого совета")
st.markdown("Вариант 13: Система генерации и критики научных тезисов.")

# --- ЗОНА 1: Конфигурация агентов (Боковая панель) ---
st.sidebar.header("⚙️ Настройка Ученого Совета")

with st.sidebar.expander("Агент 1: Докладчик (Защита)", expanded=False):
    a1_role = st.text_input("Role", "Ведущий исследователь", key="r1")
    a1_goal = st.text_area("Goal", "Привести веские научные аргументы в пользу гипотезы", key="g1")
    a1_backstory = st.text_area("Backstory", "Вы профессор с 20-летним стажем, защищающий инновационный подход.",
                                key="b1")

with st.sidebar.expander("Агент 2: Оппонент (Критика)", expanded=False):
    a2_role = st.text_input("Role", "Скептичный рецензент", key="r2")
    a2_goal = st.text_area("Goal", "Найти слабые места в логике и потребовать доказательств", key="g2")
    a2_backstory = st.text_area("Backstory", "Вы эксперт по научной методологии, который не терпит пустых слов.",
                                key="b2")

# --- ЗОНА 2: Ввод данных ---
st.subheader("🔬 Предмет дискуссии")
thesis = st.text_area(
    "Введите научную гипотезу или тему для обсуждения:",
    placeholder="Например: Использование ИИ для диагностики редких заболеваний на ранних стадиях...",
    height=100
)

# --- ЗОНА 3: Запуск и результат ---
if st.button("🚀 Начать заседание"):
    if not api_key:
        st.error("Ошибка: Не найден OPENAI_API_KEY. Добавьте его в Secrets приложения.")
    elif not thesis:
        st.warning("Пожалуйста, введите тему для дебатов.")
    else:
        with st.spinner("Агенты ведут научную дискуссию..."):
            try:
                # Настройка агентов
                presenter = Agent(
                    role=a1_role,
                    goal=a1_goal,
                    backstory=a1_backstory,
                    allow_delegation=False,
                    verbose=True
                )

                critic = Agent(
                    role=a2_role,
                    goal=a2_goal,
                    backstory=a2_backstory,
                    allow_delegation=False,
                    verbose=True
                )

                # Задачи
                task_present = Task(
                    description=f"Подготовьте тезисное выступление в защиту идеи: {thesis}",
                    agent=presenter,
                    expected_output="Структурированный доклад с 3-4 ключевыми аргументами."
                )

                task_critique = Task(
                    description=f"Проанализируйте выступление коллеги. Задайте 2 острых вопроса и сделайте вывод о научной состоятельности идеи.",
                    agent=critic,
                    expected_output="Критическая рецензия и финальный вердикт совета."
                )

                # Запуск Crew
                crew = Crew(
                    agents=[presenter, critic],
                    tasks=[task_present, task_critique],
                    process=Process.sequential
                )

                result = crew.kickoff()

                # Отображение результата
                st.success("✅ Заседание окончено")
                st.markdown("### 📜 Протокол дебатов")
                st.info(result)

            except Exception as e:
                st.error(f"Произошла ошибка при работе МАС: {str(e)}")