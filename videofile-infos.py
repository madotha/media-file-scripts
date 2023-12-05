import subprocess
import json
import sys

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
            print("No video stream found in the file.")
            return None
    else:
        print("Error running ffprobe:")
        print(result.stderr)
        return None

def beautify_output(codec, bitrate, width, height):
    print("Video Information:")
    print(f"  Codec: {codec}")
    print(f"  Bitrate: {bitrate:.2f} Mbps")
    print(f"  Resolution: {width}x{height}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <video_file_path>")
        sys.exit(1)

    video_file_path = sys.argv[1]
    info = get_video_info(video_file_path)

    if info:
        codec, bitrate, width, height = info
        beautify_output(codec, bitrate, width, height)
