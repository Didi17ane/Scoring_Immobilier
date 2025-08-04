import streamlit as st
import pandas as pd


df = pd.read_csv("scoring_locataires_scores.csv")
st.title("Scoring des locataires")
#st.dataframe(df.sort_values("Score", ascending=False))



# Fonction de segmentation
def segmenter_risque(score):
    if score > 70:
        return "Faible Risque"
    elif score >= 60:
        return "Risque Moyen"
    else:
        return "Risque Élevé"

# Appliquer la segmentation
df["Risque"] = df["Score"].apply(segmenter_risque)

# Couleurs personnalisées
couleurs = {
    "Faible Risque": "background-color: #d4edda; color: #155724",   # vert pâle
    "Risque Moyen": "background-color: #fff3cd; color: #856404",    # jaune
    "Risque Élevé": "background-color: #f8d7da; color: #721c24",    # rouge pâle
}

# Fonction de stylisation
def colorer_ligne(row):
    return [couleurs.get(row["Risque"], "")] * len(row)

st.title("📊 Tableau de Scoring des Locataires")

# Affichage du tableau avec couleurs
st.dataframe(df.style.apply(colorer_ligne, axis=1), use_container_width=True)

# Optionnel : graphique par groupe
st.subheader("Répartition des locataires par risque")
st.bar_chart(df["Risque"].value_counts())

# Graphique d'ensemble
st.subheader("Vue d'ensemble")
st.bar_chart(df[['Nom', 'Score']].set_index('Nom'))

