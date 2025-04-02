import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("/workspace/boilerplate-page-view-time-series-visualizer/fcc-forum-pageviews.csv", parse_dates=['date'], index_col='date')

# Clean data

df = df[
    (df["value"] >= df["value"].quantile(0.025)) &
    (df["value"] <= df["value"].quantile(0.975))
]


def draw_line_plot():
    # Draw line plot

    fig, ax = plt.subplots()
    ax.plot(df.index, df["value"], "r", linewidth=1)
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = None

    # Draw bar plot

    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar["month"] = df_bar.index.month
    df_bar["year"] = df_bar.index.year
    df_bar = df_bar.groupby(["year", "month"])["value"].mean()
    df_bar = df_bar.unstack()
    # Draw bar     
    fig = df_bar.plot.bar(legend=True, figsize=(10, 5), ylabel="Average Page Views", xlabel="Years").figure
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.legend(fontsize=10, title="Months", labels=[
        "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
    ])
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    month_mapping = {
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, 
        "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
    }
    df_box['month_num'] = df_box['month'].map(month_mapping)  

    df_box["year"] = df_box["year"].astype("int")
    df_box["month_angka"] = df_box["date"].dt.month

    df_box = df_box.sort_values('month')
    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(1, 2, figsize=(10,5))
    
    ax[0].set_title('Year-wise Box Plot (Trend)')
    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('Page Views')
    sns.boxplot(x='year', y='value', data=df_box, ax=ax[0])

    ax[1].set_title('Month-wise Box Plot (Seasonality)')
    ax[1].set_xlabel('Month')
    ax[1].set_ylabel('Page Views')
    sns.boxplot(x='month_num', y='value', data=df_box, ax=ax[1], order=list(month_mapping.keys())


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
