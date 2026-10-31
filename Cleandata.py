import pandas as pd
import glob

files = glob.glob("*.csv")

dataraw = pd.concat((pd.read_csv(f) for f in files), ignore_index = True)

data = dataraw[["Date", "Gross Sales", "Source"]]
data.to_csv('transactions_clean.csv', index=False)

data["Date"] = pd.to_datetime(data["Date"])
data["Year_Month"] = data["Date"].dt.to_period("M").dt.to_timestamp()
data["Year"] = data["Date"].dt.year
month_labels = pd.date_range("2000-01-01", periods=12, freq="MS").strftime("%b")
data["Month"] = pd.Categorical(
    data["Date"].dt.strftime("%b"),
    categories=month_labels,
    ordered=True,
)
data["gross_sales"] = pd.to_numeric(
    data["Gross Sales"].str.replace(r"\$|,", "", regex=True),
    errors="coerce",
)

agg_sales_month = (
    data.groupby(
        ["Year", "Month", "Year_Month", "Source"],
        as_index=False,
        dropna=False,
        observed=True,
    )
    .agg(Gross_sales=("gross_sales", lambda values: values.sum(min_count=len(values))))
)

agg_sales_month.to_csv('transaction_month.csv', index=False)