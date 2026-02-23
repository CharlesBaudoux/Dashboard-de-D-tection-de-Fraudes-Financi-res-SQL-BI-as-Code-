---
title: Dictionnaire des Données | SentinelSQL
description: Documentation des tables et colonnes utilisées dans l'analyse de fraude.
---

# 📚 Dictionnaire des Données

Ce document décrit les sources de données simulées utilisées dans le projet SentinelSQL. Ces données reproduisent des transactions financières et des prix de marché pour illustrer des techniques avancées de détection de fraude.

**Origine des données** : Les jeux de données sont générés synthétiquement via le script Python `generate_sentinel_data.py`. Ils sont stockés au format Parquet et chargés dans DuckDB via les sources configurées dans Evidence.dev.

**Objectif pédagogique** : Ces données permettent de démontrer des concepts clés de l'analyse financière (wash trading, slippage, pics de volume) dans un environnement contrôlé, sans risque de divulgation d'informations sensibles.

---

## 🗂️ Structure de la Table `sentinel.transactions`

Cette table contient l'historique des transactions effectuées par les utilisateurs.

```sql schema_transactions
DESCRIBE sentinel.transactions
```

<DataTable data={schema_transactions} title="Schéma de la Table Transactions"/>

### Explication des colonnes clés

- **`trade_id`** (INTEGER) : Identifiant unique de la transaction. Clé primaire.
- **`user_id`** (VARCHAR) : Identifiant de l'utilisateur ayant initié la transaction.
- **`asset_id`** (VARCHAR) : Code de l'actif financier échangé (ex: `BTC`, `ETH`, `AAPL`).
- **`timestamp`** (TIMESTAMP) : Date et heure précise de la transaction (UTC).
- **`amount`** (DOUBLE) : Quantité d'actif échangée.
- **`price`** (DOUBLE) : Prix unitaire auquel la transaction a été exécutée (en euros).
- **`status`** (VARCHAR) : Statut de la transaction : `'completed'` (réussie), `'failed'` (échouée), `'pending'` (en attente).
- **`exchange`** (VARCHAR) : Plateforme d'échange où la transaction a eu lieu (ex: `binance`, `coinbase`).

**Utilité dans la détection de fraude** : La colonne `status` permet de filtrer les transactions effectives ; `amount` et `price` servent à calculer les volumes et les écarts ; `timestamp` permet les analyses temporelles (fenêtres glissantes, détection de pics).

---

## 🗂️ Structure de la Table `sentinel.market_prices`

Cette table stocke les prix de marché officiels (prix de référence) à différents instants.

```sql schema_market_prices
DESCRIBE sentinel.market_prices
```

<DataTable data={schema_market_prices} title="Schéma de la Table Market Prices"/>

### Explication des colonnes clés

- **`asset_id`** (VARCHAR) : Code de l'actif financier.
- **`timestamp`** (TIMESTAMP) : Date et heure de la cotation (UTC).
- **`market_price`** (DOUBLE) : Prix de marché de référence (en euros) à cet instant.

**Utilité dans la détection de fraude** : Les prix de marché servent de référence pour calculer le **slippage** (écart entre le prix d'exécution et le prix de marché). Une jointure temporelle (`ASOF JOIN`) permet d'aligner chaque transaction avec le dernier prix connu.

---

## 🔗 Relations entre les Tables

- **Jointure naturelle** : `transactions.asset_id` ↔ `market_prices.asset_id`
- **Jointure temporelle** : `transactions.timestamp` >= `market_prices.timestamp` (via `ASOF JOIN`)

Ces relations permettent d'enrichir chaque transaction avec le contexte de marché au moment de son exécution.

---

## 📊 Métriques Calculées à Partir de Ces Données

À partir de ces tables de base, le dashboard calcule les indicateurs suivants :

1. **Volume total** = `SUM(amount * price)`
2. **Slippage** = `ABS(transactions.price - market_prices.market_price) / market_prices.market_price`
3. **Wash trading** = détection de paires de transactions par le même utilisateur sur le même actif au même prix dans un intervalle de 10 secondes.
4. **Pics de volume** = volume sur une fenêtre d'une minute dépassant la moyenne des 24 heures précédentes de plus de 3 écarts‑type.
5. **Score de risque** = combinaison de la fréquence des transactions (`trade_count`) et du volume des gros trades (`large_trades`).

---

## 🧠 Notes Techniques pour le Jury MIAGE

- **Performance DuckDB** : Les requêtes sont optimisées pour l'exécution columnar (projection pushdown, partition pruning). Les jointures `ASOF` sont natives et très efficaces sur les séries temporelles.
- **Qualité des données** : Les données simulées contiennent des anomalies intentionnelles (wash trading, pics, slippage élevé) pour permettre la démonstration des algorithmes de détection.
- **Reproductibilité** : Le script de génération (`generate_sentinel_data.py`) garantit que les mêmes données sont produites à chaque exécution, assurant la reproductibilité des résultats.

---

*Documentation technique – Projet SentinelSQL – MIAGE Université Paris Dauphine*