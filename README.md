# ARDS_pulse_study

1. analyze_other_properties.py defines a function that calculates the means and standard deviations of the patients' properties.
2. get_data.py calls upon the analyze_other_properties function and prints out the means and standard deviations of the desired properties.
3. ards_untreated.py gives a defined ARDS severity to each patient and runs for 2 simulated hours to reach a steady state.
4. ards_ventilator.py applies ventilatory therapy to each patient. Ventilator settings such as FiO2, TV, flow rate, PEEP, and RR are adjustable.
5. ards_ecmo_ventilator.py applies ventilatory and ECMO therapy to each patient. ECMO settings such as CO2 removal, flow rate, and oxygenator volume are adjustable.
6. create_state.py creates unique patients based on user inputs (height, weight, age, etc.)
7. Patients - sheet includes the patients' features that were used in this study.
