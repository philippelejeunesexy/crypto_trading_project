import random
class TradingModel:
    def __init__(self, model_id, initial_balance):
        self.id = model_id
        self.balance = initial_balance
        self.strategy = {
            "indicator_weights": {},  # Pondérations des indicateurs
        }
    
    def make_decision(self, daily_data):
        trades = []
        if "Crypto_" not in daily_data.columns:
            raise KeyError("La colonne 'Crypto_' est manquante dans les données.")
        
        grouped_data = daily_data.groupby("Crypto_")  # Grouper les données par crypto
        for crypto, group in grouped_data:
            if not group.empty:  # Vérifie si des données existent
                last_close_price = group[f"Close_{crypto}"].iloc[-1]  # Accéder à la dernière valeur
                action = "buy" if last_close_price % 2 == 0 else "sell"
                amount = self.balance * 0.1  # Investir 10% du solde
            else:
                action = "hold"  # Pas d'action si données absentes
                amount = 0

            trades.append({"crypto": crypto, "action": action, "amount": amount})
        return trades

    def execute_trade(self, crypto, action, amount, hourly_data):
        filtered_data = hourly_data[hourly_data["Crypto_"] == crypto]
        if not filtered_data.empty:
            current_price = filtered_data[f"Close_{crypto}"].iloc[-1]
            next_price = current_price * 1.01  # Variation fictive
            profit_loss = amount * ((next_price - current_price) / current_price)
            self.balance += profit_loss
            return profit_loss > 0, profit_loss
        return False, 0  # Retourner False si aucune donnée n'est disponible

    def update_strategy(self, daily_trades):
        """
        Ajuste les pondérations des indicateurs en fonction des performances.
        """
        self.strategy["indicator_weights"]["reward"] = daily_trades
