"""
令和8年分（2026年分）所得税ルール。

税額や控除額など、年度によって変更される可能性のある
ルールをこのファイルに集約する。

注意:
このモジュールは令和8年分専用。
2025年分は rules_2025.py を使用する。
"""
from decimal import Decimal, ROUND_DOWN

TAX_YEAR = 2026

SPOUSE_DEDUCTION_INCOME_LIMIT_2026 = 620_000

TAXPAYER_SPOUSE_DEDUCTION_LIMIT = 10_000_000

def round_taxable_income(
    taxable_income: int,
) -> int:
    """
    課税所得の1,000円未満を切り捨てる。
    """

    if taxable_income <= 0:
        return 0

    return (
        taxable_income // 1_000
    ) * 1_000

INCOME_TAX_BRACKETS = (
    (
        1_949_000,
        Decimal("0.05"),
        0,
    ),
    (
        3_299_000,
        Decimal("0.10"),
        97_500,
    ),
    (
        6_949_000,
        Decimal("0.20"),
        427_500,
    ),
    (
        8_999_000,
        Decimal("0.23"),
        636_000,
    ),
    (
        17_999_000,
        Decimal("0.33"),
        1_536_000,
    ),
    (
        39_999_000,
        Decimal("0.40"),
        2_796_000,
    ),
    (
        None,
        Decimal("0.45"),
        4_796_000,
    ),
)

def calculate_income_tax(
    taxable_income: int,
) -> int:
    """
    課税所得から所得税額を計算する。

    課税所得は内部で1,000円未満を切り捨てる。
    """

    taxable_income = round_taxable_income(
        taxable_income
    )

    if taxable_income <= 0:
        return 0

    for (
        upper_limit,
        tax_rate,
        deduction,
    ) in INCOME_TAX_BRACKETS:

        if (
            upper_limit is None
            or taxable_income <= upper_limit
        ):
            tax = (
                Decimal(taxable_income)
                * tax_rate
                - Decimal(deduction)
            )

            return int(
                tax.to_integral_value(
                    rounding=ROUND_DOWN
                )
            )

    raise RuntimeError(
        "所得税率の判定に失敗しました。"
    )

RECONSTRUCTION_TAX_RATE = Decimal(
    "0.021"
)

def calculate_reconstruction_tax(
    base_income_tax: int,
) -> int:
    """
    復興特別所得税を計算する。

    基準所得税額 × 2.1%
    1円未満切り捨て。
    """

    if base_income_tax <= 0:
        return 0

    tax = (
        Decimal(base_income_tax)
        * RECONSTRUCTION_TAX_RATE
    )

    return int(
        tax.to_integral_value(
            rounding=ROUND_DOWN
        )
    )

def calculate_income_and_reconstruction_tax(
    taxable_income: int,
) -> tuple[int, int, int]:
    """
    所得税と復興特別所得税をまとめて計算する。

    戻り値:
        (
            所得税,
            復興特別所得税,
            合計額,
        )
    """

    income_tax = calculate_income_tax(
        taxable_income
    )

    reconstruction_tax = (
        calculate_reconstruction_tax(
            income_tax
        )
    )

    total_tax = (
        income_tax
        + reconstruction_tax
    )

    return (
        income_tax,
        reconstruction_tax,
        total_tax,
    )

def calculate_basic_deduction(
    total_income: int,
) -> int:
    """
    令和8年分の基礎控除額を返す。

    total_income:
        合計所得金額（収入金額ではない）
    """

    if total_income < 0:
        raise ValueError(
            "合計所得金額は0円以上である必要があります。"
        )

    if total_income <= 4_890_000:
        return 1_040_000

    if total_income <= 6_550_000:
        return 670_000

    if total_income <= 23_500_000:
        return 620_000

    if total_income <= 24_000_000:
        return 480_000

    if total_income <= 24_500_000:
        return 320_000

    if total_income <= 25_000_000:
        return 160_000

    return 0

def calculate_salary_income_deduction(
    salary_revenue: int,
) -> int:
    """
    令和8年分の給与所得控除額を概算計算する。

    salary_revenue:
        給与等の収入金額

    注意:
        給与収入660万円未満について、
        実際の給与所得金額を厳密に求める場合は
        所得税法別表第五による計算が必要。

        この関数では現在、
        給与所得控除額の速算表に基づいて計算する。
    """

    if salary_revenue < 0:
        raise ValueError(
            "給与収入は0円以上である必要があります。"
        )

    if salary_revenue <= 2_200_000:
        return 740_000

    if salary_revenue <= 3_600_000:
        return int(
            salary_revenue * 0.30
            + 80_000
        )

    if salary_revenue <= 6_600_000:
        return int(
            salary_revenue * 0.20
            + 440_000
        )

    if salary_revenue <= 8_500_000:
        return int(
            salary_revenue * 0.10
            + 1_100_000
        )

    return 1_950_000


