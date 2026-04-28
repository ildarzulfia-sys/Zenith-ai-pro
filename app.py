
import streamlit as st
import requests
from datetime import datetime

API_KEY = "689705cae4msh2ab829df81c7ef9p1a2f07jsn17bc2f216264"

st.set_page_config(page_title="Zenith AI Live", page_icon="⚽️")
st.title("🛡 Zenith AI: Live Сканер")

if st.button("🔍 Найти активные матчи"):
    # Используем запрос матчей на сегодня
    today = datetime.now().strftime("%Y%m%d")
    url = "https://free-api-live-football-data.p.rapidapi.com/football-all-matches-by-date"
    
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
    }
    
    params = {"date": today}
    
    with st.spinner('Запрашиваю список игр...'):
        try:
            r = requests.get(url, headers=headers, params=params)
            data = r.json()
            
            if data.get('status') == 'success' and data.get('response'):
                matches = data['response']['matches']
                live_matches = [m for m in matches if m['status']['type'] == 'inprogress']
                
                if live_matches:
                    st.success(f"В эфире матчей: {len(live_matches)}")
                    for match in live_matches[:15]:
                        home = match['home_team']['name']
                        away = match['away_team']['name']
                        score = f"{match['home_score']['current']} : {match['away_score']['current']}"
                        time = match['status']['description']
                        st.write(f"⏱ {time} | **{home}** {score} **{away}**")
                else:
                    st.warning("В бесплатной базе сейчас нет активных LIVE-игр. Попробуй позже.")
            else:
                st.error(f"API ответил: {data.get('message', 'Ошибка данных')}")
        except Exception as e:
            st.error(f"Критическая ошибка: {e}")
