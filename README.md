<h1 align='center'>
  <br>
    Computed Tomography Reconstruction
  <br>
</h1>

<p align='center'>
  <img src="https://github.com/adh182/ct-reconstruction/blob/master/images/icon/ct-interface.png" alt="ct-interface" height="600">
</p>

## Overview
This application shows resulted sinogram and image reconstruction calculated from input image using computed tomography algorithm. The algorithm used are [Filtered Back Projection](https://en.wikipedia.org/wiki/Tomographic_reconstruction) and [SART (Simultaneous Algebraic Reconstruction Technique)](https://en.wikipedia.org/wiki/Simultaneous_algebraic_reconstruction_technique). The calculation of sinogram and image reconstruction use scikit-image [`radon`](https://scikit-image.org/docs/dev/api/skimage.transform.html#skimage.transform.radon), [`iradon`](https://scikit-image.org/docs/dev/api/skimage.transform.html#skimage.transform.iradon) and [`iradon_sart`](https://scikit-image.org/docs/dev/api/skimage.transform.html#skimage.transform.iradon_sart).
