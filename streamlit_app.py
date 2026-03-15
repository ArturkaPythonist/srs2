import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM
import os

# Оформление в стиле КазНУ им. Аль-Фараби
st.set_page_config(page_title="СРС №2 - Артур Шакиев", layout="wide")

st.title("🎓 Виртуальная симуляция дебатов ученого совета")
st.markdown("---")
st.write("**Выполнил:** Артур Шакиев")
st.write("**Тема:** Программная реализация алгоритмов взаимодействия и обмена данными (Вариант 13)")

# Получаем ключ из секретов Streamlit
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("Ошибка: Настройте GOOGLE_API_KEY в Settings -> Secrets!")
    st.stop()

# Инициализируем АКТУАЛЬНУЮ модель: gemini-2.5-flash
gemini_llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=api_key
)

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
                    llm=gemini_llm,
                    verbose=True,
                    allow_delegation=False
                )
                critic = Agent(
                    role=r2, goal=g2,
                    backstory="Вы — сторонник строгой верификации и методологии. Вы не пропускаете слабые исследования.",
                    llm=gemini_llm,
                    verbose=True,
                    allow_delegation=False
                )

                # Задачи
                t1 = Task(description=f"Напишите развернутый доклад по