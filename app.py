import streamlit as st
import pandas as pd
from datetime import datetime
import io

# Configuration de la page internet
st.set_page_config(page_title="Gestion de l'Église", page_icon="⛪", layout="wide")

# 1. SYSTÈME DE SÉCURITÉ (CONNEXION)
if "authentifie" not in st.session_state:
    st.session_state.authentifie = False

if not st.session_state.authentifie:
    st.markdown("<br><br>", unsafe_allow_html=True)
    colonne1, colonne2, colonne3 = st.columns()
    with colonne2:
        st.markdown("<h2 style='text-align: center;'>⛪ Gestion de l'Église</h2>", unsafe_allow_html=True)
        st.write("---")
        st.subheader("🔒 Accès Administrateur (Pasteur / Secrétariat)")
        
        # Saisie du mot de passe
        mot_de_passe_saisi = st.text_input("Entrez le mot de passe d'accès :", type="password")
        bouton_connexion = st.button("Se connecter", use_container_width=True)
        
        if bouton_connexion:
            if mot_de_passe_saisi == "Eglise2026":  # <-- Vous pouvez changer le mot de passe ici
                st.session_state.authentifie = True
                st.success("Connexion réussie !")
                st.rerun()
            else:
                st.error("Mot de passe incorrect. Veuillez réessayer.")
    st.stop() 

# 2. INITIALISATION DES BASES DE DONNÉES EN MÉMOIRE
if "base_fideles" not in st.session_state:
    st.session_state.base_fideles = pd.DataFrame(columns=["ID", "Nom", "Prénom", "Téléphone", "Statut"])
if "base_cotisations" not in st.session_state:
    st.session_state.base_cotisations = pd.DataFrame(columns=["Fidèle", "Montant (FCFA)", "Date", "Motif"])
if "base_programmes" not in st.session_state:
    st.session_state.base_programmes = pd.DataFrame(columns=["Événement / Fête", "Date", "Heure", "Description"])
if "base_annonces" not in st.session_state:
    st.session_state.base_annonces = []

# TITRE PRINCIPAL DE L'APPLICATION (Une fois connecté)
st.title("⛪ Système de Gestion de l'Église")
st.sidebar.markdown(f"**Statut :** 🟢 Connecté")
if st.sidebar.button("🔒 Se déconnecter"):
    st.session_state.authentifie = False
    st.rerun()

st.markdown("---")

# BARRE LATÉRALE : MENU DE NAVIGATION
menu = st.sidebar.radio(
    "Navigation",
    ["Tableau de bord", "👤 Fidèles", "💰 Cotisations & Dîmes", "📅 Programmes & Fêtes", "📢 Annonces"]
)

# 1. TABLEAU DE BORD
if menu == "Tableau de bord":
    st.subheader("📊 Vue d'ensemble")
    
    # Calcul des valeurs
    total_fideles = len(st.session_state.base_fideles)
    total_cotisations = st.session_state.base_cotisations["Montant (FCFA)"].sum()
    total_programmes = len(st.session_state.base_programmes)
    
    # Création des colonnes pour les rectangles
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div style="background-color: #1E3A8A; padding: 20px; border-radius: 10px; text-align: center; color: white; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
                <p style="margin: 0; font-size: 16px; font-weight: bold; text-transform: uppercase;">Total Fidèles</p>
                <h2 style="margin: 10px 0 0 0; font-size: 36px; font-weight: bold; color: white;">{total_fideles}</h2>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
            <div style="background-color: #065F46; padding: 20px; border-radius: 10px; text-align: center; color: white; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
                <p style="margin: 0; font-size: 16px; font-weight: bold; text-transform: uppercase;">Total Cotisations</p>
                <h2 style="margin: 10px 0 0 0; font-size: 32px; font-weight: bold; color: white;">{total_cotisations:,} FCFA</h2>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
            <div style="background-color: #C2410C; padding: 20px; border-radius: 10px; text-align: center; color: white; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
                <p style="margin: 0; font-size: 16px; font-weight: bold; text-transform: uppercase;">Programmes à venir</p>
                <h2 style="margin: 10px 0 0 0; font-size: 36px; font-weight: bold; color: white;">{total_programmes}</h2>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📢 Dernières Annonces")
    if st.session_state.base_annonces:
        for annonce in reversed(st.session_state.base_annonces):
            st.info(f"**{annonce['date']}** : {annonce['texte']}")
    else:
        st.write("Aucune annonce pour le moment.")

