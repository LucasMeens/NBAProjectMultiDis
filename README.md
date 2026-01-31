# Projet Multi-Disciplinaire : Analyse des franchises NBA 
### E3FI - 2I - Semestre 1

## I - USER GUIDE

Cette section explique comment installer et lancer le projet sur n'importe quelle machine.

### Prérequis
* **Python** (version 3.8 minimum)
* **Git**

### Installation

- **I - Cloner le dépôt et aller dans le dossier du projet :**
    ```bash
    git clone https://github.com/LucasMeens/NBAProjectMultiDis.git
    cd NBAProjectMultiDis
    ```

- **II - Installer les dépendances requises :**

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


## II - DATA

Cette section sert à renseigner sur les données utilisées.

- **Format :** 
    - Nos fichiers sont tous au format CSV pour les données et jpg ou png pour les images.

- **Source :**
    - Kaggle : Utilisation de leur API (https://www.kaggle.com/)
    - Simple Maps : Téléchargement via URL (https://simplemaps.com/data/)

    (Tous les fichiers utilisés sont téléchargés au lancement de l'application pour s'assurer de leur présence grâce au fichier get_data.py)

- **Traitement :**
    - Le traitement des fichiers au format CSV se fait dans clean_data.py pour construire des fichiers conservant uniquement les données utiles pour ce projet. (Voir clean_data.py pour plus de détails).

- **Période :**
    - Nos données couvrent de 1950 à 2018. faute de données plus récentes et de bonnes qualités.


## III - Developer Guide

Cette section renseigne sur l'architecture de l'application et ensuite démontre comment ajouter rapidement une nouvelle page à l'application

### Architecture globale : 

- **I - Cas du téléchargement et nettoyage au démarrage :**

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

- **II - Cas du lancement de la page des graphiques depuis la page d'accueil :**

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

- **I - Création de la page :**

    - Créer le fichier de la page dans src/pages/ : 
        ```
        exemple.py
        ```

- **II - Ajout de la page au registre des pages :**

    - Dans exemple.py : 
        ```python
        import dash
        from dash import html

        dash.register_page(__name__, name="Nom de page")

        def layout():
            return html.Div([])
        ```

- **III - Bonus :**

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

## IV - Rapport d'analyse

Dans cette section nous allons voir ce que les données nous disent.

Après avoir analysé nos différentes données, graphiques et notre carte, nous avons pu dégager deux grandes tendances qui expliquent le visage actuel de la NBA.

### La démographie

La carte de répartition des équipes met en lumière une réalité économique simple : la NBA s’installe là où se trouve la foule.

- **I - Remarques :**

    - On remarque très vite que les franchises sont concentrées dans les zones à forte densité de population. Cela parait assez évident. Pour qu’une équipe survive, elle a besoin de fans, de partenaires et d'infrastructures suffisamment grandes que seules les grandes villes à forte densité de populations possèdent.

- **II - Supposition :**
    
    - Il ne faut pas oublier que le système des franchises est là pour permettre de remporter de l'argent, on peut donc supposer que la ligue ou les propriétaire des franchises mettent une pression pour que les franchises soient dans les villes avec le plus de fans, infrastructure et partenaires potentiels pour rapporter le maximum via les partenariats ou les ventes (billets, maillots et merch en tout genre).

    - Nous pouvons également supposer qu'une ville avec peu d'habitants ne peut pas supporter le poids financier d'une franchise. Pour résumer, sans une forte densité de population, les villes n'ont pas les fonds ou les arguments pour permettre l'accueil d'une franchise NBA.

- **III - Conclusions :** 

    - Il est assez simple de se rendre compte qu'il n'y a pas qu'une seule cause a cette disparité des franchises dans leur localisation. Même si les potentielles pression de la ligue ou bien le souhait d'avoir du soutien (financier ou encore des supporters) Toutes ces raisons mènent au fait qu'aujourd'hui on observe clairement que les franchises ne s'installent pas n'importe où.

### Le spectacle offensif

Nos graphiques sur l'évolution du scoring montrent une tendance très marquée du basket au fil des années.

- **I - Remarques :**
    
    - On voit qu'entre les années 1950 jusqu'au années 2010, Les données montrent que le nombre de points marqués par match n’a, en moyenne, jamais cessé de grimper. 

- **II - Suppositions :**

    - Il y a clairement eu des changement au cours des années, c'est inévitable avec les changements d'époques. Il y a forcément eu des évolutions des règles et des styles de jeu (pour citer un changement majeur : l'importance du tir à trois points). Les joueurs également influencent le jeu, des phénomènes comme : Shaquille O'Neal, qui a obligé la ligue a revoir la conception de leur panier car il les brisaient, ou encore Stephen Curry qui est a l'origine de la monté de l'importance des tirs à trois points ont fortément influencé la manière dont le sport est joué aujourd'hui.
    
    - On peut assez facilement deviner que le jeu est devenu plus rapide et plus tourné vers l'attaque, rendant les matchs beaucoup plus rentables qu'auparavant car le spectacle n'en devient que meilleur. Cela est encore une fois influencé par la ligue mais aussi et surtout par les spectateurs.

- **III - Conclusions :**

    - Le constat est simple, plus les matchs sont spectaculaires, plus les spectateurs aiment. Les très bon joueurs passent d'athlète a super-star, ils redéfinissent le jeu tandis que les spectateurs deviennent des fans et les franchises se remplissent toujours plus les poches.

    - Il paraît donc normal que les règles d'une ligue basé sur le profit avec des joueurs de plus en plus spéctaculaire qui veulent absolument vaincre évolue dans ce sens.


### Conclusion globale

En regroupant ces deux analyse, on comprend mieux la stratégie de la ligue NBA aujourd'hui : sélectionner les marchés les plus denses pour assurer la stabilité économique, tout en favorisant un jeu de plus en plus offensif pour captiver le public. 
Pour le résumer en 2 mots, on pourrait dire Stratégie et Spectacles. 
    

## V - Copyright

- Nous déclarons sur l’honneur que le code fourni a été produit par nous-mêmes, à l’exception des lignes ci dessous :
    - Téléchargement Kaggle : 
        ```python
        import kagglehub

        # Download latest version
        path = kagglehub.dataset_download("kaggle-link")

        print("Path to dataset files:", path)
        ```
        Ceci est le code fourni directement sur kaggle lorsque l'on souhaite télécharger un dataset.
    
    - Fonctionnement de l'application :

        Une partie du fonctionnement de l'application a été faite grâce à la documentation en ligne de Dash.
        Par exemple pour le fonctionnement des Multi-pages : https://dash.plotly.com/urls

- Pour chaque ligne (ou groupe de lignes) empruntée, donner la référence de la source et une explication de la syntaxe utilisée.

- Toute ligne non déclarée ci dessus est réputée être produite par l’auteur (ou les auteurs) du projet. L’absence ou l’omission de déclaration sera considérée comme du plagiat.

 

    
    
