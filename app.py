
import streamlit as st
import requests

API_KEY = "689705cae4msh2ab829df81c7ef9p1a2f07jsn17bc2f216264"

st.set_page_config(page_title="Zenith AI Pro", page_icon="⚽️")
st.title("🏆 Zenith AI: Сканер")

if st.button("🚀 Запустить"):
    # Используем проверенный эндпоинт для лайв матчей
    url = "https://free-api-live-football-data.p.rapidapi.com/football-current-live"
    
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
    }
    
    with st.spinner('Поиск матчей...'):
        try:
            response = requests.get(url, headers=headers)
            res_data = response.json()
            
            # Проверяем, есть ли данные в ответе
            if res_data.get('status') == 'success' and res_data.get('data'):
                games = res_data['data']
                st.success(f"Найдено матчей: {len(games)}")
                for g in games:
                    st.write(f"⚽ {g['home_team']['name']} vs {g['away_team']['name']} | Счет: {g['score']}")
            else:
                st.info("В базе API сейчас нет активных LIVE-матчей. Попробуй через 30-60 минут.")
        except Exception as e:
            st.error(f"Ошибка: {e}")
