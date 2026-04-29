
import streamlit as st
import requests
from datetime import datetime, timedelta

# Твой ключ (проверь, чтобы не было лишних пробелов)
API_KEY = "689705cae4msh2ab829df81c7ef9p1a2f07jsn17bc2f216264"

st.set_page_config(page_title="Zenith AI Pro", page_icon="🏆", layout="wide")
st.title("🏆 Zenith AI: Omni-Сканер 3.0")

# --- БОКОВАЯ ПАНЕЛЬ ---
st.sidebar.header("⚙️ Настройки")

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

# --- КНОПКА ЗАПУСКА ---
if st.button(f"🚀 Запустить поиск: {sport_choice}"):
    sport_type = sport_map[sport_choice]
    url = f"https://livescore6.p.rapidapi.com/{sport_type}/list-by-date"
    
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "livescore6.p.rapidapi.com"
    }
    
    # ОСТАВЛЯЕМ ТОЛЬКО ДАТУ (БЕЗ КАТЕГОРИЙ)
    params = {"Date": selected_date}

    with st.spinner('Подключаюсь к серверу...'):
        try:
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            
            # Если данные пришли успешно
            if 'Stages' in data and data['Stages']:
                st.success(f"Найдено событий на {selected_label}")
                for stage in data['Stages']:
                    with st.expander(f"📍 {stage.get('Snm')} ({stage.get('Cnm', 'World')})"):
                        for event in stage.get('Events', []):
                            home = event.get('T1', [{}])[0].get('Nm', 'Команда 1')
                            away = event.get('T2', [{}])[0].get('Nm', 'Команда 2')
                            
                            score_h = event.get('Tr1')
                            score_a = event.get('Tr2')
                            status = event.get('Eps', 'NS')
                            
                            if score_h is not None:
                                st.write(f"🕒 **{status}** | {home} **{score_h} : {score_a}** {away}")
                            else:
                                raw_time = str(event.get('Esd', '00000000000000'))
                                start_t = f"{raw_time[8:10]}:{raw_time[10:12]}" if len(raw_time) >= 12 else "--:--"
                                st.write(f"📅 {start_t} | {home} vs {away}")
            else:
                # Если сервер ответил, но матчей нет
                st.info(f"На {selected_label} матчей по {sport_choice} не найдено.")
                # Вывод сообщения от сервера для отладки
                if 'Message' in data:
                    st.warning(f"Сервер сообщает: {data['Message']}")
                
        except Exception as e:
            st.error(f"Ошибка связи: {e}")
