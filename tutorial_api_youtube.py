from googleapiclient.discovery import build
import pandas as pd
import requests
import os

#coisas que eu quero

'''
#video que me ensinou https://www.youtube.com/watch?v=SwSbnmqk3zY

Estatísticas grupais canal:

Reg - Total de vídeos x número de inscritos
Reg - Total de vídeos x views
Reg - Total de vídeos x view/video
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

Alpha2 = BR

'''


developer_key = os.environ.get("DEVELOPER_KEY")
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


youtube_con = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
developerKey=developer_key)


id_canal = ['UCT4nDeU5pv1XIGySbSK-GgA', 'UC7zXCDXJssKjkij2N2az39g'] #thiago, eu



request = youtube_con.channels().list(part = 'snippet, contentDetails, statistics', id = ",".join(id_canal)) #ao utilizar essa forma, podemos passar a id de varios canais

response = request.execute()


#2

#escolhendo um canal e capturando o codigo da playlist de uploads do mesmo

id_canal = 'UCT4nDeU5pv1XIGySbSK-GgA' #eu

request = youtube_con.channels().list(part = 'snippet, contentDetails, statistics', id = id_canal) #ao utilizar essa forma, podemos passar a id de varios canais

response = request.execute()

id_minha_playlist = response['items'][0]['contentDetails']['relatedPlaylists']['uploads'] #para acessar todos os vídeos postados por um canal, basta descobrir a playlist de uploads a partir da ID do canal.  

#pegando o ID de todos os vídeos do canal:

def get_video_ids(youtube, playlist_id):

    request = youtube.playlistItems().list(part = 'contentDetails', playlistId = playlist_id, maxResults = 50) #o maximo de videos são 50

    response = request.execute()

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


ids_video_meu_canal = get_video_ids(youtube=youtube_con,  playlist_id= id_minha_playlist)

#print(response)

def get_video_details(youtube, video_ids):

    all_video_stats = []

    for i in range (0, len(video_ids), 50):

        request = youtube.videos().list(part = 'snippet,statistics', id = ','.join(video_ids[i: i+50]))
        response = request.execute()

        

        for video in response['items']:

            video_stats = dict(titulo = video['snippet']['title'],
                                data_publicacao = video['snippet']['publishedAt'],
                                views = video['statistics']['viewCount'],
                                numero_likes = video['statistics']['likeCount'],
                                favoritadas = video['statistics']['favoriteCount'],
                                numero_comentarios = video['statistics']['commentCount'])

            all_video_stats.append(video_stats)

    
    return all_video_stats

videos_primo_rico = pd.DataFrame(get_video_details(youtube=youtube_con, video_ids = ids_video_meu_canal))

def formatando_data_frame_saida_api(df):

    df = df

    df['data_publicacao'] = pd.to_datetime(df['data_publicacao'])
    df['views'] = pd.to_numeric(df['views'])
    df['numero_likes'] = pd.to_numeric(df['numero_likes'])
    df['favoritadas'] = pd.to_numeric(df['favoritadas'])
    df['numero_comentarios'] = pd.to_numeric(df['numero_comentarios'])

    return df


videos_primo_rico = formatando_data_frame_saida_api(videos_primo_rico)

videos_primo_rico  = videos_primo_rico .sort_values(by = ['numero_comentarios'], ascending=False)

request = youtube_con.search().list(part = 'snippet', q= 'thiago nigro', type = 'channel', regionCode = 'BR', relevanceLanguage = 'pt')
response = request.execute()

print(response)



#print(videos_primo_rico )



