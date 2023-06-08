import cv2
import os
import zipfile


class Video:
    path = ''
    frames = []

    def __init__(self, path, sizes=None, crop=None):
        self.sizes = sizes
        self.crop = crop
        self.path = path
        self.output_path = './storage/output'

        if sizes is None:
            self.sizes = [(1920, 1080), (1280, 720), (720, 480)]

        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        if not os.path.exists(path) or not path.endswith('.mp4'):
            raise Exception('Video path not Found Or Format Not Supported !')

        print(f"Video Path is : {path}")

    def extract_frames(self, frames_count):

        print(f"Extracting {frames_count} frames ...")

        video = cv2.VideoCapture(self.path)
        total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
        frame_interval = total_frames // frames_count

        for i in range(frames_count):
            frame_index = i * frame_interval
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            ret, frame = video.read()

            if self.crop:
                x, y, x1, y1 = self.crop
                frame = frame[y:y1, x:x1]

            if ret:
                self.frames.append(frame)

        video.release()
        return self

    def save_frames(self):
        for size in self.sizes:
            file_size_path = f"{self.output_path}/{str(size)}"

            if not os.path.exists(file_size_path):
                os.makedirs(file_size_path)

                for i, frame in enumerate(self.frames):
                    resized_frame = cv2.resize(frame, size)
                    filename = os.path.join(self.output_path, f"{size}/frame_{i}.jpg")
                    cv2.imwrite(filename, resized_frame)

            self.__save_zip(file_size_path, f"{file_size_path}.zip")

        print(f"saved on {self.output_path} !")

    def __save_zip(self, folder_path, zip_path):
        zip_file = zipfile.ZipFile(zip_path, 'w')
        files = os.listdir(folder_path)
        for file in files:
            file_path = os.path.join(folder_path, file)
            zip_file.write(file_path, os.path.basename(file_path))
        zip_file.close()
