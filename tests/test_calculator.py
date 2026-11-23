import pytest

from calculator import calculate_salary_income_deduction


@pytest.mark.parametrize(
    "salary, expected",
    [
        # 0円・最低額付近
        (0, 0),
        (1, 650_000),

        # 1,900,000円の境界
        (1_900_000, 650_000),
        (1_900_001, 650_000),

        # 3,600,000円の境界
        (3_600_000, 1_160_000),
        (3_600_001, 1_160_000),

        # 6,600,000円の境界
        (6_600_000, 1_760_000),
        (6_600_001, 1_760_000),

        # 8,500,000円の境界
        (8_500_000, 1_950_000),
        (8_500_001, 1_950_000),

        # 今回GUIで確認した500万円
        (5_000_000, 1_440_000),

        # 高額給与
        (10_000_000, 1_950_000),
    ],
)
def test_calculate_salary_income_deduction(salary, expected):
    assert calculate_salary_income_deduction(salary) == expected
