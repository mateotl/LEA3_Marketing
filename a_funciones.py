## para Visual Studio Code
## pip install google-generativeai
## para Jupyter Notebook
# !pip install google-generativeai


import pandas as pd
from mlxtend.preprocessing import TransactionEncoder


def ejecutar_sql (nombre_archivo, cur):
    sql_file=open(nombre_archivo)
    sql_as_string=sql_file.read()
    sql_file.close
    cur.executescript(sql_as_string)


# Funciones para Pipeline de preprocesamiento

# Función 1: separar géneros y convertir a binario con TransactionEncoder
def split_and_encode_genres(df):
    genres = df['movie_genres'].str.split('|')
    te = TransactionEncoder()
    genres_bin = te.fit_transform(genres)
    genres_df = pd.DataFrame(genres_bin, columns=te.columns_)

    # Eliminar "(no genres listed)" si existe
    if '(no genres listed)' in genres_df.columns:
        valid_rows = ~genres_df['(no genres listed)'] # La virgulilla me convierte lo TRUE en FALSE y viceversa
        df = df.loc[valid_rows].reset_index(drop=True) # Filtro por las columnas que si tienen género
        genres_df = genres_df.loc[valid_rows].drop(columns='(no genres listed)').reset_index(drop=True)

    # Eliminar columna original 'genres' y unir los géneros codificados
    df = df.drop(columns='movie_genres').reset_index(drop=True) # Elimina la columna original 'genres' del df
    return pd.concat([df, genres_df], axis=1)

# Función 2: extraer título y año
def extract_title_and_year(df):
    df['movie_title'] = df['movie_title'].str.strip()  # Elimina espacios al inicio y al final
    year = df['movie_title'].str.extract(r'\((\d{4})\)$')  # Extrae el año de 4 dígitos entre paréntesis al final
    year.columns = ['movie_year']
    title = df['movie_title'].str.replace(r'\s*\(\d{4}\)$', '', regex=True) # Elimina el año y espacio antes del título
    title.name = 'movie_title'
    df = df.drop(columns='movie_title') # Elimina la columna original que contenía título + año
    df = pd.concat([df.reset_index(drop=True), title.reset_index(drop=True), year.reset_index(drop=True)], axis=1)
    return df

# Función 3: eliminar registros con year == NaN, si existen
def remove_nan_years(df):
#Se usa notna para filtrar el df dejando solo las filas donde 'movie_year' no es NaN, es decir, donde si hay año
    return df[df['movie_year'].notna()].reset_index(drop=True)
