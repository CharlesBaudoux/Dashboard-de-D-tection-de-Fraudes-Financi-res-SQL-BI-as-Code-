# 🚀 Instructions pour lancer SentinelSQL

## Prérequis
- Node.js ≥ 18 (vous avez v24.13.1 ✅)
- npm ≥ 8 (vous avez 11.8.0 ✅)
- Python 3 (pour régénérer les données si besoin)

## 1. Installer les dépendances

Ouvrez un terminal dans le dossier du projet (`/home/charles_baudoux/projet_sql`) et exécutez :

```bash
npm install --legacy-peer-deps
```

*Note* : Si vous rencontrez des erreurs réseau (EAI_AGAIN), réessayez après avoir vérifié votre connexion. Vous pouvez également utiliser `npm config set registry https://registry.npmjs.org/`.

## 2. Vérifier les données

Les fichiers Parquet sont déjà générés dans `sources/sentinel/`. Pour les régénérer (optionnel) :

```bash
source venv/bin/activate  # active l'environnement virtuel Python
python generate_sentinel_data.py
```

## 3. Lancer le serveur de développement

Une fois les dépendances installées, lancez Evidence.dev :

```bash
npm run dev
```

Le serveur démarrera sur `http://localhost:3000`. Ouvrez cette URL dans votre navigateur.

## 4. Accéder au dashboard

- Le dashboard principal est sur la page d’accueil (`/`).
- Toutes les requêtes SQL s’exécutent directement sur les fichiers Parquet via `read_parquet()`.
- Les visualisations (`<Value/>`, `<AreaChart/>`, `<DataTable/>`) sont interactives.

## 5. Commandes utiles

| Commande | Description |
|----------|-------------|
| `npm run dev` | Lance le serveur de développement (hot‑reload) |
| `npm run build` | Build la version statique pour production |
| `npm run sources` | Indexe les sources (pas nécessaire avec notre configuration) |

## Dépannage

### ❌ `npm install` échoue avec des erreurs réseau
- Vérifiez votre connexion Internet.
- Essayez `npm cache clean --force` puis réinstallez.
- Utilisez `--registry=https://registry.npmjs.org` explicitement.

### ❌ `npm run dev` affiche des erreurs de plugin
Notre configuration contourne le plugin DuckDB. Si des erreurs persistent, vérifiez que `evidence.config.yaml` contient :

```yaml
template: "@evidence-dev/template"
plugins:
  duckdb:
    path: "@evidence-dev/duckdb"
  "@evidence-dev/core-components": {}
  "@evidence-dev/tailwind": {}
```

### ❌ Les données ne s’affichent pas
Assurez‑vous que les fichiers `sources/sentinel/transactions.parquet` et `market_prices.parquet` existent. Vous pouvez vérifier avec `ls -lh sources/sentinel/`.

## Structure du projet

```
sentinel-sql/
├── pages/index.md          # Dashboard principal
├── sources/sentinel/       # Données Parquet + DuckDB
├── dataArchitecture.md     # Documentation d’architecture
├── sqlLogic.md            # Règles de fraude & logique SQL
├── generate_sentinel_data.py # Générateur de données
└── package.json           # Dépendances Evidence.dev
```

## Support

Pour toute question, référez‑vous au fichier `.clinerules` (standards MIAGE) ou contactez Charles Baudoux.

**Le dashboard est maintenant prêt à démontrer votre maîtrise de SQL avancé, DuckDB et Evidence.dev !**