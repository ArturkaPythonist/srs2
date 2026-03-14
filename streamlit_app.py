import streamlit as st
from crewai import Agent, Task, Crew, Process
import os

# Оформление в стиле КазНУ им. Аль-Фараби
st.set_page_config(page_title="СРС №2 - Элмуратов М.", layout="wide")

st.title("🎓 Виртуальная симуляция дебатов ученого совета")
st.markdown("---")
st.write("**Выполнил(а):** Элмуратов М. ")
st.write("**Тема:** Программная реализация алгоритмов взаимодействия и обмена данными (Вариант 13) [cite: 11]")

# Настройка ключа через Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")
if not api_key:
    st.error("Ошибка: Настройте GOOGLE_API_KEY в Secrets!")
    st.stop()
os.environ["GOOGLE_API_KEY"] = api_key

# --- ЗОНА 1: Конфигурация Агентов ---
st.sidebar.header("⚙️ Ученый совет")
with st.sidebar.expander("Докладчик (Researcher)"):
    r1 = st.text_input("Role", "Ведущий исследователь")
    g1 = st.text_area("Goal", "Представить и защитить научный тезис")

with st.sidebar.expander("Оппонент (Critic)"):
    r2 = st.text_input("Role", "Официальный рецензент")
    g2 = st.text_area("Goal", "Провести критический разбор доклада и выявить ошибки")

# --- ЗОНА 2: Ввод данных ---
st.subheader("🔬 Тезис для обсуждения")
user_thesis = st.text_area("Введите научную гипотезу:",
                            placeholder="Пример: Использование квантовых сенсоров в сейсмологии...")

# --- ЗОНА 3: Запуск МАС ---
if st.button("🚀 Начать дебаты"):
    if user_thesis:
        with st.spinner("Идет заседание совета..."):
            try:
                # Инициализация агентов [cite: 28]
                presenter = Agent(
                    role=r1, goal=g1,
                    backstory="Вы — эксперт в области фундаментальной науки.",
                    verbose=True
                )
                critic = Agent(
                    role=r2, goal=g2,
                    backstory="Вы — сторонник строгой верификации и методологии.",
                    verbose=True
                )

                # Задачи
                t1 = Task(description=f"Напишите доклад по тезису: {user_thesis}",
                          agent=presenter, expected_output="Научный доклад.")
                t2 = Task(description="Рецензируйте доклад и вынесите вердикт совета.",
                          agent=critic, expected_output="Критический отзыв.")

                # Сборка Crew [cite: 27]
                debate_crew = Crew(
                    agents=[presenter, critic],
                    tasks=[t1, t2],
                    process=Process.sequential
                )

                result = debate_crew.kickoff()

                st.success("✅ Заседание завершено!")
                st.markdown("### 📜 Итоговое заключение:")
                st.info(result)
            except Exception as e:
                st.error(f"Ошибка: {e}")