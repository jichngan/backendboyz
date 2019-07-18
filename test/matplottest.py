#This code is to animate the graph 

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def animate(i):
  data = pd.read_csv('data.csv')
  x = data["DNS Host"]
  y1 = data["Bytes"]

  plt.cla()
  plt.bar(x,y1)
  plt.tight_layout()

ani = FuncAnimation(plt.gcf(), animate, interval=1000)
plt.tight_layout()
plt.show()

