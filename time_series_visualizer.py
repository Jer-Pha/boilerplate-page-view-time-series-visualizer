from calendar import month_name
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

COLORS = [
    "tab:blue",
    "tab:orange",
    "tab:green",
    "tab:red",
    "tab:purple",
    "tab:brown",
    "tab:pink",
    "tab:gray",
    "tab:olive",
    "tab:cyan",
    "tab:blue",
    "tab:orange",
]

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv")

# Clean data
df = df[
    df["value"].between(
        df["value"].quantile(0.025), df["value"].quantile(0.975)
    )
]
df["date"] = pd.to_datetime(df["date"])


def draw_line_plot():
    # Draw line plot
    fig = plt.figure(figsize=(15, 5))
    plt.plot(df["date"], df["value"], color="red")
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    plt.xticks(df["date"][::10])
    plt.xlabel("Date")
    plt.ylabel("Page Views")
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

    # Use tight layout to remove extra whitespace
    plt.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig("line_plot.png")
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()[["value"]]
    df_bar["year"] = df["date"].dt.year
    df_bar["month"] = df["date"].dt.month
    df_bar = (
        df_bar.groupby(["year", "month"])["value"]
        .mean()
        .reset_index(name="monthly_avg")
    )

    df_bar.head

    # Draw bar plot
    fig = plt.figure(figsize=(10, 8))
    bar_width = 0.05
    num_years = len(df_bar["year"].unique())
    group_width = 12 * bar_width
    total_width = num_years * group_width
    offset = (total_width - group_width) / 8

    for year, group in df_bar.groupby("year"):
        for i, (month, value) in enumerate(
            group.groupby("month")["monthly_avg"]
        ):
            position = year + (i * bar_width) - offset
            plt.bar(position, value, width=bar_width, color=COLORS[month - 1])

    plt.xticks(df_bar["year"].unique(), rotation=90)
    plt.yticks(range(0, int(df_bar["monthly_avg"].max()), 20000))
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")

    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, color=COLORS[i - 1]) for i in range(1, 13)
    ]
    plt.legend(labels=month_name[1:], title="Months", handles=legend_handles)

    # Save image and return fig (don't change this part)
    fig.savefig("bar_plot.png")
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box["year"] = df_box["date"].dt.year
    df_box["month"] = df_box["date"].dt.strftime("%b")

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))
    sns.boxplot(
        x="year",
        y="value",
        data=df_box,
        ax=ax1,
        palette="tab10",
        hue="year",
        legend=False,
        fliersize=2,
    )
    ax1.set_title("Year-wise Box Plot (Trend)")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Page Views")

    month_order = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    sns.boxplot(
        x="month",
        y="value",
        data=df_box,
        order=month_order,
        ax=ax2,
        palette="Set3",
        hue="month",
        legend=False,
        fliersize=2,
    )
    ax2.set_title("Month-wise Box Plot (Seasonality)")
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Page Views")

    fig.tight_layout(pad=2)

    # Save image and return fig (don't change this part)
    fig.savefig("box_plot.png")
    return fig
