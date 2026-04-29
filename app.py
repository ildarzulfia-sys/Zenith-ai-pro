
import streamlit as st
import requests

# Твой ключ и настройки
API_KEY = "689705cae4msh2ab829df81c7ef9p1a2f07jsn17bc2f216264"

st.set_page_config(page_title="Zenith AI Pro", page_icon="⚽️")
st.title("🏆 Zenith AI: Новый Сканер")

if st.button("🚀 Запустить"):
    # Ссылка для проверки всех лиг
    url = "https://free-api-live-football-data.p.rapidapi.com/football-all-leagues"
    
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
    }
    
    with st.spinner('Подключаюсь к новому серверу...'):
        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            
            if data.get('status') == 'success' and 'data' in data:
                items = data['data']
                st.success(f"Связь есть! Найдено {len(items)} категорий.")
                
                for item in items[:20]:  # Покажем первые 20 для теста
                    name = item.get('name', 'Без названия')
                    st.write(f"✅ Доступно: {name}")
            else:
                st.warning("Сервер ответил, но данных нет. Проверь подписку на RapidAPI.")
        except Exception as e:
            st.error(f"Ошибка связи: {e}")
