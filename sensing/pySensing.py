import carla

client = carla.Client(host, port); client.set_timeout(30.0)
world = client.get_world()
s = world.get_settings(); s.synchronous_mode=True; s.fixed_delta_seconds=0.05; world.apply_settings(s)

# 1) queues
img_q, lidar_q, radar_q = Queue(maxsize=64), Queue(maxsize=64), Queue(maxsize=64)

# 2) callbacks only enqueue
cam.listen(lambda data: img_q.put_nowait((data.frame, data.timestamp, data)))
lidar.listen(lambda data: lidar_q.put_nowait((data.frame, data.timestamp, data)))
radar.listen(lambda data: radar_q.put_nowait((data.frame, data.timestamp, data)))

# 3) writer processes read & write (PNG/NPY/MCAP/…)
Process(target=write_images, args=(img_q, out_dir)).start()
Process(target=write_lidar,  args=(lidar_q, out_dir)).start()
Process(target=write_radar,  args=(radar_q, out_dir)).start()

# 4) main loop: tick, then read telemetry and (optionally) block
for _ in range(N):
    world.tick()
    snap = world.get_snapshot()
    ego_state = (ego.get_transform(), ego.get_velocity(), ego.get_acceleration(), ego.get_control())
    telemetry_writer.write(snap.frame, snap.timestamp, ego_state)  # append only
