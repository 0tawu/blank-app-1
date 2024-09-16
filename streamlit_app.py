import streamlit as st
import requests
import pandas as pd

def get_club_members(club_slug):
    url = 'https://api.sorare.com/federation/graphql'
    
    # Première requête GraphQL pour récupérer le nom et la position des joueurs
    query_1 = '''
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
        'json': {'query': query_1}
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
                        'Position': player['position']
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

def get_additional_club_data(club_slug, df):
    url = 'https://api.sorare.com/federation/graphql'
    
    # Deuxième requête GraphQL pour récupérer les scores et l'éligibilité U23
    query_2 = '''
    {
      football {
        club(slug: "''' + club_slug + '''") {
          activeMemberships {
            nodes {
              player {
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
        'json': {'query': query_2}
    }

    try:
        response = requests.post(url, **options)
        data = response.json()

        if 'data' in data and 'football' in data['data'] and 'club' in data['data']['football']:
            memberships = data['data']['football']['club']['activeMemberships']['nodes']
            if memberships:
                # Récupération des informations supplémentaires pour chaque joueur
                for i, node in enumerate(memberships):
                    player = node['player']
                    # Ajout des scores et de l'éligibilité U23
                    df.at[i, 'Score moyen (15 derniers SO5)'] = player['averageScore']
                    df.at[i, 'Éligible U23'] = "Oui" if player['u23Eligible'] else "Non"
            else:
                st.write(f"Aucune donnée supplémentaire trouvée pour le club {club_slug}.")
        else:
            st.write(f"Erreur : structure inattendue dans la réponse de l'API pour les données supplémentaires du club {club_slug}.")
    except requests.exceptions.RequestException as e:
        st.write("Erreur lors de la requête à l'API:", e)

    return df

# Afficher l'interface utilisateur
st.title("Récupération des membres actifs d'un club sur Sorare")
club_slug = st.text_input("Entrez le slug du club:")

if st.button("Récupérer les données"):
    if club_slug:
        # Récupérer les premières données (nom et position)
        df = get_club_members(club_slug)

        if not df.empty:
            # Récupérer les données supplémentaires (score et U23) et les ajouter
            df = get_additional_club_data(club_slug, df)

            # Afficher le tableau avec toutes les données
            st.dataframe(df)
    else:
        st.write("Veuillez entrer un slug de club pour récupérer les données.")
