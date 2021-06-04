import random
import sys
from datetime import datetime

from binance_trade_bot.auto_trader import AutoTrader


class Strategy(AutoTrader):
    def initialize(self):
        super().initialize()
        self.initialize_current_coin()

    def scout(self):
        """
        Scout for potential jumps from the current coin to another coin
        """
        #all_tickers = self.manager.get_all_market_tickers()
        self.logger.info("scouting")
        action_recommendation = self.db.get_current_action()
        self.logger.info(f"Datetime: {action_recommendation.datetime} Action: {action_recommendation.trade_action}")
        # Display on the console, the current coin+Bridge, so users can see *some* activity and not think the bot has
        # stopped. Not logging though to reduce log size.

       # current_coin_price = all_tickers.get_price(current_coin + self.config.BRIDGE)

        #if current_coin_price is None:
        #    self.logger.info("Skipping scouting... current coin {} not found".format(current_coin + self.config.BRIDGE))
        #    return

        #self._jump_to_best_coin(current_coin, current_coin_price, all_tickers)