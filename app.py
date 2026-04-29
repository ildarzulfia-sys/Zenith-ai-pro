
import streamlit as st
import requests
from datetime import datetime, timedelta

# Твой универсальный ключ RapidAPI
API_KEY = "689705cae4msh2ab829df81c7ef9p1a2f07jsn17bc2f216264"

st.set_page_config(page_title="Zenith AI Pro", page_icon="🏆", layout="wide")
st.title("🏆 Zenith AI: Omni-Сканер 3.0")

# --- БОКОВАЯ ПАНЕЛЬ (НАСТРОЙКИ) ---
st.sidebar.header("⚙️ Настройки поиска")

# 1. Выбор вида спорта
sport_choice = st.sidebar.selectbox(
    "Вид спорта:",
    ["Football", "Hockey", "Tennis", "Basketball", "Volleyball"]
)

# 2. Логика выбора даты (Вчера, Сегодня, Завтра)
today = datetime.now()
date_options = {
    "⏪ Вчера": (today - timedelta(days=1)).strftime('%Y%m%d'),
    "📍 Сегодня": today.strftime('%Y%m%d'),
    "⏩ Завтра": (today + timedelta(days=1)).strftime('%Y%m%d')
}
selected_label = st.sidebar.radio("Период:", list(date_options.keys()), index=1)
selected_date = date_options[selected_label]

# Словарь для API
sport_map = {
    "Football": "soccer",
    "Hockey": "hockey",
    "Tennis": "tennis",
    "Basketball": "basketball",
    "Volleyball": "volleyball"
}

# --- ОСНОВНОЙ ПРОВЕРЩИК ---
if st.button(f"🔍 Сканировать {sport_choice} ({selected_label})"):
    sport_type = sport_map[sport_choice]
    url = f"https://livescore6.p.rapidapi.com/{sport_type}/list-by-date"
    
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "livescore6.p.rapidapi.com"
    }
    
    params = {"Category": "general", "Date": selected_date}

    with st.spinner('Связываюсь с глобальным сервером...'):
        try:
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            
            if 'Stages' in data and data['Stages']:
                st.success(f"Найдено турниров: {len(data['Stages'])}")
                
                for stage in data['Stages']:
                    league_name = stage.get('Snm', 'Турнир')
                    country = stage.get('Cnm', '')
                    
                    with st.expander(f"🏟 {league_name} ({country})"):
                        for event in stage.get('Events', []):
                            # Данные команд
                            home = event.get('T1', [{}])[0].get('Nm', 'Команда 1')
                            away = event.get('T2', [{}])[0].get('Nm', 'Команда 2')
                            
                            # Счет и Статус
                            score_h = event.get('Tr1')
                            score_a = event.get('Tr2')
                            status = event.get('Eps', '') # Например, 'FT', 'Live', 'NS'
                            
                            # Формируем строку вывода
                            if score_h is not None and score_h != '':
                                # Если матч идет или завершен
                                match_info = f"🕒 **{status}** | **{home}** {score_h} : {score_a}  **{away}**"
                            else:
                                # Если матч еще не начался - вычисляем время
                                raw_time = str(event.get('Esd', '00000000000000'))
                                if len(raw_time) >= 12:
                                    start_t = f"{raw_time[8:10]}:{raw_time[10:12]}"
                                else:
                                    start_t = "Время не указ."
                                match_info = f"📅 Нач. {start_t} | {home} vs {away}"
                            
                            st.write(match_info)
            else:
                st.info(f"На выбранный день ({selected_label}) событий в базе API не найдено.")
                
        except Exception as e:
            st.error(f"Произошла ошибка: {e}")
