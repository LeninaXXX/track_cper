import os
import sys
import shutil
from datetime import datetime

# Step 1: From a list of tracks whose for each row, its first field, denotes the track of interest by means of a tag, extract such tag.
#           The list is gonna exists in the directory
track_list_dir = './tracks_lists'
done_track_list_dir = './tracks_lists_processed'

trks_source_dirs = ['./tracks_source']  # Admits multiple source directories
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
        print(f'No files listing tracks present in {track_list_dir}')
        print(f'Nothing to do...')
        exit(0) # This is not an error condition, but the condition in which there's nothing to do
    else:
        for tracks_list_file in tracks_lists_files:
            timestamp = datetime.now().isoformat().replace(':', '.')
            tags = get_track_tags(tracks_list_file)
            
            files_to_copy, not_found_tags = find_files_with_tags(trks_source_dirs, tags)

            for nftag in not_found_tags:    # deal with not found tags
                print(
                    f'In tracklist file {tracks_list_file}, track tag {nftag} not found',
                    file=sys.stderr
                )
            
            if files_to_copy:
                newdir_name = os.path.join(
                    trks_dest_dir,
                    os.path.basename(tracks_list_file) + ' - ' + timestamp
                )
                os.makedirs(newdir_name, exist_ok=True)

                for f in files_to_copy:    # deal with found tags/found files
                    shutil.copy(f, newdir_name)
                
                shutil.copy(tracks_list_file,
                            os.path.join(
                                done_track_list_dir,
                                os.path.basename(tracks_list_file) + ' ' + timestamp
                            )
                        )
                os.remove(tracks_list_file)
            else:
                print(
                    f'From tracklist file {tracks_list_file}, no file was found!!!\n'
                    f'No directory was created',
                    file=sys.stderr
                )
            
def get_track_tags(file):
    tags = []

    with open(file, encoding='ibm437') as f:
        for line in f.readlines():
            if line.find(';') not in {0, -1}:
                tags.append(line[:line.find(';')].strip())

    return list(set(tags))  # return single instances

def find_files_with_tags(source_dirs, tags):
    found_files = []
    not_found_tags = tags.copy()

    for source_dir in source_dirs:
        for dirname, dirnames, filenames in os.walk(source_dir):
            for file in filenames:
                for tag in tags:
                    if tag in file:
                        found_files.append(os.path.join(dirname, file))
                        if tag in not_found_tags:
                            not_found_tags.remove(tag)

    return (found_files, not_found_tags)
    
# The idiomatic way... and only to force full parsing of the file and avoiding NameError exception when doing forward-references to python calls
if __name__ == '__main__':
    # sets up a flag
    with open('./running.bat', 'w') as f:
        f.write("tskill " + str(os.getpid()))
    main()
    os.remove('./running.bat')  # remove flag -- successful run