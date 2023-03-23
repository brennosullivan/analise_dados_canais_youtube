import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pytimeparse.timeparse import timeparse
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import os 


os.chdir('/home/brenno/Documentos/algoritmo_youtube')

'''

Estatística da moda entre as horas publicadas de todos os canais

Estatísticas grupais de vídeos:

Top 10 videos view/inscrito

Estatisticas individuais canal:

Videos publicados por mes -> video.groupby('month'(criar essa coluna), as_index = False).size()

Top videos por estatísticas:
- Top 10 comentários
- Top 10 views
- Top 10 likes

Top 10 vídeos geral (Rank somado de cada estatística)

Numero de vídeos por hora publicada -> video.groupby('hour'(criar essa coluna), as_index = False).size() 

'''

df_videos = pd.read_csv("estatisticas_de_videos.csv",  lineterminator='\n')
df_canais = pd.read_csv("estatisticas_canais.csv")

df_canais_videos = pd.merge(df_canais, df_videos, how = 'outer', on = 'nome_canal')


df_canais_videos['nome_canal'] = df_canais_videos['nome_canal'].apply(lambda x: x.strip())

#retirando videos com menos de 5 minutos da amostra. Vídeos muito curtos inpedem a análise direito. 

df_canais_videos['duracao_video'] = df_canais_videos['duracao_video'].astype(str)
df_canais_videos['duracao_video'] = df_canais_videos['duracao_video'].apply(lambda x: x.replace("PT", ""))
df_canais_videos = df_canais_videos.dropna()
df_canais_videos['duracao_video'] = df_canais_videos['duracao_video'].apply(lambda x: timeparse(x)/60)

#criando coluna do mês e da hora publicada dos vídeos:
df_canais_videos['data_publicacao'] = pd.to_datetime(df_canais_videos['data_publicacao'])

df_canais_videos['hora'] = df_canais_videos['data_publicacao'].apply(lambda x: x.hour)
df_canais_videos['mes'] = df_canais_videos['data_publicacao'].apply(lambda x: x.month)
df_canais_videos['ano'] = df_canais_videos['data_publicacao'].apply(lambda x: x.year)

df_canais_videos = df_canais_videos.query('duracao_video > 5')

#estatisticas view/inscritos

df_canais_videos['view_por_inscrito'] = df_canais_videos['views']/df_canais_videos['numero_inscritos']

df_estatistica_view_inscrito = df_canais_videos[['nome_canal', 'titulo', 'view_por_inscrito']].sort_values(by = 'view_por_inscrito', ascending=False)

df_estatistica_view_inscrito = df_estatistica_view_inscrito.query(" nome_canal != 'Tio Huli' ")

print(df_estatistica_view_inscrito.sort_values(by = 'view_por_inscrito', ascending=False).iloc[0:20, :])


#videos publicados por hora

#print(df_canais_videos[['nome_canal', 'hora']].groupby('hora').count().sort_values(by='hora'))

#videos publicados por hora e por canal

#print(df_canais_videos.groupby(['nome_canal'])['hora'].agg(pd.Series.mode))

#videos publicados por mes e ano

df_numero_videos = df_canais_videos[['nome_canal', 'mes', 'ano']].groupby(['mes', 'ano']).count().sort_values(by=['ano', 'mes'])

df_numero_videos = df_numero_videos.reset_index()

df_numero_videos['mes_ano'] = pd.to_datetime(df_numero_videos['mes'].astype(str) + "-" + df_numero_videos['ano'].astype(str))

df_numero_videos = df_numero_videos.set_index('mes_ano')

fig, ax = plt.subplots()

plt.plot(df_numero_videos.index.values, df_numero_videos['nome_canal'])

#plt.show()

#soma de comentarios por canal

df_comentarios = df_canais_videos.groupby(['nome_canal'])['numero_comentarios'].sum().sort_values(ascending=False)

#print(df_comentarios)

#soma de likes por canal

df_likes = df_canais_videos.groupby(['nome_canal'])['numero_likes'].sum().sort_values(ascending=False)

#print(df_likes)

#media duracao dos videos

df_duracao = df_canais_videos.groupby(['nome_canal'])['duracao_video'].median().sort_values(ascending=False)

print(df_duracao)

