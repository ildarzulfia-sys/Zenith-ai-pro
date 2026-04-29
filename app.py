import streamlit as st
import requests

# Твой ключ (оставляем текущий, если API поддерживает другие виды спорта)
API_KEY = "689705cae4msh2ab829df81c7ef9p1a2f07jsn17bc2f216264"

st.set_page_config(page_title="Zenith AI Omni", page_icon="🏆", layout="wide")
st.title("🏆 Zenith AI: Универсальный Сканер")

# Выбор вида спорта
sport = st.sidebar.selectbox(
    "Выберите вид спорта:",
    ["Футбол", "Хоккей", "Баскетбол", "Теннис", "Волейбол"]
)

st.header(f"Анализ: {sport}")

if st.button(f"🚀 Запустить сканер {sport}"):
    # Здесь мы будем менять ссылки в зависимости от выбора
    if sport == "Футбол":
        url = "https://free-api-live-football-data.p.rapidapi.com/football-current-live"
    elif sport == "Хоккей":
        url = "https://free-api-live-football-data.p.rapidapi.com/hockey-live" # Пример
    else:
        url = "https://free-api-live-football-data.p.rapidapi.com/multi-live" # Заглушка

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
    }

    with st.spinner(f'Ищу все матчи по виду: {sport}...'):
        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            
            if data.get('status') == 'success' and data.get('data'):
                matches = data['data']
                st.success(f"Найдено событий: {len(matches)}")
                # Вывод списка матчей
                for m in matches:
                    with st.expander(f"🏟 {m.get('home_team', {}).get('name')} vs {m.get('away_team', {}).get('name')}"):
                        st.write(f"📊 Счет: {m.get('score', '0:0')}")
            else:
                st.info(f"В данный момент активных матчей ({sport}) не найдено.")
        except Exception as e:
            st.error(f"Этот API пока не поддерживает {sport}. Нужно подключить доп. модуль.")

