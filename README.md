# MultiGpuSims
Scripts and workflows to orchestrate containerized carla simulations in 2 modes
* A. Single simulation sharing resources on multiple GPUs
* B. Multiple server each running on a GPU, unaffected by the other

### If you just want multiple controllable vehicles (for training, RL, AV testing, etc.):
* Run one CARLA server on one GPU.
* Spawn many heroes with unique role names.

### If you want high-fidelity sensor rendering for many heroes:
* Use multi-GPU CARLA mode.
* Each GPU can handle rendering tasks for one or more heroes’ sensors, preventing one GPU from bottlenecking.

## -------------------------------------- ##
## A: Single simulation multi-GPU (also called CARLA multi-GPU rendering option), 1 Primary & 8 Secondary servers

About: multi-GPU server mode where you launch one primary server and multiple secondary servers, each secondary tied to a GPU and rendering sensors for actors in the shared world. Clients only connect to the primary.

**To explain again in detail:**

* CARLA supports multi-GPU rendering mode (primary server + secondary servers).
* In this mode, one GPU handles physics + world, and additional GPUs handle sensor rendering in parallel.
* This means: multiple hero vehicles, each with heavy sensor suites (camera, LiDAR, semantic segmentation, etc.), can spread their rendering load across GPUs.
* You don’t need separate servers per hero vehicle — you run one world, multiple heroes, and CARLA distributes the sensor render tasks.

### Workflow 
Of Carla Multi-GPU Rendering Mode (Simgle Sim, Multi Ego or Large Sensor Load)

#### docker compose 
docker-compose.yml launches 1 primary (CPU-only) + 8 secondaries (one per A100 GPU). 
It uses clean porting, GPU pinning via NVIDIA_VISIBLE_DEVICES, and off-screen rendering.\

--To orchestrate with docker-compose.yml, run:--
'''
docker compose up -d
'''

--Check GPUs:--
'''
watch -n1 nvidia-smi
'''


#### Run client script for One simulation with multiple egos + full sensor suites.
'''
python3 ./singleSim/singleSim_multiEgo.py
'''

### Purpose of Mode A: run CARLA in multi-GPU mode but as simgle simulation.
One world only (all ego vehicles, traffic, pedestrians share the same physics world).

**Layout:**
1 primary server (-nullrhi, CPU only) → runs physics, synchronizes ticks.
8 secondary servers → each pinned to a GPU, doing sensor rendering.
Clients connect only to the primary (port 2000 in my compose).
All your 6 RGB + LiDAR + radar sensors across many ego vehicles are distributed over GPUs by CARLA itself.

**Good for:**
One coherent city/world.
Multi-ego with heavy sensor loads.
Scaling rendering load across GPUs.


## ---------------------------------------------- ##
## B: Multiple Simulation, spawning multiple servers

### About workflow (multiple simulation) - process pinned to a GPU device
You want 8 totally separate scenarios/worlds/maps running at once (e.g., for throughput),
launch 8 independent CARLA servers—each bound to one GPU and unique ports—then connect one client to each.

### Two options for spawning containers
#### 1: Start 8 servers (one per GPU) using CLI
'''
chmod +x spawn_multi_CarlaServers
./spawn_multi_CarlaServers.sh
'''

#### 2: Start 8 servers using docker-compose in multiSim folder
'''
docker compose up -d
watch -n1 nvidia-smi
'''

### Post spawns
#### Connect to 8 client processes (Python multiprocessing)
'''
python3 connect_multi_Clients.py
'''


## -------------------------------- ##
## Which folder should you use?

**singleSim**
Need one coherent world with many interacting egos and lots of sensors?
* Use of multi-GPU mode
Connect everybody to the primary. Let CARLA spread rendering across your 8 secondaries.

**multiSim**
Need maximum throughput with different scenarios in parallel (map/weather/seed isolation)?
Use 8 independent servers (B), one per GPU. Connect each client to its own port.


## -------------------------------------------------------- ##
## Headless rendering gotchas on A100
1. Prefer Docker + off-screen mode; that’s CARLA’s recommended headless path.
2. Do not enable MIG (again): no OpenGL/Vulkan under MIG on A100.
3. If you ever see multiple CARLA instances “all using GPU 0”, it’s typically because the process can see every GPU. Pin with Docker --gpus "device=N" or Compose device_ids.