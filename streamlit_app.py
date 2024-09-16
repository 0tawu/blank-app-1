import streamlit as st
import requests

def get_so5_scores(player_slug):
    url = 'https://api.sorare.com/federation/graphql'
    
    query = '''
    {
        football {
            player(slug: "''' + player_slug + '''") {
                allSo5Scores(first: 50) {
                    nodes {
                        score
                        playerGameStats {
                            minsPlayed
                        }
                        decisiveScore {
                            totalScore
                        }
                    }
                }
            }
        }
    }
    '''

    options = {
        'json': {'query': query}
    }

    try:
        response = requests.post(url, **options)
        data = response.json()

        st.write("Données récupérées via l'API pour le joueur", player_slug, ":")
        if 'data' in data and data['data']['football']['player']['allSo5Scores']['nodes']:
            for node in data['data']['football']['player']['allSo5Scores']['nodes']:
                st.write("Score:", node['score'])
                st.write("Minutes jouées:", node['playerGameStats']['minsPlayed'])
                st.write("Score décisif total:", node['decisiveScore']['totalScore'])
                st.write("------------")
        else:
            st.write("Erreur: Aucune donnée valide récupérée pour le joueur", player_slug)
    except requests.exceptions.RequestException as e:
        st.write("Erreur lors de la requête à l'API:", e)

# Afficher l'interface utilisateur
st.title("Récupération des données pour un joueur sur Sorare")
player_slug = st.text_input("Entrez le slug du joueur:")
if st.button("Récupérer les données"):
    if player_slug:
        get_so5_scores(player_slug)
    else:
        st.write("Veuillez entrer un slug de joueur pour récupérer les données.")
