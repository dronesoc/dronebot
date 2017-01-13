frequency_table = {'Raceband': [5658, 5695, 5732, 5769, 5806, 5843, 5880, 5917]}

def get_frequency(band, channel):
    if band.lower() in ['r', 'raceband']:
        band = 'Raceband'
    else:
        return None

    channel_index = int(channel) - 1
    if 0 < channel_index < len(frequency_table[band]):
        return (band, frequency_table[band][channel_index])
    else:
        return None
