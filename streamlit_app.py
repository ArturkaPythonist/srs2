import streamlit as st
from crewai import Agent, Task, Crew, Process
import os

# Настройка страницы в стиле КазНУ
st.set_page_config(page_title="Academic Debate AI - Variant 13", page_icon="🎓", layout="wide")

st.title("🎓 Симуляция дебатов ученого совета")
st.info("Разработка студента: [Твое Имя] | Вариант 13")

# Настройка API ключа
# На Streamlit Cloud добавь его в Settings -> Secrets
api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("Критическая ошибка: GOOGLE_API_KEY не найден в секретах приложения!")
    st.stop()

os.environ["GOOGLE_API_KEY"] = api_key

# --- ЗОНА 1: Конфигурация (Боковая панель) ---
st.sidebar.header("⚙️ Конфигурация МАС")

with st.sidebar.expander("Агент: Докладчик"):
    r1 = st.text_input("Role", "Ведущий исследователь")
    g1 = st.text_area("Goal", "Аргументированно защитить научную гипотезу")

with st.sidebar.expander("Агент: Оппонент"):
    r2 = st.text_input("Role", "Скептичный рецензент")
    g2 = st.text_area("Goal", "Найти уязвимости в защите и вынести вердикт")

# --- ЗОНА 2: Ввод данных ---
st.subheader("🔬 Тезис для обсуждения")
user_thesis = st.text_area("Введите гипотезу (например: 'Внедрение безусловного дохода приведет к росту ВВП'):",
                           placeholder="Введите текст тезиса здесь...")

# --- ЗОНА 3: Выполнение ---
if st.button("🚀 Запустить дебаты"):
    if not user_thesis:
        st.warning("Сначала введите тезис!")
    else:
        with st.spinner("Идет заседание совета..."):
            try:
                # Инициализация агентов
                presenter = Agent(
                    role=r1,
                    goal=g1,
                    backstory="Вы — профессор с мировым именем, ваша репутация зависит от успешной защиты этой идеи.",
                    llm="gemini/gemini-1.5-flash",
                    verbose=True
                )

                critic = Agent(
                    role=r2,
                    goal=g2,
                    backstory="Вы — главный критик академии. Ваша цель — не допустить публикации слабых и непроверенных теорий.",
                    llm="gemini/gemini-1.5-flash",
                    verbose=True
                )

                # Задачи
                t1 = Task(
                    description=f"Подготовь научный доклад в защиту тезиса: {user_thesis}. Используй 3 логических аргумента.",
                    agent=presenter,
                    expected_output="Текст доклада с аргументацией."
                )

                t2 = Task(
                    description="Проанализируй доклад. Найди 2 слабых места и напиши финальное решение: 'Одобрено' или 'Отклонено' с объяснением.",
                    agent=critic,
                    expected_output="Критическая рецензия и итоговый вердикт."
                )

                # Запуск процесса
                crew = Crew(
                    agents=[presenter, critic],
                    tasks=[t1, t2],
                    process=Process.sequential
                )

                result = crew.kickoff()

                st.success("✅ Анализ завершен!")
                st.markdown("### 📜 Протокол заседания:")
                st.markdown(result.raw)

            except Exception as e:
                st.error(f"Ошибка выполнения: {str(e)}")