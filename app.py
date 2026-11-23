import tkinter as tk
from tkinter import ttk, messagebox

from calculator import calculate_salary_income_deduction


def calculate():
    """画面に入力された給与収入から給与所得を計算する。"""

    text = salary_entry.get()

    # 「,」や空白が入っていても計算できるようにする
    text = text.replace(",", "").replace(" ", "").strip()

    if not text:
        messagebox.showwarning(
            "入力エラー",
            "給与収入を入力してください。"
        )
        return

    try:
        salary = int(text)
    except ValueError:
        messagebox.showerror(
            "入力エラー",
            "給与収入は整数で入力してください。"
        )
        return

    if salary < 0:
        messagebox.showerror(
            "入力エラー",
            "給与収入は0円以上で入力してください。"
        )
        return

    deduction = calculate_salary_income_deduction(salary)

    # 控除額が給与収入を超えないようにする
    deduction = min(deduction, salary)

    salary_income = salary - deduction

    salary_result_var.set(f"{salary:,} 円")
    deduction_result_var.set(f"{deduction:,} 円")
    income_result_var.set(f"{salary_income:,} 円")


def clear():
    """入力値・計算結果をクリアする。"""

    salary_entry.delete(0, tk.END)

    salary_result_var.set("-")
    deduction_result_var.set("-")
    income_result_var.set("-")

    salary_entry.focus()


# =========================================================
# メインウィンドウ
# =========================================================

root = tk.Tk()
root.title("給与所得計算")
root.geometry("500x380")
root.resizable(False, False)


# =========================================================
# タイトル
# =========================================================

title_label = ttk.Label(
    root,
    text="給与所得計算",
    font=("Yu Gothic UI", 18, "bold")
)
title_label.pack(pady=(20, 5))


description_label = ttk.Label(
    root,
    text="給与収入を入力すると給与所得を計算します。",
    font=("Yu Gothic UI", 10)
)
description_label.pack(pady=(0, 20))


# =========================================================
# 入力部分
# =========================================================

input_frame = ttk.Frame(root)
input_frame.pack(pady=5)


salary_label = ttk.Label(
    input_frame,
    text="給与収入",
    font=("Yu Gothic UI", 11)
)
salary_label.grid(
    row=0,
    column=0,
    padx=10,
    pady=10
)


salary_entry = ttk.Entry(
    input_frame,
    width=20,
    justify="right",
    font=("Yu Gothic UI", 12)
)
salary_entry.grid(
    row=0,
    column=1,
    padx=5,
    pady=10
)


yen_label = ttk.Label(
    input_frame,
    text="円",
    font=("Yu Gothic UI", 11)
)
yen_label.grid(
    row=0,
    column=2,
    padx=5
)


# =========================================================
# ボタン
# =========================================================

button_frame = ttk.Frame(root)
button_frame.pack(pady=15)


calculate_button = ttk.Button(
    button_frame,
    text="計算",
    command=calculate,
    width=15
)
calculate_button.grid(
    row=0,
    column=0,
    padx=5
)


clear_button = ttk.Button(
    button_frame,
    text="クリア",
    command=clear,
    width=15
)
clear_button.grid(
    row=0,
    column=1,
    padx=5
)


# =========================================================
# 計算結果
# =========================================================

result_frame = ttk.LabelFrame(
    root,
    text="計算結果",
    padding=15
)
result_frame.pack(
    padx=30,
    pady=10,
    fill="x"
)


salary_result_var = tk.StringVar(value="-")
deduction_result_var = tk.StringVar(value="-")
income_result_var = tk.StringVar(value="-")


ttk.Label(
    result_frame,
    text="給与収入：",
    font=("Yu Gothic UI", 11)
).grid(
    row=0,
    column=0,
    sticky="w",
    pady=5
)


ttk.Label(
    result_frame,
    textvariable=salary_result_var,
    font=("Yu Gothic UI", 11)
).grid(
    row=0,
    column=1,
    sticky="e",
    pady=5
)


ttk.Label(
    result_frame,
    text="給与所得控除：",
    font=("Yu Gothic UI", 11)
).grid(
    row=1,
    column=0,
    sticky="w",
    pady=5
)


ttk.Label(
    result_frame,
    textvariable=deduction_result_var,
    font=("Yu Gothic UI", 11)
).grid(
    row=1,
    column=1,
    sticky="e",
    pady=5
)


ttk.Label(
    result_frame,
    text="給与所得：",
    font=("Yu Gothic UI", 12, "bold")
).grid(
    row=2,
    column=0,
    sticky="w",
    pady=(10, 5)
)


ttk.Label(
    result_frame,
    textvariable=income_result_var,
    font=("Yu Gothic UI", 12, "bold")
).grid(
    row=2,
    column=1,
    sticky="e",
    pady=(10, 5)
)


result_frame.columnconfigure(
    1,
    weight=1
)


# =========================================================
# Enterキーでも計算
# =========================================================

root.bind(
    "<Return>",
    lambda event: calculate()
)


# 初期フォーカス
salary_entry.focus()


# =========================================================
# 起動
# =========================================================

root.mainloop()

#テスト