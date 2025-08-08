# import streamlit as st
# import pandas as pd

# # Charger les données avec score
# df = pd.read_csv("scoring_locataires_scores.csv")

# # Fonction de segmentation du risque
# def segmenter_risque(score):
#     if score > 70:
#         return "Faible Risque"
#     elif score >= 60:
#         return "Risque Moyen"
#     else:
#         return "Risque Élevé"

# # Appliquer la segmentation
# df["Risque"] = df["Score"].apply(segmenter_risque)

# # Couleurs personnalisées pour affichage conditionnel
# couleurs = {
#     "Faible Risque": "background-color: #d4edda; color: #155724",
#     "Risque Moyen": "background-color: #fff3cd; color: #856404",
#     "Risque Élevé": "background-color: #f8d7da; color: #721c24",
# }

# def colorer_ligne(row):
#     return [couleurs.get(row["Risque"], "")] * len(row)

# # Interface Streamlit
# st.set_page_config(page_title="Scoring Locataires Tylimmo", layout="wide")
# st.title("📊 Tableau de Scoring des Locataires")

# # Section résumé du rapport
# st.markdown("""
# ### 🧾 À propos du projet
# Ce tableau présente l'évaluation de locataires fictifs selon plusieurs critères :
# - Habitudes de paiement (ponctualité, retards, paiements fractionnés)
# - Revenus et emploi
# - Durée dans le logement et conflits passés

# Le score est calculé sur 100 et segmenté en trois catégories de risque :
# - ✅ **Faible Risque** (> 70)
# - ⚠️ **Risque Moyen** (60 à 70)
# - ❌ **Risque Élevé** (< 60)
# """)

# # Affichage tableau stylisé
# st.subheader("📋 Données des locataires")
# st.dataframe(df.style.apply(colorer_ligne, axis=1), use_container_width=True)

# # Graphique de répartition des risques
# st.subheader("📊 Répartition des locataires par niveau de risque")
# st.bar_chart(df["Risque"].value_counts())

# # Graphique des scores individuels
# st.subheader("📈 Vue d'ensemble des scores")
# st.bar_chart(df[['Nom', 'Score']].set_index('Nom'))

# # Bouton de téléchargement du rapport PDF
# # with open("Rapport_Scoring_Tylimmo.pdf", "rb") as f:
# #    st.download_button("📥 Télécharger le rapport PDF", f, file_name="Rapport_Scoring_Tylimmo.pdf")






















import streamlit as st
import pandas as pd
import random
import numpy as np

st.set_page_config(page_title="Scoring Locataires Tylimmo", layout="wide")
st.title("📊  Tableau de Scoring des Locataires")

# 1. Génération du dataset fictif
n = 100
noms = [f"Locataire_{i}" for i in range(n)] 
revenus = [random.randint(150000, 1000000) for _ in range(n)]
loyers = [random.randint(50000, 300000) for _ in range(n)]
types_location = random.choices(
    ["Appartement", "Villa", "Studio", "Chambre", "Bureau", "Commerce", "Entrepôt", "Appart'Hôtel", "Espace de travail", "Terrain", "Bâtiment"],
    weights=[0.2, 0.15, 0.15, 0.1, 0.05, 0.05, 0.05, 0.05, 0.05, 0.075, 0.075],
    k=n
)
types_emploi = random.choices(
    ["CDI", "Fonctionnaire", "CDD", "Indépendant", "Intérimaire", "Informel", "Étudiant"],
    weights=[0.25, 0.15, 0.2, 0.15, 0.1, 0.1, 0.05],
    k=n
)
nombre_locations = [random.randint(1, 5) for _ in range(n)]
duree_location = [random.randint(1, 60) for _ in range(n)]
ponctualites = random.choices(["Oui", "Non"], weights=[0.7, 0.3], k=n)
observations = random.choices(["RAS", "Difficultés temporaires", "Retards fréquents", "Conflits"], weights=[0.5, 0.2, 0.2, 0.1], k=n)

paiements_a_temps = [random.randint(6, 12) if p == "A temps" else random.randint(0, 5) for p in ponctualites]
retards = [12 - pt if pt < 12 else random.randint(0, 3) for pt in paiements_a_temps]
duree_moy_retard = [round(random.uniform(0, 10), 1) if r > 0 else 0 for r in retards]
paiements_fractionnes = [random.randint(1, 3) if p == "Oui" else 0 for p in ponctualites]
conflits = ["Oui" if obs == "Conflits" else "Non" for obs in observations]