# 2. GESTION DES FIDÈLES
elif menu == "👤 Fidèles":
    st.subheader("👥 Gestion des Fidèles")
    
    with st.expander("➕ Ajouter un nouveau fidèle"):
        with st.form("formulaire_fidele"):
            nom = st.text_input("Nom")
            prenom = st.text_input("Prénom")
            tel = st.text_input("Numéro de Téléphone")
            statut = st.selectbox("Statut dans l'église", ["Membre actif", "Nouveau converti", "Visiteur", "Ancien / Responsable"])
            soumettre = st.form_submit_button("Enregistrer le fidèle")
            
            if soumettre and nom and prenom:
                nouvel_id = len(st.session_state.base_fideles) + 1
                nouvel_enregistrement = pd.DataFrame([{"ID": nouvel_id, "Nom": nom, "Prénom": prenom, "Téléphone": tel, "Statut": statut}])
                st.session_state.base_fideles = pd.concat([st.session_state.base_fideles, nouvel_enregistrement], ignore_index=True)
                st.success(f"{prenom} {nom} a été ajouté avec succès !")

    st.markdown("### 📋 Liste des membres")
    if not st.session_state.base_fideles.empty:
        st.dataframe(st.session_state.base_fideles, use_container_width=True)
        
        tampon_fideles = io.BytesIO()
        with pd.ExcelWriter(tampon_fideles, engine='openpyxl') as ecrivain:
            st.session_state.base_fideles.to_excel(ecrivain, index=False, sheet_name='Fidèles')
        st.download_button(
            label="📥 Télécharger la liste des fidèles en Excel (.xlsx)",
            data=tampon_fideles.getvalue(),
            file_name=f"liste_fideles_{datetime.now().strftime('%d_%m_%Y')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("Aucun fidèle enregistré pour le moment.")

# 3. GESTION DES COTISATIONS
elif menu == "💰 Cotisations & Dîmes":
    st.subheader("💵 Suivi des Contributions Financières")
    
    if st.session_state.base_fideles.empty:
        st.error("⚠️ Veuillez d'abord ajouter des fidèles dans l'onglet '👤 Fidèles' pour pouvoir enregistrer un paiement.")
    else:
        with st.form("formulaire_cotisation"):
            liste_fideles = st.session_state.base_fideles["Prénom"] + " " + st.session_state.base_fideles["Nom"]
            fidele_selectionne = st.selectbox("Sélectionner le fidèle", liste_fideles)
            montant = st.number_input("Montant (FCFA)", min_value=0, step=500)
            motif = st.selectbox("Motif", ["Dîme", "Offrande", "Action de grâce", "Soutien Fête / Événement", "Travaux Église"])
            date_cot = st.date_input("Date du versement")
            soumettre_cot = st.form_submit_button("Enregistrer le paiement")
            
            if soumettre_cot and montant > 0:
                nouvelle_cot = pd.DataFrame([{"Fidèle": fidele_selectionne, "Montant (FCFA)": montant, "Date": str(date_cot), "Motif": motif}])
                st.session_state.base_cotisations = pd.concat([st.session_state.base_cotisations, nouvelle_cot], ignore_index=True)
                st.success(f"Cotisation de {montant} FCFA enregistrée pour {fidele_selectionne} !")

    st.markdown("---")
    st.markdown("### 📜 Historique des paiements")
    
    if not st.session_state.base_cotisations.empty:
        st.dataframe(st.session_state.base_cotisations, use_container_width=True)
        
        tampon_cotisations = io.BytesIO()
        with pd.ExcelWriter(tampon_cotisations, engine='openpyxl') as ecrivain:
            st.session_state.base_cotisations.to_excel(ecrivain, index=False, sheet_name='Cotisations')
        
        st.download_button(
            label="📥 Télécharger l'historique des cotisations en Excel (.xlsx)",
            data=tampon_cotisations.getvalue(),
            file_name=f"cotisations_eglise_{datetime.now().strftime('%d_%m_%Y')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    else:
        st.write("Aucun paiement enregistré pour le moment.")

# 4. GESTION DES PROGRAMMES ET FÊTES
elif menu == "📅 Programmes & Fêtes":
    st.subheader("🗓️ Calendrier des Cultes, Fêtes et Événements")
    
    with st.expander("➕ Planifier un événement / une fête"):
        with st.form("formulaire_programme"):
            nom_evenement = st.text_input("Nom de l'événement (ex: Culte de Moisson, Fête de la Jeunesse, Veillée)")
            date_ev = st.date_input("Date")
            heure_ev = st.time_input("Heure de début")
            desc_ev = st.text_area("Description / Prédicateur invité")
            soumettre_prog = st.form_submit_button("Planifier")
            
            if soumettre_prog and nom_evenement:
                nouveau_prog = pd.DataFrame([{"Événement / Fête": nom_evenement, "Date": str(date_ev), "Heure": str(heure_ev), "Description": desc_ev}])
                st.session_state.base_programmes = pd.concat([st.session_state.base_programmes, nouveau_prog], ignore_index=True)
                st.success(f"L'événement '{nom_evenement}' a été planifié avec succès !")

    st.markdown("### 📋 Liste des programmes")
    if not st.session_state.base_programmes.empty:
        st.dataframe(st.session_state.base_programmes, use_container_width=True)
    else:
        st.write("Aucun événement prévu au calendrier.")

# 5. GESTION DES ANNONCES
elif menu == "📢 Annonces":
