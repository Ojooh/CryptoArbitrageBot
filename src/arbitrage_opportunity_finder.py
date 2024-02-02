import asyncio
import random
import json
import time  # For calculating time window based on market volatility
from exchange_api_manager import ExchangeAPIManager  # Assuming the ExchangeAPIManager is in a separate file

class ArbitrageOpportunityFinder:
    def __init__(self, num_exchanges, exchange_names_or_ids, use_random=False, base_currency='BTC', quote_currency='USDT'):
        if num_exchanges <= 0:
            raise ValueError("Number of exchanges should be greater than zero.")

        self.num_exchanges = num_exchanges
        self.exchange_names_or_ids = exchange_names_or_ids
        self.use_random = use_random
        self.base_currency = base_currency
        self.quote_currency = quote_currency
        self.exchange_manager = ExchangeAPIManager()

    async def _fetch_market_prices(self):
        tasks = []

        # Generate random exchange names or IDs if required
        selected_exchanges = (
            random.sample(self.exchange_manager.get_available_exchanges(), self.num_exchanges)
            if self.use_random else self.exchange_names_or_ids
        )

        # Fetch market prices concurrently
        for exchange in selected_exchanges:
            tasks.append(
                asyncio.create_task(
                    self.exchange_manager.fetch_current_price(exchange, self.base_currency, self.quote_currency)
                )
            )

        return await asyncio.gather(*tasks)
    
    def _calculate_profit_rate(self, min_price, max_price, buy_fee, sell_fee):
        if min_price == 0:
            return 0  # Avoid division by zero

        buy_price_with_fee = min_price * (1 + buy_fee / 100)
        sell_price_with_fee = max_price * (1 - sell_fee / 100)

        return ((sell_price_with_fee - buy_price_with_fee) / buy_price_with_fee) * 100

    def _calculate_time_window(self, market_volatility):
        # Placeholder for time window calculation based on market volatility
        # Implement your logic for calculating the time window here
        return 60 * 60  # Default time window of 1 hour (in seconds)
    
    async def find_arbitrage_opportunity(self, threshold=5, logger=None):
        while True:
            # Fetch market prices
            # prices = asyncio.run(self._fetch_market_prices())
            prices = await self._fetch_market_prices()

            # Calculate min, max, and profit rate
            minimum   = min(prices, key=lambda x: float(x['current_price']))
            maximum   = max(prices, key=lambda x: float(x['current_price']))
            
            min_price = float(minimum["current_price"])
            max_price = float(maximum["current_price"])
            
            min_exchange = minimum['exchange_name']
            max_exchange = maximum['exchange_name']
            
            buy_fee     = minimum["buy_order_fee"]
            sell_fee    = maximum["sell_order_fee"]
            profit_rate = self._calculate_profit_rate(min_price, max_price, buy_fee, sell_fee)

            # Log the results
            log_message = (
                f"Min Price: {min_price} (From: {min_exchange}), "
                f"Max Price: {max_price} (From: {max_exchange}), "
                f"Profit Rate: {profit_rate}%"
            )
            
            if profit_rate < threshold:
                log_message += " (Below Threshold)"
                if logger:
                    logger.log(log_message, status='info')
            else:
                log_message += " (Above Threshold)"
                if logger:
                    logger.log(log_message, status='success')
                    
                return {
                    "buy_from_exchange": min_exchange,
                    "sell_to_exchange": max_exchange,
                    "profit_rate": profit_rate,
                    "time_window": self._calculate_time_window(None)
                }

# Example usage:
# finder = ArbitrageOpportunityFinder(num_exchanges=3, exchange_names_or_ids=['binance', 'another_exchange'])
# result = asyncio.run(finder.find_arbitrage_opportunity('BTC/USDT'))
# print(result)
