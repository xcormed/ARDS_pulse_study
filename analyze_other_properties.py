import numpy as np
import matplotlib.pyplot as plt

# This script produces boxplots for generic patient properties (respiration rate, blood pH, ...)

# Arguments: case - (COPD or ARDS), property_type - what property to compare


def analyze_other_properties(case, property_type):
    # Make a list of patient names and severities
    #names = ["Cynthia", "Gus", "Joel", "Nathan", "Rick", "Hassan", "Soldier", "Jeff", "Carol", "Jane"]
    names = ["Adam", "Bert", "Chris", "David", "Elie", "Anna", "Bella", "Charlotte", "Dorothy", "Emma"]
    severities = [0.9]#, 0.6, 0.9]

    # Initialize arrays to hold CO2 values for each patient and each severity. One array per treatment.
    property_untreated = np.zeros((len(names), len(severities)))
    property_ecmo = np.zeros((len(names), len(severities)))
    property_nasal_cannula = np.zeros((len(names), len(severities)))
    property_nonrebreather = np.zeros((len(names), len(severities)))
    property_ventilator = np.zeros((len(names), len(severities)))
    property_traditional_ventilator = np.zeros((len(names), len(severities)))
    property_ecmo_traditional_ventilator = np.zeros((len(names), len(severities)))
    property_ecmo_protective_ventilator = np.zeros((len(names), len(severities)))

    for i in range(len(names)):
        for j in range(len(severities)):
            # Load in each csv file corresponding to patient name, disease severity, and treatment

            # Use these three lines for the ards_ventilator script:
            data = np.genfromtxt('./test_results/XCOR/{}_ventilator{}_{}.csv'.format(case, names[i], severities[j]),
                                 delimiter=',', names=True, dtype=None, encoding=None)
            property_ventilator[i, j] = np.mean(data[property_type][-1000:])
            
            # Use these three lines for the ards_ecmo_ventilator script:
            #data = np.genfromtxt('./test_results/XCOR/{}_ecmo_ventilator{}_{}.csv'.format(case, names[i], severities[j]),
             #                    delimiter=',', names=True, dtype=None, encoding=None)
            #property_ventilator[i, j] = np.mean(data[property_type][-1000:])



    print(property_type, ":", np.round(np.mean(property_ventilator), 2),"±", np.round(np.std(property_ventilator), 2))

    