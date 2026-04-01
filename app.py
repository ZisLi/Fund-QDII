import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import akshare as ak
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 持仓基金
## 1. 广发纳指100ETF联接(QDII)F（021778）
fund_nasdaq = ak.fund_open_fund_info_em(
    symbol="021778",
    indicator="单位净值走势"
)

fund_nasdaq = fund_nasdaq.rename(
    columns={
        "净值日期": "date", 
        "单位净值": "net_value", 
        "日增长率": "growth_rate(%)"
        }
        )

fund_nasdaq["date"] = pd.to_datetime(fund_nasdaq["date"])
fund_nasdaq = fund_nasdaq[fund_nasdaq["date"] >= "2026-02-24"]
fund_nasdaq.reset_index(drop = True, inplace = True)

# 默认 daily invest = 0
fund_nasdaq["daily_invest"] = 0

# ----------- 定投规则 -----------
fund_nasdaq.loc[fund_nasdaq["date"] >= "2026-02-24", "daily_invest"] = 20
fund_nasdaq.loc[fund_nasdaq["date"] >= "2026-03-16", "daily_invest"] = 18
fund_nasdaq.loc[fund_nasdaq["date"] >= "2026-03-23", "daily_invest"] = 27
fund_nasdaq.loc[fund_nasdaq["date"] >= "2026-03-30", "daily_invest"] = 25

# ----------- 手动加仓 -----------
extra = {
    "2026-03-03": 200,
    "2026-03-05": 100,
    "2026-03-20": 50
}

for d, amt in extra.items():
    fund_nasdaq.loc[fund_nasdaq["date"] == pd.to_datetime(d), "daily_invest"] += amt

total_shares = 0
total_invest = 0

fund_nasdaq["shares"] = 0.0
fund_nasdaq["total_shares"] = 0.0
fund_nasdaq["asset"] = 0.0
fund_nasdaq["total_invest"] = 0.0

for i in range(len(fund_nasdaq)):
    nav = fund_nasdaq.loc[i, "net_value"]
    invest_today = fund_nasdaq.loc[i, "daily_invest"]

    # 买入 / 卖出
    shares = invest_today / nav

    total_shares += shares
    total_invest += invest_today

    fund_nasdaq.loc[i, "shares"] = round(shares, 2)
    fund_nasdaq.loc[i, "total_shares"] = round(total_shares, 2)
    fund_nasdaq.loc[i, "asset"] = round(total_shares * nav, 2)
    fund_nasdaq.loc[i, "total_invest"] = round(total_invest, 2)

fund_nasdaq["profit"] = round(fund_nasdaq["asset"] - fund_nasdaq["total_invest"], 2)
fund_nasdaq["Return Rate (%)"] = round(fund_nasdaq["profit"] / fund_nasdaq["total_invest"] * 100, 2)
fund_nasdaq["Fund"] = "广发纳斯达克100"

fund_nasdaq = fund_nasdaq[[ "Fund", "date", "net_value", "growth_rate(%)", "daily_invest", "total_shares", "asset", "total_invest", "profit", "Return Rate (%)"]]

## 2. 摩根标普500指数(QDII)A（017641）
fund_sp500 = ak.fund_open_fund_info_em(
    symbol="017641",
    indicator="单位净值走势"
)

fund_sp500 = fund_sp500.rename(
    columns={
        "净值日期": "date", 
        "单位净值": "net_value", 
        "日增长率": "growth_rate(%)"
        }
        )

fund_sp500["date"] = pd.to_datetime(fund_sp500["date"])
fund_sp500 = fund_sp500[fund_sp500["date"] >= "2026-03-03"]
fund_sp500.reset_index(drop = True, inplace = True)

# 默认 daily invest = 0
fund_sp500["daily_invest"] = 0
fee_rate = 0.0012
# ----------- 定投规则 -----------
fund_sp500.loc[fund_sp500["date"] >= "2026-03-03", "daily_invest"] = 50* (1 - fee_rate)
fund_sp500.loc[fund_sp500["date"] >= "2026-03-09", "daily_invest"] = 50 * (1 - fee_rate)
fund_sp500.loc[fund_sp500["date"] >= "2026-03-17", "daily_invest"] = 10 * (1 - fee_rate)
fund_sp500.loc[fund_sp500["date"] >= "2026-03-21", "daily_invest"] = 0 * (1 - fee_rate)
fund_sp500.loc[fund_sp500["date"] >= "2026-03-30", "daily_invest"] = 12 * (1 - fee_rate)
# ----------- 手动加仓 -----------
extra = {
    "2026-03-27": 50 * (1 - fee_rate)
}

for d, amt in extra.items():
    fund_sp500.loc[fund_sp500["date"] == pd.to_datetime(d), "daily_invest"] += amt

total_shares = 0
total_invest = 0

fund_sp500["shares"] = 0.0
fund_sp500["total_shares"] = 0.0
fund_sp500["asset"] = 0.0
fund_sp500["total_invest"] = 0.0

