import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr,kendalltau,spearmanr
import pingouin as pg

#------------------------------------------DATASET------------------------------------------------------------
#read the csv
df1=pd.read_csv('HS_data_2.csv')
df2=pd.read_csv('FL_data_2.csv')
df3=pd.read_csv('HSH_data_2.csv')

#combine all tracks
combined_df = pd.concat([df1, df2, df3], ignore_index=True)

#save it to a main csv after combining (this is optional)
combined_df.to_csv('harr_all_tracks_2.csv')

interested_columns=['duration_ms','danceability','energy','key','loudness','speechiness','instrumentalness',
                   'liveness','valence','tempo','popularity']
subset_df = combined_df[interested_columns]


#-------------------------------------------------ANALYSIS-----------------------------------------------------


# Calculate the correlation matrix
correlation_matrix = subset_df.corr(method='kendall')

#P-value
for col in interested_columns:
    correlation_coeff,p_value=kendalltau(subset_df[col],subset_df['popularity'])
    print(f"parameter: {col}")
    print(f"Correlation Coefficient: {correlation_coeff}")
    print(f"P-Value: {p_value}")

#------------------------------------------------VISUALISATION-------------------------------------------------------
# Mask for the upper triangle (to remove redundancy)
mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
plt.rcParams["font.family"] = 'monospace'
plt.figure(figsize=(10, 8))
plt.title("Correlation among Harry's track features")
# Create a heatmap using seaborn
sns.heatmap(correlation_matrix, annot=True, cmap='BrBG', fmt=".2f", linewidths=.5,mask=mask)
plt.show()





c_sorted_df = combined_df.sort_values(by='speechiness', ascending=False)
c2_sorted_df=combined_df.sort_values(by='popularity', ascending=False)
# Print the 'track' column of the sorted DataFrame
print(c2_sorted_df['track'])
print("-----------------")
print(c2_sorted_df['popularity'])
