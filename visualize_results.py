import pandas as pd
import matplotlib.pyplot as plt

def plot_model_balance(csv_path, model_id):
    """
    Génère un graphique montrant l'évolution du solde pour un modèle donné.
    
    :param csv_path: Chemin vers le fichier CSV contenant les résultats.
    :param model_id: Identifiant du modèle à tracer.
    """
    # Charger le fichier CSV
    data = pd.read_csv(csv_path)
    
    # Filtrer les données pour le modèle spécifié
    model_data = data[data['Model_ID'] == model_id]

    # Vérifier si le modèle existe
    if model_data.empty:
        print(f"⚠️ Aucun résultat pour le modèle ID {model_id}")
        return

    # Tracer le solde journalier
    plt.figure(figsize=(12, 6))
    plt.plot(model_data['Date'], model_data['Daily_Balance'], label=f"Model {model_id}", color='blue')

    # Ajouter des titres et légendes
    plt.title(f"Évolution du solde - Modèle {model_id}", fontsize=16)
    plt.xlabel("Date", fontsize=14)
    plt.ylabel("Solde ($)", fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()

    # Afficher le graphique
    plt.tight_layout()
    plt.savefig(f"model_{model_id}_balance_plot.png")
    plt.show()


# Exemple d'utilisation
if __name__ == "__main__":
    # Chemin vers le fichier CSV
    csv_file = "../data/trading_simulation_results.csv"

    # ID du modèle que vous voulez visualiser
    model_id_to_plot = 1

    # Générer le graphique
    plot_model_balance(csv_file, model_id_to_plot)
