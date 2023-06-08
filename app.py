from video import Video

path = input("input video path : ")
try:

    video = Video(path=path, sizes=[(1920, 1080), (1280, 720)])
    video.extract_frames(24).save_frames()

except Exception as e:
    red_color = '\033[91m'
    print(f"{red_color}The error is: ", e)