# Création du DataFrame
df = pd.DataFrame({
    "Nom": noms,
    "Revenu_Mensuel": revenus,
    "Loyer_Mensuel": loyers,
    "Type_Location": types_location,
    "Type_Emploi": types_emploi,
    "Nombre_Locations": nombre_locations,
    "Duree_Location": duree_location,
    "Ponctualite_Paiement": ponctualites,
    "Observations": observations,
    "Paiements_A_Temps": paiements_a_temps,
    "Retards": retards,
    "Duree_Moyenne_Retard": duree_moy_retard,
    "Paiements_Fractionnes": paiements_fractionnes,
    "Conflits_Passes": conflits
})

# 2. Fonction de scoring automatique
def calculer_score(row):
    score = 0
    score += row['Paiements_A_Temps'] * 3         # sur 36
    score += (12 - row['Retards']) * 1            # sur 12
    score -= row['Duree_Moyenne_Retard'] * 0.5    # sur 10
    score += 5 if row['Paiements_Fractionnes'] == 0 else 0

    ratio_loyer = row['Loyer_Mensuel'] / row['Revenu_Mensuel']
    if ratio_loyer <= 0.25:
        score += 10
    elif ratio_loyer <= 0.35:
        score += 7
    elif ratio_loyer <= 0.5:
        score += 4
    else:
        score += 1

    emploi_score = {
        "CDI": 6, "Fonctionnaire": 6, "CDD": 4,
        "Indépendant": 4, "Intérimaire": 3, "Informel": 2, "Étudiant": 1
    }
    score += emploi_score.get(row['Type_Emploi'], 0)

    if row['Duree_Location'] >= 36:
        score += 5
    elif row['Duree_Location'] >= 24:
        score += 4
    elif row['Duree_Location'] >= 12:
        score += 3
    elif row['Duree_Location'] >= 6:
        score += 2
    else:
        score += 1

    score += min(row['Nombre_Locations'], 5) * 1
    score -= 5 if row['Conflits_Passes'] == "Oui" else 0

    return round(max(score, 0), 2)

df['Score'] = df.apply(calculer_score, axis=1)

# 3. Segmentation du risque
def segmenter_risque(score):
    if score > 70:
        return "Faible Risque"
    elif score >= 60:
        return "Risque Moyen"
    else:
        return "Risque Élevé"

df["Risque"] = df["Score"].apply(segmenter_risque)

# Couleurs personnalisées pour affichage conditionnel
couleurs = {
    "Faible Risque": "background-color: #d4edda; color: #155724",
    "Risque Moyen": "background-color: #fff3cd; color: #856404",
    "Risque Élevé": "background-color: #f8d7da; color: #721c24",
}

def colorer_ligne(row):
    return [couleurs.get(row["Risque"], "")] * len(row)

# Section résumé du rapport
st.markdown("""
### A propos du projet
Ce tableau présente l'évaluation de locataires fictifs selon plusieurs critères :

**Caractéristiques observées :**
- Revenu mensuel, Loyer mensuel
- Type de location, Type d'emploi
- Nombre de locations passées, Durée de location
- Ponctualité de paiement, Observations

**Caractéristiques déduites automatiquement :**
- Nombre de paiements à temps
- Nombre de retards
- Durée moyenne des retards
- Nombre de paiements fractionnés
- Conflits passés

Le score est calculé sur 100 et segmenté en trois catégories de risque :
- ✅ **Faible Risque** (> 70)
- ⚠️ **Risque Moyen** (60 à 70)
- ❌ **Risque Élevé** (< 60)
""")

# Affichage tableau stylisé
st.subheader(" Données des locataires")
st.dataframe(df.style.apply(colorer_ligne, axis=1), use_container_width=True)

# Graphique de répartition des risques
st.subheader("Répartition des locataires par niveau de risque")
st.bar_chart(df["Risque"].value_counts())

# Graphique des scores individuels
st.subheader("Vue d'ensemble des scores")
st.bar_chart(df[['Nom', 'Score']].set_index('Nom'))

