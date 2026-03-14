import streamlit as st
from crewai import Agent, Task, Crew, Process
import os

# Оформление в стиле СРС КазНУ [cite: 1, 2, 9]
st.set_page_config(page_title="CPC 2 - Elmuratov M.", layout="wide")

st.title("🎓 Виртуальная симуляция дебатов ученого совета")
st.write("---")
st.write("**Выполнил:** Студент кафедры «Компьютерных наук» Элмуратов М. [cite: 9, 12]")
st.write("**Тема:** Программная реализация алгоритмов взаимодействия и обмена данными (Вариант 13) [cite: 11]")

# Настройка API ключа через Secrets Streamlit
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("Критическая ошибка: Введите GOOGLE_API_KEY в Settings -> Secrets приложения.")
    st.stop()

os.environ["GOOGLE_API_KEY"] = api_key

# --- ЗОНА 1: Конфигурация Агентов ---
st.sidebar.header("⚙️ Настройки Совета")
with st.sidebar.expander("Агент: Ученый-докладчик"):
    a1_role = st.text_input("Role", "Ведущий исследователь")
    a1_goal = st.text_input("Goal", "Защитить научный тезис")

with st.sidebar.expander("Агент: Оппонент"):
    a2_role = st.text_input("Role", "Скептичный рецензент")
    a2_goal = st.text_input("Goal", "Провести критический анализ тезиса")

# --- ЗОНА 2: Ввод тезиса ---
st.subheader("📝 Предмет научной дискуссии")
scientific_thesis = st.text_area("Введите гипотезу для дебатов:",
                                 placeholder="Пример: Внедрение квантовых вычислений в криптографию...")

# --- ЗОНА 3: Запуск МАС ---
if st.button("🚀 Начать дебаты"):
    if scientific_thesis:
        with st.spinner("Агенты ведут дискуссию..."):
            try:
                # Создание агентов [cite: 28]
                presenter = Agent(
                    role=a1_role,
                    goal=a1_goal,
                    backstory="Вы выдающийся ученый, защищающий свою работу перед советом.",
                    verbose=True
                )

                critic = Agent(
                    role=a2_role,
                    goal=a2_goal,
                    backstory="Вы официальный оппонент. Ваша задача — найти уязвимости в логике.",
                    verbose=True
                )

                # Определение задач
                task1 = Task(
                    description=f"Подготовь подробный доклад в защиту тезиса: {scientific_thesis}.",
                    agent=presenter,
                    expected_output="Развернутый научный доклад."
                )

                task2 = Task(
                    description="Проанализируй доклад, найди 3 критических замечания и вынеси итоговое решение.",
                    agent=critic,
                    expected_output="Критическая рецензия и вердикт совета."
                )

                # Сборка экипажа
                debate_crew = Crew(
                    agents=[presenter, critic],
                    tasks=[task1, task2],
                    process=Process.sequential
                )

                result = debate_crew.kickoff()

                st.success("✅ Заседание завершено!")
                st.markdown("### 📜 Итоговый протокол:")
                st.info(result)

            except Exception as e:
                st.error(f"Произошла ошибка: {str(e)}")
    else:
        st.warning("Введите тему дебатов!")