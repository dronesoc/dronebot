frequency_table = {'Raceband': [5658, 5695, 5732, 5769, 5806, 5843, 5880, 5917],
                   'Fatshark': [5740, 5760, 5780, 5800, 5820, 5840, 5860, 5880],
                   'B':        [5733, 5752, 5771, 5790, 5809, 5828, 5847, 5866],
                   'A':        [5865, 5845, 5825, 5805, 5785, 5765, 5745, 5725],
                   'E':        [5705, 5685, 5665, 5645, 5885, 5905, 5925, 5945]}

def get_frequency(band, channel):
    if band.lower() in ['r', 'raceband']:
        band = 'Raceband'
    elif band.lower() in ['irc', 'fs', 'fatshark', 'immersionrc']:
        band = 'Fatshark'
    elif band.lower() in ['a', 'tbs']:
        band = 'A'
    elif band.lower() in ['b']:
        band = 'B'
    elif band.lower() in ['e', 'dji']:
        band = 'E'
    else:
        return None

    channel_index = int(channel) - 1
    if 0 <= channel_index < len(frequency_table[band]):
        return (band, frequency_table[band][channel_index])
    else:
        return None

def format_info(band, channel, frequency):
    text = """
> Band: `{}`
> Channel: `{}`
> Frequency: `{} MHz`""".format(band, channel, frequency)
    return text

