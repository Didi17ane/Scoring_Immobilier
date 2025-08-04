# 1. Construction du dataset
import pandas as pd
import random
from datetime import datetime, timedelta

# Simulation de 100 locataires fictifs
n = 100

noms = [f"Locataire_{i}" for i in range(n)]
revenus = [random.randint(150000, 1000000) for _ in range(n)]
loyers = [random.randint(50000, 300000) for _ in range(n)]
types_emploi = random.choices(["CDI", "CDD", "Indépendant", "Informel"], weights=[0.4,0.2,0.2,0.2], k=n)
paiements_a_temps = [random.randint(0, 12) for _ in range(n)]
retards = [12 - p for p in paiements_a_temps]
duree_moy_retard = [random.randint(0, 20) if r > 0 else 0 for r in retards]
paiement_fractionne = random.choices(["Oui", "Non"], weights=[0.3, 0.7], k=n)
duree_location = [random.randint(3, 36) for _ in range(n)]  # en mois
conflits = random.choices(["Oui", "Non"], weights=[0.1, 0.9], k=n)

# Création du DataFrame
df = pd.DataFrame({
    "Nom": noms,
    "Revenu": revenus,
    "Loyer": loyers,
    "Type_Emploi": types_emploi,
    "Paiements_A_Temps": paiements_a_temps,
    "Retards": retards,
    "Duree_Moyenne_Retard": duree_moy_retard,
    "Paiement_Fractionne": paiement_fractionne,
    "Duree_Location": duree_location,
    "Conflits": conflits
})

# Enregistrement du dataset
csv_path = "scoring_locataires.csv"
df.to_csv(csv_path, index=False)

# 2. Fonction de scoring automatique
def calculer_score(row):
    score = 0

    # Comportement de paiement
    score += row['Paiements_A_Temps'] * 3         # sur 36
    score += (12 - row['Retards']) * 1            # sur 12
    score -= row['Duree_Moyenne_Retard'] * 0.5    # sur 10
    score += 5 if row['Paiement_Fractionne'] == "Non" else 0

    # Financier
    ratio_loyer = row['Loyer'] / row['Revenu']
    if ratio_loyer < 0.3:
        score += 10
    elif ratio_loyer < 0.4:
        score += 5

    # Type d'emploi
    emploi_score = {"CDI": 10, "CDD": 5, "Indépendant": 3, "Informel": 2}
    score += emploi_score.get(row['Type_Emploi'], 0)

    # Historique
    score += min(row['Duree_Location'], 24) * 0.5  # max 12 pts
    score -= 5 if row['Conflits'] == "Oui" else 0

    return round(score, 2)

df['Score'] = df.apply(calculer_score, axis=1)

# Sauvegarde avec scores inclus
df.to_csv("scoring_locataires_scores.csv", index=False)

# 3. Streamlit prototype (app.py)
# Créer un fichier séparé "app.py" avec :
# import streamlit as st
# import pandas as pd
# df = pd.read_csv("scoring_locataires_avec_scores.csv")
# st.title("Scoring des locataires")
# st.dataframe(df.sort_values("Score", ascending=False))
# st.bar_chart(df[['Nom', 'Score']].set_index('Nom'))
