% This example shows how to run PU21 metrics on HDR images

if ~exist( 'pu21_encoder', 'class' )
    addpath( fullfile( pwd, '..') );
end

I_ref = hdrread( 'nancy_church.hdr' );
fprintf( 1, 'Mean = %g\n', mean(mean(mean(I_ref))) );
L_peak = 1000; % Peak luminance of an HDR display

A = [[1,100];[45,80]];
B = [[1,100];[45,80]];
C = [[255,150];[170,15]];
D = cat(3,A,B,C);
I_ref = D ;
% HDR images are often given in relative photometric units. They MUST be
% mapped to absolute amount of light emitted from the display. For that, 
% we map the peak value in the image to the peak value of the display:
I_ref = I_ref/max(I_ref(:)) * L_peak

% Add Gaussian noise of 20% contrast. Make sure all values are greater than
% 0.05.
E = [[1,10];[5,0]];
F = [[3,7];[20,-10]];
G = [[-15,3];[-8,0]];
N = cat(3,E,F,G);
I_test_noise = I_ref+N
%I_test_noise = max( I_ref + I_ref.*randn(size(I_ref))*0.2, 0.05 );

T = [[ 317.74402,  358.33322];[ 319.98932,  329.44864]];
Y = [[ 415.46072,  358.40552];[ 409.243  ,  321.9764 ]];
Z = [[ 518.7597 ,  358.482  ];[ 503.59552,  314.07733]];
I_test_blur = cat(3,T,Y,Z)
%I_test_blur = imgaussfilt( I_ref, 3 )

PSNR_noise = pu21_metric( I_test_noise, I_ref, 'PSNR' );
SSIM_noise = pu21_metric( I_test_noise, I_ref, 'SSIM' );
fprintf( 1, '--------------------------------------------\n');
PSNR_blur = pu21_metric( I_test_blur, I_ref, 'PSNR' );
SSIM_blur = pu21_metric( I_test_blur, I_ref, 'SSIM' );

fprintf( 1, 'Image with noise: PSNR = %g dB, SSIM = %g\n', PSNR_noise, SSIM_noise );
fprintf( 1, 'Image with blur: PSNR = %g dB, SSIM = %g\n', PSNR_blur, SSIM_blur );