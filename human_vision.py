import gbvision as gbv
import numpy as np

CAMERA_DISTANCE = 0.1  # distance from camera to center
                       # CAMERA_DISTANCE = half of the distance between the cameras

threshold_func = gbv.Threshold([[0, 98], [128, 255], [175, 255]], 'HSV') + gbv.Erode(3) + gbv.Dilate(3)
# Threshold for FRC Cargo from 2019 Deep Space competition
# found using median threshold

OBJECT_DESCRIPTOR = gbv.GameObject(1)
# Can be any number except 0

finder = gbv.CircleFinder(threshold_func, OBJECT_DESCRIPTOR, contour_min_area=1000)


def height_angle(loc):
    return np.arctan(loc[1] / loc[2])


def main():
    win1 = gbv.CameraWindow('camera 2', gbv.USBCamera(2, gbv.LIFECAM_3000))
    win2 = gbv.CameraWindow('camera 1', gbv.USBCamera(1, gbv.LIFECAM_3000))
    win1.wrap_object.set_exposure(-4)
    win2.wrap_object.set_exposure(-4)
    windows = [win1, win2]
    while True:
        frames = [win1.show_and_get_frame(), win2.show_and_get_frame()]
        if any([x is None for x in frames]):
            continue
        not_found = False
        angles = np.zeros((2, 2))
        for i in range(2):
            loc = finder(frames[i], windows[i].wrap_object)
            if len(loc) == 0:
                not_found = True
                break
            loc = loc[0]
            angles[i] = np.array([gbv.plane_angle_by_location(loc), height_angle(loc)])

        if not_found:
            continue
        print(angles)
        a, b, c, d = np.tan(angles.flatten())
        if c < a:
            c, a = a, c
            d, b = b, d
        z = 2 * CAMERA_DISTANCE / (c - a)
        # the minimum of the distance function between the two lines
        # also the x intersection, assuming both cameras are aligned on the y and z axis
        x = z * (a + c) / 2
        y = z * (b + d) / 2
        print(f'Location: {np.array([x, y, z])}')


if __name__ == '__main__':
    main()
