            
import streamlit as st
import requests

# Твой ключ и настройки
API_KEY = "689705cae4msh2ab829df81c7ef9p1a2f07jsn17bc2f216264"

st.set_page_config(page_title="Zenith AI Pro", page_icon="⚽️")
st.title("🏆 Zenith AI: Сканер LIVE")

if st.button("🚀 Запустить поиск"):
    # Правильная ссылка без двойных "url ="
    url = "https://free-api-live-football-data.p.rapidapi.com/football-current-live"
    
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
    }
    
    with st.spinner('Связываюсь с футбольным сервером...'):
        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            
            if data.get('status') == 'success' and 'data' in data:
                games = data['data']
                if not games:
                    st.info("Сейчас нет активных матчей. Попробуй чуть позже!")
                else:
                    st.success(f"Найдено {len(games)} матчей в эфире!")
                    for game in games:
                        home = game['home_team']['name']
                        away = game['away_team']['name']
                        score = game.get('score', '0:0')
                        league = game['league']['name']
                        with st.expander(f"🏟 {league}: {home} {score} {away}"):
                            st.write(f"📊 Статус: LIVE")
            else:
                st.warning("Сервер ответил, но матчи не найдены. Проверь подписку на RapidAPI.")
        except Exception as e:
            st.error(f"Ошибка связи: {e}")
