
"""
Single Simulation, Multiple Ego Vechile, 
Full Sensor Suite on Each Ego Vechicle """
import carla, random, time
from contextlib import contextmanager

HOST, PORT = "127.0.0.1", 2000  # primary from the compose file

@contextmanager
def carla_client(host, port, timeout=30.0):
    client = carla.Client(host, port)
    client.set_timeout(timeout)
    yield client

def setup_world(world, fixed_dt=0.05):
    settings = world.get_settings()
    settings.synchronous_mode = True
    settings.fixed_delta_seconds = fixed_dt  # 20 FPS; tune as needed
    settings.max_substep_delta_time = fixed_dt
    world.apply_settings(settings)

def spawn_vehicle(world, bp_lib, spawn_point, role_name):
    veh_bp = bp_lib.filter("vehicle.*model3*")[0]  # choose your model
    veh_bp.set_attribute("role_name", role_name)
    vehicle = world.spawn_actor(veh_bp, spawn_point)
    return vehicle

def attach_camera(world, bp_lib, parent, rel_loc=(0.8,0.0,1.7), rel_rot=(0,0,0), name="rgb"):
    cam_bp = bp_lib.find("sensor.camera.rgb")
    cam_bp.set_attribute("image_size_x", "1280")
    cam_bp.set_attribute("image_size_y", "720")
    cam_bp.set_attribute("fov", "90")
    cam_bp.set_attribute("sensor_tick", "0.05")  # match world fps
    cam_tf = carla.Transform(carla.Location(*rel_loc), carla.Rotation(*rel_rot))
    cam = world.spawn_actor(cam_bp, cam_tf, attach_to=parent)
    cam.listen(lambda image: None)  # replace with your callback/queue
    return cam

def attach_lidar(world, bp_lib, parent, name="lidar"):
    li_bp = bp_lib.find("sensor.lidar.ray_cast")
    li_bp.set_attribute("range", "120.0")
    li_bp.set_attribute("rotation_frequency", "20.0")
    li_bp.set_attribute("points_per_second", "800000")
    li_bp.set_attribute("channels", "64")
    li_bp.set_attribute("upper_fov", "10.0")
    li_bp.set_attribute("lower_fov", "-30.0")
    li_bp.set_attribute("sensor_tick", "0.05")
    li = world.spawn_actor(li_bp, carla.Transform(carla.Location(0,0,1.8)), attach_to=parent)
    li.listen(lambda cloud: None)
    return li

def attach_radar(world, bp_lib, parent, name="radar"):
    rd_bp = bp_lib.find("sensor.other.radar")
    rd_bp.set_attribute("horizontal_fov", "30")
    rd_bp.set_attribute("vertical_fov", "15")
    rd_bp.set_attribute("range", "100")
    rd_bp.set_attribute("sensor_tick", "0.05")
    rd = world.spawn_actor(rd_bp, carla.Transform(carla.Location(2.0,0.0,1.0)), attach_to=parent)
    rd.listen(lambda meas: None)
    return rd

def drive_autopilot(world, vehicle, tm_port=8000):
    tm = carla.TrafficManager.get_instance(world, tm_port)
    vehicle.set_autopilot(True, tm_port)
    tm.ignore_lights_percentage(vehicle, 0.0)
    tm.vehicle_percentage_speed_difference(vehicle, 0)  # 0% slower than limit

def main(num_egos=4):
    with carla_client(HOST, PORT) as client:
        world = client.get_world()
        setup_world(world, fixed_dt=0.05)

        bp_lib = world.get_blueprint_library()
        spawn_points = world.get_map().get_spawn_points()
        random.shuffle(spawn_points)

        actors = []
        try:
            for i in range(num_egos):
                veh = spawn_vehicle(world, bp_lib, spawn_points[i], role_name=f"hero{i}")
                drive_autopilot(world, veh)
                cam = attach_camera(world, bp_lib, veh)
                li  = attach_lidar(world, bp_lib, veh)
                rd  = attach_radar(world, bp_lib, veh)
                actors.extend([veh, cam, li, rd])

            # sync loop
            for _ in range(2000):  # ~100 seconds at 20 FPS
                world.tick()

        finally:
            client.apply_batch([carla.command.DestroyActor(a) for a in actors])
            # return world to async if you want
            s = world.get_settings(); s.synchronous_mode=False; world.apply_settings(s)

if __name__ == "__main__":
    main(num_egos=8)  # scale up; CARLA will spread sensor rendering across your 8 GPUs
