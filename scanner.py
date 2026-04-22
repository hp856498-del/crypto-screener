def is_inside_bar(c1, c2):
    return c2['high'] < c1['high'] and c2['low'] > c1['low']

def bullish_harami(c1, c2):
    return c1['close'] < c1['open'] and c2['close'] > c2['open'] and \
           c2['open'] > c1['close'] and c2['close'] < c1['open']

def bearish_harami(c1, c2):
    return c1['close'] > c1['open'] and c2['close'] < c2['open'] and \
           c2['open'] < c1['close'] and c2['close'] > c1['open']

def bullish_engulfing(c1, c2):
    return c1['close'] < c1['open'] and c2['close'] > c2['open'] and \
           c2['open'] < c1['close'] and c2['close'] > c1['open']

def bearish_engulfing(c1, c2):
    return c1['close'] > c1['open'] and c2['close'] < c2['open'] and \
           c2['open'] > c1['close'] and c2['close'] < c1['open']


def detect_patterns(df, selected_patterns, backscan=False, backscan_range=10):
    results = []

    if not backscan:
        i = len(df) - 1

        c1 = df.iloc[i-2]
        c2 = df.iloc[i-1]

        check_and_add(results, c1, c2, selected_patterns)

    else:
        for i in range(len(df) - backscan_range, len(df) - 1):
            c1 = df.iloc[i-1]
            c2 = df.iloc[i]

            check_and_add(results, c1, c2, selected_patterns)

    return results


def check_and_add(results, c1, c2, selected_patterns):

    time = str(c2['timestamp'])

    if "Inside Bar" in selected_patterns and is_inside_bar(c1, c2):
        results.append({"pattern": "Inside Bar", "signal": "Neutral", "time": time})

    if "Bullish Harami" in selected_patterns and bullish_harami(c1, c2):
        results.append({"pattern": "Bullish Harami", "signal": "Bullish", "time": time})

    if "Bearish Harami" in selected_patterns and bearish_harami(c1, c2):
        results.append({"pattern": "Bearish Harami", "signal": "Bearish", "time": time})

    if "Bullish Engulfing" in selected_patterns and bullish_engulfing(c1, c2):
        results.append({"pattern": "Bullish Engulfing", "signal": "Bullish", "time": time})

    if "Bearish Engulfing" in selected_patterns and bearish_engulfing(c1, c2):
        results.append({"pattern": "Bearish Engulfing", "signal": "Bearish", "time": time})