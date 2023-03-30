import os
import sys
import shutil
from datetime import datetime

# Step 1: From a list of tracks whose for each row, its first field, denotes the track of interest by means of a tag, extract such tag.
#           The list is gonna exists in the directory
track_list_dir = './tracks_lists'
done_track_list_dir = './tracks_lists_processed'

trks_source_dir = './tracks_source'
trks_dest_dir = './tracks_dest'

def main():
    # 1.1 Check if a files exist in track_list_dir...
    try:
        tracks_lists_files = [os.path.join(track_list_dir, fn) for fn in os.listdir(track_list_dir)]
    except FileNotFoundError:
        print(f'A directory with name {track_list_dir} should exist, where the tracks lists files reside', file=sys.stderr)
        exit(1)
    except:
        print(f'... something went wrong')
        exit(1)

    tracks_lists_files = [fn for fn in tracks_lists_files if os.path.isfile(fn)]

    if not tracks_lists_files:
        print(f'No files listing tracks present in {track_list_dir}\nNothing to do...')
        exit(0) # This is not an error condition, but the condition in which there's nothing to do
    else:
        tags = []
        for f in tracks_lists_files:
            tags.extend(get_track_tags(f))
    
    tags = list(set(tags))  # consider each tag only once -- deduplicate

    files_to_copy = find_files_with_tags(trks_source_dir, tags)

    for track_file in files_to_copy:
        shutil.copy(track_file, trks_dest_dir)
    
    timestamp = datetime.now().isoformat().replace(':', '.')
    
    for list_file in tracks_lists_files:
        shutil.copy(list_file, 
                    os.path.join(
                        done_track_list_dir, 
                        os.path.basename(list_file) + ' ' + timestamp
                    )
                   )
        os.remove(list_file)

def get_track_tags(file):
    tags = []

    with open(file, encoding='ibm437') as f:
        for line in f.readlines():
            if line.find(';') not in {0, -1}:
                tags.append(line[:line.find(';')].strip())

    return list(set(tags))  # return single instances

def find_files_with_tags(source_dir, tags):
    files = []

    for dirname, dirnames, filenames in os.walk(source_dir):
        for file in filenames:
            for tag in tags:
                if tag in file:
                    files.append(os.path.join(dirname, file))

    if len(files) < len(tags): 
        pass    # placeholder -- inform that some file has not been found

    return files
    
# The idiomatic way... and only to force full parsing of the file and avoiding NameError exception when doing forward-references to python calls
if __name__ == '__main__':
    main()