import numpy as np
import sys
from pathlib import Path
import click
import util

camerasfile = sys.argv[1]
samples = int(sys.argv[2])

print(camerasfile)
print(samples)

path = Path(camerasfile)
print(path.parent.absolute())

print(f"loading {click.style(camerasfile, fg='yellow', bold=True)}")
cameras = util.CamerasXML().read(camerasfile)

camera_names = sorted(cameras.cameras.keys())
print(np.zeros(3))