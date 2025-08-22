# MultiGpuSims


## Starting Multiple Containers
### docker-compose.yml launches 1 primary (CPU-only) + 8 secondaries (one per A100 GPU). 
### It uses clean porting, GPU pinning via NVIDIA_VISIBLE_DEVICES, and off-screen rendering.
### To orchestrate with docker-compose.yml, run: 
'''
docker compose up -d
'''
#### Check GPUs: 
'''
watch -n1 nvidia-smi
'''


## Which should you use?

## * singleSim *
### Need one coherent world with many interacting egos and lots of sensors?
#### **Use multi-GPU mode (A)**
#### Connect everybody to the primary. Let CARLA spread rendering across your 8 secondaries.

## * multiSim *
### Need maximum throughput with different scenarios in parallel (map/weather/seed isolation)?
#### Use 8 independent servers (B), one per GPU. Connect each client to its own port.