% Plots thermal test results
% Alan Hsu

filename = input('Enter data filename: ', "s");
raw_data = readmatrix(filename);

time_s = raw_data(:, 1);
adc_raw = raw_data(:, 2:17);
temp_c = raw_data(:, 18:20);

time_min = time_s / 60;
femta_temp = temp_conversion(adc_raw(:, 3), 8);
tank_temp = temp_conversion(adc_raw(:, 12), 4);

femta_heater_power = heater_power(adc_raw(:, 9));
tank_heater_power = heater_power(adc_raw(:, 11));

t_pcb_1 = temp_c(:, 1);
t_pcb_2 = temp_c(:, 3);
t_plate = temp_c(:, 2);

hold on
xlabel('Time [min]');
ylabel('Temperature [*C]');
title('Tank and FEMTA thermistor temperature against true temperatures');
plot(time_min, femta_temp, '-b');
plot(time_min, tank_temp, '-r');
plot(time_min(t_pcb_1~=85), t_pcb_1(t_pcb_1~=85), '-g');
plot(time_min(t_pcb_2~=85), t_pcb_2(t_pcb_2~=85), '-c');
plot(time_min(t_plate~=85), t_plate(t_plate~=85), '-k');
legend({'FEMTA', 'Tank', 'PCB side 1', 'PCB side 2', 'Plate Temp'}, 'Location', 'northeast');
grid on
hold off