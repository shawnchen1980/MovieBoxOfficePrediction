# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 08:17:15 2019

@author: shawn
"""

import matplotlib.pyplot as plt
import numpy as np

x = np.arange(100)
plt.figure()
print(plt.get_fignums())
print(plt.gcf(),plt.gca())


#for i in plt.get_fignums():
##    print("hello")
#    plt.figure(i)