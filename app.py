

    import streamlit as st
import requests
from datetime import datetime, timedelta

# Твой ключ
API_KEY = "689705cae4msh2ab829df81c7ef9p1a2f07jsn17bc2f216264"

st.set_page_config(page_title="Zenith AI Pro", page_icon="🏆", layout="wide")
st.title("🏆 Zenith AI: Omni-Сканер 3 Дня")

# 1. Выбор вида спорта
sport_choice = st.sidebar.selectbox(
    "Вид спорта:",
    ["Football", "Hockey", "Tennis", "Basketball", "Volleyball"]
)

# 2. Выбор даты (3 дня)
today = datetime.now()
date_options = {
    "Вчера": (today - timedelta(days=1)).strftime('%Y%m%d'),
    "Сегодня": today.strftime('%Y%m%d'),
    "Завтра": (today + timedelta(days=1)).strftime('%Y%m%d')
}
selected_date_label = st.sidebar.radio("Выберите день:", list(date_options.keys()), index=1)
selected_date_value = date_options[selected_date_label]

sport_map = {
    "Football": "soccer",
    "Hockey": "hockey",
    "Tennis": "tennis",
    "Basketball": "basketball",
    "Volleyball": "volleyball"
}

if st.button(f"🔍 Показать матчи: {sport_choice} ({selected_date_label})"):
    sport_type = sport_map[sport_choice]
    # Используем запрос по дате вместо LIVE
    url = f"https://livescore6.p.rapidapi.com/{sport_type}/list-by-date"
    
    query_params = {"Category": "general", "Date": selected_date_value}
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "livescore6.p.rapidapi.com"
    }

    with st.spinner('Загрузка расписания...'):
        try:
            response = requests.get(url, headers=headers, params=query_params)
            data = response.json()
            
            if 'Stages' in data and data['Stages']:
                for stage in data['Stages']:
                    with st.expander(f"📍 {stage.get('Snm')} ({stage.get('Cnm')})"):
                        for event in stage.get('Events', []):
                            home = event.get('T1', [{}])[0].get('Nm', 'Команда 1')
                            away = event.get('T2', [{}])[0].get('Nm', 'Команда 2')
                            # Если матч идет - покажет счет, если нет - время начала
                            score_home = event.get('Tr1', '')
                            score_away = event.get('Tr2', '')
                            status = event.get('Eps', 'Ожидание')
                            
                            if score_home != '':
                                st.write(f"🕒 {status} | **{home}** {score_home} : {score_away} **{away}**")
                            else:
                                start_time = str(event.get('Esd'))[8:10] + ":" + str(event.get('Esd'))[10:12]
                                st.write(f"📅 Начало в {start_time} | {home} vs {away}")
            else:
                st.info(f"На {selected_date_label} матчей по виду {sport_choice} не найдено.")
        except Exception as e:
            st.error(f"Ошибка: {e}")


