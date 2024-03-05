function [temp_c] = temp_conversion(adc_raw)
% Converts 12 bit ADC reading to temperature

% ADC Specs
ADC_VREF = 2.5;
ADC_RES = 4096;
ADC_IN_MAX = 2*ADC_VREF;

THERM_VDIV_RATIO = 5.1; % Voltage divider ratio from thermistor to input
RSET = 2000;
I_S = 227e-6 * (298.15) / RSET; % Supply current

% Thermistor specs
T0 = 298.15;
R0 = 10000;
Beta = 3570;

% Calculations
v_sum = adc_raw * THERM_VDIV_RATIO * ADC_IN_MAX / ADC_RES;
r_sum = v_sum / I_S;
r_avg = r_sum / 8;
temp_k = 1 ./ (1./T0 - log(R0./r_avg)./Beta);
temp_c = temp_k - 273.15;