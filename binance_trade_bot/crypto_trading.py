#!python3
import time

from .binance_api_manager import BinanceAPIManager
from .config import Config
from .database import Database
from .logger import Logger
from .scheduler import SafeScheduler
from .strategies import get_strategy
import math
import sys


def main():
    logger = Logger()
    logger.info("Starting")

    config = Config()
    db = Database(logger, config)
    manager = BinanceAPIManager(config, db, logger)
    # check if we can access API feature that require valid config
    try:
        _ = manager.get_account()
    except Exception as e:  # pylint: disable=broad-except
        logger.error("Couldn't access Binance API - API keys may be wrong or lack sufficient permissions")
        logger.error(e)
        return
    strategy = get_strategy(config.STRATEGY)
    if strategy is None:
        logger.error("Invalid strategy name")
        return
    trader = strategy(manager, db, logger, config)
    logger.info(f"Chosen strategy: {config.STRATEGY}")

    ## removed db creation temporarely for safety precautions
    ##logger.info("Creating database schema if it doesn't already exist")

    ##db.create_database()

    ##db.set_coins(config.SUPPORTED_COIN_LIST)
    ##db.migrate_old_state()

    ##trader.initialize()
    ##trader.update_values()
    # schedule.every(config.SCOUT_SLEEP_TIME).seconds.do(trader.scout).tag("scouting")
    #schedule.every(1).minutes.do(trader.update_values).tag("updating value history")
    #schedule.every(1).minutes.do(trader.update_values_eur).tag("updating value history")
    # schedule.every(1).minutes.do(db.prune_scout_history).tag("pruning scout history")
    # schedule.every(1).hours.do(db.prune_value_history).tag("pruning value history")
    logger.info(f"Trader Status: {config.TRADE}")
    logger.info(f"Crawler Status: {config.CRAWL}")
    if config.CRAWL == "1":
        trader.update_values()
    if config.TRADE == "1":
        trader.scout()
    starting = math.floor(time.time() / 60)
    while True:
        if math.floor(time.time() / 60) > starting:
            starting = math.floor(time.time() / 60)
            try:
                if config.CRAWL == "1":
                    trader.update_values()
                if config.TRADE == "1":
                    trader.scout()
            except:
                logger.info(f"An error occurred: {sys.exc_info()[0]}")

                with db.db_session() as session:
                    session.commit()
                    session.close()
                time.sleep(10)

        time.sleep(1)

