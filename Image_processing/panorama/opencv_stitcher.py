import glob
import numpy as np
import cv2 as cv
import argparse
import sys

modes = (cv.Stitcher_PANORAMA, cv.Stitcher_SCANS)

parser = argparse.ArgumentParser(prog='stitching.py', description='Stitching sample.')
parser.add_argument('--mode',
                    type=int, choices=modes, default=cv.Stitcher_PANORAMA,
                    help='Determines configuration of stitcher. The default is `PANORAMA` (%d), '
                         'mode suitable for creating photo panoramas. Option `SCANS` (%d) is suitable '
                         'for stitching materials under affine transformation, such as scans.' % modes)
parser.add_argument('--output', default='result.jpg',
                    help='Resulting image. The default is `result.jpg`.')
parser.add_argument('img', nargs='+', help='input images')

# __doc__ += '\n' + parser.format_help()


def main():
    args = parser.parse_args()

    # read input path of images or file which contains images
    imgs = []
    for img_name in args.img:
        if len(args.img) != 1:
            img = cv.imread(cv.samples.findFile(img_name))
            imgs.append(img)
        elif len(args.img) == 1:
            imgs = [cv.imread(file) for file in sorted(glob.glob(args.img[0]))]
        else:
            print("can't read image " + img_name)
            sys.exit(-1)

    stitcher = cv.Stitcher.create(args.mode)
    status, pano = stitcher.stitch(imgs)

    if status != cv.Stitcher_OK:
        print("Can't stitch images, error code = %d" % status)
        sys.exit(-1)

    cv.imwrite(args.output, pano)
    print("stitching completed successfully. %s saved!" % args.output)

    print('Done')


if __name__ == '__main__':
    print(__doc__)
    main()
    cv.destroyAllWindows()
