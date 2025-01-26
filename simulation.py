import sys
import os
from tqdm import tqdm

# Créer le dossier 'data' s'il n'existe pas
os.makedirs("data", exist_ok=True)

# Ajouter le dossier racine du projet au chemin des modules Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
import numpy as np

from datetime import datetime, timedelta
from utils.data_fetcher import get_historical_data
from models.trading_model import TradingModel

# Paramètres de la simulation
CRYPTO_LIST = [
    "BTC-USD", "ETH-USD", "BNB-USD", "XRP-USD", "ADA-USD",
    "DOGE-USD", "SOL-USD", "DOT-USD", "LTC-USD", "AVAX-USD"
]
START_DATE = "2023-01-01"
END_DATE = "2023-12-31"
INITIAL_BALANCE = 100

# Charger les données historiques
price_data = get_historical_data(CRYPTO_LIST, START_DATE, END_DATE)

# Supprime les niveaux inutiles d'indices si MultiIndex
if isinstance(price_data.columns, pd.MultiIndex):
    price_data.columns = price_data.columns.droplevel(level=1)

# Assure que la colonne 'Date' est bien formatée
price_data['Date_'] = pd.to_datetime(price_data['Date_'])

print(price_data.columns)  # Vérifie les colonnes pour s'assurer que 'Date' est bien présente

# Configurer les modèles de trading
models = [TradingModel(model_id=i, initial_balance=INITIAL_BALANCE) for i in range(1, 101)]

# Simulation journalière
results = []

max_iterations = 100000  # Nombre maximal d'itérations attendues
iteration_count = 0
# Ajouter une colonne 'Hour' si elle n'existe pas
if "Hour" not in price_data.columns:
    price_data["Hour"] = price_data["Date_"].dt.hour

# Boucle principale
for current_date in tqdm(pd.date_range(START_DATE, END_DATE), desc="Simulation en cours"):
    print(f"Traitement de la date : {current_date}")  # Affiche la date en cours
    
    # Filtrer les données pour la journée en cours
    daily_data = price_data[price_data["Date_"] == current_date]
    
    for model in models:
        iteration_count += 1
        if iteration_count > max_iterations:
            raise RuntimeError("Le programme semble être dans une boucle infinie.")
        
        daily_balance = model.balance  # Sauvegarder le solde initial de la journée
        daily_trades = 0  # Compteur de trades fructueux pour la journée
        
        # Le modèle décide de ses investissements
        if not daily_data.empty:  # Vérifie que les données existent
            trades = model.make_decision(daily_data)
        else:
            print(f"Pas de données disponibles pour {current_date}")
            trades = []

        # Appliquer les trades et mettre à jour le solde
        for trade in trades:
            crypto = trade["crypto"]
            amount = trade["amount"]
            action = trade["action"]  # "buy" ou "sell"
            success, profit_loss = model.execute_trade(crypto, action, amount, daily_data)
            if success:
                daily_trades += 1  # Compter les trades fructueux

        # Récompenser le modèle en fonction des résultats
        model.update_strategy(daily_trades)
        
        # Sauvegarder les résultats de la journée
        results.append({
            "Date": current_date,
            "Model_ID": model.id,
            "Daily_Balance": model.balance,
            "Daily_Trades": daily_trades
        })
        print(f"Résultat ajouté : Date={current_date}, Model_ID={model.id}, Balance={model.balance}, Trades={daily_trades}")

# Créer le dossier 'data' s'il n'existe pas
os.makedirs("data", exist_ok=True)

# Convertir la liste des résultats en DataFrame
results_df = pd.DataFrame(results)
print("Résultats avant sauvegarde :")
print(results_df.head())  # Afficher les premières lignes du DataFrame

# Sauvegarder les résultats dans un fichier CSV
results_df.to_csv("data/trading_simulation_results.csv", index=False)
print("Fichier CSV sauvegardé avec succès.")