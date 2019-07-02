

import matplotlib.pyplot as plt
import scipy
 
# gqrx_yyyymmdd_hhmmss_freq_samplerate_fc.raw
input_filename = "gqrx_20190630_203446_98901000_1800000_fc.raw"
output_suffix = "subset"
 
sample_rate = input_filename.split('_')[4]
 
with open(input_filename, 'rb') as f:
    x = scipy.fromfile(f, dtype=scipy.complex64)
len(x)
 
# Look at the data
plt.plot(abs(x))
plt.show()

# Determine region of interest & extract
start = int(2.8e7)
end = int(4.2e7)
roi = x[start:end]

output_filename = input_filename.replace(".raw", output_suffix + ".raw")
 
with open(output_filename, 'wb') as 2:
    f.write(roi.tobytes())

# https://me.m01.eu/blog/2018/04/basic-gqrx-i/q-and-gnuradio-file-editing/