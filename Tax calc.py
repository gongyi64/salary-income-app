"""
給与収入から給与所得・基礎控除を計算する。

年度別のルール（給与所得控除・基礎控除）は、tax_engine の
get_tax_rules(tax_year) が返す rules_2025 / rules_2026 を使う。
tax_engine への依存はこのファイルに集約し、
tax_engine の場所や呼び出し方が変わった場合はこのファイルだけ直す。
"""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from types import ModuleType

SUPPORTED_TAX_YEARS = (2025, 2026)

# get_tax_rules が定義されているモジュールのパス。
# tax_engine の実際の構成に合わせて、ここだけ直す（要確認）。
GET_TAX_RULES_MODULE = "tax_engine.rules"


@dataclass(frozen=True)
class SalaryResult:
    tax_year: int
    salary_revenue: int            # 給与収入
    salary_income_deduction: int   # 給与所得控除
    salary_income: int             # 給与所得
    total_income: int              # 合計所得金額（給与のみのため給与所得と同額）
    basic_deduction: int           # 基礎控除


def load_rules(tax_year: int) -> ModuleType:
    """税制年度に対応するルールモジュールを tax_engine から取得する。"""

    if tax_year not in SUPPORTED_TAX_YEARS:
        raise ValueError(f"{tax_year}年分は未対応です。")

    try:
        module = importlib.import_module(GET_TAX_RULES_MODULE)
        get_tax_rules = getattr(module, "get_tax_rules")
    except (ImportError, AttributeError) as e:
        raise RuntimeError(
            f"{GET_TAX_RULES_MODULE} から get_tax_rules を読み込めませんでした。\n"
            f"tax_engine がこの環境にインストールされているか、"
            f"tax_calc.py の GET_TAX_RULES_MODULE を確認してください。\n"
            f"（元のエラー: {e}）"
        ) from e

    return get_tax_rules(tax_year)


def calculate_salary_result(
    tax_year: int,
    salary_revenue: int,
) -> SalaryResult:
    """給与収入から、給与所得控除・給与所得・基礎控除を計算する。"""

    if salary_revenue < 0:
        raise ValueError("給与収入は0円以上である必要があります。")

    rules = load_rules(tax_year)

    deduction = rules.calculate_salary_income_deduction(salary_revenue)

    # 控除額が給与収入を超えないようにする
    deduction = min(deduction, salary_revenue)

    salary_income = salary_revenue - deduction

    # 基礎控除は収入ではなく「合計所得金額」で決まる。
    # 給与のみの簡易計算なので、合計所得金額 = 給与所得。
    total_income = salary_income

    basic_deduction = rules.calculate_basic_deduction(total_income)

    return SalaryResult(
        tax_year=tax_year,
        salary_revenue=salary_revenue,
        salary_income_deduction=deduction,
        salary_income=salary_income,
        total_income=total_income,
        basic_deduction=basic_deduction,
    )