def calculate_spouse_deduction(
    *,
    taxpayer_total_income: int,
    spouse_total_income: int,
    spouse_age_70_or_over: bool,
    eligibility_conditions_met: bool,
) -> int:
    """
    令和8年分の配偶者控除額を計算する。

    taxpayer_total_income:
        控除を受ける本人の合計所得金額

    spouse_total_income:
        配偶者の合計所得金額

    spouse_age_70_or_over:
        老人控除対象配偶者ならTrue

    eligibility_conditions_met:
        所得以外の配偶者控除要件を
        満たしている場合True
    """

    if taxpayer_total_income < 0:
        raise ValueError(
            "納税者本人の合計所得金額は"
            "0円以上である必要があります。"
        )

    if spouse_total_income < 0:
        raise ValueError(
            "配偶者の合計所得金額は"
            "0円以上である必要があります。"
        )

    if not eligibility_conditions_met:
        return 0

    # 令和8年分は配偶者の合計所得62万円以下
    if (
        spouse_total_income
        > SPOUSE_DEDUCTION_INCOME_LIMIT_2026
    ):
        return 0

    if (
        taxpayer_total_income
        > TAXPAYER_SPOUSE_DEDUCTION_LIMIT
    ):
        return 0

    # 本人の合計所得900万円以下
    if taxpayer_total_income <= 9_000_000:
        if spouse_age_70_or_over:
            return 480_000

        return 380_000

    # 本人の合計所得900万円超950万円以下
    if taxpayer_total_income <= 9_500_000:
        if spouse_age_70_or_over:
            return 320_000

        return 260_000

    # 本人の合計所得950万円超1,000万円以下
    if spouse_age_70_or_over:
        return 160_000

    return 130_000


SPOUSE_SPECIAL_DEDUCTION_MIN_INCOME_2026 = (
    620_000
)

SPOUSE_SPECIAL_DEDUCTION_MAX_INCOME_2026 = (
    1_330_000
)

TAXPAYER_SPOUSE_SPECIAL_DEDUCTION_MAX_INCOME = (
    10_000_000
)

def calculate_spouse_special_deduction(
    *,
    taxpayer_total_income: int,
    spouse_total_income: int,
    eligibility_conditions_met: bool,
) -> int:
    """
    令和8年分の配偶者特別控除額を計算する。

    配偶者の合計所得金額:
        620,000円超 1,330,000円以下

    納税者本人の合計所得金額:
        10,000,000円以下

    eligibility_conditions_met:
        所得金額以外の適用要件を満たす場合True
    """

    if taxpayer_total_income < 0:
        raise ValueError(
            "納税者本人の合計所得金額は"
            "0円以上である必要があります。"
        )

    if spouse_total_income < 0:
        raise ValueError(
            "配偶者の合計所得金額は"
            "0円以上である必要があります。"
        )

    if not eligibility_conditions_met:
        return 0

    # 本人所得が1,000万円を超える場合
    if (
        taxpayer_total_income
        > TAXPAYER_SPOUSE_SPECIAL_DEDUCTION_MAX_INCOME
    ):
        return 0

    # 配偶者控除の範囲
    if (
        spouse_total_income
        <= SPOUSE_SPECIAL_DEDUCTION_MIN_INCOME_2026
    ):
        return 0

    # 配偶者特別控除の上限超過
    if (
        spouse_total_income
        > SPOUSE_SPECIAL_DEDUCTION_MAX_INCOME_2026
    ):
        return 0

    # 本人所得区分
    if taxpayer_total_income <= 9_000_000:
        taxpayer_band = 0
    elif taxpayer_total_income <= 9_500_000:
        taxpayer_band = 1
    else:
        taxpayer_band = 2

    # 配偶者所得区分ごとの控除額
    deduction_table = (
        (
            950_000,
            380_000,
            260_000,
            130_000,
        ),
        (
            1_000_000,
            360_000,
            240_000,
            120_000,
        ),
        (
            1_050_000,
            310_000,
            210_000,
            110_000,
        ),
        (
            1_100_000,
            260_000,
            180_000,
            90_000,
        ),
        (
            1_150_000,
            210_000,
            140_000,
            70_000,
        ),
        (
            1_200_000,
            160_000,
            110_000,
            60_000,
        ),
        (
            1_250_000,
            110_000,
            80_000,
            40_000,
        ),
        (
            1_300_000,
            60_000,
            40_000,
            20_000,
        ),
        (
            1_330_000,
            30_000,
            20_000,
            10_000,
        ),
    )

    for (
        spouse_income_upper_limit,
        deduction_band_0,
        deduction_band_1,
        deduction_band_2,
    ) in deduction_table:
        if (
            spouse_total_income
            <= spouse_income_upper_limit
        ):
            deductions = (
                deduction_band_0,
                deduction_band_1,
                deduction_band_2,
            )

            return deductions[
                taxpayer_band
            ]

    return 0

