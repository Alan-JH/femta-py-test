function [power] = heater_power(adc_raw)
% Converts 12 bit ADC reading to power

% ADC Specs
ADC_VREF = 2.5;
ADC_RES = 4096;
ADC_IN_MAX = 2*ADC_VREF;

V_TO_POWER = 1;

power = V_TO_POWER * adc_raw * ADC_IN_MAX / ADC_RES;