import numpy as np
import pandas as pd


def calculate_target_as_rate(df: pd.DataFrame) -> None:
    """
    "open" is the price at the beginning of the day, "close" is the stock price when it closes.
    So "close" is the stock price at the end of the day.

    Close_shift1 is the next day's Close, and Close_shift2 is the next day's Close.

    Rank indicates the ranking of the change rate of the closing price (Close) of the next day and the next day for each
    date of 2000 stocks, counting from the largest of the 2000 stocks.

    You can see that the rate and Target derived by the formula below match.
    The larger the Target, the higher the Rank.
    """
    df["Close_shift1"] = df["Close"].shift(-1)
    df["Close_shift2"] = df["Close"].shift(-2)
    df["rate"] = (df["Close_shift2"] - df["Close_shift1"]) / df["Close_shift1"]


def calc_spread_return_sharpe(df: pd.DataFrame, portfolio_size: int = 200, toprank_weight_ratio: float = 2) -> float:
    """
    Args:
        df (pd.DataFrame): predicted results
        portfolio_size (int): # of equities to buy/sell
        toprank_weight_ratio (float): the relative weight of the most highly ranked stock compared to the least.
    Returns:
        (float): sharpe ratio
    """

    def _calc_spread_return_per_day(df, portfolio_size, toprank_weight_ratio):
        """
        Args:
            df (pd.DataFrame): predicted results
            portfolio_size (int): # of equities to buy/sell
            toprank_weight_ratio (float): the relative weight of the most highly ranked stock compared to the least.
        Returns:
            (float): spread return
        """
        assert df['Rank'].min() == 0
        assert df['Rank'].max() == len(df['Rank']) - 1
        weights = np.linspace(start=toprank_weight_ratio, stop=1, num=portfolio_size)
        purchase = (df.sort_values(by='Rank')['Target'][:portfolio_size] * weights).sum() / weights.mean()
        short = (df.sort_values(by='Rank', ascending=False)['Target'][:portfolio_size] * weights).sum() / weights.mean()
        return purchase - short

    buf = df.groupby('Date').apply(_calc_spread_return_per_day, portfolio_size, toprank_weight_ratio)
    sharpe_ratio = buf.mean() / buf.std()
    return sharpe_ratio
