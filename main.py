"""
Face and Emotion Recogition App with Simple Statistics
"""
from cli import load_cli
from data_science import get_history, get_mood_for_time_window
from emotion import detect_emotions

if __name__ == "__main__":
    args = load_cli()

    if args.list:
        get_history()
    elif args.stats:
        mood = get_mood_for_time_window(args.stats)
        print(f"The mood for the last {args.stats} seconds is: {mood}")
    else:
        detect_emotions()
