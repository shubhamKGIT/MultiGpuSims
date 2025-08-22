
## About Workflow: CARLA’s built-in Multi-GPU mode (primary + secondary servers)


### Orchestrating Primary + Secondary servers
Use this when one simulation has many sensors and you want CARLA to distribute sensor rendering across GPUs automatically.
1. Start a primary server with no GPU: it runs physics and sync.
2. Start secondary servers, one per GPU, and point them at the primary; each selects a GPU via Unreal’s r.GraphicsAdapter.
3. Clients always connect to the primary. Point every client to the primary: host=… , port=2000. Don’t connect clients to secondaries; CARLA automatically spreads sensor rendering across them.

### * The following commands are placed inside docker *
Primary (no GPU):
'''
./CarlaUE4.sh -nullrhi -carla-primary-port=2002
'''
Secondary (GPU 0):
'''
./CarlaUE4.sh \
  -carla-rpc-port=3000 \
  -carla-primary-host=127.0.0.1 -carla-primary-port=2002 \
  -ini:[/Script/Engine.RendererSettings]:r.GraphicsAdapter=0
'''
Secondary (GPU 1):
'''
./CarlaUE4.sh \
  -carla-rpc-port=4000 \
  -carla-primary-host=127.0.0.1 -carla-primary-port=2002 \
  -ini:[/Script/Engine.RendererSettings]:r.GraphicsAdapter=1
'''

