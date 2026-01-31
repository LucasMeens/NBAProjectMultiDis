# Projet Multi-Disciplinaire : Analyse des franchises NBA 
### E3FI - 2I - Semestre 1

## 1. USER GUIDE

Cette section explique comment installer et lancer le projet sur n'importe quelle machine.

### Prérequis
* **Python** (version 3.8 minimum)
* **Git**

### Installation

1.  **Cloner le dépôt et aller dans le dossier du projet :**
    ```bash
    git clone https://github.com/LucasMeens/NBAProjectMultiDis.git
    cd NBAProjectMultiDis
    ```

2.  **Installer les dépendances requises :**

    Si vous souhaitez utiliser un environnement virtuel : 
    ```bash
    python -m venv venv
    
    source venv/bin/activate

    pip install -r requirements.txt
    ```

### Lancement du Dashboard

- **Démarrer l'application :**

```bash
python main.py
```


## 2. DATA

Cette section sert a renseigner sur les données utilisées.

- **Format :** 
    - Nos fichiers sont tous au format CSV pour les données et jpg ou png pour les images.

- **Source :**
    - Kaggle : Utilisation de leur API (https://www.kaggle.com/)
    - Simple Maps : Téléchargement via URL (https://simplemaps.com/data/)

    (Tous les fichiers utilisés sont téléchargés au lancement de l'application pour s'assurer de leur présence grâce au fichier get_data.py)

- **Traitement :**
    - Le traitement des fichiers au format CSV se fait dans clean_data.py pour construire des fichiers conservant uniquement les données utiles pour ce projet. (Voir clean_data.py pour plus de détails).

- **Période :**
    - Nos données couvre de 1950 à 2018 fautes de données plus récentes de bonnes qualités.


## 3. Developer Guide

Cette section renseigne sur l'architecture de l'application et ensuite démontre comment ajouter rapidement une nouvelle page à l'application

### Architecture globale : 

- **1. Cas du téléchargement et nettoyage au démarrage :**

    - Le sens de la lecture se fait du haut vers le bas et de la gauche vers la droite (comme un roman)
        ```mermaid
        graph
            A((Kaggle / Internet))
            B[main.py]
            C(["download()"])
            D(["clean()"])
            J[get_data.py]
            K[clean_data.py]
            E[(Dossier raw)]
            F[(Dossier cleaned)]
            G[Dash App]
            H[stats_service.py]
            I((Utilisateur))

            A <--> C
            B --> |Appelle| C
            C --> |Lance| J
            J --> |Télécharge| E

            B --> |Appelle| D
            K --> |Lit| E
            D --> |Lance| K
            K --> |Nettoie| F

            B -->|Lance| G
            I <-->|Utilise| G
            G -->|Appelle| H

            H -.->|"Charge (Lazy Loading)"| F
        ```

- **2. Cas du lancement de la page des graphiques depuis la page d'accueil :**

    - Le sens de la lecture est le même
        ```mermaid
        graph 
            A((Page Accueil))
            B[[Bouton 'ALLER AUX GRAPHIQUES']]
            
            C["charts.py <br> (Charge filtres & HTML)"]
            
            D(["Affiche la Page <br> (Filtres remplis, Graphes vides)"])
            
            E(["Callbacks<br> (Lecture et calculs)"])
            
            F((Graphes <br> Remplis))

            G[(Donnees CSV)]

            A --> |Clic| B
            B -->|Lance| C
            
            C -->|Lit| G
            C -->|Renvoie le Layout| D
            
            D --> E
            E -->|Lit| G
            E -->|Met à jour| F
        ```

### Ajout d'une nouvelle page :

- **1. Création de la page :**

    - Créer le fichier de la page dans src/pages/ : 
        ```
        exemple.py
        ```

- **2. Ajout de la page au registre des pages :**

    - Dans exemple.py : 
        ```python
        import dash
        from dash import html

        dash.register_page(__name__, name="Nom de page")

            def layout():
                return html.Div([])
        ```

- **3. Bonus :**

    - Ajout de la barre de navigation :
        ```python
        import dash
        from dash import html
        from src.components.components.header import * # AJOUTER

        dash.register_page(__name__, name="Nom de page")

            def layout():
                return html.Div(
                    [
                        header() # AJOUTER
                    ]
                )
        ```

    - Ajout du filtre pour les saisons et les franchises :
        ```python
        import dash
        from dash import html
        from src.components.components.header import * 
        from src.components.components.filter import * # AJOUTER

        dash.register_page(__name__, name="Nom de page")

            def layout():
                return html.Div(
                    [
                        header(),
                        filter() # AJOUTER
                    ]
                )
        ```


    


    
    
