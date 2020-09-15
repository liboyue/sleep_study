#!/bin/bash
WORLD_SIZE=4

ENVS="OMP_NUM_THREADS=10 \
MASTER_ADDR=127.0.0.1 \
MASTER_PORT=23456 \
RANK=\${RANK} \
WORLD_SIZE=\${WORLD_SIZE} \
LOCAL_RANK=\${RANK} \
WORLD_LOCAL_SIZE=\${WORLD_SIZE} \
WORLD_NODE_RANK=0"

PARAMS="--epochs=10 \
--lr=0.01 \
--momentum=0.9 \
--num_workers=5"

for (( RANK=$WORLD_SIZE-1; RANK>=0; RANK-- )) do
    if [[ "${RANK}" -eq 0 ]]; then
        eval "${ENVS} python rnn.py ${PARAMS} ${@}"
    else
        eval "${ENVS} python rnn.py ${PARAMS} ${@}" &
    fi
done
