import os
import sys
import math
import tempfile
import pytest
import logging
from pathlib import Path
import numpy as np
from dtaidistance import dtw, clustering
import dtaidistance.dtw_visualisation as dtwvis


logger = logging.getLogger("be.kuleuven.dtai.distance")


def test_bug1(directory=None):
    series = np.array([
        [0., 0, 1, 2, 1, 0, 1, 0, 0],
        [0., 1, 2, 0, 0, 0, 0, 0, 0],
        [1., 2, 0, 0, 0, 0, 0, 1, 1],
        [0., 0, 1, 2, 1, 0, 1, 0, 0],
        [0., 1, 2, 0, 0, 0, 0, 0, 0],
        [1., 2, 0, 0, 0, 0, 0, 1, 1]])
    model = clustering.LinkageTree(dtw.distance_matrix_fast, {})
    cluster_idx = model.fit(series)

    if directory:
        hierarchy_fn = directory / "hierarchy.png"
    else:
        file = tempfile.NamedTemporaryFile()
        hierarchy_fn = Path(file.name + "_hierarchy.png")
    model.plot(hierarchy_fn)
    print("Figure saved to", hierarchy_fn)


def test_bug2(directory=None):
    s1 = np.array([0, 0, 1, 2, 1, 0, 1, 0, 0], dtype=np.double)
    s2 = np.array([0.0, 1, 2, 0, 0, 0, 0, 0, 0])
    d1a = dtw.distance_fast(s1, s2, window=2)
    d1b = dtw.distance(s1, s2, window=2)

    if directory:
        fn = directory / "warpingpaths.png"
    else:
        file = tempfile.NamedTemporaryFile()
        fn = Path(file.name + "_warpingpaths.png")
    d2, paths = dtw.warping_paths(s1, s2, window=2)
    best_path = dtw.best_path(paths)
    dtwvis.plot_warpingpaths(s1, s2, paths, best_path, filename=fn, shownumbers=False)
    print("Figure saved to", fn)

    assert d1a == pytest.approx(d2)
    assert d1b == pytest.approx(d2)


if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    sh = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(message)s')
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    logger.propagate = 0
    test_bug2(directory=Path.home() / "Desktop/")
