import streamlit as st
import pickle as pkl
import requests
new_df=pkl.load(open('movies.pkl','rb'))
similarity=pkl.load(open('similarity.pkl','rb'))

# function to fetch the posters of the recommended movies from the API
def fetch_poster(movie_id):
    response=requests.get("https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

# function to return the recommended movies when the recommend button is clicked
def recommend(movie):
    movie_index=new_df[new_df['title']==movie].index[0]
    distances=similarity[movie_index]
    movie_list=sorted(list(enumerate(distances)),reverse=True, key=lambda x: x[1])[1:6]
    selected_movie_index=sorted(list(enumerate(distances)),reverse=True,key=lambda x: x[1])[0:1]
    selected_movie_id=new_df.iloc[selected_movie_index[0][0]].id


    recommended_list=[]
    recommended_movies_poster=[]
    recommended_movie_id = []

    for i in movie_list:

        movie_id= new_df.iloc[i[0]].id
        recommended_movie_id.append(movie_id)
        recommended_list.append(new_df.iloc[i[0]].title)

        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movie_id,selected_movie_id,recommended_list,recommended_movies_poster



st.title("SD Movie Recommendation System")

selected_movie_name=st.selectbox("Select Your Movie",new_df['title'].values)



if st.button('Recommend'):
    recommended_movie_id,selected_movie_id,names,poster=recommend(selected_movie_name)
    selected_movie_poster=fetch_poster(selected_movie_id)
    st.text("Selected movie")
    selected_movie_name_lower=selected_movie_name.lower()
    temp=selected_movie_name.lower().split()
    temp="-".join(temp)
    link="https://www.themoviedb.org/movie/"
    selected_movie_address = link + str(selected_movie_id)+ "-"+temp
    st.image(selected_movie_poster,width=150)
    st.write("[{}]({})".format(selected_movie_name,selected_movie_address))

    address_rec = []
# for the recommended movies
    for i in range(0,5):
        temp=names[i].lower().split()
        temp="-".join(temp)
        link="https://www.themoviedb.org/movie/"
        address=link+str(recommended_movie_id[i])+"-"+temp
        address_rec.append(address)

    #selected_movie_name
    st.text("Recommended Movies")
    col1, col2, col3, col4, col5= st.columns(5)
    with col1:
        st.image(poster[0])
        st.write("[{}]({})".format(names[0],address_rec[0]))

    with col2:
        st.image(poster[1])
        st.write("[{}]({})".format(names[1], address_rec[1]))

    with col3:
        st.image(poster[2])
        st.write("[{}]({})".format(names[2], address_rec[2]))

    with col4:
        st.image(poster[3])
        st.write("[{}]({})".format(names[3], address_rec[3]))

    with col5:
        st.image(poster[4])
        st.write("[{}]({})".format(names[4], address_rec[4]))


#st.write('[{}](https://share.streamlit.io/mesmith027/streamlit_webapps/main/MC_pi/streamlit_app.py)'.format(var1))