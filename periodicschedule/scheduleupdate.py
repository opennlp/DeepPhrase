import schedule


def update_scheduler(function_to_execute, time_quantum=360, time_quantum_unit='minutes'):
    if time_quantum_unit.lower() == 'minutes':
        schedule.every(time_quantum).minutes.do(function_to_execute)
    elif time_quantum_unit.lower() == 'hours':
        schedule.every(time_quantum).hours.do(function_to_execute)
    else:
        schedule.every(time_quantum).seconds.do(function_to_execute)
    while True:
        schedule.run_pending()
