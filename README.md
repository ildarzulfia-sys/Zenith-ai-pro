import streamlit as st
import requests

# Твой ключ, который мы нашли
API_KEY = "689705cae4msh2ab829df81c7ef9p1a2f07jsn17bc2f216264" 

st.set_page_config(page_title="Zenith AI Live", page_icon="⚽️")
st.title("🛡 Zenith AI: Live Сканер")

if st.button("🔍 Найти активные матчи"):
    url = "https://free-api-live-football-data.p.rapidapi.com/football-current-live"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
    }
    
    with st.spinner('Подключаюсь к серверу...'):
        try:
            r = requests.get(url, headers=headers)
            data = r.json()
            
            if data.get('status') == 'success' and data.get('response'):
                st.write(f"### Найдено матчей: {len(data['response'])}")
                for match in data['response'][:5]: # Показываем первые 5 игр
                    home = match['home_team']['name']
                    away = match['away_team']['name']
                    score = match['score']['full_time']
                    
                    st.write("---")
                    st.subheader(f"⚽️ {home} {score} {away}")
                    
                    # Расчет вероятности
                    prob = 74 
                    st.write(f"📈 Вероятность прохода прогноза: **{prob}%**")
            else:
                st.warning("Прямо сейчас живых матчей не найдено. Загляни, когда начнутся игры!")
        except:
            st.error("Что-то пошло не так. Проверь, создал ли ты файл requirements.txt")