for i in range(len(fund_sp500)):
    nav = fund_sp500.loc[i, "net_value"]
    invest_today = fund_sp500.loc[i, "daily_invest"]

    # 买入 / 卖出
    shares = invest_today / nav

    total_shares += shares
    total_invest += invest_today

    fund_sp500.loc[i, "shares"] = round(shares, 2)
    fund_sp500.loc[i, "total_shares"] = round(total_shares, 2)
    fund_sp500.loc[i, "asset"] = round(total_shares * nav, 2)
    fund_sp500.loc[i, "total_invest"] = round(total_invest, 2)

fund_sp500["profit"] = round(fund_sp500["asset"] - fund_sp500["total_invest"], 2)
fund_sp500["Return Rate (%)"] = round(fund_sp500["profit"] / fund_sp500["total_invest"] * 100, 2)
fund_sp500["Fund"] = "摩根标普500"

fund_sp500 = fund_sp500[[ "Fund", "date", "net_value", "growth_rate(%)", "daily_invest", "total_shares", "asset", "total_invest", "profit", "Return Rate (%)"]]

## 3. 易方达全球成长精选混合(QDII)A（012920）
fund_global = ak.fund_open_fund_info_em(
    symbol="012920",
    indicator="单位净值走势"
)

fund_global = fund_global.rename(
    columns={
        "净值日期": "date", 
        "单位净值": "net_value", 
        "日增长率": "growth_rate(%)"
        }
        )

fund_global["date"] = pd.to_datetime(fund_global["date"])
fund_global = fund_global[fund_global["date"] >= "2026-02-24"]
fund_global.reset_index(drop = True, inplace = True)

# 默认 daily invest = 0
fund_global["daily_invest"] = 0
fee_rate_global = 0.0015
# ----------- 定投规则 -----------
fund_global.loc[fund_global["date"] >= "2026-02-24", "daily_invest"] = 10 * (1 - fee_rate_global)
fund_global.loc[fund_global["date"] >= "2026-03-03", "daily_invest"] = 0
fund_global.loc[fund_global["date"] >= "2026-03-24", "daily_invest"] = 50
fund_global.loc[fund_global["date"] >= "2026-03-30", "daily_invest"] = 25

# ----------- 手动加仓 -----------
extra = {
    "2026-03-03": 50 * (1 - fee_rate_global),
    "2026-03-05": 30 * (1 - fee_rate_global),
    "2026-03-18": -43.54+0.33,
    "2026-03-19": -44.12+0.33

}

for d, amt in extra.items():
    fund_global.loc[fund_global["date"] == pd.to_datetime(d), "daily_invest"] += amt

total_shares = 0
total_invest = 0

fund_global["shares"] = 0.0
fund_global["total_shares"] = 0.0
fund_global["asset"] = 0.0
fund_global["total_invest"] = 0.0

for i in range(len(fund_global)):
    nav = fund_global.loc[i, "net_value"]
    invest_today = fund_global.loc[i, "daily_invest"]

    # 买入 / 卖出
    shares = invest_today / nav

    total_shares += shares
    total_invest += invest_today

    fund_global.loc[i, "shares"] = round(shares, 2)
    fund_global.loc[i, "total_shares"] = round(total_shares, 2)
    fund_global.loc[i, "asset"] = round(total_shares * nav, 2)
    fund_global.loc[i, "total_invest"] = round(total_invest, 2)

fund_global["profit"] = round(fund_global["asset"] - fund_global["total_invest"], 2)
fund_global["Return Rate (%)"] = round(fund_global["profit"] / fund_global["total_invest"] * 100, 2)
fund_global["Fund"] = "易方达全球成长"

fund_global = fund_global[[ "Fund", "date", "net_value", "growth_rate(%)", "daily_invest", "total_shares", "asset", "total_invest", "profit", "Return Rate (%)"]]

funds = pd.concat([fund_nasdaq, fund_sp500, fund_global], ignore_index = True)
funds["daily profit"] = funds.groupby("Fund")["profit"].diff()
funds.head()

date = funds["date"].max()
date_only = date.date()


total_funds = funds[funds["date"] <= date].copy()
total_funds["weight"] = (
    total_funds["asset"] /
    total_funds.groupby("date")["asset"].transform("sum")
)

# 加权收益率
total_funds["weighted_rate"] = (
    total_funds["Return Rate (%)"] * total_funds["weight"]
)

# 每天组合收益
portfolio_rate = (
    total_funds.groupby("date")["weighted_rate"]
    .sum()
    .reset_index()
)
portfolio_rate["smooth"] = portfolio_rate["weighted_rate"].rolling(5).mean()

fig_rate = px.line(
    funds,
    x="date",
    y="Return Rate (%)",
    color="Fund",
    title=f"Portfolio Total Profit Rate(%) (Updated on {date_only})"
)

fig_rate.add_trace(
    go.Scatter(
        x=portfolio_rate["date"],
        y=round(portfolio_rate["weighted_rate"],2),
        mode="lines",
        name="Portfolio",
        line=dict(color="black", width=2, dash="dash")
    )
)

