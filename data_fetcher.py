import pandas as pd
import yfinance as yf
def get_historical_data(crypto_list, start_date, end_date):
    all_data = []

    for crypto in crypto_list:
        # Télécharger les données avec un intervalle quotidien
        data = yf.download(crypto, start=start_date, end=end_date, interval="1d")
        
        if data.empty:
            raise ValueError(f"Aucune donnée trouvée pour {crypto}. Vérifiez les paramètres ou la disponibilité des données.")

        # Réinitialiser l'index pour convertir la date en colonne
        data.reset_index(inplace=True)

        # Vérifier que la colonne 'Date' existe
        if "Date" not in data.columns:
            raise ValueError("La colonne 'Date' est manquante dans les données téléchargées.")

        # Ajouter une colonne pour identifier la crypto
        data["Crypto"] = crypto

        # Ajouter les données à la liste
        all_data.append(data)

    # Combiner toutes les données en un seul DataFrame
    combined_data = pd.concat(all_data, ignore_index=True)
    combined_data.columns = ['_'.join(col) for col in combined_data.columns]
    
    # Vérifier les colonnes disponibles
    print("Colonnes disponibles après combinaison :", combined_data.columns)

    return combined_data