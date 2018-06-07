# -*- coding: utf-8 -*-
"""
plot totals
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("data/stats.csv")

sns.boxplot(x="genre", y="per_song", data=df,
                showfliers=False)

sns.set_context("notebook", font_scale=1.1)
sns.set_style("ticks")

sns.lmplot('overall', 'per_song',data=df, 
           fit_reg=False, hue="genre")
# Set title
plt.title('Histogram of IQ')

# Set x-axis label
plt.xlabel('Time')

# Set y-axis label
plt.ylabel('Deaths')