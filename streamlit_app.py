import streamlit as st
from crewai import Agent, Task, Crew, Process
import os

# Оформление в стиле КазНУ им. Аль-Фараби
st.set_page_config(page_title="СРС №2 - Артур Шакиев", layout="wide")

st.title("🎓 Виртуальная симуляция дебатов ученого совета")
st.markdown("---")
st.write("**Выполнил:** Артур Шакиев")
st.write("**Тема:** Программная реализация алгоритмов взаимодействия и обмена данными (Вариант 13)")

# Настройка ключа через Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")
if not api_key:
    st.error("Ошибка: Настройте GOOGLE_API_KEY в Settings -> Secrets!")
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
                            placeholder="Пример: Использование ИИ в медицине полностью заменит врачей-диагностов...")

# --- ЗОНА 3: Запуск МАС ---
if st.button("🚀 Начать дебаты"):
    if user_thesis:
        with st.spinner("Идет заседание совета..."):
            try:
                # Инициализация агентов
                presenter = Agent(
                    role=r1, goal=g1,
                    backstory="Вы — эксперт в области фундаментальной науки. Ваша карьера зависит от защиты этого тезиса.",
                    verbose=True
                )
                critic = Agent(
                    role=r2, goal=g2,
                    backstory="Вы — сторонник строгой верификации и методологии. Вы не пропускаете слабые исследования.",
                    verbose=True
                )

                # Задачи
                t1 = Task(description=f"Напишите развернутый доклад по тезису: {user_thesis}. Приведите 3 аргумента 'ЗА'.",
                          agent=presenter, expected_output="Научный доклад.")
                t2 = Task(description="Проанализируйте доклад, укажите на его слабые места и вынесите вердикт совета (Одобрено/Отклонено).",
                          agent=critic, expected_output="Критический отзыв и вердикт.")

                # Сборка Crew
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
                st.error(f"Ошибка выполнения: {e}")
    else:
        st.warning("Пожалуйста, введите тему для обсуждения!")