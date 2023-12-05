import os
import argparse
from pymediainfo import MediaInfo

def analyze_video_files(directory_path=None, verbose=False):
    if directory_path is None:
        directory_path = os.getcwd()

    ignored_extensions = {'.srt', '.nfo', '.idx', '.sub', '.sfv', '.URL', '.url', '.ass', '.txt'}
    not_hevc_output_file = None
    errors_output_file = None

    # Create subfolders
    not_hevc_folder = os.path.join(os.getcwd(), 'not_hevc')
    errors_folder = os.path.join(os.getcwd(), 'errors')

    if not os.path.exists(not_hevc_folder):
        os.makedirs(not_hevc_folder)

    if not os.path.exists(errors_folder):
        os.makedirs(errors_folder)

    if verbose:
        not_hevc_output_file_path = os.path.join(not_hevc_folder, f'not_hevc_{directory_path.replace("/", "-")}.txt')
        errors_output_file_path = os.path.join(errors_folder, f'errors_{directory_path.replace("/", "-")}.txt')

        not_hevc_output_file = open(not_hevc_output_file_path, 'w')
        errors_output_file = open(errors_output_file_path, 'w')

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in ignored_extensions):
                # Skip files with ignored extensions
                continue
            
            file_path = os.path.join(root, file)

            try:
                media_info = MediaInfo.parse(file_path)
                video_track = next(track for track in media_info.tracks if track.track_type == 'Video')
                codec_name = video_track.format.lower()

                # Color coding based on codec
                if 'x265' in codec_name or 'h265' in codec_name or 'hevc' in codec_name:
                    if verbose:
                        print(f'\033[92m{file_path}: {codec_name}\033[0m')  # Green
                else:
                    if verbose:
                        print(f'\033[91m{file_path}: {codec_name}\033[0m')  # Red
                        not_hevc_output_file.write(f'{file_path}: {codec_name}\n')

            except Exception as e:
                if verbose:
                    print(f'Error analyzing {file_path}: {str(e)}')
                    errors_output_file.write(f'{file_path}: {str(e)}\n')

    if not_hevc_output_file:
        not_hevc_output_file.close()

    if errors_output_file:
        errors_output_file.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Video File Analyzer')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode')
    parser.add_argument('-d', '--directory', help='Specify the starting directory')

    args = parser.parse_args()

    directory_path = args.directory or os.getcwd()
    analyze_video_files(directory_path, args.verbose)
