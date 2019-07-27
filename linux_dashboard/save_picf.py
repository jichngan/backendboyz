import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style

style.use('fivethirtyeight')

data = pd.read_csv('data.csv')  

x = data['DNS Host']
y1 = data['Bytes']
plt.barh(x,y1, color = '#FFA07A')

plt.xlabel("Bytes Sent", fontweight = 'black')
plt.ylabel("DNS Host", fontweight= 'black')
figure = plt.gcf()
figure.set_size_inches(8,5)

plt.savefig('static/images/new_plot.png',bbox_inches = "tight",dpi=100)

plt.tight_layout()
#plt.show()



