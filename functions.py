from math import *
def period_factor(freq_label):
    return {"Ежемесячно": 12, "Ежеквартально": 4, "Ежегодно": 1, 0: 0}[freq_label]

# для НА СЧЁТ ВКЛАДА
def calculate_deposit(balance, rate, years, cap_freq=1.0):
    """
    balance: начальная сумма
    monthly_contr: сумма пополнения (за одно пополнение)
    rate: годовая ставка (например, 0.15 для 15%)
    years: срок в годах
    cap_freq: частота капитализации в год (12 - ежемесячно, 1 - ежегодно)
    contr_freq: частота пополнений в год (12 - ежемесячно, 4 - ежеквартально)
    """
    balances = [balance]

    # Считаем ставку за один период капитализации
    interest_per_cap = rate / 100.0 / cap_freq
    for year in range(1, years + 1):
        start_year_balance = balance
        for month in range(1, 13):
            # 1. Начисление процентов (если наступил месяц капитализации)
            if month % (12 / cap_freq) == 0:
                interest = balance * interest_per_cap
                balance += interest
        balances.append(balance)
    return balance, balances

def calculate_start_sum(Sk, r, t, n=1.0):
    return Sk/(1+r/100/n)**(n*t)

def p_years(sk, sn, r, n):
    return log(sk/sn)/(n*log(1 + r/100/n))

# для некрутого вклада с отправлением процентов на др счёт
def alt_start_sum(Sk, r, t):
    return Sk/(1+(r/100)*(t/365))

def alt_p_years(sk, sn, r):
    return ((sk-sn)*100)/(sn*r)

def alt_calculate_deposit(balance, rate, years):
    balances = [balance]
    for year in range(years):
        balances.append(balances[year] + balance*(rate/100))
    return balances[-1], balances


#credit
def cre_plat(s, r, years):
    #n - срок, s - сумма, r = ставка в процентах
    i = r/12/100
    n = years*12
    return s*((i*(1+i)**n)/((1+i)**n-1))

def cre_sum(a, r, years):
    i = r/12/100
    n = years*12
    try:
        return (a*((1+i)**n-1))/(i*(1+i)**n)
    except OverflowError or ValueError:
        return inf
def cre_years(s, a, r):
    i = r/12/100
    return log(a/(a-s*i), 1+i) if (a-s*i) > 0 else inf

