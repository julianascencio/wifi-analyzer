"""
A 50 m property with three extenders
=========================================

Synthetic demonstration only: these are not measurements of a real finca.
A strong extender signal does not establish a good link back to the router.
Each radio is mapped separately to avoid hiding weak links behind a best-AP map.
The arbitrary obstacle loss illustrates a potential discontinuity; it is not
calibrated to wall materials. Background interpolation does not reconstruct walls.
"""

import matplotlib.pyplot as plt

from wifi_analyzer.analysis import summarize
from wifi_analyzer.demo import demo_samples
from wifi_analyzer.report import plot_group

samples = demo_samples()
for summary in summarize(samples):
    print(summary)
    plot_group([s for s in samples if s.ap_id == summary["ap_id"]])
plt.show()
