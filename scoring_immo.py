import streamlit as st
import pandas as pd

# Charger les données avec score
df = pd.read_csv("scoring_locataires_scores.csv")

# Fonction de segmentation du risque
def segmenter_risque(score):
    if score > 70:
        return "Faible Risque"
    elif score >= 60:
        return "Risque Moyen"
    else:
        return "Risque Élevé"

# Appliquer la segmentation
df["Risque"] = df["Score"].apply(segmenter_risque)

# Couleurs personnalisées pour affichage conditionnel
couleurs = {
    "Faible Risque": "background-color: #d4edda; color: #155724",
    "Risque Moyen": "background-color: #fff3cd; color: #856404",
    "Risque Élevé": "background-color: #f8d7da; color: #721c24",
}

def colorer_ligne(row):
    return [couleurs.get(row["Risque"], "")] * len(row)

# Interface Streamlit
st.set_page_config(page_title="Scoring Locataires Tylimmo", layout="wide")
st.title("📊 Tableau de Scoring des Locataires")

# Section résumé du rapport
st.markdown("""
### 🧾 À propos du projet
Ce tableau présente l'évaluation de locataires fictifs selon plusieurs critères :
- Habitudes de paiement (ponctualité, retards, paiements fractionnés)
- Revenus et emploi
- Durée dans le logement et conflits passés

Le score est calculé sur 100 et segmenté en trois catégories de risque :
- ✅ **Faible Risque** (> 70)
- ⚠️ **Risque Moyen** (60 à 70)
- ❌ **Risque Élevé** (< 60)
""")

# Affichage tableau stylisé
st.subheader("📋 Données des locataires")
st.dataframe(df.style.apply(colorer_ligne, axis=1), use_container_width=True)

# Graphique de répartition des risques
st.subheader("📊 Répartition des locataires par niveau de risque")
st.bar_chart(df["Risque"].value_counts())

# Graphique des scores individuels
st.subheader("📈 Vue d'ensemble des scores")
st.bar_chart(df[['Nom', 'Score']].set_index('Nom'))

# Bouton de téléchargement du rapport PDF
with open("Rapport_Scoring_Tylimmo.pdf", "rb") as f:
    st.download_button("📥 Télécharger le rapport PDF", f, file_name="Rapport_Scoring_Tylimmo.pdf")
