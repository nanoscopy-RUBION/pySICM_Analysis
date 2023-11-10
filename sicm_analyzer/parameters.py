from enum import Enum
import sicm_analyzer.measurements


class ParameterEnum(Enum):

    @classmethod
    def list(cls) -> list:
        """Returns the enums values as a list."""
        return [e.value for e in cls]


class GeneralParameters(ParameterEnum):
    Minimum = "min [µm]"
    Maximum = "max [µm]"
    SurfaceArea = "surface area"


class AmplitudeParameters(ParameterEnum):
    ArithmeticAverageHeight = "2.1 Arithmetic average height (R_a)"
    RootMeanSquareRoughness = "2.2 Root mean square roughness"
    TenPointHeight_ISO = "2.3 Ten-point height (ISO) (R_z)"
    TenPointHeight_DIN = "2.3 Ten-point height (DIN) (R_z)"
    MaximumHeightOfPeaks = "2.4 Maximum height of peaks (R_p)"
    MaximumDepthOfValleys = "2.5 Maximum depth of valleys (R_v)"
    MeanHeightOfPeaks = "2.6 Mean height of peaks (R_pm)"
    MeanDepthOfValleys = "2.7 Mean depth of valleys (R_vm)"
    MaximumHeightOfProfile = "2.8 Maximum height of profile (R_t or R_max)"
    MaximumPeakToValleyHeight = "2.9 Maximum peak to valley height (R_ti)"
    MeanOfMaxPeakToValleyHeight = "2.10 Mean of max peak to valley height (R_tm)"
    LargestPeakToValleyHeight = "2.11 Largest peak to valley height (R_y)"
    ThirdPointHeight = "2.12 Third point height (R_3y)"
    MeanOfTheThirdPointHeight = "2.13 Mean of the third point height (R_3z)"
    ProfileSolidarityFactor = "2.14 Profile solidarity factor (k)"
    Skewness = "2.15 Skewness (R_sk)"
    Kurtosis = "2.16 Kurtosis (R_ku)"
    AmplitudeDensityFunction = "2.17 Amplitude density function (ADF)"
    AutoCorrelationFunction = "2.18 Auto correlation function (ACF)"
    CorrelationLength = "2.19 Correlation Length (beta)"
    PowerSpectralDensity = "2.20 Power spectral density (PSD)"


class SpacingParameters(ParameterEnum):
    HighSpotCount = "High spot count (HSC)"
    PeakCount = "Peak count (P_c)"
    MeanSpacingOfAdjacentLocalPeaks = "Mean spacing of adjacent local peaks (S)"
    MeanSpacingAtMeanLine = "Mean spacing at mean line (S_m)"
    NumberOfIntersectionsOfTheProfileAtMeanLine = "Number of intersections of the profile at mean line (n(0))"
    NumberOfPeaksInTheProfile = "Number of peaks in the profile (m)"
    NumberOfInflectionPoints = "Number of inflection points (g)"
    MeanRadiusOfAsperities = "Mean radius of asperities (r_p)"


class HybridParameters(ParameterEnum):
    ProfileSlopeAtMeanLine = "Profile slope at mean line (gamma)"
    MeanSlopeOfTheProfile = "Mean slope of the profile (delta_a)"
    RMSSlopeOfTheProfile = "RMS slope of the profile (delta_q)"
    AverageWavelength = "Average wavelength (lambda_a)"
    RelativeLengthOfTheProfile = "Relative length of the profile (l_o)"
    BearingAreaLength = "Bearing area length (t_p) and bearing area curve"
    StepnessFactorOfTheProfile = "Stepness factor of the profile (S_f)"
    WavinessFactorOfTheProfile = "Waviness factor of the profile (W_f)"
    RoughnessHeightUniformity = "Roughness height uniformity (H_u)"
    RoughnessHeightSkewness = "Roughness height skewness (H_s)"
    RoughnessPitchUniformity = "Roughness pitch uniformity (P_u)"
    RoughnessPitchSkewness = "Roughness pitch skewness (P_s)"


# map enum values to functions
# extend this dictionary for further parameter functions
IMPLEMENTED_PARAMETERS = {
    GeneralParameters.Minimum.value: sicm_analyzer.measurements.get_minimum_value,
    GeneralParameters.Maximum.value: sicm_analyzer.measurements.get_maximum_value,
    AmplitudeParameters.ArithmeticAverageHeight.value: sicm_analyzer.measurements.get_arithmetic_average_height,
    AmplitudeParameters.RootMeanSquareRoughness.value: sicm_analyzer.measurements.get_root_mean_sq_roughness,
    AmplitudeParameters.TenPointHeight_ISO.value: sicm_analyzer.measurements.get_ten_point_height_ISO,
    AmplitudeParameters.TenPointHeight_DIN.value: sicm_analyzer.measurements.get_ten_point_height_DIN,
    AmplitudeParameters.MaximumHeightOfPeaks.value: sicm_analyzer.measurements.get_max_peak_height_from_mean,
    AmplitudeParameters.MaximumDepthOfValleys.value: sicm_analyzer.measurements.get_max_valley_depth_from_mean,
    AmplitudeParameters.MeanHeightOfPeaks.value: sicm_analyzer.measurements.get_mean_height_of_peaks,
    AmplitudeParameters.MeanDepthOfValleys.value: sicm_analyzer.measurements.get_mean_depth_of_valleys,
    AmplitudeParameters.MaximumHeightOfProfile.value: sicm_analyzer.measurements.get_max_height_of_profile,
    AmplitudeParameters.MaximumPeakToValleyHeight.value: sicm_analyzer.measurements.get_maximum_height_single_profile,
    AmplitudeParameters.MeanOfMaxPeakToValleyHeight.value: sicm_analyzer.measurements.get_mean_maximum_peak_valley_heights,
    AmplitudeParameters.LargestPeakToValleyHeight.value: sicm_analyzer.measurements.get_largest_peak_to_valley_height,
    AmplitudeParameters.ThirdPointHeight.value: sicm_analyzer.measurements.get_third_point_height,
    AmplitudeParameters.MeanOfTheThirdPointHeight.value: sicm_analyzer.measurements.get_mean_of_third_point_height,
    AmplitudeParameters.ProfileSolidarityFactor.value: sicm_analyzer.measurements.get_profile_solidarity_factor,
    AmplitudeParameters.Skewness.value: sicm_analyzer.measurements.get_skewness,
    AmplitudeParameters.Kurtosis.value: sicm_analyzer.measurements.get_kurtosis_coefficient,
    #AmplitudeParameters.AmplitudeDensityFunction.value: sicm_analyzer.measurements.get_amplitude_density_function,
    #AmplitudeParameters.AutoCorrelationFunction.value: sicm_analyzer.measurements.get_auto_correlation_function,
    #AmplitudeParameters.CorrelationLength.value: sicm_analyzer.measurements.get_correlation_length,
    #AmplitudeParameters.PowerSpectralDensity.value: sicm_analyzer.measurements.get_power_spectral_density
}