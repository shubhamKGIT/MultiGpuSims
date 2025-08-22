IMAGE=carlasim/carla:0.9.14
for i in $(seq 0 7); do
  BASE=$((20000 + i*100))                  # 20000,20100,...,20700
  docker run -d --name carla_$i \
    --gpus '"device='"$i"'"' \
    -e SDL_VIDEODRIVER=offscreen -e DISPLAY= \
    -p ${BASE}:${BASE} -p $((BASE+1)):$((BASE+1)) \
    $IMAGE \
    ./CarlaUE4.sh -RenderOffScreen -quality-level=Low \
    -carla-rpc-port=${BASE} -carla-streaming-port=$((BASE+1)) \
    -nosound -prefernvidia
done
