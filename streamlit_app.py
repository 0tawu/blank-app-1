import streamlit as st
import requests

def get_club_members(club_slug):
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

        # Debugging output
        st.write("Réponse brute de l'API :", data)

        if 'data' in data and 'football' in data['data'] and 'club' in data['data']['football']:
            memberships = data['data']['football']['club']['activeMemberships']['nodes']
            if memberships:
                st.write(f"Membres actifs du club {club_slug} :")
                for node in memberships:
                    player = node['player']
                    st.write("Nom du joueur:", player['displayName'])
                    st.write("Position:", player['position'])
                    st.write("Score moyen (15 derniers SO5):", player['averageScore'])
                    st.write("Éligible U23:", "Oui" if player['u23Eligible'] else "Non")
                    st.write("------------")
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
