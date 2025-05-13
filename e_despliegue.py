import pandas as pd
from sklearn import neighbors
from sklearn.preprocessing import MinMaxScaler
import sqlite3 as sql
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
import a_funciones as fn
import logging
from tqdm import tqdm

# Configurar logs
logging.basicConfig(
    filename='G:\\Mi unidad\\cod\\LEA3_Marketing\\Salidas\\reco\\script_log.log',  
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def preprocesar(conn=None, cur=None):
    #con = sql.connect('data\\db_movies')
    #cur = con.cursor()

    # Ejecutar SQL para filtrar datos
    fn.ejecutar_sql('G:\\Mi unidad\\cod\\LEA3_Marketing\\preprocesamientos.sql', cur)
    log_mes = 'Ejecución de SQL completada.'
    logging.info(log_mes)
    print(log_mes)

    df_full = pd.read_sql('SELECT * FROM full_rating', conn)

    # Pipeline para transformar datos
    pipeline = Pipeline(steps=[
        ('genres_transform', FunctionTransformer(fn.split_and_encode_genres, validate=False)),
        ('extract_title_year', FunctionTransformer(fn.extract_title_and_year, validate=False)),
        ('remove_nan_years', FunctionTransformer(fn.remove_nan_years, validate=False))
    ])
    df_full = pipeline.fit_transform(df_full)

    # Escalar año y rating
    scaler = MinMaxScaler()
    df_full['movie_year'] = scaler.fit_transform(df_full[['movie_year']])
    df_full['movie_rating'] = scaler.fit_transform(df_full[['movie_rating']])

    # Columnas dummy de género
    columnas_excluir = {'movie_id', 'movie_title', 'user_id', 'movie_rating', 'movie_year'}
    genre_cols = [col for col in df_full.columns if col not in columnas_excluir and df_full[col].dropna().isin([0, 1]).all()]
    feature_cols = genre_cols + ['movie_year']

    return df_full, feature_cols, genre_cols, conn, cur

def recomendar_con_genero(df_full, feature_cols, user_id, genero, n_recomendaciones=10,conn=None, cur=None):
    df_user = df_full[df_full['user_id'] == user_id]
    if df_user.empty:
        return pd.DataFrame({'user_id': [user_id], 'mensaje': [f'Usuario sin registros.']})

    rated_ids = df_user['movie_id'].unique()
    df_rated = df_user[feature_cols].copy()
    df_rated['dummy'] = 1
    perfil = df_rated.groupby('dummy').mean()

    log_mes=f'Generando recomendaciones para el usuario {user_id}.'
    logging.info(log_mes)   
    print(log_mes)

    # Filtrar no vistas del género solicitado
    df_no_rated = df_full[(~df_full['movie_id'].isin(rated_ids)) & (df_full[genero] == 1)]
    df_no_rated = df_no_rated.drop_duplicates('movie_id')
    if df_no_rated.empty:
        return pd.DataFrame({'user_id': [user_id], 'mensaje': [f'Sin películas del género {genero} para recomendar.']})

    X_no_rated = df_no_rated[feature_cols]
    model = neighbors.NearestNeighbors(n_neighbors=n_recomendaciones, metric='cosine')
    model.fit(X_no_rated)
    dist, idx = model.kneighbors(perfil)

    recs = df_no_rated.iloc[idx[0]][['movie_title', 'movie_id']].copy()
    recs['similitud'] = 1 - dist[0]  
    recs['user_id'] = user_id
    recs['genero'] = genero

    log_mes=f'Recomendaciones para el usuario {user_id} finalizadas'
    logging.info(log_mes)
    print(log_mes)

    return recs


def main(list_users, generos):
    #df_full, feature_cols, genre_cols = preprocesar()

    conn=sql.connect('G:\\Mi unidad\\cod\\LEA3_Marketing\\data\\db_movies')
    cur=conn.cursor()

    log_mes = 'Conexión y preprocesamiento completados.'
    logging.info(log_mes)
    print(log_mes)

    recomendaciones_todos = pd.DataFrame()
    
    df_full, feature_cols, genre_cols, conn, cur= preprocesar(conn, cur)

    for user_id in tqdm(list_users):
        for genero in generos:
            if genero in genre_cols:
                recs = recomendar_con_genero(df_full, feature_cols, user_id, genero)
                recomendaciones_todos = pd.concat([recomendaciones_todos, recs], ignore_index=True)

    recomendaciones_todos.to_excel('G:\\Mi unidad\\cod\\LEA3_Marketing\\Salidas\\reco\\recomendaciones.xlsx')
    recomendaciones_todos.to_csv('G:\\Mi unidad\\cod\\LEA3_Marketing\\Salidas\\reco\\recomendaciones.csv')

    log_mes = 'Recomendaciones generadas y guardadas en Excel y CSV.'
    logging.info(log_mes)
    print(log_mes)

if __name__ == "__main__":
    list_users = [609, 161, 266]
    generos = ['Action', 'Comedy', 'Romance']
    main(list_users, generos)

import sys
sys.executable