fig_rate.add_hline(
    y=0,
    line=dict(color="red", width=2, dash="dash")
)
fig_rate.update_layout(legend_title="Fund")

funds_share = (
    funds[funds["date"] == date]
         .groupby("Fund")
         .tail(1)
         .reset_index(drop=True)
)

funds_share["color"] = funds_share["daily profit"].apply(
    lambda x: "Positive" if x >= 0 else "Negative"
)

funds_share = funds_share.sort_values("daily profit")

fig_pie = px.pie(
    funds_share,
    names="Fund",
    values="asset",
    title=f"Asset Allocation (Updated on {date_only})"
)

fig_pie.update_traces(
    textinfo="percent"
)

fig_pie.update_traces(hole=0.3)



profit_nasdaq = funds_share["daily profit"][funds_share["Fund"] == "广发纳斯达克100	"]
profit_sp500 = funds_share["daily profit"][funds_share["Fund"] == "摩根标普500	"]
profit_global = funds_share["daily profit"][funds_share["Fund"] == "易方达全球成长"]

fig_profit = px.bar(
    funds_share,
    x="Fund",
    y="daily profit",
    color="color",
    title=f"Earnings (Updated on {date_only})",
    color_discrete_map={
        "Positive": "#16c784",
        "Negative": "#ea3943"
    }
)

fig_profit.update_traces(
    hovertemplate="Fund: %{x}<br>Profit: %{y:.2f}"
)

fig_profit.update_layout(showlegend=False)

fig_profit.update_layout(xaxis_title=None, yaxis_title=None)

Profit = funds_share["daily profit"].sum()

Invest = funds_share["total_invest"].sum()

Asset = funds_share["asset"].sum()

Return_Rate = round((Asset - Invest)/Invest * 100, 2)

Arrow = "▲" if Asset > Invest else "▼"
arrow = "▲" if Profit > 0 else "▼"

df_time = (
    funds.groupby("date")
    .agg({
        "asset": "sum",
        "total_invest": "sum"
    })
    .reset_index()
)

df_time["Returns"] = df_time["asset"] - df_time["total_invest"]

def make_card(title, value, color="black"):
    return dbc.Card(
        dbc.CardBody([
            html.H6(title, className="text-muted"),
            html.H2(value, style={"color": color,
                                  "fontWeight": "bold"})
        ]),
        style={
            "textAlign": "center",
            "borderRadius": "15px",
            "boxShadow": "0 4px 10px rgba(0,0,0,0.1)"
        }
    )


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])


# ===== layout =====
app.layout = dbc.Container([

    html.H2("📊 Portfolio", className="my-4"),
    html.Br(),
    
    dbc.Row([
        dbc.Col(make_card("Total Asset", f"{Asset:.2f}({Arrow}{Return_Rate:.2f}%)",
                          color = "#16c784" if Asset > Invest else "#ea3943")),
        dbc.Col(make_card("Total Invest", f"{Invest:.2f}")),
        dbc.Col(make_card("Return", f"{arrow}{Profit:.2f}",
                          color = "#16c784" if Profit > 0 else "#ea3943"
                          ))
    ]),
    html.Br(),
    
    html.Div([
    
    dcc.Dropdown(
        id="time-filter",
        options=[
            {"label": "1W", "value": 7},
            {"label": "1M", "value": 30},
            {"label": "3M", "value": 90},
            {"label": "All", "value": "all"},
        ],
        value="all",
        clearable=False,
        style={
            "position": "absolute",
            "top": "10px",
            "right": "20px",
            "width": "120px",
            "zIndex": 1000,
            "backgroundColor": "white"
        }),
    dcc.Graph(id="profit-chart")], 
    style={"position": "relative"}),
    html.Br(),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_profit), xs = 12, md = 6),
        dbc.Col(dcc.Graph(figure=fig_pie), xs = 12, md = 6)])], fluid=True)

@app.callback(
    Output("profit-chart", "figure"),
    Input("time-filter", "value")
)

def update_chart(days):
    print("Dropdown value:", days)
    df_filtered = funds.copy()
    if days != "all":
        df_filtered = (
            df_filtered.sort_values("date")
            .groupby("Fund")
            .tail(days)
        )
    fig_rate = px.line(
        df_filtered,
        x="date",
        y="Return Rate (%)",
        color="Fund",
        title=f"Return Rate(%)"
    )
    
    pr_filtered = portfolio_rate.copy()

    if days != "all":
        pr_filtered = pr_filtered.tail(days)

    fig_rate.add_trace(
        go.Scatter(
            x=pr_filtered["date"],
            y=round(pr_filtered["weighted_rate"], 2),
            mode="lines",
            name="Portfolio",
            line=dict(color="black", width=2.5)
        )
    )
    fig_rate.add_hline(
        y=0,
        line=dict(color="red", width=2, dash="dash")
    )
    fig_rate.update_layout(
    xaxis_title=None,
    yaxis_title=None)
    return fig_rate

app.layout.style = {
    "backgroundColor": "#DAE8FA"
    }


server = app.server
if __name__ == "__main__":
    app.run(debug=True)