# --- Do not remove these libs ---
from freqtrade.strategy import IStrategy
from freqtrade.strategy import CategoricalParameter, IntParameter
from functools import reduce
from pandas import DataFrame
# --------------------------------

import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
import numpy # noqa

class wbtc(IStrategy):
    """
    Strategy WBTC Arbitrage by abydon
    author@: Iggy Pi
    github@: https://github.com/ipctec/freqtrade-strategies
    How to use it with docker ?
    > docker-compose run --rm freqtrade backtesting --strategy wbtc --timerange 20210901-
    """
    INTERFACE_VERSION = 2

    # Timeframe
    timeframe = '3m'

    # Minimal ROI 
    # time | percentage
    minimal_roi = {
        "03": 0.0,
        "15": 0.07,
        "9": 0.05,
        "3": 0.06,
        "2": 0.08,
    }

    # stoploss
    trailing_stop = False
    stoploss = -0.99

    # run "populate_indicators" only for new candle
    process_only_new_candles = True

    # Experimental settings (configuration will overide these if set)
    use_sell_signal = True
    sell_profit_only = True
    ignore_roi_if_buy_signal = False

    # Optional order type mapping
    order_types = {
        'buy': 'limit',
        'sell': 'limit',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }
    close = IntParameter(low=1.0001, high=1.15, default=1.002, space='buy', optimize=True)
    close = IntParameter(low=50, high=300, default=70, space='sell', optimize=True)


    # Buy hyperspace params:
    buy_params = {
        "open": 1,
    }

    # Sell hyperspace params:
    sell_params = {
        "close": 1,
    }

    def informative_pairs(self):
        """
        Define additional, informative pair/interval combinations to be cached from the exchange.
        These pair/interval combinations are non-tradeable, unless they are part
        of the whitelist as well.
        For more information, please consult the documentation
        :return: List of tuples in the format (pair, interval)
            Sample: return [("ETH/USDT", "5m"),
                            ("BTC/USDT", "15m"),
                            ]
        """
        return [
            ("BTC/USDT", "3m"),
            ("BTC/USDT", "1h"),
            ]

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Adds several different TA indicators to the given DataFrame
        Performance Note: For the best performance be frugal on the number of indicators
        you are using. Let uncomment only the indicator you are using in your strategies
        or your hyperopt configuration, otherwise you will waste your memory and CPU usage.
        """

        # MACD
        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']

        # RSI
        dataframe['rsi'] = ta.RSI(dataframe)

        # Overlap Studies
        # ------------------------------------

        # SAR Parabol
        dataframe['sar'] = ta.SAR(dataframe)

        # SMA - Simple Moving Average
        dataframe['sma'] = ta.SMA(dataframe, timeperiod=40)

        return dataframe

        # WBTC/BTC buy/sell
        # ------------------------------------

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            # Prod
            (
                dataframe['open'] < 1.00250000
            ),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            # Prod
            (
                dataframe['close'] > 1.00250000
            ),
            'sell'] = 1
        return dataframe
