# -*- coding: utf-8 -*-

import os
from skimage import io  # @UnresolvedImport
from skimage.transform import resize as ski_resize  # @UnresolvedImport

from monu.logger import getLogger

log = getLogger(__file__)


def resize(in_file, out_file, height=200):
    if os.path.exists(out_file):
        return True
    img = io.imread(in_file)
    ow = 1.0 * len(img)
    oh = 1.0 * len(img[0])
    width = int(height * ow / oh)
    height = int(height)
    img = ski_resize(img, (width, height))
    try:
        io.imsave(out_file, img)
    except Exception as e:
        log.critical('Error: %s', e)
        return False
    return True
