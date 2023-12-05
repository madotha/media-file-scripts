import subprocess
import json
import sys
import os

def get_video_info(video_file):
    command = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=codec_name,width,height', '-show_entries', 'format=bit_rate', '-of', 'json', video_file]
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 0:
        info_json = json.loads(result.stdout)
        video_stream = info_json.get('streams', [])[0]
        format_info = info_json.get('format', {})

        if video_stream:
            codec_name = video_stream.get('codec_name', 'N/A')
            bitrate_bps = int(format_info.get('bit_rate', 0))
            bitrate_mbps = bitrate_bps / 1_000_000  # Convert to Mbps
            width = video_stream.get('width', 'N/A')
            height = video_stream.get('height', 'N/A')

            return codec_name, bitrate_mbps, width, height
        else:
            print(f"No video stream found in the file: {video_file}")
            return None
    else:
        print("Error running ffprobe:")
        print(result.stderr)
        return None

def beautify_output(file_path, codec, bitrate, width, height):
    print("\n" + "="*50)
    print(" " + os.path.basename(file_path))
    print("="*50 + "\n")

    print("Path to file:", os.path.dirname(file_path))
    print("File name:", os.path.basename(file_path))
    print("\nVideo Information:")
    print(f"  Codec: {codec}")
    print(f"  Bitrate: {bitrate:.2f} Mbps")
    print(f"  Resolution: {width}x{height}")

def process_directory(directory_path):
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if is_video_file(file_path):
                info = get_video_info(file_path)
                if info:
                    codec, bitrate, width, height = info
                    beautify_output(file_path, codec, bitrate, width, height)

def is_video_file(file_path):
    video_extensions = {'.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm'}
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower() in video_extensions

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <video_file_path_or_directory>")
        sys.exit(1)

    target_path = sys.argv[1]

    if os.path.isfile(target_path):
        # Single file case
        info = get_video_info(target_path)
        if info:
            codec, bitrate, width, height = info
            beautify_output(target_path, codec, bitrate, width, height)
    elif os.path.isdir(target_path):
        # Directory case
        process_directory(target_path)
    else:
        print(f"The specified path ({target_path}) is neither a file nor a directory.")
