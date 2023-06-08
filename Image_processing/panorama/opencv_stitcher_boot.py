imgs = []
for img_name in args.img:
    if len(args.img) != 1:
        img = cv.imread(cv.samples.findFile(img_name))
        imgs.append(img)
    elif len(args.img) == 1:
        imgs = [cv.imread(file) for file in sorted(glob.glob(args.img[0]))]