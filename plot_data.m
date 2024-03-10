% Plots thermal test results
% Alan Hsu

filename = input('Enter data filename: ', "s");
raw_data = readmatrix(filename);

time_s = raw_data(:, 1);
adc_raw = raw_data(:, 2:17);
temp_c = raw_data(:, 18:end);

time_min = time_s / 60;
femta_temp = temp_conversion(adc_raw(:, 3), 8, 3570);
tank_temp = temp_conversion(adc_raw(:, 12), 4, 3934);

femta_heater_power = heater_power(adc_raw(:, 9));
tank_heater_power = heater_power(adc_raw(:, 11));

t_tank1 = temp_c(:, 1);
t_valve = temp_c(:, 2);
t_tank2 = temp_c(:, 3);
t_femta1 = temp_c(:, 4);
t_control_pcb = temp_c(:, 5);
t_plate = temp_c(:, 6);
t_femta2 = temp_c(:, 7);

hold on
xlabel('Time [min]');
ylabel('Temperature [*C]');
title('Tank and FEMTA thermistor temperature against true temperatures');
plot(time_min, femta_temp, '-b');
plot(time_min, tank_temp, '-r');
plot(time_min(t_tank1~=85), t_tank1(t_tank1~=85), '-.g');
plot(time_min(t_valve~=85), t_valve(t_valve~=85), '-.c');
plot(time_min(t_tank2~=85), t_tank2(t_tank2~=85), '-.m');
plot(time_min(t_femta1~=85), t_femta1(t_femta1~=85), '-.y');
plot(time_min(t_control_pcb~=85), t_control_pcb(t_control_pcb~=85), '-.r');
plot(time_min(t_plate~=85), t_plate(t_plate~=85), '-.k');
plot(time_min(t_femta2~=85), t_femta2(t_femta2~=85), '-.b');
plot(time_min, 20*(femta_heater_power > 0.5), '-b');
plot(time_min, 20*(tank_heater_power > 0.5), '-r');
legend({'FEMTA', 'Tank', 'Tank 1', 'Valve Channels', 'Tank 2', 'Femta Interface 1', 'Control PCB', 'Plate', 'Femta Interface 2', 'FEMTA Heater', 'Tank Heater'}, 'Location', 'southwest');
grid on
hold off