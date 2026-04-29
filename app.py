
import streamlit as st
import requests
from datetime import datetime, timedelta

# Твой ключ
API_KEY = "689705cae4msh2ab829df81c7ef9p1a2f07jsn17bc2f216264"

st.set_page_config(page_title="Zenith AI Pro", page_icon="🏆", layout="wide")
st.title("🏆 Zenith AI: Omni-Сканер 3.0")

# Настройки в сайдбаре
sport_choice = st.sidebar.selectbox(
    "Вид спорта:",
    ["Football", "Hockey", "Tennis", "Basketball", "Volleyball"]
)

today = datetime.now()
date_options = {
    "⏪ Вчера": (today - timedelta(days=1)).strftime('%Y%m%d'),
    "📍 Сегодня": today.strftime('%Y%m%d'),
    "⏩ Завтра": (today + timedelta(days=1)).strftime('%Y%m%d')
}
selected_label = st.sidebar.radio("Период:", list(date_options.keys()), index=1)
selected_date = date_options[selected_label]

sport_map = {
    "Football": "soccer",
    "Hockey": "hockey",
    "Tennis": "tennis",
    "Basketball": "basketball",
    "Volleyball": "volleyball"
}

if st.button(f"🔍 Сканировать {sport_choice}"):
    sport_type = sport_map[sport_choice]
    
    # ВАЖНО: Измененный URL для list-by-date
    url = f"https://livescore6.p.rapidapi.com/{sport_type}/list-by-date"
    
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "livescore6.p.rapidapi.com"
    }
    
    # Убираем лишние фильтры, оставляем только дату
    params = {"Date": selected_date}

    with st.spinner('Запрос к базе данных...'):
        try:
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            
            # Проверка структуры ответа
            if 'Stages' in data and data['Stages']:
                for stage in data['Stages']:
                    with st.expander(f"📍 {stage.get('Snm')} ({stage.get('Cnm', 'World')})"):
                        for event in stage.get('Events', []):
                            home = event.get('T1', [{}])[0].get('Nm', 'Команда 1')
                            away = event.get('T2', [{}])[0].get('Nm', 'Команда 2')
                            
                            # Счет
                            score_h = event.get('Tr1')
                            score_a = event.get('Tr2')
                            status = event.get('Eps', 'NS')
                            
                            if score_h is not None:
                                st.write(f"🕒 **{status}** | **{home}** {score_h} : {score_a} **{away}**")
                            else:
                                # Время начала
                                raw_time = str(event.get('Esd', '00000000000000'))
                                start_t = f"{raw_time[8:10]}:{raw_time[10:12]}" if len(raw_time) >= 12 else "--:--"
                                st.write(f"📅 {start_t} | {home} vs {away}")
            else:
                # Вывод для отладки, если данных нет
                st.info(f"На {selected_label} матчей по {sport_choice} не найдено.")
                if 'Message' in data:
                    st.warning(f"Сообщение от сервера: {data['Message']}")
                
        except Exception as e:
            st.error(f"Ошибка связи: {e}")
