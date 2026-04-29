
import streamlit as st
import requests
from datetime import datetime, timedelta
import pytz

# Твой ключ (без пробелов)
API_KEY = "689705cae4msh2ab829df81c7ef9p1a2f07jsn17bc2f216264"

st.set_page_config(page_title="Zenith AI Pro", page_icon="🏆", layout="wide")
st.title("🏆 Zenith AI: Omni-Сканер 3.0")

# --- НАСТРОЙКИ ВРЕМЕНИ (Казахстан) ---
kz_tz = pytz.timezone('Asia/Almaty')
now_kz = datetime.now(kz_tz)

# --- БОКОВАЯ ПАНЕЛЬ ---
st.sidebar.header("⚙️ Настройки поиска")

sport_choice = st.sidebar.selectbox(
    "Вид спорта:",
    ["Football", "Hockey", "Tennis", "Basketball", "Volleyball"]
)

# Ручной выбор даты для точности
selected_date_dt = st.sidebar.date_input("Выберите дату матчей:", now_kz)
selected_date = selected_date_dt.strftime('%Y%m%d')

sport_map = {
    "Football": "soccer",
    "Hockey": "hockey",
    "Tennis": "tennis",
    "Basketball": "basketball",
    "Volleyball": "volleyball"
}

# --- КНОПКА ЗАПУСКА ---
if st.button(f"🚀 Просканировать {sport_choice}"):
    sport_type = sport_map[sport_choice]
    url = f"https://livescore6.p.rapidapi.com/{sport_type}/list-by-date"
    
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "livescore6.p.rapidapi.com"
    }
    
    # Прямой запрос по дате без лишних фильтров
    params = {"Date": selected_date}

    with st.spinner(f'Стучусь на сервер Livescore за данными на {selected_date}...'):
        try:
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            
            if 'Stages' in data and data['Stages']:
                st.success(f"Найдено турниров: {len(data['Stages'])}")
                
                for stage in data['Stages']:
                    league_name = stage.get('Snm', 'Лига')
                    country = stage.get('Cnm', 'Мир')
                    
                    with st.expander(f"🏟 {league_name} ({country})"):
                        for event in stage.get('Events', []):
                            # Команды
                            home = event.get('T1', [{}])[0].get('Nm', 'Команда 1')
                            away = event.get('T2', [{}])[0].get('Nm', 'Команда 2')
                            
                            # Счет и Статус
                            score_h = event.get('Tr1')
                            score_a = event.get('Tr2')
                            status = event.get('Eps', 'NS')
                            
                            if score_h is not None:
                                # Матч завершен или идет прямо сейчас
                                st.write(f"🕒 **{status}** | **{home}** {score_h} : {score_a} **{away}**")
                            else:
                                # Матч еще не начался
                                raw_time = str(event.get('Esd', '00000000000000'))
                                start_t = f"{raw_time[8:10]}:{raw_time[10:12]}" if len(raw_time) >= 12 else "Время уточняется"
                                st.write(f"📅 {start_t} | {home} vs {away}")
            else:
                st.info(f"На дату {selected_date} матчей по {sport_choice} в базе не найдено.")
                if 'Message' in data:
                    st.warning(f"Ответ сервера: {data['Message']}")
                
        except Exception as e:
            st.error(f"Произошла ошибка связи: {e}")
