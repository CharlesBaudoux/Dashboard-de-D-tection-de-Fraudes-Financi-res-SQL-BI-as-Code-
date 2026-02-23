---
title: SentinelSQL | Détection de Fraude Analytique
description: Analytique SQL avancée pour détecter le wash trading, les pics de volume et les manipulations de marché.
---

<button onclick="const base = window.location.pathname.split('/projets/')[0]; window.top.location.href = window.location.origin + base + '/'; return false;" style="position: fixed; top: 20px; left: 20px; z-index: 9999; display: inline-flex; align-items: center; gap: 8px; padding: 10px 16px; background: rgba(37, 99, 235, 0.85); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 12px; color: white; cursor: pointer; font-family: ui-sans-serif, system-ui, sans-serif; font-size: 14px; font-weight: 600; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15); transition: all 0.2s ease;">
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0;">
    <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
    <polyline points="9 22 9 12 15 12 15 22"></polyline>
  </svg>
  <span>HOME</span>
</button>

# 🛡️ SentinelSQL – Analyse de Fraude Financière

*Projet de fin d'études : Maîtrise SQL avancée avec DuckDB et Evidence.dev – MIAGE Université Paris Dauphine*

---

## 📊 Tableau de Bord de Risque Global

```sql risk_summary
SELECT
    COUNT(*) AS total_trades,
    COUNT(DISTINCT user_id) AS unique_users,
    SUM(amount * price) AS total_volume,
    AVG(amount * price) AS avg_trade_size,
    SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) AS failed_trades
FROM sentinel.transactions
```

<div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 20px;">
    <Value data={risk_summary} column=total_trades title="Total Transactions"/>
    <Value data={risk_summary} column=unique_users title="Utilisateurs Distincts"/>
    <Value data={risk_summary} column=total_volume title="Volume Global (€)" fmt=eur/>
    <Value data={risk_summary} column=failed_trades title="Transactions Échouées"/>
</div>

**Explication métier** : Ces indicateurs clés (KPIs) offrent une vue d'ensemble de la santé du marché. Un volume disproportionné par rapport au nombre d'utilisateurs réels peut être le signe précurseur d'une activité de manipulation de liquidité.

---

## 🕵️ Détection de Wash Trading

**Problématique** : Le *wash trading* consiste à gonfler artificiellement les volumes via des transactions circulaires où l'acheteur et le vendeur sont la même entité.

```sql wash_events
WITH suspicious_pairs AS (
  SELECT
    a.user_id,
    a.asset_id,
    a.price,
    ABS(EXTRACT(EPOCH FROM (b.timestamp - a.timestamp))) AS sec_diff
  FROM sentinel.transactions a
  INNER JOIN sentinel.transactions b
    ON a.user_id = b.user_id
    AND a.asset_id = b.asset_id
    AND a.price = b.price
    -- Sécurité build Svelte : b > a évite l'interprétation de balise HTML
    AND b.trade_id > a.trade_id
  WHERE a.status = 'completed' AND b.status = 'completed'
)
SELECT
    user_id,
    asset_id,
    COUNT(*) AS wash_count,
    AVG(sec_diff) AS avg_time_gap
FROM suspicious_pairs
-- Sécurité build : 10 > sec_diff remplace sec_diff < 10
WHERE 10 > sec_diff
GROUP BY ALL
ORDER BY wash_count DESC
LIMIT 20
```

<DataTable data={wash_events} title="Détection des Boucles de Wash Trading (Self-Join)"/>

**Analyse technique** : Utilisation d'un **Self-Join** sur la table des transactions. Nous filtrons les paires d'opérations exécutées par le même `user_id` sur le même `asset_id` dans une fenêtre de temps critique (inférieure à 10 secondes).

---

## 📉 Volatilité Relative & Slippage

**Problématique** : Le slippage mesure l'écart entre le prix d'exécution et le prix du marché. Un slippage élevé (> 1%) est souvent un indicateur de manipulation de prix ou de front-running.



```sql slippage_summary
WITH trade_prices AS (
  SELECT
    t.asset_id,
    ABS(t.price - m.market_price) / NULLIF(m.market_price, 0) AS slippage_pct
  FROM sentinel.transactions t
  INNER JOIN sentinel.market_prices m
    ON t.asset_id = m.asset_id
    AND DATE_TRUNC('minute', t.timestamp) = m.timestamp
  WHERE t.status = 'completed'
)
SELECT
    asset_id,
    COUNT(*) AS trades,
    AVG(slippage_pct) AS avg_slippage_pct
FROM trade_prices
-- Sécurité build : 0.1 > slippage_pct (filtre les outliers > 10%)
WHERE 0.1 > slippage_pct
GROUP BY ALL
ORDER BY avg_slippage_pct DESC
```

