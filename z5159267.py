import pandas as pd
import matplotlib.pyplot as plt


def question_1():
    print("--------------- question_1 ---------------")
    df_summer = pd.read_csv('Olympics_dataset1.csv')
    df_winter = pd.read_csv('Olympics_dataset2.csv')
    df = pd.merge(df_summer, df_winter, on="Team", how="outer")
    df.columns = [c.replace(' ', '_') for c in df.columns]
    columns_to_drop = [
        'Combined_Total',
        'Unnamed:_7',
        'Unnamed:_8',
        'Unnamed:_9',
        'Unnamed:_10'
    ]
    df.drop(columns_to_drop, inplace=True, axis=1)
    df.columns = [
        'Country', 'summer_rubbish', 'summer_participation', 'summer_gold', 'summer_silver', 'summer_bronze',
        'summer_total', 'winter_participation', 'winter_gold', 'winter_silver', 'winter_bronze', 'winter_total'
    ]
    # drop row 0
    df.drop(0, inplace=True, axis=0)
    # drop Totals row (last)
    df = df[:-1]
    print(df.head(5).to_string())
    return df


def question_2(df):
    print("--------------- question_2 ---------------")
    df['Country'] = df['Country'].str.extract(r'^\ *(.*)\s\(.*', expand=False)
    # set country as index
    df.set_index('Country', inplace=True)
    # remove some more columns
    columns_to_drop2 = [
        'summer_rubbish',
        'summer_total',
        'winter_total'
    ]
    df.drop(columns_to_drop2, inplace=True, axis=1)
    print(df.head(5).to_string())
    return df


def question_3(df):
    print("--------------- question_3 ---------------")
    # Remove the rows with NaN fields
    df = df.dropna()

    cols = ['summer_participation', 'summer_gold', 'summer_silver', 'summer_bronze',
            'winter_participation', 'winter_gold', 'winter_silver', 'winter_bronze']
    df[cols] = df[cols].apply(lambda s: pd.to_numeric(s.str.replace(',', '')))

    print(df.tail(10).to_string())
    return df


def question_4(df):
    print("--------------- question_4 ---------------")
    print(df['summer_gold'].idxmax())


def question_5(df):
    print("--------------- question_5 ---------------")
    name = (abs(df.summer_gold - df.winter_gold)).idxmax()
    diff = (abs(df.summer_gold - df.winter_gold)).max()
    print(name + " " + str(diff))


def question_6(df):
    print("--------------- question_6 ---------------")
    fn = lambda row: row.summer_gold + row.summer_silver + row.summer_bronze + row.winter_gold + row.winter_silver + row.winter_bronze
    total = df.apply(fn, axis=1)  # get column data with an index
    df = df.assign(total_medals=total.values)  # assign values to column 'total'

    total_df = df.sort_values(by='total_medals', ascending=False)
    print('Top 5 medals')
    print(total_df.head(5).to_string())

    print('\nBottom 5 medals')
    print(total_df.tail(5).to_string())


def question_7(df):
    print("--------------- question_7 ---------------")
    fn = lambda row: row.summer_gold + row.summer_silver + row.summer_bronze + row.winter_gold + row.winter_silver + row.winter_bronze
    total = df.apply(fn, axis=1)  # get column data with an index
    df = df.assign(total=total.values)  # assign values to column 'total'

    fn1 = lambda row: row.summer_gold + row.summer_silver + row.summer_bronze
    summer_total = df.apply(fn1, axis=1)
    df = df.assign(summer_total=summer_total.values)

    fn2 = lambda row: row.winter_gold + row.winter_silver + row.winter_bronze
    winter_total = df.apply(fn2, axis=1)
    df = df.assign(winter_total=winter_total.values)

    df_res = df.sort_values(['total'], ascending=False).head(10)
    df_stack = df_res[['summer_total', 'winter_total']]
    df_stack.plot.barh(stacked=True, title="Medals for Winter and Summer Games", legend=True, grid=True)
    plt.show()


def question_8(df):
    print("--------------- question_8 ---------------")
    df_winter = df.loc[['United States', 'Australia', 'Great Britain', 'Japan', 'New Zealand']]
    df_winter = df_winter[['winter_gold', 'winter_silver', 'winter_bronze']]

    df_winter.plot.bar(title='Winter Games', legend=True)
    plt.legend(['Gold', 'Silver', 'Bronze'])
    plt.show()


def question_9(df):
    print("--------------- question_9 ---------------")
    r = lambda row: (5 * row.summer_gold + 3 * row.summer_silver + 1 * row.summer_bronze) / row.summer_participation if row.summer_participation > 0 else 0
    rate = df.apply(r, axis=1)  # get column data with an index
    df = df.assign(rate=rate.values)  # assign values to column 'rate'

    rates_df = df[['rate']].sort_values(by='rate', ascending=False)
    print(rates_df.head(5).to_string())


def question_10(df):
    print("--------------- question_10 ---------------")
    df_cont = pd.read_csv('Countries-Continents.csv')

    s = lambda row: (5 * row.summer_gold + 3 * row.summer_silver + 1 * row.summer_bronze) / row.summer_participation if row.summer_participation > 0 else 0
    summer_rate = df.apply(s, axis=1)  # get column data with an index
    df = df.assign(summer_rate=summer_rate.values)  # assign values to column 'rate'

    w = lambda row: (5 * row.winter_gold + 3 * row.winter_silver + 1 * row.winter_bronze) / row.winter_participation if row.winter_participation > 0 else 0
    winter_rate = df.apply(w, axis=1)  # get column data with an index
    df = df.assign(winter_rate=winter_rate.values)  # assign values to column 'rate'

    df_merge = pd.merge(df_cont, df, how='right', on='Country')

    # divide the dataset into based on the continents
    africa_df = df_merge.query('Continent == "Africa"')
    asia_df = df_merge.query(' Continent == "Asia"')
    europe_df = df_merge.query('Continent == "Europe"')
    na_df = df_merge.query('Continent == "North America"')
    oceania_df = df_merge.query(' Continent == "Oceania"')
    sa_df = df_merge.query('Continent == "South America"')
    nan_df = df_merge.query('Continent != Continent')

    # Plot a scatter chart using x='summer_rate', y='winter_rate', and separate colors for each of the dataframes
    ax = africa_df.plot.scatter(x='summer_rate', y='winter_rate', label='Africa', color='blue')
    ax = asia_df.plot.scatter(x='summer_rate', y='winter_rate', label='Asia', color='red', ax=ax)
    ax = europe_df.plot.scatter(x='summer_rate', y='winter_rate', label='Europe', color='green', ax=ax)
    ax = na_df.plot.scatter(x='summer_rate', y='winter_rate', label='North America', color='yellow', ax=ax)
    ax = oceania_df.plot.scatter(x='summer_rate', y='winter_rate', label='Oceania', color='aqua', ax=ax)
    ax = sa_df.plot.scatter(x='summer_rate', y='winter_rate', label='South America', color='pink', ax=ax)
    ax = nan_df.plot.scatter(x='summer_rate', y='winter_rate', label='Others', color='gray', ax=ax)

    for i, name in enumerate(df_merge['Country']):
        ax.annotate(name, (df_merge.iloc[i]['summer_rate'], df_merge.iloc[i]['winter_rate']))

    plt.xlabel('Summer Rate')
    plt.ylabel('Winter Rate')
    plt.grid()
    plt.show()


if __name__ == "__main__":
    df = question_1()
    df = question_2(df)
    df = question_3(df)
    question_4(df)
    question_5(df)
    question_6(df)
    question_7(df)
    question_8(df)
    question_9(df)
    question_10(df)
