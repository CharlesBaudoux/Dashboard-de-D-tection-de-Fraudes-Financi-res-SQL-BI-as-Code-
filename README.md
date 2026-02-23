# 🛡️ SentinelSQL : Système de Détection de Fraudes Financières (BI-as-Code)

[![Live Demo](https://img.shields.io/badge/Demo-Live_Portfolio-blue?style=for-the-badge&logo=vercel)](TA_URL_VERCEL_ICI)
[![Tech](https://img.shields.io/badge/Stack-SQL_%7C_DuckDB_%7C_Evidence-orange?style=for-the-badge)](https://evidence.dev)

## 📌 Présentation du Projet
SentinelSQL est un tableau de bord analytique haute performance conçu pour identifier les comportements frauduleux sur les marchés financiers. Contrairement aux outils BI traditionnels, ce projet adopte une approche **"BI-as-Code"**, où toute la logique de données et la visualisation sont versionnées et traitées comme du logiciel.

**Objectif :** Transformer des millions de transactions brutes en signaux d'alerte exploitables pour les équipes de conformité (Compliance).

---

## 🚀 Fonctionnalités Analytiques (Expertise SQL)
Le projet met en œuvre des requêtes SQL complexes pour détecter trois types d'anomalies majeures :

1. **Détection de Wash Trading :** Identification des transactions circulaires (Acheteur = Vendeur) via des **Self-Joins** optimisés avec des fenêtres temporelles de 10 secondes.
2. **Analyse de Risque Statistique (Z-Score) :** Utilisation de **Window Functions** pour calculer l'écart-type de l'activité des utilisateurs et isoler les profils à risque (> 3 sigmas).
3. **Surveillance du Slippage :** Jointures temporelles précises pour comparer le prix d'exécution aux oracles de marché et détecter les manipulations de prix.
4. **Détection de Pics de Volume :** Algorithme de moyenne mobile sur 24h pour identifier les comportements de type "Pump and Dump".

---

## 🛠️ Stack Technique
Ce projet utilise la **Modern Data Stack** pour garantir rapidité et portabilité :

* **Moteur SQL :** [DuckDB](https://duckdb.org/) (In-process OLAP) pour des agrégations ultra-rapides.
* **Framework BI :** [Evidence.dev](https://evidence.dev/) (BI-as-Code) pour le rendu Markdown + SQL.
* **Format de Données :** Fichiers **Apache Parquet** pour un stockage colonnaire optimisé.
* **Ingestion :** Scripts Python pour la génération de données synthétiques réalistes.
* **Déploiement :** Vercel (CI/CD automatisé via GitHub).

---

## 🏗️ Architecture des Données
1. **Génération :** `generate_sentinel_data.py` crée des jeux de données transactionnels.
2. **Stockage :** Les données sont stockées dans `/sources/sentinel/` au format `.parquet`.
3. **Transformation :** Les calculs analytiques sont effectués à la volée par DuckDB lors du build.
4. **Visualisation :** Le rendu est généré de manière statique pour une performance maximale.

---

## 💻 Installation Locale
Pour explorer le projet sur votre machine :

```bash
# Cloner le projet
git clone [https://github.com/CharlesBaudoux/Dashboard-de-D-tection-de-Fraudes-Financi-res-SQL-BI-as-Code-.git](https://github.com/CharlesBaudoux/Dashboard-de-D-tection-de-Fraudes-Financi-res-SQL-BI-as-Code-.git)

# Installer les dépendances
npm install

# Lancer le serveur de développement
npm run dev
