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

**Démarrer l'application :**

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



### Ajout d'une nouvelle page :

**1. Création de la page :**

    - Créer le fichier de la page dans src/pages/ : 
        ```
        exemple.py
        ```

**2. Ajout de la page au registre des pages :**

    - Dans exemple.py : 
        ```python
        import dash
        from dash import html

        dash.register_page(__name__, name="Nom de page")

            def layout():
                return html.Div([])
        ```

**3. Bonus :**

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


    


    
    
