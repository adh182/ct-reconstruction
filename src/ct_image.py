from skimage import io  
from CTProgram import CT 
import matplotlib.pyplot as plt 


filename = "../images/gambar_1.jpg"
image = io.imread(filename)
max_angle = 180.0 

# filters = ['ramp', 'shepp-logan', 'cosine', 'hamming', 'hann']

filter_used = "hann"

CT = CT(image, max_angle, filter_used)
fig = CT.graph()
plt.show()