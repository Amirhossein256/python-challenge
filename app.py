from video import Video

video = Video("./storage/input/video.mp4", sizes=[(1920, 1080), (1280, 720)])

video.extract_frames(24).save_frames()
