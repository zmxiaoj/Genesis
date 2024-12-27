import genesis as gs

gs.init(backend = gs.cpu, 
        theme='light',
)

scene = gs.Scene(
    sim_options = gs.options.SimOptions(
        dt = 0.01,
        gravity = (0, 0, -9.81),
    ),
    show_viewer = True,
    viewer_options = gs.options.ViewerOptions(
        res = (1280, 960),
        camera_pos = (3.5, 0.0, 2.5),
        camera_lookat = (0.0, 0.0, 0.5),
        camera_fov = 40,
        max_FPS = 60,
    ),
    vis_options = gs.options.VisOptions(
        show_world_frame = True, # 显示原点坐标系
        world_frame_size = 1.0,  # 坐标系长度(米)
        show_link_frame  = True, # 显示实体链接坐标系 
        show_cameras     = True, # 显示相机网格和视锥
        plane_reflection = True, # 开启平面反射
        ambient_light    = (0.1, 0.1, 0.1), # 环境光
    ),
    renderer = gs.renderers.Rasterizer(), # 使用光栅化渲染器
)

plane = scene.add_entity(
    gs.morphs.Plane(),
)
box = scene.add_entity(
    gs.morphs.Box(pos = (1.0, 1.0, 0.0),
                  size = (0.2, 0.2, 0.2),
                  ),
)
sphere = scene.add_entity(
    gs.morphs.Sphere(pos = (-1.0, -1.0, 0.0),
                     radius = 0.3,
                     ),
)
franka = scene.add_entity(
    # gs.morphs.URDF(
    #     file='urdf/panda_bullet/panda.urdf',
    #     fixed=True,
    # ),
    gs.morphs.MJCF(file = "xml/franka_emika_panda/panda.xml",
                   pos = (0.0, 0.0, 0.0),
                   euler = (0.0, 0.0, 90.0),
                   scale = 1.0,
                   ),
)

cam = scene.add_camera(
    res    = (640, 480),
    pos    = (3.5, 0.0, 2.5),
    lookat = (0, 0, 0.5),
    fov    = 30,
    GUI    = True,
)

scene.build()
# 渲染rgb、深度、分割掩码和法线图
rgb, depth, segmentation, normal = cam.render(rgb = True, 
                                              depth = True, 
                                              segmentation = True, 
                                              normal = True
)

cam.start_recording()
import numpy as np

for i in range(2000):
    scene.step()
    cam.set_pose(
        pos    = (3.0 * np.sin(i / 60), 3.0 * np.cos(i / 60), 2.5),
        lookat = (0, 0, 0.5),
    )
    cam.render()
cam.stop_recording(save_to_filename = 'video.mp4', 
                   fps = 60
)