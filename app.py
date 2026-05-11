import streamlit as st
import requests 
import time 
import streamlit.components.v1 as components 

# Sayfa ayarları (Sadece BİR KERE yazılmalı)
st.set_page_config(page_title="UPS Delivery Panel", page_icon="📦", layout="centered")

# --- ALTAR YENİ: MOBİL UYGULAMA (PWA) DESTEĞİ ---
# Linkleri direkt senin GitHub deponun içindeki dosyalara yönlendirdim
st.markdown(
    """
    <link rel="manifest" href="https://raw.githubusercontent.com/ozoglualtar2-cloud/ups-kurye-app/main/manifest.json">
    <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/ozoglualtar2-cloud/ups-kurye-app/main/logo.png">
    """,
    unsafe_allow_html=True
)
# --- ALTAR YENİ BİTİŞ ---

# --- GÜVENLİK KAPISI (LOGIN SİSTEMİ) ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.markdown('<h1 style="color:#5A3418; text-align:center;">Delivery Login</h1>', unsafe_allow_html=True)
    
    # Kullanıcıdan bilgileri alıyoruz
    kullanici_adi = st.text_input("Username")
    sifre = st.text_input("Password", type="password") 
    
    if st.button("Login", use_container_width=True):
        if kullanici_adi == "driver1" and sifre == "abcd": 
            st.session_state["logged_in"] = True
            st.rerun() 
        else:
            st.error("Invalid Username or Password!")
            
    st.stop() 

# --- ASIL UYGULAMA ---
st.markdown('<h1 style="color:#5A3418;">Delivery Panel</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#5A3418; font-size: 18px;">Today\'s assigned routes are shown below.</p>', unsafe_allow_html=True)

if st.button("🔄 Refresh Route", use_container_width=True):
    st.rerun()

url = f"https://api.jsonbin.io/v3/b/6a00cd28adc21f119a7e6bb9/latest?_t={time.time()}"
headers = {
    "X-Master-Key": "$2a$10$T72jRhqyg.phWLbuSxdMVe.PQpnDi8BN6pEU/Sa7KaJvevaHK5eyO" 
}

try:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        hazir_rota = response.json().get("record", {})
        
        distance_info = hazir_rota.get("total_distance", "")
        
        st.markdown(f"<p style='color:#5A3418; font-size:18px;'><b>Distance:</b> {distance_info}</p>", unsafe_allow_html=True)
        
        if "map_html" in hazir_rota and hazir_rota["map_html"]:
            st.markdown("<p style='color:#5A3418; font-size:18px; margin-top:20px;'><b>Google Maps Route View:</b></p>", unsafe_allow_html=True)
            components.html(hazir_rota["map_html"], height=400)

        if "google_links" in hazir_rota and hazir_rota["google_links"]:
            st.markdown("<p style='color:#5A3418; font-size:18px; margin-top:20px;'><b>Google Maps Road Directions:</b></p>", unsafe_allow_html=True)
            for vehicle, link_data in hazir_rota["google_links"].items():
                url_link = link_data["url"]
                st.markdown(f"**Vehicle {vehicle}:** [📍 Open in Google Maps]({url_link})")
        
    else:
        st.warning("Henüz yeni bir rota oluşturulmadı veya anahtar hatalı.")
except Exception as e:
    st.error("Buluta bağlanılamadı, internetinizi kontrol edin.")
