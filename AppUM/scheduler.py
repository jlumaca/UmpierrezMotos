from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from .functions import mi_funcion_diaria

def iniciar_scheduler():
    scheduler = BackgroundScheduler()
    
    # Programar la función para que se ejecute todos los días a las 9 AM
    scheduler.add_job(mi_funcion_diaria, 
                      trigger=CronTrigger(hour=6, minute=00), 
                      id="mi_funcion_diaria", 
                      replace_existing=True)
    
    scheduler.start()
    print("Scheduler iniciado. Mi función diaria programada para las 9 AM.")