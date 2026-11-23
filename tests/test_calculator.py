import pytest

from calculator import calculate_salary_income_deduction


@pytest.mark.parametrize(
    "salary, year, expected",
    [
        # 2025年
        (2_000_000, 2025, 680_000),
        (5_000_000, 2025, 1_440_000),

        # 2026年
        (2_000_000, 2026, 740_000),
        (5_000_000, 2026, 1_440_000),
    ],
)
def test_calculate_salary_income_deduction(
    salary,
    year,
    expected,
):
    assert (
        calculate_salary_income_deduction(salary, year)
        == expected
    )


def test_unsupported_year():
    with pytest.raises(ValueError):
        calculate_salary_income_deduction(
            5_000_000,
            2027,
        )