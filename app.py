
5import streamlit as st
import requests

# ВСТАВЬ СЮДА СВОЙ НОВЫЙ КЛЮЧ
API_KEY = "ТВОЙ_НОВЫЙ_КЛЮЧ_ОТ_API_FOOTBALL"

st.set_page_config(page_title="Zenith AI Pro", page_icon="🏆")
st.title("🔥 Zenith AI: Элитный Сканер")

if st.button("🚀 Найти топ-матчи LIVE"):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "api-football-v1.p.rapidapi.com"
    }
    # Запрашиваем только живые матчи (live=all)
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
                st.warning("В данный момент матчей не найдено. Проверь подписку на API.")
        except Exception as e:
            st.error(f"Ошибка: {e}")