<BarChart
  data={slippage_summary}
  x=asset_id
  y=avg_slippage_pct
  yFmt=pct
  title="Analyse du Slippage Moyen par Actif"
/>

**Expertise métier** : La jointure temporelle (Time-series Join) permet de valider la conformité du prix d'exécution par rapport aux oracles de marché externes à l'instant T.

---

## ⚡ Anomalies de Volume (Pics Statistiques)

**Problématique** : Identifier les "Pump and Dump" en isolant les volumes qui s'écartent statistiquement de la normale.

```sql spikes
WITH windowed_volume AS (
  SELECT
    DATE_TRUNC('minute', timestamp) AS window_start,
    SUM(amount) AS volume,
    AVG(SUM(amount)) OVER (ORDER BY DATE_TRUNC('minute', timestamp) RANGE BETWEEN INTERVAL '24 hours' PRECEDING AND CURRENT ROW) AS mean_24h,
    STDDEV(SUM(amount)) OVER (ORDER BY DATE_TRUNC('minute', timestamp) RANGE BETWEEN INTERVAL '24 hours' PRECEDING AND CURRENT ROW) AS std_24h
  FROM sentinel.transactions
  WHERE status = 'completed'
  GROUP BY 1
)
SELECT
    window_start,
    volume,
    volume / NULLIF(mean_24h, 0) AS volume_ratio
FROM windowed_volume
WHERE volume > (mean_24h + 3 * std_24h)
ORDER BY volume_ratio DESC
LIMIT 15
```

<DataTable data={spikes} title="Pics de Volume Détectés (> 3 Sigmas)"/>

**Approche statistique** : Ce tableau exploite les **Window Functions** pour calculer une moyenne et un écart-type mobiles. Une alerte est déclenchée dès que le volume d'une fenêtre dépasse le seuil de 3 écarts-types (3σ).

---

## 🏆 Score de Risque Utilisateur (Z-Score)

**Méthode** : Nous appliquons une normalisation statistique (Z-Score) pour segmenter les profils. 
> **Formule appliquée** : **Z = (x - Moyenne) / Écart-type**

```sql risk_scores
WITH user_metrics AS (
  SELECT
    user_id,
    COUNT(*) AS trade_count,
    SUM(amount * price) AS total_volume
  FROM sentinel.transactions
  WHERE status = 'completed'
  GROUP BY user_id
),
stats AS (
  SELECT
    *,
    (trade_count - AVG(trade_count) OVER()) / NULLIF(STDDEV(trade_count) OVER(), 0) AS z_score
  FROM user_metrics
)
SELECT
    user_id,
    trade_count,
    ROUND(total_volume) AS volume_total,
    CASE
      WHEN z_score > 2 THEN '🔴 CRITIQUE'
      WHEN z_score > 1 THEN '🟠 ÉLEVÉ'
      ELSE '🟢 NORMAL'
    END AS risk_level
FROM stats
ORDER BY trade_count DESC
LIMIT 25
```

<DataTable data={risk_scores} title="Segmentation des Profils de Risque (Z-Score)"/>

---

## 📈 Évolution du Volume Quotidien

```sql daily_volume
SELECT
  DATE(timestamp) AS day,
  SUM(amount * price) AS volume
FROM sentinel.transactions
WHERE status = 'completed'
GROUP BY 1
ORDER BY 1
```

<AreaChart
  data={daily_volume}
  x=day
  y=volume
  title="Volume de Trading Quotidien (€)"
/>

---

## 🎓 Conclusion du Projet

Ce dashboard démontre la capacité à transformer des données brutes en **renseignement financier exploitable** :
1.  **Maîtrise SQL** : Usage intensif de CTEs, Self-Joins et fonctions analytiques.
2.  **Sens métier MIAGE** : Application des statistiques à la surveillance réglementaire.
3.  **Performance** : Traitement de volumes importants via l'architecture DuckDB/Parquet.

---
*Charles Baudoux, Master MIAGE Université Paris Dauphine*
