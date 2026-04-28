
import streamlit as st
import requests

# Твой рабочий ключ для API
API_KEY = "689705cae4msh2ab829df81c7ef9p1a2f07jsn17bc2f216264"

st.set_page_config(page_title="Zenith AI Pro", page_icon="🏆")
st.title("🔥 Zenith AI: Элитный Сканер")

if st.button("🚀 Найти топ-матчи LIVE"):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "api-football-v1.p.rapidapi.com"
    }
    # Запрашиваем только живые матчи
    params = {"live": "all"}
    
    with st.spinner('Сканирую мировые стадионы...'):
        try:
            r = requests.get(url, headers=headers, params=params)
            data = r.json()
            
            if data.get('response'):
                st.success(f"Найдено {len(data['response'])} активных игр!")
                for item in data['response']:
                    league = item['league']['name']
                    home = item['teams']['home']['name']
                    away = item['teams']['away']['name']
                    goals_home = item['goals']['home']
                    goals_away = item['goals']['away']
                    elapsed = item['fixture']['status']['elapsed']
                    
                    # Красивый вывод каждой игры
                    with st.container():
                        st.markdown(f"**{league}** — {elapsed}' минута")
                        st.subheader(f"{home} {goals_home} : {goals_away} {away}")
                        st.divider()
            else:
                # Если подписка не активирована, API пришлет сообщение об ошибке
                message = data.get('message', 'В данный момент активных LIVE-матчей не найдено.')
                st.warning(f"Результат: {message}")
                st.info("Если видишь ошибку подписки, нажми 'Subscribe' на странице API-Football в RapidAPI.")
        except Exception as e:
            st.error(f"Критическая ошибка: {e}")
