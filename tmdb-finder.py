import os
import re
import argparse

def is_single_char_directory(directory):
    return len(directory) == 1 and not directory.isalnum()

def find_directories_without_tmdb(starting_directory, series_mode=False, verbose=False):
    result_directories = []

    for root, dirs, files in os.walk(starting_directory):
        if series_mode:
            dirs = [d for d in dirs if 'season' not in d.lower() and 'specials' not in d.lower()]

        for directory in dirs:
            directory_path = os.path.join(root, directory)

            # Ignore single-character directories
            if is_single_char_directory(directory):
                continue

            # Check if the directory does not contain the regex '\{tmdb-(\d+)\}' or '\{tvdb-(\d+)\}'
            match_tmdb = re.search(r'\{tmdb-(\d+)\}', directory)
            match_tvdb = re.search(r'\{tvdb-(\d+)\}', directory)
            if not match_tmdb and not match_tvdb:
                result_directories.append(directory_path)

                if verbose:
                    print(directory_path)

    return result_directories

def save_to_file(directory_list, starting_directory):
    if directory_list:
        file_path = f'no_tmdb_id_{starting_directory.replace("/", "-")}.txt'
        with open(file_path, 'w') as result_file:
            result_file.write(f"Directories without tmdb-id or tvdb-id: {len(directory_list)}\n\n")
            for directory in directory_list:
                result_file.write(f'{directory}\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Directory Finder')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode')
    parser.add_argument('-d', '--directory', required=True, help='Specify the starting directory')
    parser.add_argument('-s', '--series', action='store_true', help='Ignore directories containing "Season" and "Specials"')

    args = parser.parse_args()

    starting_directory = args.directory
    result_directories = find_directories_without_tmdb(starting_directory, args.series, args.verbose)
    save_to_file(result_directories, starting_directory)

    if args.verbose:
        for directory in result_directories:
            print(directory)
