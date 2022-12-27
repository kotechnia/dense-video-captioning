#!/bin/bash -i
curdir=`pwd`
export PYTHONPATH=$PYTHONPATH:$curdir/video_backbone/TSP
export PYTHONPATH=$PYTHONPATH:$curdir/video_backbone/TSP/data
export PYTHONPATH=$PYTHONPATH:$curdir/video_backbone/TSP/extract_features
export PYTHONPATH=$PYTHONPATH:$curdir/visualization

DATA_PATH=$1 # path of the raw video folder
OUTPUT_FOLDER=$2 # path of the output folder to save generated captions
GPU_ID=$3

if [ -z "$DATA_PATH" ]; then
    echo "DATA_PATH variable is not set."
    echo "Please set DATA_PATH to the folder containing the videos you want to process."
    exit 1
fi

if [ -z "$OUTPUT_FOLDER" ]; then
    echo "OUTPUT_FOLDER variable is not set."
      echo "Please set OUTPUT_FOLDER to the folder you want to save generate captions."
    exit 1
    exit 1
fi


####################################################################################
########################## PARAMETERS THAT NEED TO BE SET ##########################
####################################################################################


METADATA_CSV_FILENAME=$OUTPUT_FOLDER/"metadata.csv" # path/to/metadata/csv/file. Use the ones provided in the data folder.
RELEASED_CHECKPOINT=r2plus1d_34-tsp_on_activitynet


# Choose the stride between clips, e.g. 16 for non-overlapping clips and 1 for dense overlapping clips
STRIDE=16

# Optional: Split the videos into multiple shards for parallel feature extraction
# Increase the number of shards and run this script independently on separate GPU devices,
# each with a different SHARD_ID from 0 to NUM_SHARDS-1.
# Each shard will process (num_videos / NUM_SHARDS) videos.
SHARD_ID=0
NUM_SHARDS=1
DEVICE=cuda
WORKER_NUM=8

mkdir -p $OUTPUT_FOLDER

echo "START GENERATE METADATA"
python video_backbone/TSP/data/generate_metadata_csv.py --video-folder $DATA_PATH --output-csv $METADATA_CSV_FILENAME

FEATURE_DIR=$OUTPUT_FOLDER/${RELEASED_CHECKPOINT}_stride_${STRIDE}/
mkdir -p $OUTPUT_DIR

echo "START EXTRACT VIDEO FEATURES"
CUDA_VISIBLE_DEVICES=$GPU_ID python video_backbone/TSP/extract_features/extract_features.py \
--data-path $DATA_PATH \
--metadata-csv-filename $METADATA_CSV_FILENAME \
--released-checkpoint $RELEASED_CHECKPOINT \
--stride $STRIDE \
--shard-id $SHARD_ID \
--num-shards $NUM_SHARDS \
--device $DEVICE \
--output-dir $FEATURE_DIR \
--workers $WORKER_NUM \
