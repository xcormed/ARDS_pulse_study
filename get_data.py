import sys, os.path
dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(dir)

from analysis.analyze_CO2 import analyze_CO2
from analysis.analyze_other_properties import analyze_other_properties

# Examples of properties that can be analyzed (anything in the results list):
#analyze_other_properties('ARDS', 'DiastolicArterialPressuremmHg')
#analyze_other_properties('ARDS', 'MechanicalVentilatorPlateauPressurecmH2O')
#analyze_other_properties('ARDS', 'MechanicalVentilatorMeanAirwayPressurecmH2O')
#analyze_other_properties('ARDS', 'MechanicalVentilatorPositiveEndExpiredPressurecmH2O')
#analyze_other_properties('ARDS', 'AortaCarbonDioxidePartialPressuremmHg')
#analyze_other_properties('ARDS', 'AortaOxygenPartialPressuremmHg')
#analyze_other_properties('ARDS', 'RespirationRate1min')
#analyze_other_properties('ARDS', 'BloodPH')
#analyze_other_properties('ARDS', 'MechanicalVentilatorPeakInspiratoryPressurecmH2O')
#analyze_other_properties('ARDS', 'TidalVolumemL')
#analyze_other_properties('ARDS', 'ECMOOxygenatorBicarbonateConcentrationgdL')
#analyze_other_properties('ARDS', 'ECMOOxygenatorCarbonDioxidePartialPressuremmHg')



