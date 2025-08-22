import multiprocessing as mp, carla, time

ENDPOINTS = [( "127.0.0.1", port ) for port in (20000,20100,20200,20300,20400,20500,20600,20700)]

def run_scenario(host, port, seed):
    client = carla.Client(host, port); client.set_timeout(30.0)
    world = client.get_world()
    settings = world.get_settings(); settings.synchronous_mode=True; settings.fixed_delta_seconds=0.05; world.apply_settings(settings)
    bp_lib = world.get_blueprint_library()
    spawns = world.get_map().get_spawn_points()

    # simple: one ego per server (add sensors as in example A)
    veh_bp = bp_lib.filter("vehicle.*model3*")[0]; veh_bp.set_attribute("role_name","hero")
    ego = world.try_spawn_actor(veh_bp, spawns[seed % len(spawns)])
    ego.set_autopilot(True)
    for _ in range(1200): world.tick()
    ego.destroy()
    s = world.get_settings(); s.synchronous_mode=False; world.apply_settings(s)

if __name__ == "__main__":
    with mp.Pool(len(ENDPOINTS)) as pool:
        pool.starmap(run_scenario, [(h,p,i) for i,(h,p) in enumerate(ENDPOINTS)])
