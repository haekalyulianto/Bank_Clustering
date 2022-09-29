from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
from difflib import SequenceMatcher
import plotly.graph_objs as go

def clustering(list_df):
  list_df_cluster = []
  list_of_letter = []
  list_of_cluster = []
  df_cluster = pd.DataFrame()

  for df in list_df:
    df_numpy = df.to_numpy()

    model = KMeans(n_clusters = 4, init = "k-means++", random_state=0)
    label = model.fit_predict(df_numpy)
    
    cluster_name = 'Cluster '+ df.columns[0]
    df_cluster = pd.DataFrame(label, columns = [cluster_name])
    df_cluster = df_cluster.set_index(df.index)
    
    letter_name = 'Letter ' + df.columns[0]
    df_cluster[letter_name] = df_cluster[cluster_name].apply(lambda x: chr(ord('`')+x+1))

    list_df_cluster.append(df_cluster)
    list_of_letter.append(letter_name)
    list_of_cluster.append(cluster_name)

  df_cluster = pd.concat(list_df_cluster, axis=1)
  cols = list_of_letter
  df_cluster["Fuzzy"] = df_cluster[cols].apply(lambda row: ''.join(row.values.astype(str)), axis=1)
  list_of_cluster.append('Fuzzy')
  df_cluster = df_cluster[list_of_cluster]
  
  return df_cluster

def calculate_fuzzy(a, b):
  s = SequenceMatcher()
  s.set_seqs(a, b)
  
  return s.ratio()

def plot(bank1, bank2, df, kolom):
  layout = go.Layout(paper_bgcolor='rgba(229,236,246,0)', plot_bgcolor='rgba(229,236,246,100)')

  df = df.loc[(df[kolom] == bank1) | (df[kolom] == bank2)]
  df = df.set_index(kolom)
  df2 = df.T

  fig = go.Figure(layout=layout)

  x_axis = [x for x in range(1,len(df2)+1)]

  fig.add_trace(
    go.Scatter(
      x=x_axis, 
      y=df2[bank1], 
      marker=dict(color="red"), 
      name='Bank '+str(bank1), 
      mode='markers',
      text=df2.index
    )
  )

  fig.add_trace(
    go.Scatter(
      x=x_axis, 
      y=df2[bank2], 
      marker=dict(color="blue"), 
      name='Bank '+str(bank2), 
      mode='markers',
      text=df2.index
    )
  )

  fig.update_traces(marker_size=6)
  fig.update_layout(height=540)
  fig.update_layout(width=960)

  return fig
