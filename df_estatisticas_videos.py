from urllib import response
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


df_canais = pd.read_csv("estatisticas_canais.csv")


def get_video_ids(youtube, playlist_id):

    request = youtube.playlistItems().list(part = 'contentDetails', playlistId = playlist_id, maxResults = 50) #o maximo de videos são 50

    response = request.execute()

    print(response)

    video_ids = []

    for i in range(len(response['items'])):

        video_ids.append(response['items'][i]['contentDetails']['videoId']) 

    next_page_token = response.get('nextPageToken') #dentro do primeiro response está o código para a próxima página caso tenha mais de 50 vídeos  

    more_pages = True

    while more_pages:
        if next_page_token is None:
            more_pages = False

        else:
            request = youtube.playlistItems().list(part = 'contentDetails', playlistId = playlist_id, maxResults = 50, pageToken = next_page_token)
            response = request.execute() 

            for i in range(len(response['items'])):

                video_ids.append(response['items'][i]['contentDetails']['videoId'])

            
            next_page_token = response.get('nextPageToken') 
    
    return video_ids

def get_video_details(youtube, video_ids, nome_do_canal):

    all_video_stats = []

    for i in range (0, len(video_ids), 50):

        request = youtube.videos().list(part = 'snippet,statistics, contentDetails', id = ','.join(video_ids[i: i+50]))
        response = request.execute()

        
        try: 
            for video in response['items']:

                video_stats = dict(titulo = video['snippet']['title'],
                                    data_publicacao = video['snippet']['publishedAt'],
                                    views = video['statistics']['viewCount'],
                                    numero_likes = video['statistics']['likeCount'],
                                    favoritadas = video['statistics']['favoriteCount'],
                                    numero_comentarios = video['statistics']['commentCount'],
                                    nome_canal = nome_do_canal,
                                    duracao_video = video['contentDetails']['duration'])

                all_video_stats.append(video_stats)
        except:
            pass


    
    return all_video_stats

def formatando_data_frame_saida_api(df):

    df = df

    df['data_publicacao'] = pd.to_datetime(df['data_publicacao'])
    df['views'] = pd.to_numeric(df['views'])
    df['numero_likes'] = pd.to_numeric(df['numero_likes'])
    df['favoritadas'] = pd.to_numeric(df['favoritadas'])
    df['numero_comentarios'] = pd.to_numeric(df['numero_comentarios'])

    return df

lista_df_estatisticas_todos_os_canais_e_todos_os_videos = []

for i, canal in enumerate(df_canais.index):

    

    id_dos_videos_do_canal = get_video_ids(youtube=youtube_con, playlist_id=df_canais.iloc[i, 1])
    df_dos_videos = pd.DataFrame(get_video_details(youtube=youtube_con, video_ids=id_dos_videos_do_canal, nome_do_canal=df_canais.iloc[i, 0]))
    df_dos_videos = formatando_data_frame_saida_api(df_dos_videos)

    lista_df_estatisticas_todos_os_canais_e_todos_os_videos.append(df_dos_videos)



df_estatisticas_todos_os_canais_e_todos_os_videos = pd.concat(lista_df_estatisticas_todos_os_canais_e_todos_os_videos)

df_estatisticas_todos_os_canais_e_todos_os_videos.to_csv('estatisticas_de_videos.csv', index=False)

id_dos_videos_do_canal = get_video_ids(youtube=youtube_con, playlist_id='UUCE-jo1GvBJqyj1b287h7jA')