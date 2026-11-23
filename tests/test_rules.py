import pytest

from rules import rules_2025, rules_2026


@pytest.mark.parametrize(
    "salary, expected",
    [
        (0, 650_000),
        (1_625_000, 650_000),
        (1_625_001, 650_000),
        (1_800_000, 650_000),
        (1_900_000, 650_000),
        (1_900_001, 650_000),
        (2_000_000, 680_000),
        (3_600_000, 1_160_000),
        (5_000_000, 1_440_000),
        (6_600_000, 1_760_000),
        (8_500_000, 1_950_000),
        (8_500_001, 1_950_000),
    ],
)
def test_salary_income_deduction_2025(salary, expected):
    assert (
        rules_2025.calculate_salary_income_deduction(salary)
        == expected
    )


@pytest.mark.parametrize(
    "salary, expected",
    [
        (0, 740_000),
        (1_625_000, 740_000),
        (1_900_000, 740_000),
        (2_000_000, 740_000),
        (2_200_000, 740_000),
        (2_200_001, 740_000),
        (3_600_000, 1_160_000),
        (5_000_000, 1_440_000),
        (6_600_000, 1_760_000),
        (8_500_000, 1_950_000),
        (8_500_001, 1_950_000),
    ],
)
def test_salary_income_deduction_2026(salary, expected):
    assert (
        rules_2026.calculate_salary_income_deduction(salary)
        == expected
    )


@pytest.mark.parametrize(
    "rule",
    [
        rules_2025,
        rules_2026,
    ],
)
def test_negative_salary_raises_value_error(rule):
    with pytest.raises(ValueError):
        rule.calculate_salary_income_deduction(-1)