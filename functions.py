def calculate_target_as_rate(df):
    """
    Rank indicates the ranking of the change rate of the closing price (Close) of the next day and the next day for each
    date of 2000 stocks, counting from the largest of the 2000 stocks.

    The larger the Target, the higher the Rank.

    Close_shift1 is the next day's Close, and Close_shift2 is the next day's Close.
    You can see that the rate and Target derived by the formula below match.
    """
    df["Close_shift1"] = df["Close"].shift(-1)
    df["Close_shift2"] = df["Close"].shift(-2)
    df["rate"] = (df["Close_shift2"] - df["Close_shift1"]) / df["Close_shift1"]
