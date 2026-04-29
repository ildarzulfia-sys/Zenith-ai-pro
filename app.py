
import streamlit as st
import requests
from datetime import datetime
import pytz

# Твой ключ
API_KEY = "689705cae4msh2ab829df81c7ef9p1a2f07jsn17bc2f216264"

st.set_page_config(page_title="Zenith AI Pro", page_icon="🏆", layout="wide")
st.title("🏆 Zenith AI: Omni-Сканер 3.0")

# Настройка времени
kz_tz = pytz.timezone('Asia/Almaty')
now_kz = datetime.now(kz_tz)

st.sidebar.header("⚙️ Настройки")

# Важно: Названия для API теперь другие
sport_map = {
    "Football": "soccer",
    "Hockey": "hockey",
    "Tennis": "tennis",
    "Basketball": "basketball",
    "Volleyball": "volleyball"
}

sport_choice = st.sidebar.selectbox("Вид спорта:", list(sport_map.keys()))
selected_date_dt = st.sidebar.date_input("Выберите дату:", now_kz)
selected_date = selected_date_dt.strftime('%Y%m%d')

if st.button(f"🚀 Найти матчи: {sport_choice}"):
    # НОВЫЙ URL (общий для всех видов спорта)
    url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-date"
    
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "livescore6.p.rapidapi.com"
    }
    
    # Теперь Category — это и есть вид спорта!
    params = {
        "Category": sport_map[sport_choice], 
        "Date": selected_date
    }

    with st.spinner('Связываюсь с глобальной базой...'):
        try:
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            
            if 'Stages' in data and data['Stages']:
                st.success(f"Найдено турниров: {len(data['Stages'])}")
                for stage in data['Stages']:
                    with st.expander(f"📍 {stage.get('Snm')} ({stage.get('Cnm', 'World')})"):
                        for event in stage.get('Events', []):
                            home = event.get('T1', [{}])[0].get('Nm', 'Команда 1')
                            away = event.get('T2', [{}])[0].get('Nm', 'Команда 2')
                            score_h = event.get('Tr1')
                            score_a = event.get('Tr2')
                            status = event.get('Eps', 'NS')
                            
                            if score_h is not None:
                                st.write(f"🕒 **{status}** | **{home}** {score_h}:{score_a} **{away}**")
                            else:
                                raw_time = str(event.get('Esd', '00000000000000'))
                                start_t = f"{raw_time[8:10]}:{raw_time[10:12]}"
                                st.write(f"📅 {start_t} | {home} vs {away}")
            else:
                st.info("На эту дату матчей в бесплатной базе нет. Попробуй другую дату.")
                if 'message' in data:
                    st.warning(f"Ошибка API: {data['message']}")
        except Exception as e:
            st.error(f"Ошибка: {e}")
