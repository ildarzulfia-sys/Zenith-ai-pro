import streamlit as st
import requests

# Твой универсальный ключ
API_KEY = "689705cae4msh2ab829df81c7ef9p1a2f07jsn17bc2f216264"

st.set_page_config(page_title="Zenith AI Omni", page_icon="🏆", layout="wide")
st.title("🏆 Zenith AI: Универсальный LIVE-Сканер")

# Боковая панель для выбора спорта
sport_choice = st.sidebar.selectbox(
    "Выберите вид спорта:",
    ["Football", "Hockey", "Tennis", "Basketball"]
)

# Словарь для связи с API (подстраиваем под Livescore)
sport_map = {
    "Football": "soccer",
    "Hockey": "hockey",
    "Tennis": "tennis",
    "Basketball": "basketball"
}

st.header(f"📡 Мониторинг: {sport_choice}")

if st.button(f"🚀 Найти активные матчи"):
    sport_type = sport_map[sport_choice]
    # Универсальный адрес Livescore API
    url = f"https://livescore6.p.rapidapi.com/{sport_type}/list-live"
    
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "livescore6.p.rapidapi.com"
    }

    with st.spinner(f'Сканирую планету на наличие матчей ({sport_choice})...'):
        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            
            # Логика вывода данных из Livescore API
            if 'Stages' in data:
                stages = data['Stages']
                st.success(f"Найдено лиг в эфире: {len(stages)}")
                
                for stage in stages:
                    league_name = stage.get('Snm', 'Турнир')
                    st.subheader(f"📍 {league_name}")
                    
                    for event in stage.get('Events', []):
                        home = event.get('T1', [{}])[0].get('Nm', 'Команда 1')
                        away = event.get('T2', [{}])[0].get('Nm', 'Команда 2')
                        score = f"{event.get('Tr1', '0')} : {event.get('Tr2', '0')}"
                        time = event.get('Eps', 'LIVE')
                        
                        with st.expander(f"➕ {home} {score} {away} ({time})"):
                            st.write(f"📊 Статус матча: Идет сейчас")
            else:
                st.info(f"В данный момент активных LIVE-матчей по виду {sport_choice} не найдено.")
                
        except Exception as e:
            st.error(f"Ошибка подключения к Livescore API: {e}")

    

