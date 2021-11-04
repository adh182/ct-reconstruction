import numpy as np
import matplotlib.pyplot as plt 
from skimage import color
from skimage.transform import radon, iradon, iradon_sart, rescale

class CT:

	def __init__(self, image, max_angle, filter_name):
		"""
		Parameter:
			image = an image to transform to sinogram
			max_angle = the maximum angle of projection
			filter_name = the type of filter used in fbp
		Result:
			the graph of original, sinogram, filter back projection.

		"""
		self.image = image
		#convet 3D image to 2D image
		if len(self.image.shape) == 3:
			self.image = color.rgb2gray(image)
			
		self.max_angle = max_angle
		self.filter = filter_name

	def process_image(self):
		"""Scale the image and calculate theta as numbers of projection"""

		image_scaled = rescale(self.image, scale=0.4, mode='reflect', multichannel=False)
		theta = np.linspace(0.0, self.max_angle, max(image_scaled.shape))
		# num_projection = len(theta)
		num_projection = len(theta)*max(image_scaled.shape)
		
		return image_scaled, theta, num_projection

	def radon_transform(self):
		"""Calculate sinogram by radon transformation"""

		img, theta, __ = self.process_image()
		sinogram = radon(img, theta=theta)

		return sinogram


	def filtered_back_projection(self):
		"""Back projection to reconstruct image from sinogram"""

		__, theta, __ = self.process_image()
		sinogram = self.radon_transform()

		reconstruction = iradon(sinogram, theta=theta, filter_name=self.filter)

		return reconstruction

	def sart(self):
		"""Simultaneous algebraic reconstruction technique"""

		__, theta, __ = self.process_image()
		sinogram = self.radon_transform()

		reconstruction_sart = iradon_sart(sinogram, theta=theta)

		return reconstruction_sart

	def graph(self):
		"""Plot graph of original image, sinogram, image reconstruction"""

		image, __, __ = self.process_image()
		sinogram = self.radon_transform()
		reconstruction = self.filtered_back_projection()
		reconstruction_sart = self.sart()


		fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

		#Plot original image
		ax1.set_title("Original Image")
		ax1.imshow(image, cmap=plt.cm.Greys_r)

		#Plot sinogram
		ax2.set_title("Sinogram")
		ax2.set_xlabel("Projection angle (deg)")
		ax2.set_ylabel("Projection position (pixels)")
		ax2.imshow(sinogram, cmap=plt.cm.Greys_r)

		#Plot reconstructed image
		ax3.set_title("Filtered Back Projection")
		ax3.imshow(reconstruction, cmap=plt.cm.Greys_r)

		#Plot reconstructed image
		ax4.set_title("SART")
		ax4.imshow(reconstruction_sart, cmap=plt.cm.Greys_r)

		plt.show()