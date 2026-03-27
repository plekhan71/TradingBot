# filters/market_filter.py

class MarketFilter:
    def __init__(
        self,
        atr_period=14,
        range_bars=20,
        atr_multiplier=0.6,
        min_range_pips=6
    ):
        self.atr_period = atr_period
        self.range_bars = range_bars
        self.atr_multiplier = atr_multiplier
        self.min_range_pips = min_range_pips

    def is_flat(self, candles_m5):
        """
        candles_m5: list of dicts with keys:
        ['high', 'low', 'close']
        """
        if len(candles_m5) < max(self.atr_period * 2, self.range_bars):
            return True  # недостаточно данных → не торгуем

        atr = self._calculate_atr(candles_m5)
        avg_atr = sum(atr[:-1]) / len(atr[:-1])
        current_atr = atr[-1]

        atr_flat = current_atr < avg_atr * self.atr_multiplier

        recent = candles_m5[-self.range_bars:]
        high = max(c['high'] for c in recent)
        low = min(c['low'] for c in recent)
        range_pips = (high - low) * 10_000

        range_flat = range_pips < self.min_range_pips

        return atr_flat or range_flat

    def _calculate_atr(self, candles):
        atr = []
        for i in range(1, len(candles)):
            high = candles[i]['high']
            low = candles[i]['low']
            prev_close = candles[i - 1]['close']

            tr = max(
                high - low,
                abs(high - prev_close),
                abs(low - prev_close)
            )
            atr.append(tr)

        return atr[-self.atr_period:]
