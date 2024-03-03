% Plots thermal test results
% Alan Hsu

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

filename = input('Enter data filename: ', "s");
raw_data = readmatrix(filename);

time_s = raw_data(:, 1);
adc_raw = raw_data(:, 2:17);
temp_c = raw_data(:, 18:20);

time_min = time_s / 60;
therm_v_sum = adc_raw(:, 3) * THERM_VDIV_RATIO * ADC_IN_MAX / ADC_RES;
therm_r_sum = therm_v_sum / I_S;
therm_r_avg = therm_r_sum / 8;
therm_k = 1 ./ (1./T0 - log(R0./therm_r_avg)./Beta);
therm_c = therm_k - 273.15;