import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv("medical_examination.csv")

# 2
df["overweight"]=df["weight"]/((df["height"]/100)**2)
df["overweight"]=df["overweight"].apply(lambda x:1 if x>25 else 0)
# 3
df['cholesterol']=df['cholesterol'].apply(lambda x:1 if x>1 else 0)
df['gluc']=df['gluc'].apply(lambda x:1 if x>1 else 0)

# 4
def draw_cat_plot():
    df_cat = pd.melt(df, id_vars=['cardio'],
                     value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index()
    df_cat = df_cat.rename(columns={0: 'total'})

    
    graph = sns.catplot(data=df_cat, kind="bar", x="variable", y="total", hue="value", col="cardio")
    fig = graph.fig

    
    fig.savefig('catplot.png')
    return fig


# 10
def draw_heat_map():
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) &
                 (df['height'] >= df['height'].quantile(0.025)) &
                 (df['height'] <= df['height'].quantile(0.975)) &
                 (df['weight'] >= df['weight'].quantile(0.025)) &
                 (df['weight'] <= df['weight'].quantile(0.975))
                 ]
    corr = df_heat.corr()
    mask = np.triu(np.ones_like(corr,dtype=bool))
    fig, ax = plt.subplots(figsize=(16, 9))
    sns.heatmap(corr,mask=mask,square=True, linewidths=0.5,annot=True,fmt='.1f')

    # 16
    fig.savefig('heatmap.png')
    return fig
