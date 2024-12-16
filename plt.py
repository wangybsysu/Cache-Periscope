
#%%
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
# 1. load worldmap
world = gpd.read_file('ne_110m_admin_0_countries.shp')
data = pd.read_csv('open_result.csv')


data = data[data['whitewight']<70]

data['Spam_normalized'] = (data['wightSpam'] - data['wightSpam'].min()) / (data['wightSpam'].max() - data['wightSpam'].min())
data['Malware_normalized'] = (data['wightMalware'] - data['wightMalware'].min()) / (data['wightMalware'].max() - data['wightMalware'].min())
data['Phishing_normalized'] = (data['wightphishing'] - data['wightphishing'].min()) / (data['wightphishing'].max() - data['wightphishing'].min())

data['sum_column'] = data[['Spam_normalized', 'Malware_normalized', 'Phishing_normalized']].sum(axis=1)

# 2. load dataframe
df = data

# 3. create GeoDataFrame
geometry = gpd.GeoSeries.from_xy(df['lon'], df['lat'])
geo_df = gpd.GeoDataFrame(df, geometry=geometry)

# 4. create figure
fig, ax = plt.subplots(figsize=(15, 10))
worldf = world.cx[-180:180,-60:90]

worldf.plot(ax=ax, color='#8a96db', edgecolor='white')

# 5. plt scatter

scatter = ax.scatter(geo_df.geometry.x, geo_df.geometry.y, 
                     s=np.log1p(geo_df['sum_column'])* 1000,  # size
                     c=geo_df['sum_column'],  # colour
                     #cmap='OrRd',  # Color scheme
                     #edgecolor='black',  # 
                     alpha=0.6)  # 
ax.set_axis_off()
# 6. legend
cbar = plt.colorbar(scatter, ax=ax, label='Score', fraction=0.015, pad=0.04)  # 颜色条显示数值（例如人口）

# 7. 
#plt.title('Scatter Plot of Countries with Population Size')
plt.savefig('threatmap.pdf', dpi=600, )
# 8. 
plt.show()






# %%
