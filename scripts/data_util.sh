# data_util.sh
#   dataset utility script for generating a checksum
#   for the puzzle files of the repository. taking a
#   single directory argument, checksums are written
#   and files are compressed again into .tar.gz.

DATA_DIRECTORY=./data

while [ $# -gt 0 ]; do
    case "$1" in --dir=*) DATA_DIRECTORY="${1#*=}" ;; *)
        echo "Error: unknown argument: $1 (requires --dir=<path_to_data>)"
        exit 1
    esac
    shift
done

md5sum $DATA_DIRECTORY/puzzles* > $DATA_DIRECTORY/.checksums
cat $DATA_DIRECTORY/.checksums
tar -czvf $DATA_DIRECTORY.tar.gz $DATA_DIRECTORY
tar -xvf $DATA_DIRECTORY.tar.gz
