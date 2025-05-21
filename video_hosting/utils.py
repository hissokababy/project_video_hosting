import subprocess
import os
import shutil

from typing import IO

from django.core.files.storage import default_storage

S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")
storage = default_storage

class VideoProcess:
    def __init__(self):
        pass

    def create_hls(self, input_file: IO, resolutions: list, file_name: str) -> str:
        input_file = f'{S3_ENDPOINT_URL}/videos/{input_file}'

        cmd = []

        initial = [        
            "ffmpeg",
            "-i", input_file,
            "-c:v", "libx264",
            "-c:a", "aac",]

        cmd.extend(initial)

        var_stream_names = ["-var_stream_map"]
        var_names = []
        for index, resolution in enumerate(resolutions):
            variant = [        
            "-map",
            "0:v:0",
            "-map",
            "0:a:0",
            f"-filter:v:{index}", f"scale=w=-2:h={resolution}",
            f"-crf:{index}", "23",]
            cmd.extend(variant)
            var_names.append(f'v:{index},a:{index},name:{resolution}')

        map_names = [' '.join(var_names)]
        var_stream_names.extend(map_names)

        cmd.extend(var_stream_names)

        common = [
            "-preset", "veryfast",
            "-f", "hls",
            "-hls_playlist_type", "vod",
            "-hls_time", "10",
            "-hls_flags", "independent_segments",
            "-hls_segment_type", "mpegts",
            
            "-master_pl_name", f"{file_name}_m.m3u8",
            "-hls_segment_filename", f"./{file_name}/%v/{file_name}_%04d.ts",
            
            f"./{file_name}/%v/{file_name}.m3u8",
            ]

        cmd.extend(common)

        print(cmd)
        subprocess.run(cmd)

        files = self.recursive_func(file_name)

        ##### загрузка файлов в s3 #####    
        for file in files:
            storage.bucket.upload_file(file, file)

        ##### удаление локальной папки #####
        shutil.rmtree(file_name)

        return files[-1]
        

    def recursive_func(self, dir: str) -> list:
        lst = []

        for file in os.listdir(dir):
            if os.path.isdir(f'{dir}/{file}'):
                r = self.recursive_func(f'{dir}/{file}')
                lst.extend(r)
            
            if os.path.isfile(f'{dir}/{file}'):
                lst.append(f'{dir}/{file}')

        return lst

    