#!/usr/bin/env python3
"""
SentinelSQL Data Generator
Generates synthetic financial transactions with embedded fraud patterns.
MIAGE Data Engineering - Charles Baudoux
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_market_prices(days=30, seed=42):
    """Generate minute-level market prices for each asset using Random Walk."""
    np.random.seed(seed)
    assets = {
        'BTC': 65000.0,
        'ETH': 3500.0,
        'SOL': 150.0,
        'ADA': 0.50,
        'DOT': 8.0,
        'AVAX': 40.0
    }
    
    start = datetime(2025, 1, 1)
    n_minutes = days * 24 * 60
    timestamps = pd.date_range(start, periods=n_minutes, freq='1min')
    
    records = []
    for asset, initial_price in assets.items():
        # Volatilité réaliste (faible pour BTC, plus haute pour les altcoins)
        volatility = 0.001 if asset in ['BTC', 'ETH'] else 0.003
        
        # Mouvement Brownien Géométrique
        returns = np.random.normal(0, volatility, n_minutes)
        price_path = initial_price * np.exp(np.cumsum(returns))
        
        df_asset = pd.DataFrame({
            'timestamp': timestamps,
            'asset_id': asset,
            'market_price': np.round(price_path, 2)
        })
        records.append(df_asset)
        
    return pd.concat(records, ignore_index=True)

def generate_transactions(market_df, n=150000, seed=42):
    """Generate transaction data based on actual market prices to control slippage."""
    np.random.seed(seed)
    
    # Base transaction data
    user_ids = np.random.randint(1000, 2000, size=n)
    
    # Pick random rows from market data to act as the exact moment of the trade
    market_sample = market_df.sample(n=n, replace=True).reset_index(drop=True)
    
    # Base amounts (Lognormal distribution for realistic trade sizes)
    amounts = np.random.lognormal(mean=0, sigma=1.5, size=n)
    # Scale amounts inversely to price (people buy less BTC than ADA)
    market_sample['amount'] = (amounts * (1000 / market_sample['market_price'])).round(4)
    # Ensure minimum amount
    market_sample['amount'] = np.maximum(market_sample['amount'], 0.0001)

    # ---------------------------------------------------------
    # INJECT REALISTIC SLIPPAGE
    # ---------------------------------------------------------
    # 1. Normal slippage for 95% of trades (between 0.01% and 0.5%)
    normal_slippage = np.random.normal(0.001, 0.002, size=n)
    
    # 2. High/Suspicious slippage for 5% of trades (between 1% and 8%)
    high_slippage_mask = np.random.random(n) < 0.05
    suspicious_slippage = np.random.uniform(0.01, 0.08, size=n)
    
    # Apply slippage (combination of normal and high)
    final_slippage = np.where(high_slippage_mask, suspicious_slippage, normal_slippage)
    
    # Calculate execution price (market_price * (1 + slippage))
    # We use absolute value for slippage calculation in SQL, so direction doesn't matter much here
    direction = np.random.choice([1, -1], size=n) 
    market_sample['price'] = (market_sample['market_price'] * (1 + (final_slippage * direction))).round(2)
    
    # Status
    statuses = np.random.choice(['completed', 'pending', 'failed'], size=n, p=[0.95, 0.03, 0.02])
    
    # Build final DataFrame
    df = pd.DataFrame({
        'trade_id': range(1, n+1),
        'user_id': user_ids,
        'asset_id': market_sample['asset_id'],
        'amount': market_sample['amount'],
        'price': market_sample['price'],
        'timestamp': market_sample['timestamp'] + pd.to_timedelta(np.random.randint(0, 59, size=n), unit='s'), # Add random seconds
        'status': statuses
    })
    
    # Sort by timestamp
    df = df.sort_values('timestamp').reset_index(drop=True)
    df['trade_id'] = range(1, len(df)+1)
    
    # Inject patterns
    df = inject_wash_trading(df, n_wash=300)
    df = inject_volume_spikes(df, n_spikes=60)
    
    return df

def inject_wash_trading(df, n_wash=300):
    """Inject wash trading: same user buys and sells same asset within <10 seconds at same price."""
    # Find completed trades to act as the first leg of the wash trade
    completed_idx = df[df['status'] == 'completed'].index
    wash_sources = np.random.choice(completed_idx, size=n_wash, replace=False)
    
    new_rows = []
    for idx in wash_sources:
        source_trade = df.loc[idx].copy()
        
        # Create the wash leg
        wash_trade = source_trade.copy()
        wash_trade['trade_id'] = df['trade_id'].max() + len(new_rows) + 1
        # Add 1 to 9 seconds
        wash_trade['timestamp'] = source_trade['timestamp'] + timedelta(seconds=np.random.randint(1, 10))
        
        new_rows.append(wash_trade)
        
    if new_rows:
        df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
        df = df.sort_values('timestamp').reset_index(drop=True)
        df['trade_id'] = range(1, len(df)+1)
        
    return df

def inject_volume_spikes(df, n_spikes=60):
    """Inject volume spikes (anomalous amounts)."""
    completed_idx = df[df['status'] == 'completed'].index
    spike_idx = np.random.choice(completed_idx, size=n_spikes, replace=False)
    
    # Multiply amount by a massive factor (50x to 200x)
    df.loc[spike_idx, 'amount'] *= np.random.uniform(50.0, 200.0)
    
    return df


def main():
    print("🚀 Starting SentinelSQL Data Generation...")
    
    os.makedirs('sources/sentinel', exist_ok=True)
    
    # 1. Generate market first
    print("📊 Generating Market Prices...")
    market_df = generate_market_prices(days=30)
    market_df.to_parquet('sources/sentinel/market_prices.parquet', index=False)
    print(f"✅ Market Prices saved: {len(market_df)} rows")
    
    # 2. Generate transactions based on market
    print("💱 Generating Transactions with realistic slippage...")
    transactions_df = generate_transactions(market_df, n=150000)
    transactions_df.to_parquet('sources/sentinel/transactions.parquet', index=False)
    print(f"✅ Transactions saved: {len(transactions_df)} rows")
    
    print("\n🎉 Data generation complete!")
    print(f"- Normal slippage: ~0.1%")
    print(f"- Suspicious slippage embedded: ~1% to 8%")
    
if __name__ == '__main__':
    main()
