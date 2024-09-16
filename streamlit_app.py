import streamlit as st
import requests
import pandas as pd

def get_club_data(club_slug):
    url = 'https://api.sorare.com/federation/graphql'

    # Requête combinée pour récupérer les données principales et supplémentaires
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

        if 'data' in data and 'football' in data['data'] and 'club' in data['data']['football']:
            memberships = data['data']['football']['club']['activeMemberships']['nodes']
            if memberships:
                # Récupération des informations des joueurs
                players_data = []
                for node in memberships:
                    player = node['player']
                    players_data.append({
                        'Nom du joueur': player['displayName'],
                        'Position': player['position'],
                        'Score moyen (15 derniers SO5)': player['averageScore'],
                        'Éligible U23': "Oui" if player['u23Eligible'] else "Non"
                    })
                
                # Création du DataFrame
                df = pd.DataFrame(players_data)
                return df
            else:
                st.write(f"Aucun membre actif trouvé pour le club {club_slug}.")
        else:
            st.write(f"Erreur : structure inattendue dans la réponse de l'API pour le club {club_slug}.")
    except requests.exceptions.RequestException as e:
        st.write("Erreur lors de la requête à l'API:", e)
    
    return pd.DataFrame()

# Afficher l'interface utilisateur
st.title("Récupération des membres actifs d'un club sur Sorare")
club_slug = st.text_input("Entrez le slug du club:")

if st.button("Récupérer les données"):
    if club_slug:
        # Récupérer toutes les données (nom, position, score et éligibilité U23)
        df = get_club_data(club_slug)

        if not df.empty:
            # Afficher le tableau avec toutes les données
            st.dataframe(df)
    else:
        st.write("Veuillez entrer un slug de club pour récupérer les données.")
