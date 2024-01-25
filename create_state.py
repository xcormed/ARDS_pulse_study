from pulse.engine.PulseEngine import PulseEngine
from pulse.cdm.engine import SEDataRequest, SEDataRequestManager
from pulse.cdm.patient import eSex, SEPatient, SEPatientConfiguration
from pulse.cdm.scalars import FrequencyUnit, PressureUnit, \
                              TimeUnit, VolumeUnit, VolumePerTimeUnit, MassPerVolumeUnit, MassUnit, LengthUnit
def Create_state(name):
    pulse = PulseEngine()
    pulse.set_log_filename("./test_results/howto/Create_state_{}.py.log".format(name))
    pulse.log_to_console(True)
    data_requests = [
        SEDataRequest.create_physiology_request("HeartRate", unit=FrequencyUnit.Per_min),
        SEDataRequest.create_physiology_request("ArterialPressure", unit=PressureUnit.mmHg),
        SEDataRequest.create_physiology_request("MeanArterialPressure", unit=PressureUnit.mmHg),
        SEDataRequest.create_physiology_request("SystolicArterialPressure", unit=PressureUnit.mmHg),
        SEDataRequest.create_physiology_request("DiastolicArterialPressure", unit=PressureUnit.mmHg),
        SEDataRequest.create_physiology_request("OxygenSaturation"),
        SEDataRequest.create_physiology_request("EndTidalCarbonDioxidePressure", unit=PressureUnit.mmHg),
        SEDataRequest.create_physiology_request("RespirationRate", unit=FrequencyUnit.Per_min),
        SEDataRequest.create_physiology_request("CardiacOutput", unit=VolumePerTimeUnit.L_Per_min),
        SEDataRequest.create_physiology_request("BloodVolume", unit=VolumeUnit.mL)
    ]

    data_req_mgr = SEDataRequestManager(data_requests)
    data_req_mgr.set_results_filename("./test_results/howto/Create_state_{}.py.csv".format(name))

    cfg = SEPatientConfiguration()
    #cfg.set_data_root_dir(r"C:\Users\14438\Desktop\Programming\builds\pulse-engine\install\bin\states")

    patient = cfg.get_patient()
    patient.set_name(name)
    patient.set_sex(eSex.Male)
    patient.get_age().set_value(27, TimeUnit.yr)
    patient.get_weight().set_value(187, MassUnit.lb)
    patient.get_height().set_value(70, LengthUnit.inch)
    patient.get_body_fat_fraction().set_value(0.222)
    patient.get_systolic_arterial_pressure_baseline().set_value(107, PressureUnit.mmHg)
    patient.get_diastolic_arterial_pressure_baseline().set_value(60, PressureUnit.mmHg)
    patient.get_heart_rate_baseline().set_value(106, FrequencyUnit.Per_min)
    patient.get_respiration_rate_baseline().set_value(20, FrequencyUnit.Per_min)
    pulse.process_action(cfg)

    #if (!pulse.InitializeEngine(cfg, new SEDataRequestManager())):
     #   Console.WriteLine("Error Initializing Pulse!")
    if not pulse.initialize_engine(cfg, data_req_mgr):
        print("Unable to load stabilize engine")
        return
    pulse.serialize_to_file("./states/{}@0s.json".format(name))

if __name__ == '__main__':
    # Input patient name
    Create_state("Adam")