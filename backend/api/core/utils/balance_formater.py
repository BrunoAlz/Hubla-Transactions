def balance_formater(balance):
    """Converte um valor em centavos para reais formatados."""
    formated_balance = float(balance) / 100.0
    return f'R$ {formated_balance:.2f}'
