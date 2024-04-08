# sudo apt install ffmpeg
# pip install moviepy

from moviepy.editor import VideoFileClip
import os
import uuid
import json
import sys

def extract_thumbnail(video_path, thumbnail_path):
    clip = VideoFileClip(video_path)
    thumbnail_time = clip.duration / 2  # middle of the video
    clip.save_frame(thumbnail_path, t=thumbnail_time)  # save frame at t seconds

def extract_thumbnails_from_videos(videos_folder, thumbnails_folder):
    video_files = os.listdir(videos_folder)

    for video_file in video_files:
        if video_file.endswith('.mp4'):
            video_path = os.path.join(videos_folder, video_file)
            thumbnail_path = os.path.join(thumbnails_folder, video_file.replace('.mp4', '') + '.jpg')
            extract_thumbnail(video_path, thumbnail_path)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--input":
        videos_folder = sys.argv[2]
    else:
        print("Usage: python preparedb.py --input <path_to_input_videos_folder>")
        sys.exit(1)

    output_folder = "../output/videos"
    os.makedirs(output_folder, exist_ok=True)
    thumbnails_folder = "../output/thumbnails"
    os.makedirs(thumbnails_folder, exist_ok=True)

    # delete everything in the output folder
    os.system(f'rm -rf {output_folder}/*')
    os.system(f'rm -rf {thumbnails_folder}/*')

    # list all files in the videos_folder
    video_files = os.listdir(videos_folder)
    video_files = [f for f in video_files if f.endswith('.mp4')] # keep only the mp4 files

    video_list = []
    for i, f in enumerate(video_files):
        new_id = str(uuid.uuid4())

        video_list.append({
            'id': new_id,
            'title': f.replace('.mp4', ''),
            'original_filename': f
        })

    # copy and rename the video files to the output folder
    for video in video_list:
        video_path = os.path.join(videos_folder, video['original_filename'])
        output_path = os.path.join(output_folder, video['id']+".mp4")
        os.system(f'cp "{video_path}" "{output_path}"')

    extract_thumbnails_from_videos(output_folder, thumbnails_folder)

    # write the database to output/database.json
    
    with open('../output/database.json', 'w') as f:
        json.dump(video_list, f, indent=2)