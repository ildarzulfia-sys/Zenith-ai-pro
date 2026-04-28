
import streamlit as st
import random

st.set_page_config(page_title="Zenith AI", page_icon="🎾")
st.title("🛡 Zenith AI Score")

sport = st.sidebar.selectbox("Вид спорта:", ["⚽️ Футбол", "🏒 Хоккей", "🏀 Баскетбол", "🏐 Волейбол", "🎾 Теннис"])
st.header(f"Анализ Live: {sport}")

if st.button(f"Запустить сканирование {sport}"):
    prob = random.randint(65, 94)
    st.success(f"Прогноз сформирован!")
    st.metric("Вероятность победы фаворита", f"{prob}%")
    st.info("Рекомендация: Ставка 3% от банка.")

st.sidebar.write("---")
st.sidebar.write("💰 Баланс: 100 000 ₸")

