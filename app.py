import pandas as pd
from pathlib import Path
from dash import Dash, dcc, html
import plotly.express as px

# Load data
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "pink_morsels_sales.csv"

df = pd.read_csv(DATA_PATH)
df["date"] = pd.to_datetime(df["date"])

# Aggregate sales by date
daily_sales = (
    df.groupby("date", as_index=False)["sales"]
    .sum()
    .sort_values("date")
)

# Create line chart
fig = px.line(
    daily_sales,
    x="date",
    y="sales",
    labels={"date": "Date", "sales": "Total Sales ($)"},
    title="Pink Morsels Sales Over Time"
)

# Price increase marker (SAFE METHOD)
price_increase_date = pd.to_datetime("2021-01-15")

fig.add_shape(
    type="line",
    x0=price_increase_date,
    x1=price_increase_date,
    y0=0,
    y1=1,
    yref="paper",
    line=dict(color="red", dash="dash")
)

fig.add_annotation(
    x=price_increase_date,
    y=1,
    yref="paper",
    text="Price Increase (15 Jan 2021)",
    showarrow=False,
    xanchor="left",
    yanchor="bottom"
)

# Dash app
app = Dash(__name__)
app.layout = html.Div([
    html.H1(
        "Soul Foods – Pink Morsels Sales Visualiser",
        style={"textAlign": "center"}
    ),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)

