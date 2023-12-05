import os
import argparse

def search_and_output(directory, verbose):
    results = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if 'funxd.mkv' in file:
                file_path = os.path.join(root, file)
                results.append(file_path)
                if verbose:
                    print(file_path)
                
    return results

def main():
    parser = argparse.ArgumentParser(description='Search for files containing "funxd.mkv" and output the results.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode')
    parser.add_argument('-d', '--directory', default='.', help='Specify the directory to search (default is the current directory)')

    args = parser.parse_args()

    directory = args.directory
    verbose = args.verbose

    if verbose:
        print(f"Searching for 'funxd.mkv' files in directory: {directory}")

    results = search_and_output(directory, verbose)

    if results:
        output_filename = f"funxd_files_{directory.replace('/', '-')}.txt"
        
        with open(output_filename, 'w') as output_file:
            output_file.write(f"Search results for 'funxd.mkv' in directory: {directory}\n")
            output_file.write(f"Number of files found: {len(results)}\n\n")
            
            for result in results:
                output_file.write(result + '\n')
        
        print(f"\nResults written to: {output_filename}")
    else:
        print("No matching files found.")

if __name__ == "__main__":
    main()
