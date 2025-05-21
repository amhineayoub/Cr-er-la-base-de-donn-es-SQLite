import streamlit as st
import sqlite3
import pandas as pd

# Connexion à la base de données
conn = sqlite3.connect("hotel.db")
cur = conn.cursor()

st.set_page_config(page_title="Système de Réservation d'Hôtel", layout="wide")
st.title("🏨 Système de Réservation d'Hôtel")

# Menu de navigation
menu = ["Accueil", "Réservations", "Clients", "Chambres", "Évaluations"]
choice = st.sidebar.selectbox("Menu", menu)

# ACCUEIL
if choice == "Accueil":
    st.subheader("📊 Statistiques générales")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        cur.execute("SELECT COUNT(*) FROM Client")
        st.metric("Nombre de clients", cur.fetchone()[0])
    
    with col2:
        cur.execute("SELECT COUNT(*) FROM Reservation")
        st.metric("Nombre de réservations", cur.fetchone()[0])

    with col3:
        cur.execute("SELECT COUNT(*) FROM Chambre")
        st.metric("Nombre de chambres", cur.fetchone()[0])

    st.markdown("---")
    st.subheader("Aperçu des hôtels")
    df_hotels = pd.read_sql_query("SELECT * FROM Hotel", conn)
    st.dataframe(df_hotels)

# RÉSERVATIONS
elif choice == "Réservations":
    st.subheader("📅 Liste des réservations")
    df_res = pd.read_sql_query("""
        SELECT R.id_reservation, R.date_arrivee, R.date_depart, C.nom_complet, CH.numero, H.ville
        FROM Reservation R
        JOIN Client C ON R.id_client = C.id_client
        JOIN Chambre CH ON R.id_chambre = CH.id_chambre
        JOIN Hotel H ON CH.id_hotel = H.id_hotel
    """, conn)
    st.dataframe(df_res)

# CLIENTS
elif choice == "Clients":
    st.subheader("👤 Liste des clients")
    df_clients = pd.read_sql_query("SELECT * FROM Client", conn)
    st.dataframe(df_clients)

    st.markdown("### Ajouter un nouveau client")
    with st.form("form_client"):
        nom = st.text_input("Nom complet")
        adresse = st.text_input("Adresse")
        ville = st.text_input("Ville")
        code_postal = st.number_input("Code postal", step=1)
        email = st.text_input("Email")
        telephone = st.text_input("Téléphone")
        submitted = st.form_submit_button("Ajouter")
        if submitted:
            cur.execute("INSERT INTO Client (adresse, ville, code_postal, email, telephone, nom_complet) VALUES (?, ?, ?, ?, ?, ?)",
                        (adresse, ville, code_postal, email, telephone, nom))
            conn.commit()
            st.success("✅ Client ajouté avec succès")

# CHAMBRES
elif choice == "Chambres":
    st.subheader("🛏️ Liste des chambres")
    df_chambres = pd.read_sql_query("""
        SELECT CH.id_chambre, CH.numero, CH.etage, TC.type, TC.tarif, H.ville
        FROM Chambre CH
        JOIN Type_Chambre TC ON CH.id_type = TC.id_type
        JOIN Hotel H ON CH.id_hotel = H.id_hotel
    """, conn)
    st.dataframe(df_chambres)

# ÉVALUATIONS
elif choice == "Évaluations":
    st.subheader("⭐ Avis des clients")
    df_eval = pd.read_sql_query("""
        SELECT E.date_arrivee, E.note, E.texte, C.nom_complet
        FROM Evaluation E
        JOIN Client C ON E.id_client = C.id_client
        ORDER BY E.date_arrivee DESC
    """, conn)
    st.dataframe(df_eval)

    st.markdown("### Ajouter une évaluation")
    with st.form("form_eval"):
        client_id = st.number_input("ID client", min_value=1, step=1)
        date_eval = st.date_input("Date d’arrivée")
        note = st.slider("Note", 1, 5)
        texte = st.text_area("Commentaire")
        submit_eval = st.form_submit_button("Soumettre")
        if submit_eval:
            cur.execute("INSERT INTO Evaluation (date_arrivee, note, texte, id_client) VALUES (?, ?, ?, ?)",
                        (str(date_eval), note, texte, client_id))
            conn.commit()
            st.success("✅ Évaluation enregistrée")

