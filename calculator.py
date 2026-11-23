from rules import rules_2025, rules_2026


def calculate_salary_income_deduction(
    salary_revenue: int,
    year: int,
) -> int:
    """
    対象年度に応じて給与所得控除額を計算する。
    """

    if year == 2025:
        return rules_2025.calculate_salary_income_deduction(
            salary_revenue
        )

    if year == 2026:
        return rules_2026.calculate_salary_income_deduction(
            salary_revenue
        )

    raise ValueError(
        f"未対応の年度です: {year}"
    )