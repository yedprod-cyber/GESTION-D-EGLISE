import streamlit as st
import pandas as pd
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="Gestion de l'Église", page_icon="⛪", layout="wide")

# Initialisation des bases de données en mémoire (Simulées avec la session Streamlit)
if "fideles" not in st.session_state:
    st.session_state.fideles = pd.DataFrame(columns=["ID", "Nom", "Prénom", "Téléphone", "Statut"])
if "cotisations" not in st.session_state:
    st.session_state.cotisations = pd.DataFrame(columns=["Fidèle", "Montant (FCFA)", "Date", "Motif"])
if "programmes" not in st.session_state:
    st.session_state.programmes = pd.DataFrame(columns=["Événement / Fête", "Date", "Heure", "Description"])
if "annonces" not in st.session_state:
    st.session_state.annonces = []

# TITRE PRINCIPAL
st.title("⛪ Système de Gestion de l'Église")
st.markdown("---")

# BARRE LATÉRALE : MENU
menu = st.sidebar.radio(
    "Navigation",
    ["Tableau de bord", "👤 Fidèles", "💰 Cotisations & Dîmes", "📅 Programmes & Fêtes", "📢 Annonces"]
)

# 1. TABLEAU DE BORD
if menu == "Tableau de bord":
    st.subheader("📊 Vue d'ensemble")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Fidèles", len(st.session_state.fideles))
    with col2:
        total_cotisations = st.session_state.cotisations["Montant (FCFA)"].sum()
        st.metric("Total Cotisations", f"{total_cotisations:,} FCFA")
    with col3:
        st.metric("Programmes à venir", len(st.session_state.programmes))

    st.markdown("### 📢 Dernières Annonces")
    if st.session_state.annonces:
        for ann in reversed(st.session_state.annonces):
            st.info(f"**{ann['date']}** : {ann['texte']}")
    else:
        st.write("Aucune annonce pour le moment.")

# 2. GESTION DES FIDÈLES
elif menu == "👤 Fidèles":
    st.subheader("👥 Gestion des Fidèles")
    
    # Formulaire d'ajout
    with st.expander("➕ Ajouter un nouveau fidèle"):
        with st.form("form_fidele"):
            nom = st.text_input("Nom")
            prenom = st.text_input("Prénom")
            tel = st.text_input("Numéro de Téléphone")
            statut = st.selectbox("Statut", ["Membre actif", "Nouveau converti", "Visiteur", "Ancien / Responsable"])
            soumettre = st.form_submit_button("Enregistrer le fidèle")
            
            if soumettre and nom and prenom:
                nouvel_id = len(st.session_state.fideles) + 1
                nouvel_enregistrement = pd.DataFrame([{"ID": nouvel_id, "Nom": nom, "Prénom": prenom, "Téléphone": tel, "Statut": statut}])
                st.session_state.fideles = pd.concat([st.session_state.fideles, nouvel_enregistrement], ignore_index=True)
                st.success(f"{prenom} {nom} a été ajouté avec succès !")

    # Affichage de la liste
    st.markdown("### 📋 Liste des membres")
    if not st.session_state.fideles.empty:
        st.dataframe(st.session_state.fideles, use_container_width=True)
    else:
        st.warning("Aucun fidèle enregistré pour le moment.")

# 3. GESTION DES COTISATIONS
elif menu == "💰 Cotisations & Dîmes":
    st.subheader("💵 Suivi des Contributions Financières")
    
    if st.session_state.fideles.empty:
        st.error("Veuillez d'abord ajouter des fidèles pour pouvoir enregistrer une cotisation.")
    else:
        with st.form("form_cotisation"):
            liste_fideles = st.session_state.fideles["Prénom"] + " " + st.session_state.fideles["Nom"]
            fidele_selectionne = st.selectbox("Sélectionner le fidèle", liste_fideles)
            montant = st.number_input("Montant (FCFA)", min_value=0, step=500)
            motif = st.selectbox("Motif", ["Dîme", "Offrande", "Action de grâce", "Soutien Fête / Événement", "Travaux Église"])
            date_cot = st.date_input("Date du versement")
            soumettre_cot = st.form_submit_button("Enregistrer le paiement")
            
            if soumettre_cot and montant > 0:
                nouvelle_cot = pd.DataFrame([{"Fidèle": fidele_selectionne, "Montant (FCFA)": montant, "Date": str(date_cot), "Motif": motif}])
                st.session_state.cotisations = pd.concat([st.session_state.cotisations, nouvelle_cot], ignore_index=True)
                st.success(f"Cotisation de {montant} FCFA enregistrée pour {fidele_selectionne} !")

    st.markdown("### 📜 Historique des paiements")
    if not st.session_state.cotisations.empty:
        st.dataframe(st.session_state.cotisations, use_container_width=True)
    else:
        st.write("Aucun paiement enregistré.")

# 4. GESTION DES PROGRAMMES ET FÊTES
elif menu == "📅 Programmes & Fêtes":
    st.subheader("🗓️ Calendrier des Cultes, Fêtes et Événements")
    
    with st.expander("➕ Planifier un événement / une fête"):
        with st.form("form_prog"):
            nom_evenement = st.text_input("Nom de l'événement (ex: Culte de Moisson, Fête de la Jeunesse, Veillée)")
            date_ev = st.date_input("Date")
            heure_ev = st.time_input("Heure de début")
            desc_ev = st.text_area("Description / Prédicateur invité")
            soumettre_prog = st.form_submit_button("Planifier")
            
            if soumettre_prog and nom_evenement:
                nouveau_prog = pd.DataFrame([{"Événement / Fête": nom_evenement, "Date": str(date_ev), "Heure": str(heure_ev), "Description": desc_ev}])
                st.session_state.programmes = pd.concat([st.session_state.programmes, nouveau_prog], ignore_index=True)
                st.success(f"L'événement '{nom_evenement}' a été planifié !")

    st.markdown("### 📋 Liste des programmes")
    if not st.session_state.programmes.empty:
        st.dataframe(st.session_state.programmes, use_container_width=True)
    else:
        st.write("Aucun événement prévu au calendrier.")

# 5. GESTION DES ANNONCES
elif menu == "📢 Annonces":
    st.subheader("📣 Annonces Officielles de l'Église")
    
    with st.form("form_annonce"):
        texte_annonce = st.text_area("Rédiger l'annonce à communiquer aux fidèles")
        soumettre_ann = st.form_submit_button("Publier l'annonce")
        
        if soumettre_ann and texte_annonce:
            date_actuelle = datetime.now().strftime("%d/%m/%Y %H:%M")
            st.session_state.annonces.append({"date": date_actuelle, "texte": texte_annonce})
            st.success("Annonce publiée sur le tableau de bord !")
