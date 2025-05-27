# from sklearn.model_selection import train_test_split, cross_val_score
# from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
# from sklearn.linear_model import Lasso

# import os

from flask import Flask, request, render_template
import pandas as pd
import pickle
from scipy.sparse import load_npz


app = Flask(__name__)
app.config["DEBUG"] = True

df = pd.read_parquet("df_combined_books_final.parquet")
tfidf_vectorizer = pickle.load(open("tfidf_vectorizer.pkl", "rb"))
cosine_sim = load_npz("cosine_sim_matrix.npz")

# print("El fichero que se está ejecutando es:")
# print(__file__)
# print("... que está en el directorio:")
# print(os.path.dirname(__file__))
# os.chdir(os.path.dirname(__file__))


# End Point "/"
@app.route('/', methods=['GET'])
def home():
    return "<h1>DeLibreroo</h1><p>Esta es una API para recomendar libros a manos de nuestro erudito lector IbAI.</p>"


# Función de recomendación híbrida
def get_recommendations_based_on_book_and_genre(selected_title, selected_genre, top_n=5):
    # Filtrar por género
    df_genre = df[df['genre'] == selected_genre].reset_index(drop=True)
    
    # Asegurar que el libro esté en el subconjunto
    if selected_title not in df_genre['title'].values:
        return []

    # Obtener índice del libro
    idx = df_genre[df_genre['title'] == selected_title].index[0]

    # Recalcular similitud dentro del género
    genre_texts = df_genre['combined_text']  # O lo que uses para la vectorización
    genre_matrix = tfidf_vectorizer.transform(genre_texts)
    similarities = genre_matrix.dot(genre_matrix[idx].T).toarray().ravel()

    top_indices = similarities.argsort()[::-1][1:top_n + 1]  # Omitimos el libro base
    return df_genre.iloc[top_indices][['title', 'genre']].to_dict(orient='records')


@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    generos = sorted(df['genre'].dropna().unique())
    libros = sorted(df['title'].dropna().unique())
    
    recomendaciones = []

    if request.method == 'POST':
        genero = request.form.get('genre')
        libro = request.form.get('book')
        # Aquí puedes generar recomendaciones con esos datos
        # recomendaciones = get_recommendations(genero, libro)

    return render_template('main.html', generos=generos, libros=libros, recomendaciones=recomendaciones)



# @app.route('/v1/predict', methods=['GET'])
# def predict():
#     model = pickle.load(open('ad_model.pkl','rb'))
#     genre = request.args.get('tv', None)
#     radio = request.args.get('radio', None)
#     newspaper = request.args.get('newspaper', None)

#     print(tv,radio,newspaper)
#     print(type(tv))

#     if tv is None or radio is None or newspaper is None:
#         return "Args empty, the data are not enough to predict"
#     else:
#         prediction = model.predict([[float(tv),float(radio),float(newspaper)]])
#     # [[float(tv),float(radio),float(newspaper)]]
#     # [pred1]
#     return jsonify({'predictions': prediction[0]})

# @app.route('/v1/retrain', methods=['GET'])
# def retrain():
#     if os.path.exists("data/Advertising_new.csv"):
#         data = pd.read_csv('data/Advertising_new.csv')

#         X_train, X_test, y_train, y_test = train_test_split(data.drop(columns=['sales']),
#                                                         data['sales'],
#                                                         test_size = 0.20,
#                                                         random_state=42)

#         model = Lasso(alpha=6000)
#         model.fit(X_train, y_train)
#         rmse = np.sqrt(mean_squared_error(y_test, model.predict(X_test)))
#         mape = mean_absolute_percentage_error(y_test, model.predict(X_test))
#         model.fit(data.drop(columns=['sales']), data['sales'])
#         pickle.dump(model, open('ad_model.pkl', 'wb'))

#         return f"Model retrained. New evaluation metric RMSE: {str(rmse)}, MAPE: {str(mape)}"
#     else:
#         return f"<h2>New data for retrain NOT FOUND. Nothing done!</h2>"


if __name__ == "__main__":
    app.run()
