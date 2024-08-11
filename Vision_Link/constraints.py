# constraints.py
def engine_oil_pressure(value):
    if value < 25 or value > 65:
        return 1.0  # High probability of failure
    elif value < 30 or value > 60:
        return 0.8  # Medium probability of failure
    else:
        return 0.2  # Low probability of failure

def engine_speed(value):
    if value > 1800:
        return 0.7  # Medium probability of failure
    else:
        return 0.2  # Low probability of failure

def engine_temperature(value):
    if value > 105:
        return 1.0  # High probability of failure
    else:
        return 0.7  # High probability of failure

def brake_control(value):
    if value < 1:
        return 1.0  # High probability of failure
    else:
        return 0.5  # Medium probability of failure

def transmission_pressure(value):
    if  value > 450:
        return 1.0  # High probability of failure
    elif value > 250 and value < 400:
        return 0.8  # Medium probability of failure
    else:
        return 0.3  # Low probability of failure

def pedal_sensor(value):
    if value > 4.7:
        return 1.0  # High probability of failure
    else:
        return 0.3  # Low probability of failure

def water_fuel(value):
    if value > 1800:
        return 1.0  # High probability of failure
    else:
        return 0.8  # High probability of failure

def fuel_level(value):
    if value < 1:
        return 1.0  # High probability of failure
    else:
        return 0.5  # Low probability of failure

def fuel_pressure(value):
    if value < 35 or value > 65:
        return 1.0  # High probability of failure
    else:
        return 0.5  # Low probability of failure

def fuel_temperature(value):
    if value > 400:
        return 1.0  # High probability of failure
    else:
        return 0.7  # High probability of failure

def system_voltage(value):
    if value < 12.0 or value > 15.0:
        return 1.0  # High probability of failure
    else:
        return 0.7  # High probability of failure

def exhaust_gas_temperature(value):
    if value > 365:
        return 1.0  # High probability of failure
    else:
        return 0.8  # High probability of failure

def hydraulic_pump_rate(value):
    if value > 125:
        return 0.8  # Medium probability of failure
    else:
        return 0.5  # Medium probability of failure

def air_filter_pressure_drop(value):
    if value < 20:
        return 0.8  # Medium probability of failure
    else:
        return 0.5  # Medium probability of failure

# Example usage
def get_failure_probability(parameters):
    return {
        "engine_oil_pressure": engine_oil_pressure(parameters['engine_oil_pressure']),
        "engine_speed": engine_speed(parameters['engine_speed']),
        "engine_temperature": engine_temperature(parameters['engine_temperature']),
        "brake_control": brake_control(parameters['brake_control']),
        "transmission_pressure": transmission_pressure(parameters['transmission_pressure']),
        "pedal_sensor": pedal_sensor(parameters['pedal_sensor']),
        "water_fuel": water_fuel(parameters['water_fuel']),
        "fuel_level": fuel_level(parameters['fuel_level']),
        "fuel_pressure": fuel_pressure(parameters['fuel_pressure']),
        "fuel_temperature": fuel_temperature(parameters['fuel_temperature']),
        "system_voltage": system_voltage(parameters['system_voltage']),
        "exhaust_gas_temperature": exhaust_gas_temperature(parameters['exhaust_gas_temperature']),
        "hydraulic_pump_rate": hydraulic_pump_rate(parameters['hydraulic_pump_rate']),
        "air_filter_pressure_drop": air_filter_pressure_drop(parameters['air_filter_pressure_drop']),
    }
