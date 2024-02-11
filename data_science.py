"""
The data science logic for the app.
"""
import csv
import pandas as pd

emotion_set = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

def save_data(date: str, num_faces: int, emotion_counts: dict[str, int]):
    """
    Saves the date, number of faces and recognised emotions into a csv file.

    :param date: the current date in %d %b %Y %H:%M:%S format.
    :param num_faces: the number of faces.
    :param emotion_counts: a dictionary used to count 
    how many instances of each emotion have been recognissed.
    """
    fieldnames = ['Date', 'Num_Faces'] + list(emotion_counts.keys())
    data = [date, num_faces] + list(emotion_counts.values())

    with open('data_record.csv', 'a', newline='', encoding='UTF-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow(dict(zip(fieldnames, data)))

def get_current_mood():
    """
    Gets the most common emotion for the last row logged.

    :return: the most common emotion.
    """
    df = pd.read_csv('data_record.csv')
    latest_record = df.iloc[-1]
    emotion_counts = latest_record[emotion_set]
    emotion_counts_numeric = pd.to_numeric(emotion_counts)
    most_common_emotion = emotion_counts_numeric.idxmax()
    return most_common_emotion

def get_mood_for_time_window(time_window: int):
    """
    Gets the most common emotion for a period of time in seconds

    :param time_window: an integer specifying how many seconds back to look for.
    :return: the most common emotion.
    """
    df = pd.read_csv('data_record.csv')
    latest_records = df.tail(time_window)
    emotion_counts = latest_records[emotion_set]
    most_common_emotion = emotion_counts.sum().idxmax()
    return most_common_emotion


def get_history():
    """
    Loads the history into the terminal.
    """
    df = pd.read_csv('data_record.csv')
    print(df)
