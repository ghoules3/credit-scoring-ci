def score_client(limit_bal: int, pay_delay: int, age: int) -> str:
    """
    Простая логика оценки кредитного риска клиента.
    Возвращает одну из категорий:
    - low
    - medium
    - high
    """

    if limit_bal < 50000 or pay_delay > 2:
        return "high"

    if pay_delay > 0 or age < 25:
        return "medium"

    return "low"


if __name__ == "__main__":
    result = score_client(limit_bal=120000, pay_delay=0, age=30)
    print(f"Predicted risk: {result}")