from googleapiclient.discovery import build
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os 

developer_key = os.environ.get("DEVELOPER_KEY")
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


youtube_con = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
developerKey=developer_key)


lista_canais = pd.read_csv('lista_canais.csv')

del lista_canais['nome_canal']

lista_canais = lista_canais['codigo'].to_list()

def extraindo_estatisticas_canais(lista_de_canais):

    ids_playlist_canais = []
    titulo_canal = []
    numero_inscritos = []
    numero_de_vizu = []
    numero_de_videos = []


    if len(lista_de_canais) != 1:

        request = youtube_con.channels().list(part = 'snippet, contentDetails, statistics', id = ",".join(lista_de_canais))

        response = request.execute()

        for i in range(0, len(lista_de_canais) - 1):
            
            numero_inscritos.append(np.int64(response['items'][i]['statistics']['subscriberCount']))
            numero_de_vizu.append(np.int64(response['items'][i]['statistics']['viewCount']))
            numero_de_videos.append(np.int64(response['items'][i]['statistics']['videoCount']))
            titulo_canal.append(response['items'][i]['snippet']['title'])
            ids_playlist_canais.append(response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
    
    else:

        request = youtube_con.channels().list(part = 'snippet, contentDetails, statistics', id = lista_de_canais)

        response = request.execute()
        
        numero_inscritos.append(np.int64(response['items'][0]['statistics']['subscriberCount']))
        numero_de_vizu.append(np.int64(response['items'][0]['statistics']['viewCount']))
        numero_de_videos.append(np.int64(response['items'][0]['statistics']['videoCount']))
        titulo_canal.append(response['items'][0]['snippet']['title'])
        ids_playlist_canais.append(response['items'][0]['contentDetails']['relatedPlaylists']['uploads'])
    
    view_por_video = np.array(numero_de_vizu)/np.array(numero_de_videos)

    df_id_playlist_canais = pd.DataFrame(data = {'nome_canal': titulo_canal, 
                                                'id_playlist_upload': ids_playlist_canais, 
                                                'numero_inscritos': numero_inscritos,
                                                'numero_de_vizu': numero_de_vizu,
                                                'numero_videos_canal': numero_de_videos,
                                                'view_por_video': view_por_video})

    return df_id_playlist_canais


df_estatisticas_canais = extraindo_estatisticas_canais(lista_de_canais=lista_canais)

df_estatisticas_canais.to_csv("estatisticas_canais.csv", index = False)


'''
Reg - Total de vídeos x número de inscritos
Reg - Total de vídeos x views
Reg - Total de vídeos x view/video

'''

#Reg - Total de vídeos x view/video ------------------------------------------

df_estatisticas_canais = df_estatisticas_canais.set_index("nome_canal")

df_estatisticas_canais = df_estatisticas_canais.drop(['Me poupe!', 'O Primo Rico'], axis= 0) #os dois são outliers muito bizarros

df_estatisticas_canais.sort_values(by = 'view_por_video').plot.scatter(x = "numero_videos_canal", y = "view_por_video", s = 10) 



df_estatisticas_canais.sort_values(by = 'view_por_video').iloc[:, 4].plot(kind='bar')


#Reg - Total de vídeos x view/video ------------------------------------------

df_estatisticas_canais.sort_values(by = 'view_por_video').plot.scatter(x = "numero_videos_canal", y = "numero_de_vizu", s = 10) 



#Reg - Total de vídeos x número de inscritos ------------------------------------------

df_estatisticas_canais = df_estatisticas_canais.reset_index()

# open figure + axis
fig, ax = plt.subplots()
# plot
ax.scatter(x=df_estatisticas_canais['numero_videos_canal'],y=df_estatisticas_canais['numero_inscritos'],c='DarkBlue')
# set labels
ax.set_xlabel('Numero_videos')
ax.set_ylabel('Numero inscritos')

#nomeando os canais por ponto

sns.lmplot(x='numero_videos_canal', y='numero_inscritos', data=df_estatisticas_canais, hue='nome_canal', fit_reg=False)


plt.show()










