import streamlit as st
import requests
import pandas as pd

def get_club_members(club_slug):
    url = 'https://api.sorare.com/federation/graphql'
    
    # Nouvelle requête GraphQL
    query = '''
    {
      football {
        club(slug: "''' + club_slug + '''") {
          activeMemberships {
            nodes {
              player {
                displayName
                position
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

        # Debugging output
        st.write("Réponse brute de l'API :", data)

        if 'data' in data and 'football' in data['data'] and 'club' in data['data']['football']:
            memberships = data['data']['football']['club']['activeMemberships']['nodes']
            if memberships:
                # Récupération des informations des joueurs
                players_data = []
                for node in memberships:
                    player = node['player']
                    players_data.append({
                        'Nom du joueur': player['displayName'],
                        'Position': player['position']
                    })
                
                # Création du DataFrame
                df = pd.DataFrame(players_data)
                
                # Affichage du tableau dans Streamlit
                st.write(f"Membres actifs du club {club_slug} :")
                st.dataframe(df)
            else:
                st.write(f"Aucun membre actif trouvé pour le club {club_slug}.")
        else:
            st.write(f"Erreur : structure inattendue dans la réponse de l'API pour le club {club_slug}.")
    except requests.exceptions.RequestException as e:
        st.write("Erreur lors de la requête à l'API:", e)

# Afficher l'interface utilisateur
st.title("Récupération des membres actifs d'un club sur Sorare")
club_slug = st.text_input("Entrez le slug du club:")
if st.button("Récupérer les données"):
    if club_slug:
        get_club_members(club_slug)
    else:
        st.write("Veuillez entrer un slug de club pour récupérer les données.")
