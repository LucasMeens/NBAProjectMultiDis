# Projet Multi-Disciplinaire : Analyse des franchises NBA 
### E3FI - 2I - Semestre 1

## 1. USER GUIDE

Cette section explique comment installer et lancer le projet sur n'importe quelle machine.

### Prérequis
* **Python** (version 3.8 minimum)
* **Git**

### Installation

1.  **Cloner le dépôt et aller dans le dossier du projet :**
    ```
    git clone https://github.com/LucasMeens/NBAProjectMultiDis.git
    cd NBAProjectMultiDis
    ```

2.  **Installer les dépendances requises :**

    Si vous souhaitez utiliser un environnement virtuel : 
    ```
    python -m venv venv
    
    source venv/bin/activate

    pip install -r requirements.txt
    ```

### Lancement du Dashboard

**Démarrer l'application :**

```
python main.py
```

## 2. DATA

Cette section sert a renseigner sur les données utilisées.

- **Format :** 
    - Nos fichiers sont tous au format CSV pour les données et jpg ou png pour les images.

- **Source :**
    - Kaggle : Utilisation de leur API (https://www.kaggle.com/)
    - Simple Maps : Téléchargement via URL (https://simplemaps.com/data/)

    (Tous les fichiers sont téléchargé au lancement de l'application pour s'assurer de leur présence grâce au fichier get_data.py)

- **Traitement :**

Le traitement des fichiers au format CSV se fait dans clean_data.py pour construire des fichiers conservant uniquement les données utiles pour ce projet. (Voir clean_data.py pour plus de détails).

- **Période :**

Nos données couvre de 1950 à 2018 fautes de données plus récentes de bonnes qualités.