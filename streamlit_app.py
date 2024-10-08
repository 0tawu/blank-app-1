import streamlit as st
import requests
import pandas as pd

def get_club_data(club_slug):
    url = 'https://api.sorare.com/federation/graphql'

    query = '''
    {
        football {
            club(slug: "''' + club_slug + '''") {
                activeMemberships {
                    nodes {
                        player {
                            displayName
                            position
                            averageScore(type: LAST_FIFTEEN_SO5_AVERAGE_SCORE)
                            u23Eligible
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

        if data is not None:
            if 'data' in data and 'football' in data['data'] and 'club' in data['data']['football']:
                memberships = data['data']['football']['club']['activeMembers']
                if memberships:
                    players_data = []
                    for node in memberships:
                        player = node['player']
                        players_data.append({
                            'Nom du joueur': player['displayName'],
                            'Position': player['position'],
                            'Score moyen (15 derniers SO5)': player['averageScore'],
                            'Éligible U23': "Oui" if player['u23Eligible'] else "Non"
                        })

                    df = pd.DataFrame(players_data)
                    return df
                else:
                    st.write(f"Aucun membre actif trouvé pour le club {club_slug}.")
            else:
                st.write(f"Erreur : structure inattendue dans la réponse de l'API pour le club {club_slug}.")
        else:
            st.write("Aucune donnée reçue de l'API.")
    except requests.exceptions.RequestException as e:
        st.write("Erreur lors de la requête à l'API:", e)

    return pd.DataFrame()

st.title("Récupération des membres actifs d'un club sur Sorare")
club_slug = st.text_input("Entrez le slug du club:")

if st.button("Récupérer les données"):
    if club_slug:
        df = get_club_data(club_slug)

        if not df.empty:
            st.dataframe(df)
    else:
        st.write("Veuillez entrer un slug de club pour récupérer les données.")
