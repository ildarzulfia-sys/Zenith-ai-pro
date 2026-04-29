
import streamlit as st
import requests

# Твой универсальный ключ RapidAPI
API_KEY = "689705cae4msh2ab829df81c7ef9p1a2f07jsn17bc2f216264"

st.set_page_config(page_title="Zenith AI Pro", page_icon="⚽️")
st.title("🏆 Zenith AI: Новый Сканер")

if st.button("🚀 Запустить поиск LIVE"):
    # URL нового сервиса
    url = "https://free-api-live-football-data.p.rapidapi.com/football-current-live"
    
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
    }
    
    with st.spinner('Подключаюсь к новому серверу...'):
        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            
            if data.get('status') == 'success' and 'data' in data:
                games = data['data']
                st.success(f"Найдено {len(games)} матчей в прямом эфире!")
                
                for game in games:
                    home = game['home_team']['name']
                    away = game['away_team']['name']
                    score = game['score']
                    league = game['league']['name']
                    time = game.get('time', 'LIVE')
                    
                    with st.expander(f"🏟 {league}: {home} {score} {away}"):
                        st.write(f"⏱ **Время:** {time}")
                        st.write(f"📊 **Статус:** Матч идет в реальном времени")
            else:
                st.warning("В данный момент активных матчей не найдено или проверь подписку.")
        except Exception as e:
            st.error(f"Ошибка связи: {e}")