def round_payment_amount(
    amount: int,
) -> int:
    """
    正の納付額について100円未満を切り捨てる。

    実際にどの計算段階へ適用するかは
    calculator.py 側で管理する。
    """

    if amount <= 0:
        return 0

    return (
        amount // 100
    ) * 100


MEDICAL_DEDUCTION_MAX = 2_000_000

def calculate_medical_expense_deduction(
    *,
    medical_expenses_paid: int,
    medical_reimbursements: int,
    total_income: int,
) -> int:
    """
    通常の医療費控除額を計算する。

    医療費控除額 =
      支払医療費
      - 保険金等の補てん額
      - 足切り額

    足切り額:
      総所得金額等200万円以上 → 100,000円
      総所得金額等200万円未満 → 総所得金額等の5%

    控除上限: 2,000,000円
    """

    if medical_expenses_paid < 0:
        raise ValueError(
            "支払医療費は0円以上である必要があります。"
        )

    if medical_reimbursements < 0:
        raise ValueError(
            "補てん額は0円以上である必要があります。"
        )

    if total_income < 0:
        raise ValueError(
            "所得金額は0円以上である必要があります。"
        )

    net_medical_expenses = max(
        medical_expenses_paid
        - medical_reimbursements,
        0,
    )

    if total_income < 2_000_000:
        threshold = int(
            total_income * 0.05
        )
    else:
        threshold = 100_000

    deduction = max(
        net_medical_expenses
        - threshold,
        0,
    )

    return min(
        deduction,
        MEDICAL_DEDUCTION_MAX,
    )


def calculate_miscellaneous_income(
    *,
    revenue: int,
    expenses: int,
) -> int:
    """
    公的年金以外の雑所得を計算する。

    雑所得 = 総収入金額 - 必要経費

    雑所得の損失は給与所得などと
    損益通算しないため、負の場合は0円とする。
    """

    if revenue < 0:
        raise ValueError(
            "雑所得の収入金額は"
            "0円以上である必要があります。"
        )

    if expenses < 0:
        raise ValueError(
            "雑所得の必要経費は"
            "0円以上である必要があります。"
        )

    return max(
        revenue - expenses,
        0,
    )

def calculate_public_pension_income(
    *,
    pension_revenue: int,
    age_65_or_over: bool,
    non_pension_income: int,
) -> int:
    """
    令和8年分の公的年金等に係る雑所得を計算する。

    pension_revenue:
        公的年金等の収入金額

    age_65_or_over:
        令和8年12月31日時点で65歳以上ならTrue

    non_pension_income:
        公的年金等に係る雑所得以外の
        合計所得金額

    現在はnon_pension_incomeが
    1,000万円以下のケースに対応する。
    """

    if pension_revenue < 0:
        raise ValueError(
            "公的年金等の収入金額は"
            "0円以上である必要があります。"
        )

    if non_pension_income < 0:
        raise ValueError(
            "年金以外の所得は"
            "0円以上である必要があります。"
        )

    if non_pension_income > 10_000_000:
        raise ValueError(
            "年金以外の所得が1,000万円を超える"
            "公的年金計算は現在未対応です。"
        )

    if pension_revenue == 0:
        return 0

    # 65歳以上
    if age_65_or_over:
        if pension_revenue <= 1_100_000:
            return 0

        if pension_revenue < 3_300_000:
            return (
                pension_revenue
                - 1_100_000
            )

    # 65歳未満
    else:
        if pension_revenue <= 600_000:
            return 0

        if pension_revenue < 1_300_000:
            return (
                pension_revenue
                - 600_000
            )

    # 以下は年齢共通
    if pension_revenue < 4_100_000:
        income = (
            pension_revenue
            * 75
            // 100
            - 275_000
        )

    elif pension_revenue < 7_700_000:
        income = (
            pension_revenue
            * 85
            // 100
            - 685_000
        )

    elif pension_revenue < 10_000_000:
        income = (
            pension_revenue
            * 95
            // 100
            - 1_455_000
        )

    else:
        income = (
            pension_revenue
            - 1_955_000
        )

    return max(
        income,
        0,
    )

def calculate_pension_income_adjustment_deduction(
    *,
    salary_income_after_deduction: int,
    pension_income: int,
) -> int:
    """
    給与所得と公的年金等の雑所得の双方がある場合の
    所得金額調整控除を計算する。

    salary_income_after_deduction:
        給与所得控除後の給与等の金額

    pension_income:
        公的年金等に係る雑所得の金額
    """

    if (
        salary_income_after_deduction <= 0
        or pension_income <= 0
    ):
        return 0

    return max(
        min(
            salary_income_after_deduction,
            100_000,
        )
        + min(
            pension_income,
            100_000,
        )
        - 100_000,
        0,
    )