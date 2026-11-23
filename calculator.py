def calculate_salary_income_deduction(salary: int) -> int:
    """
    給与収入から給与所得控除額を計算する。

    ※ 現段階では画面動作確認用の計算ロジック。
       税制年度を正式に固定する場合は、
       年度別ルールとして分離する。
    """

    if salary <= 0:
        return 0

    if salary <= 1_900_000:
        return 650_000

    if salary <= 3_600_000:
        return int(salary * 0.30 + 80_000)

    if salary <= 6_600_000:
        return int(salary * 0.20 + 440_000)

    if salary <= 8_500_000:
        return int(salary * 0.10 + 1_100_000)

    return 1_950_000