import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from functions import *
from math import *

# 1. Настройка страницы
st.set_page_config(page_title="Financial Calculator", layout="wide", page_icon="icon_v2.png")

# 2. CSS для центрирования вкладок
st.markdown("""
    <style>
    /* Центрируем заголовок */
    .main-title {
        text-align: center;
        font-size: 3rem !important;
        font-weight: 700;
        margin-bottom: 2rem;
        color: #1E1E1E;
    }
    /* Центрируем блок вкладок */
    div[data-testid="stTabs"] [role="tablist"] {
        justify-content: center;
    }
    /* Делаем вкладки чуть крупнее */
    button[data-baseweb="tab"] p {
        font-size: 1.2rem;
    }
    /* Убираем лишние отступы у контейнеров */
    .block-container {
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title"> Финансовый калькулятор</h1>', unsafe_allow_html=True)

# Ограничиваем контент по центру для симметрии
_, main_col, _ = st.columns([1, 3, 1])

with main_col:
    tabs = st.tabs([" Калькулятор вклада", " Калькулятор кредита"])

    # --- ВКЛАД ---
    with tabs[0]:
        st.subheader("Расчёт вклада")
        st.info("Расчёт разных параметров вклада")
        c1, c2, c3 = st.columns(3)
        with c1:
            type_of_vklad = st.selectbox("Начисление процентов", ["на счёт вклада", "на другой счёт"])
            type_of_calculating = st.selectbox("Выбор расчёта", ["Конечная сумма", "Начальная сумма", "Срок вклада"])

        if type_of_vklad == "на счёт вклада":
            if type_of_calculating == "Конечная сумма":  # Вклад: общий блок
                with c2:
                    amount = st.number_input("Начальная сумма вклада", min_value=100.0, value=100000.0, step=10000.0,
                                             format="%.1f")  # нач сумма
                    rate = st.number_input("Годовая ставка (%)", min_value=0.1, value=10.0, step=0.1,
                                           format="%.1f")  # ставка
                    period_years = st.number_input("Срок вклада (лет)", min_value=1, value=5, step=1)  # срок
                    comp_freq = st.selectbox("Частота капитализации",
                                             ["Ежемесячно", "Ежеквартально", "Ежегодно"])  # частота процентов
            elif type_of_calculating == "Начальная сумма":
                with c2:
                    final_amount = st.number_input("Конечная сумма вклада", min_value=200.0, value=100000.0, step=1000.0,
                                                   format="%.1f")  # кон сумма
                    rate = st.number_input("Годовая ставка (%)", min_value=0.1, value=10.0, step=0.1,
                                           format="%.1f")  # ставка
                    period_years = st.number_input("Срок вклада (лет)", min_value=1, value=5, step=1)  # срок
                    comp_freq = st.selectbox("Частота капитализации",
                                             ["Ежемесячно", "Ежеквартально", "Ежегодно"])
                amount = calculate_start_sum(final_amount, rate, period_years, period_factor(comp_freq))
            else:
                with c2:
                    amount = st.number_input("Начальная сумма вклада", min_value=100.0, value=100000.0, step=10000.0,
                                             format="%.1f")  # нач сумма
                    final_amount = st.number_input("Конечная сумма вклада", min_value=200.0, value=150000.0, step=10000.0,
                                                   format="%.1f")
                    rate = st.number_input("Годовая ставка (%)", min_value=0.1, value=10.0, step=0.1,
                                           format="%.1f")  # ставка
                    comp_freq = st.selectbox("Частота капитализации",
                                             ["Ежемесячно", "Ежеквартально", "Ежегодно"])
                period_years = p_years(final_amount, amount, rate, period_factor(comp_freq))

            balance, balances = calculate_deposit(amount, rate, ceil(period_years), period_factor(comp_freq))
        else:
            if type_of_calculating == "Конечная сумма":  # Вклад: общий блок
                with c2:
                    amount = st.number_input("Начальная сумма вклада", min_value=100.0, value=100000.0, step=10000.0,
                                             format="%.1f")  # нач сумма
                    rate = st.number_input("Годовая ставка (%)", min_value=0.1, value=10.0, step=0.1,
                                           format="%.1f")  # ставка
                    period_years = st.number_input("Срок вклада (лет)", min_value=1, value=5, step=1)  # срок

            elif type_of_calculating == "Начальная сумма":
                with c2:
                    final_amount = st.number_input("Конечная сумма вклада", min_value=200.0, value=100000.0, step=10000.0,
                                                   format="%.1f")  # кон сумма
                    rate = st.number_input("Годовая ставка (%)", min_value=0.1, value=10.0, step=0.1,
                                           format="%.1f")  # ставка
                    period_years = st.number_input("Срок вклада (лет)", min_value=1, value=5, step=1)  # срок
                amount = alt_start_sum(final_amount, rate, period_years)
            else:
                with c2:
                    amount = st.number_input("Начальная сумма вклада", min_value=100.0, value=100000.0, step=10000.0,
                                             format="%.1f")  # нач сумма
                    final_amount = st.number_input("Конечная сумма вклада", min_value=200.0, value=150000.0, step=10000.0,
                                                   format="%.1f")
                    rate = st.number_input("Годовая ставка (%)", min_value=0.1, value=10.0, step=0.1,
                                           format="%.1f")  # ставка
                period_years = alt_p_years(final_amount, amount, rate)

            balance, balances = alt_calculate_deposit(amount, rate, ceil(period_years))
        with c3:
            color_lines = st.color_picker(label="color of the lines", value='#32821e')
            color_dots = st.color_picker(label="color of the dots", value='#32821e')

        result = {"Конечная сумма": [balance, '₽'], "Начальная сумма": [amount, '₽'],
                  "Срок вклада": [period_years, 'лет']}

        st.divider()
        m1, m2 = st.columns(2)
        m1.metric("Итоговая сумма", f"{balance:,.2f} ₽")
        m2.metric("Чистая прибыль",
                  f"{balances[-1] - amount:,.2f} ₽")
        m3, m4 = st.columns(2)
        m3.metric("Начальная сумма", f"{amount:,.2f} ₽")
        m4.metric("Срок вклада", f'{period_years:,.2f} лет')

        # График по годам
        years = list(range(0, int(period_years) + 1))
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=years, y=balances, mode="lines+markers", name="Сумма",
                                 marker=dict(color=color_lines, size=8, line=dict(color=color_dots, width=5))))
        fig.update_layout(title="График роста суммы вклада по годам"
                          # if type_of_vklad == "на счёт вклада" else "График роста суммы на другом счёте"
                          , xaxis_title="Время, годы",
                          yaxis_title="Сумма, ₽")
        st.plotly_chart(fig, width='stretch')

    # Кредит
    with tabs[1]:
        st.subheader("Расчёт кредита")
        st.info("Расчёт основных параметров кредита")
        c4, c5, c6 = st.columns(3)
        with c4:
            type_of_calccred = st.selectbox("Выбор расчёта", ["Ежемесячный платёж", "Конечная сумма", "Срок"])
        if type_of_calccred == "Ежемесячный платёж":
            with c5:
                loan_amount = st.number_input("Сумма кредита", min_value=10000.0, value=2000000.0, step=10000.0,
                                              format="%.1f")
                apr = st.number_input("Годовая ставка по кредиту (%)", min_value=0.1, value=10.0, step=0.1,
                                      format="%.1f")
                term_years_cr = st.number_input("Срок кредита (лет)", min_value=1, value=5, step=1)
            monthly_payment = cre_plat(loan_amount, apr, term_years_cr)
        elif type_of_calccred == "Срок":
            with c5:
                loan_amount = st.number_input("Сумма кредита", min_value=10000.0, value=2000000.0, step=10000.0,
                                              format="%.1f")
                apr = st.number_input("Годовая ставка по кредиту (%)", min_value=0.1, value=10.0, step=0.1,
                                      format="%.1f")
                monthly_payment = st.number_input("Ежемесячный платёж", min_value=100.0, value=50000.0, step=100.0,
                                                  format="%.1f")
            term_years_cr = cre_years(loan_amount, monthly_payment, apr) / 12
        else:
            with c5:
                apr = st.number_input("Годовая ставка по кредиту (%)", min_value=0.1, value=10.0, step=0.1,
                                      format="%.1f")
                monthly_payment = st.number_input("Ежемесячный платёж", min_value=100.0, value=50000.0, step=100.0,
                                                  format="%.1f")
                term_years_cr = st.number_input("Срок кредита (лет)", min_value=1, value=5, step=1)
            loan_amount = cre_sum(monthly_payment, apr, term_years_cr)

        if loan_amount != inf and term_years_cr != inf:

            with c6:
                color_up = st.color_picker(label="Цвет кредитной суммы", value='#053c5e')
                color_down = st.color_picker(label="Цвет процентов", value='#a31621')
                color_lines = st.color_picker(label="Цвeт линий", value='#538d22')
                color_dots = st.color_picker(label="Цвет точек", value='#538d22')

            r = apr / 100.0 / 12
            n = ceil(term_years_cr * 12)
            st.divider()
            m1, m2 = st.columns(2)
            m1.metric("Сумма кредита", f"{loan_amount:,.2f} ₽")
            m2.metric("Общая переплата", f"{monthly_payment * n - loan_amount:,.2f} ₽")
            m1.metric("Ежемесячный платёж", f"{monthly_payment:,.2f} ₽")
            m2.metric("Срок кредита", f'{term_years_cr:,.2f} лет')
    
            # график амортизации
            payments = []
            balances = []

            balance = loan_amount
            for i in range(1, n + 1):
                interest = balance * apr / 100.0 / 12
                principal = monthly_payment - interest
                balance = balance - principal
                payments.append({"period": i, "payment": monthly_payment, "interest": interest, "principal": principal,
                                "balance": max(balance, 0)})
                balances.append(balance)

            df = pd.DataFrame(payments)
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(x=df["period"], y=df["principal"], name="Кредитная сумма", marker=dict(color=color_up)))
            fig2.add_trace(go.Bar(x=df["period"], y=df["interest"], name="Проценты", marker=dict(color=color_down)))
            fig2.update_layout(barmode='stack', title="График от",
                            xaxis_title="Период, мес",
                            yaxis_title="Сумма, ₽")
            st.plotly_chart(fig2, width='stretch')

            fig3 = go.Figure()
            fig3.add_trace(
                go.Scatter(x=df["period"], marker=dict(color=color_lines, size=6, line=dict(color=color_dots, width=4)),
                        y=df["balance"], mode="lines+markers", name="Остаток долга"))
            fig3.update_layout(title="Остаток долга по месяцам",
                            xaxis_title="Период, мес", yaxis_title="Остаток долга, ₽")
            st.plotly_chart(fig3, width='stretch')
        else:
            st.info("Вы никогда не выплатите и не возьмёте такой кредит, даже если оставите его на своих пра-пра-правнуков, попробуйте ввести другие значения:)")