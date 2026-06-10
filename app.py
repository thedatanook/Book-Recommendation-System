from flask import Flask, render_template, request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
pt_df = pickle.load(open('pt_df.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_score = pickle.load(open('similarity_score.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', 
                           book_name = list(popular_df['book_title'].values),
                           author = list(popular_df['book_author'].values),
                           rating = list(popular_df['no_of_rating'].values),
                           image = list(popular_df['image_url_l'].values),
                           vote = list(popular_df['avg_of_rating'].values))

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt_df.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key = lambda x:x[1], reverse = True)[1:11]

    data = []
    for i in similar_items:
        title = pt_df.index[i[0]]
        
        # Try to get rating and details from popular_df if available
        if title in popular_df['book_title'].values:
            temp = popular_df[popular_df['book_title'] == title].drop_duplicates('book_title')
            item = [
                temp.iloc[0]['book_title'],
                temp.iloc[0]['book_author'],
                temp.iloc[0]['image_url_l'],
                temp.iloc[0]['avg_of_rating']  # ⭐ Star rating
            ]
        else:
            # Fallback to books dataframe (no rating)
            temp = books[books['book_title'] == title].drop_duplicates('book_title')
            item = [
                temp.iloc[0]['book_title'],
                temp.iloc[0]['book_author'],
                temp.iloc[0]['image_url_l'],
                0  # Default to 0 if rating not available
            ]

        data.append(item)
        
    return render_template('recommend.html', data=data, user_input=user_input)

if __name__ == '__main__':
    app.run(debug=True)