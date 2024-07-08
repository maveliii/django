from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from .jobs import send_alert_mails

def start():
    scheduler = BackgroundScheduler()
    # Schedule to run every day at 8:00 AM
    scheduler.add_job(send_alert_mails, CronTrigger(hour=15, minute=32))
    scheduler.start()

    print('Scheduler started, sending emails daily at 8:00 AM')