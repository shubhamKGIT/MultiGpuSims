
## How to connet

You want 8 totally separate scenarios/worlds/maps running at once (e.g., for throughput),
* launch 8 independent CARLA servers—each bound to one GPU and unique ports—then connect one client to each. *

## Start 8 servers (one per GPU)
'''
chmod +x spawn_multi_CarlaServers
./spawn_multi_CarlaServers.sh
'''

## Connect 8 client processes (Python multiprocessing)
'''
python3 connect_multi_Clients.py
'''
