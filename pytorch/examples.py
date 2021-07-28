# This example shows how to run PU21 metrics on HDR images
import HDRutils
import os 
import pu21_metric
import torch
import scipy.ndimage as ndimage
import numpy as np
import cv2
# in python

I_ref = HDRutils.imread( os.path.join("..","matlab","examples",'nancy_church.hdr' ))
I_ref = torch.tensor(I_ref)

A = [[1,100],[45,80]]
B = [[1,100],[45,80]]
C = [[255,150],[170,15]]

I_ref = torch.tensor([[[1,100],[45,80]],[[1,100],[45,80]],[[255,150],[170,15]]] ,dtype=torch.float)
I_ref /= 255.0



print(I_ref.mean())
L_peak = 1000 # Peak luminance of an HDR display

# HDR images are often given in relative photometric units. They MUST be
# mapped to absolute amount of light emitted from the display. For that, 
# we map the peak value in the image to the peak value of the display:

I_ref = I_ref/torch.max(I_ref) * L_peak
# Add Gaussian noise of 20% contrast. Make sure all values are greater than
# 0.05.
E = [[1,10],[5,0]]
F = [[3,7],[20,-10]]
G = [[-15,3],[-8,0]]

I_test_noise =I_ref + torch.tensor([[[1,10],[5,0]],[[3,7],[20,-10]],[[-15,3],[-8,0]]] ,dtype=torch.float)
#I_test_noise = torch.maximum(I_ref + I_ref*torch.randn(I_ref.shape)*0.2, torch.tensor(0.05) )
def matlab_style_gauss2D(shape=(3,3),sigma=0.5):
    """
    2D gaussian mask - should give the same result as MATLAB's
    fspecial('gaussian',[shape],[sigma])
    """
    m,n = [(ss-1.)/2. for ss in shape]
    y,x = np.ogrid[-m:m+1,-n:n+1]
    h = np.exp( -(x*x + y*y) / (2.*sigma*sigma) )
    h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
    sumh = h.sum()
    if sumh != 0:
        h /= sumh
    return h
I_test_blur = cv2.GaussianBlur(I_ref.numpy(), ksize=(0, 0), sigmaX=3, borderType=cv2.BORDER_REPLICATE)

print("Print Ref", I_ref)
print("Print Noise", I_test_noise)
print("Print Blur", I_test_blur)


PSNR_noise = pu21_metric.pu21_metric( I_test_noise, I_ref, 'PSNR' )
SSIM_noise = pu21_metric.pu21_metric( I_test_noise, I_ref, 'SSIM' )

print('Image with noise: PSNR = {} dB, SSIM = {}'.format( PSNR_noise, SSIM_noise) )


PSNR_blur = pu21_metric.pu21_metric( I_test_blur, I_ref, 'PSNR' )
SSIM_blur = pu21_metric.pu21_metric( I_test_blur, I_ref, 'SSIM' )
print('Image with blur: PSNR = {} dB, SSIM = {}'.format( PSNR_blur, SSIM_blur) )
