
import streamlit as st
import requests

# Твой ключ остается тем же
API_KEY = "689705cae4msh2ab829df81c7ef9p1a2f07jsn17bc2f216264"

st.title("🏆 Zenith AI: Перезагрузка")

# Простейший тест связи
if st.button("Проверить соединение"):
    url = "https://livescore6.p.rapidapi.com/soccer/list-live" # Только LIVE матчи
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "livescore6.p.rapidapi.com"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            st.success("Связь установлена!")
            st.write(data) # Выведет сырые данные, чтобы мы поняли, что они вообще идут
        else:
            st.error(f"Сервер отклонил запрос. Код: {response.status_code}")
            st.write(response.text)
    except Exception as e:
        st.error(f"Ошибка: {e}")
