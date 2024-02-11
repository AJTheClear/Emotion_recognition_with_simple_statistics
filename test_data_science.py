"""
The tests for the functions inside data_science.py
"""
import unittest
import numpy as np
from data_science import save_data, get_current_mood, get_mood_for_time_window


emotion_set = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

class DataScienceTests(unittest.TestCase):
    """
    A class housing the tests for the functions inside data_science.py
    """
    def test_save_data(self):
        """
        tests the save_data function
        """
        date = "10 Feb 2024 13:54:14"
        num_faces = 3
        emotion_counts = {
            'angry': 2, 
            'disgust': 0, 
            'fear': 0, 
            'happy': 1, 
            'sad': 0, 
            'surprise': 0, 
            'neutral': 0
            }
        save_data(date, num_faces,emotion_counts)
        expected = "10 Feb 2024 13:54:14,3,2,0,0,1,0,0,0\n"

        with open('data_record.csv', 'r', encoding='UTF-8') as csvfile:
            last_line = csvfile.readlines()[-1]
            self.assertEqual(expected,last_line)

    def test_get_current_mood(self):
        """
        tests the get_current_mood function
        """
        mood = get_current_mood()
        with open('data_record.csv', 'r', encoding='UTF-8') as csvfile:
            last_line = csvfile.readlines()[-1]
            data = last_line.split(',')
            emotion_counts = [int(value.strip()) for value in data[2:]]
            max_value = max(emotion_counts)
            max_value_index = emotion_counts.index(max_value)
            expected = emotion_set[max_value_index]
            self.assertEqual(mood,expected)

    def test_get_mood_for_time_window(self):
        """
        tests the get_mood_for_time_window function
        """
        time_window = 10
        result = get_mood_for_time_window(time_window)

        with open('data_record.csv', 'r', encoding='UTF-8') as csvfile:
            lines = csvfile.readlines()
            last_lines = lines[-time_window:]

        sum_array = np.zeros(len(emotion_set))
        for line in last_lines:
            emotions = line.strip().split(',')[2:]
            emotion_counts = [int(emotion) for emotion in emotions]
            sum_array += np.array(emotion_counts)
        position_of_greatest_sum = np.argmax(sum_array)
        expected = emotion_set[position_of_greatest_sum]

        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
