from pulse.engine.PulseEngine import PulseEngine
from pulse.cdm.physiology import eLungCompartment
from pulse.cdm.engine import SEDataRequest, SEDataRequestManager
from pulse.cdm.scalars import FrequencyUnit, MassUnit, MassPerVolumeUnit, \
                              PressureUnit, VolumeUnit, VolumePerTimeMassUnit, VolumePerTimeUnit, TimeUnit, VolumePerPressureUnit
from pulse.cdm.patient_actions import SEAcuteRespiratoryDistressSyndromeExacerbation
from pulse.cdm.ecmo_actions import SEECMOConfiguration
from pulse.cdm.ecmo import eECMO_CannulationLocation
from pulse.cdm.mechanical_ventilator_actions import SEMechanicalVentilatorVolumeControl, \
                                                    eMechanicalVentilator_VolumeControlMode
from pulse.cdm.mechanical_ventilator import eSwitch
from pulse.cdm.patient_actions import SEDyspnea
from pulse.cdm.patient_actions import SERespiratoryMechanicsConfiguration
from pulse.cdm.patient_actions import SEIntubation, eIntubationType


import multiprocessing as mp

# Arguments: patient - a patient name, level_severity - level of severity COPD, VoT - a tidal volume
def ARDS_ecmo_ventilator(patient, level_severity, VoT):
    # Initialize the pulse engine, tell pulse where to send the log file, and also show the log on the console
    pulse = PulseEngine()
    pulse.set_log_filename("./test_results/XCOR/COPD_ecmo_protective_ventilator_{}_{}.log".format(patient,
                                                                                                   level_severity))
    pulse.log_to_console(True)

    # Produce a list of data requests to save to csv. All other timeseries data is calculated but not saved to disk.
    data_requests = [
        SEDataRequest.create_physiology_request("BloodPH"),
        SEDataRequest.create_physiology_request("BloodVolume", unit=VolumeUnit.mL),
        SEDataRequest.create_physiology_request("CardiacOutput", unit=VolumePerTimeUnit.L_Per_min),
        SEDataRequest.create_physiology_request("EndTidalCarbonDioxidePressure", unit=PressureUnit.mmHg),
        SEDataRequest.create_physiology_request("HeartRate", unit=FrequencyUnit.Per_min),
        SEDataRequest.create_physiology_request("Hematocrit"),
        SEDataRequest.create_physiology_request("OxygenSaturation"),
        SEDataRequest.create_physiology_request("CarbonDioxideSaturation"),
        SEDataRequest.create_mechanical_ventilator_request("TidalVolume", unit=VolumeUnit.L),
        SEDataRequest.create_physiology_request("RespirationRate", unit=FrequencyUnit.Per_min),
        SEDataRequest.create_physiology_request("SystolicArterialPressure", unit=PressureUnit.mmHg),
        SEDataRequest.create_physiology_request("DiastolicArterialPressure", unit=PressureUnit.mmHg),
        SEDataRequest.create_physiology_request("TidalVolume", unit=VolumeUnit.mL),
        SEDataRequest.create_physiology_request("TotalPulmonaryVentilation", unit=VolumePerTimeUnit.L_Per_min),
        SEDataRequest.create_substance_request("Bicarbonate", "BloodConcentration", unit=MassPerVolumeUnit.g_Per_L),
        SEDataRequest.create_substance_request("CarbonDioxide", "AlveolarTransfer", unit=VolumePerTimeUnit.mL_Per_s),
        SEDataRequest.create_substance_request("Oxygen", "AlveolarTransfer", unit=VolumePerTimeUnit.mL_Per_s),
        SEDataRequest.create_substance_request("Sodium", "BloodConcentration", unit=MassPerVolumeUnit.g_Per_L),
        SEDataRequest.create_substance_request("Sodium", "Clearance-RenalClearance",
                                               unit=VolumePerTimeMassUnit.mL_Per_min_kg),
        SEDataRequest.create_substance_request("Sodium", "MassInBody", unit=MassUnit.g),
        SEDataRequest.create_liquid_compartment_substance_request("Aorta", "CarbonDioxide", "PartialPressure",
                                                                  unit=PressureUnit.mmHg),
        SEDataRequest.create_liquid_compartment_substance_request("Aorta", "Oxygen", "PartialPressure",
                                                                  unit=PressureUnit.mmHg),
        # ECMO Compartments
        SEDataRequest.create_liquid_compartment_request("ECMOBloodSamplingPort", "InFlow",
                                                        unit=VolumePerTimeUnit.mL_Per_s),
        SEDataRequest.create_liquid_compartment_request("ECMOBloodSamplingPort", "OutFlow",
                                                        unit=VolumePerTimeUnit.mL_Per_s),
        SEDataRequest.create_liquid_compartment_request("ECMOOxygenator", "InFlow", unit=VolumePerTimeUnit.mL_Per_s),
        SEDataRequest.create_liquid_compartment_request("ECMOOxygenator", "OutFlow", unit=VolumePerTimeUnit.mL_Per_s),
        SEDataRequest.create_liquid_compartment_substance_request("ECMOOxygenator", "Sodium", "Concentration",
                                                                  unit=MassPerVolumeUnit.g_Per_dL),
        SEDataRequest.create_liquid_compartment_substance_request("VenaCava", "Sodium", "Concentration",
                                                                  unit=MassPerVolumeUnit.g_Per_dL),
        SEDataRequest.create_liquid_compartment_substance_request("Aorta", "Sodium", "Concentration",
                                                                  unit=MassPerVolumeUnit.g_Per_dL),
        SEDataRequest.create_liquid_compartment_substance_request("ECMOBloodSamplingPort", "CarbonDioxide",
                                                                  "PartialPressure",
                                                                  unit=PressureUnit.mmHg),
        SEDataRequest.create_liquid_compartment_substance_request("ECMOBloodSamplingPort", "Oxygen", "PartialPressure",
                                                                  unit=PressureUnit.mmHg),
        SEDataRequest.create_liquid_compartment_substance_request("ECMOBloodSamplingPort", "Oxygen", "Concentration",
                                                                  unit=MassPerVolumeUnit.g_Per_dL),
        SEDataRequest.create_liquid_compartment_substance_request("ECMOBloodSamplingPort", "CarbonDioxide",
                                                                  "Concentration",
                                                                  unit=MassPerVolumeUnit.g_Per_dL),
        SEDataRequest.create_liquid_compartment_substance_request("ECMOBloodSamplingPort", "Bicarbonate",
                                                                  "Concentration",
                                                                  unit=MassPerVolumeUnit.g_Per_dL),
        SEDataRequest.create_liquid_compartment_substance_request("ECMOOxygenator", "CarbonDioxide", "Concentration",
                                                                  unit=MassPerVolumeUnit.g_Per_dL),
        SEDataRequest.create_liquid_compartment_substance_request("ECMOOxygenator", "Bicarbonate", "Concentration",
                                                                  unit=MassPerVolumeUnit.g_Per_dL),
        SEDataRequest.create_liquid_compartment_substance_request("ECMOOxygenator", "CarbonDioxide",
                                                                  "PartialPressure",
                                                                  unit=PressureUnit.mmHg),
        SEDataRequest.create_liquid_compartment_substance_request("ECMOBloodSamplingPort", "Sodium",
                                                                  "Concentration",
                                                                  unit=MassPerVolumeUnit.g_Per_dL),
        SEDataRequest.create_liquid_compartment_substance_request("ECMOBloodSamplingPort", "Chloride",
                                                                  "Concentration",
                                                                  unit=MassPerVolumeUnit.g_Per_dL),
        SEDataRequest.create_liquid_compartment_request("ECMOOxygenator", "PH"),
        SEDataRequest.create_substance_request("CarbonDioxide", "MassInBody", unit=MassUnit.g),
        SEDataRequest.create_substance_request("Bicarbonate", "MassInBody", unit=MassUnit.g),
        SEDataRequest.create_substance_request("Carbaminohemoglobin", "MassInBody", unit=MassUnit.g),
        SEDataRequest.create_substance_request("OxyCarbaminohemoglobin", "MassInBody", unit=MassUnit.g),
        SEDataRequest.create_liquid_compartment_substance_request("ECMOOxygenator", "Bicarbonate", "Mass",
                                                                  unit=MassUnit.g),
        SEDataRequest.create_liquid_compartment_substance_request("ECMOBloodSamplingPort", "Bicarbonate", "Mass",
                                                                  unit=MassUnit.g),
        SEDataRequest.create_liquid_compartment_substance_request("VenaCava", "Bicarbonate", "Concentration",
                                                                  unit=MassPerVolumeUnit.g_Per_dL),
        SEDataRequest.create_liquid_compartment_substance_request("LeftLegVasculature", "Bicarbonate", "Concentration",
                                                                  unit=MassPerVolumeUnit.g_Per_dL),
        SEDataRequest.create_liquid_compartment_substance_request("LeftLegVasculature", "CarbonDioxide",
                                                                  "Concentration",
                                                                  unit=MassPerVolumeUnit.g_Per_dL),
        SEDataRequest.create_liquid_compartment_substance_request("LeftLegVasculature", "CarbonDioxide",
                                                                  "PartialPressure",
                                                                  unit=PressureUnit.mmHg),
        SEDataRequest.create_liquid_compartment_request("LeftLegVasculature", "PH"),
        SEDataRequest.create_mechanical_ventilator_request("MeanAirwayPressure", unit=PressureUnit.cmH2O),
        SEDataRequest.create_mechanical_ventilator_request("PlateauPressure", unit=PressureUnit.cmH2O),
        SEDataRequest.create_mechanical_ventilator_request("PeakInspiratoryPressure", unit=PressureUnit.cmH2O)
    ]

    # Produce a data manager object with the data request list, and tell it where to save
    data_mgr = SEDataRequestManager(data_requests)
    data_mgr.set_results_filename("./test_results/XCOR/ARDS_ecmo_ventilator{}_{}.csv".format(patient,
                                                                                                         level_severity))

    # Initialize the engine with our configuration. Load patient steady state
    if not pulse.serialize_from_file("./states/{}_ARDS_{}@0s.json".format(patient, level_severity), data_mgr):
        print("Unable to load initial state file")
        return



    dyspnea = SEDyspnea()
    dyspnea.set_comment("Patient's dyspnea occurs")
    dyspnea.get_respiration_rate_severity().set_value(1)
    #dyspnea.get_tidal_volume_severity().set_value(1)
    #dsypnea.get_severity().set_value(1)
    pulse.process_action(dyspnea)
    pulse.advance_time_s(10)

    # Initialize ECMO
    
    cfg = SEECMOConfiguration()
    settings = cfg.get_settings()
    # Attach ECMO from jugular to left leg
    settings.set_inflow_location(eECMO_CannulationLocation.InternalJugular)
    settings.set_outflow_location(eECMO_CannulationLocation.LeftFemoralVein)
    settings.get_oxygenator_volume().set_value(100, VolumeUnit.mL)
    settings.get_transfusion_flow().set_value(4.167, VolumePerTimeUnit.mL_Per_s)
    pulse.process_action(cfg)
    # Advance a little time to get ECMO connected and flowing
    pulse.advance_time_s(10)
    
    # Clear our settings, as we don't need to specify our initial values each time
    settings.clear()
    
    results = pulse.pull_data()
    data_mgr.to_console(results)

    intubation = SEIntubation()
    intubation.set_comment("Patient undergoes intubation of the trachea")
    intubation.set_type(eIntubationType.Tracheal)
    pulse.process_action(intubation)
    pulse.advance_time_s(10)

    # Define and process a ventilator action. Assist control, FiO2=0.8, PEEP=10cmH2O, VT user-defined
    vc_ac = SEMechanicalVentilatorVolumeControl()
    vc_ac.set_connection(eSwitch.On)
    vc_ac.set_mode(eMechanicalVentilator_VolumeControlMode.ContinuousMandatoryVentilation)
    vc_ac.get_flow().set_value(60.0, VolumePerTimeUnit.L_Per_min)
    vc_ac.get_fraction_inspired_oxygen().set_value(0.7)
    vc_ac.get_inspiratory_period().set_value(0.8, TimeUnit.s)
    vc_ac.get_positive_end_expired_pressure().set_value(10, PressureUnit.cmH2O)
    vc_ac.get_respiration_rate().set_value(20, FrequencyUnit.Per_min)
    vc_ac.get_tidal_volume().set_value(VoT, VolumeUnit.mL)


    pulse.process_action(vc_ac)
    
    
    for i in range(900*50*2):

        settings.get_substance_concentration("Bicarbonate").get_concentration().set_value(
            list(results)[34] * 0.2, MassPerVolumeUnit.g_Per_dL)

        pulse.process_action(cfg)
        pulse.advance_time()

        results = pulse.pull_data()
    
    results = pulse.pull_data()
    data_mgr.to_console(results)

    #print()
    #print("Plateau Pressure: ", list(results)[53])
    #print("Mean Airway Pressure: ", list(results)[52])
    #print("pCO2: ", list(results)[21])
    #print("pO2: ", list(results)[22])
    #print("Respiration Rate: ", list(results)[10])
    #print("pH: ", list(results)[1])
    #print("O2 Saturation: ", list(results)[7])

# only need to uncomment if running individual file

if __name__ == '__main__':
    # # Simulate across all 10 patients, giving each severities of 0.3, 0.6, and 0.9
    # Default patients: names = ["Cynthia", "Gus", "Joel", "Nathan", "Rick", "Hassan", "Soldier", "Jeff", "Carol", "Jane"]
    # weights = [100, 167, 177, 177, 146, 187, 177, 187, 116, 100]
    severities = [0.9]
    processes = []
    names = ["Adam", "Bert", "Chris", "David", "Elie", "Anna", "Bella", "Charlotte", "Dorothy", "Emma"]
    weights = [161, 165, 171, 136, 156, 116, 126, 116, 121, 121]
    # Give each patient VT
    VT = [w / 2.20462 * 4 for w in weights]

# Add a new thread for every patient at each severity, start each thread, and join them
    for i, name in enumerate(names):
        for severity in severities:
            processes.append(mp.Process(None, ARDS_ecmo_ventilator, args=(name, severity, VT[i])))

    for p in processes:
        p.start()

    for p in processes:
        p.join()
