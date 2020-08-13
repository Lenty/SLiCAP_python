============
Noise design
============

SLiCAP has a number of built-in scripts to support circuit designers with the analysis and design of the stationary noise behavior of electronic circuits. These functions can be used to process the result of the execution of an instruction with the data type set to NOISE. These functions are listed below and discussed in detail in the following sections.

Please notice that some of these functions use symbolic integration which may fail if the frequency dependency of the spectra becomes too complex.

In the brief descriptions below, we assume that a noise simulation comprising j runs (j-1 steps), has been performed.

--------------------------
Correlated double sampling
--------------------------

Correlated double sampling is a popular technique to reduce the influence of low-frequency noise and switching noise of sample and hold circuits. The post processing function ``doCDS.m`` can be used for this purpose. This function requires one argument :math:`\tau` which represents the time delay between the two samples. CDS is implemented as a continuous-time post-processing function. The sampling itself is not modeled. The CDS post processor returns the spectra of the difference between the signal and its delayed copy (delayed over :math:`\tau` seconds). The squared magnitude of the frequency-domain transfer :math:`| H\left(f\right) |^2` of this operation can be written as:

.. math::

    | H\left(f\right) |^2=| 1 - \exp{(-2 \pi f \tau)} |^2

which can alternatively be written as:

.. math::

    | H\left(f\right) |^2=(2 \sin(\pi f \tau))^2

The doCDS function replaces all detector-referred spectral density results :math:`S_{x}` in the ``.results`` field with :math:`(2 \sin(\pi f \tau))^2 S_{x}`. It also replaces both the lists with the source-referred noises pectral density contributions and the total source referred noise spectra in the ``.results`` field with the MuPAD boolean FALSE. It returns the modified execution result with its ``.postProc`` field set to ``'CDS'``.

.. code-block:: matlab
        
    sym('tau');
    dataType('noise');
    result            = execute();
    CDSresult         = doCDS(result, tau);

-----------------------------
Extract source-referred noise
-----------------------------

The function ``getInoise.m`` extracts and returns the j source-referred noise spectra from the ``.results`` field. If a
second, optional argument ``sourceName`` is given, it returns the contribution to the source-referred noise spectrum of the
noise source ``sourceName`` only.

.. code-block:: matlab

    dataType('noise');
    result            = execute();
    iNoiseSpectrum    = getInoise(result);       % Spectrum of the total source-referred noise
    iNoiseContribV1   = getInoise(result, 'V1'); % Contribution of the noise source V1
                                                 % in the source-referred noise spectrum

-------------------------------
Extract detector-referred noise
-------------------------------

The function ``getOnoise.m`` extracts and returns the j detector-referred noise spectra from .results field. If a
second, optional argument ``sourceName`` is given, it returns the contribution to the source-referred noise spectrum of the noise source ``sourceName`` only.

.. code-block:: matlab

    dataType('noise');
    result            = execute();
    oNoiseSpectrum    = getOnoise(result);
    oNoiseContribV1   = getOnoise(result, 'V1'); % Contribution of the noise source 'V1' 
                                                 % in the detector-referred noise sprectrum 

---------
RMS noise
---------

The function ``RMSnoise.m`` can be used to calculate the total RMS noise over a frequency range. The function requires two additional arguments :math:`f_{min}` and :math:`f_{max}` and returns the j RMS values:

.. math::

    RMS_j=\sqrt{\int_{f_{min}}^{f_{max}} S_{source,j} df}

If the noise spectra :math:`S_{source,j}` we obtained after application of correlated double sampling, a fourth optional argument ``tau`` which represents the delay dime in the sampler, can be given. This will easy the symbolic calculation of the integral :math:`\mathrm{Si}(\phi)=\int{\left(\frac{\sin{\phi}}{\phi}\right)^2d\phi}`, where :math:`\phi=2\pi f\tau`, and :math:`\tau` is the sampler delay.

Below the calculation of the total RMS source-referred noise over a frequency range from 10Hz to 10MHz, with and without CDS:

.. code-block:: matlab

    dataType('noise');
    result            = execute();
    soureRefNoiseRMS  = RMSnoise(getInoise(result), 10, 1E7);
    tau               = 1E-6; 
    resultCDS         = doCDS(result, tau);
    detRefRMSNoiseCDS = RMSnoise(getOnoise(resultCDS), 10, 1E7, tau);
