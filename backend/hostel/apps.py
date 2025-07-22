from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from .cron import cancel_expired_bookings, mark_expired_payment, create_db_dump_and_send_email, extend_payment_expiry

class HostelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hostel'
    icon = "fa-solid fa-hotel"
    divider_title = 'Manage Hostels'    
    
    scheduler_started = False

    def ready(self):
        import os
        if os.environ.get('RUN_MAIN', None) != 'true' and not HostelConfig.scheduler_started:
            HostelConfig.scheduler_started = True
            scheduler = BackgroundScheduler()
            scheduler.add_job(
                cancel_expired_bookings,
                'interval',
                minutes=10,
                next_run_time=timezone.now()
            )

            scheduler.add_job(
                create_db_dump_and_send_email,
                'cron',
                hour=1,
                next_run_time=timezone.now()
            )

            # scheduler.add_job(
            #     mark_expired_payment,
            #     'cron',
            #     hour=0,
            #     minute=0,
            #     next_run_time=timezone.now()
            # )

            scheduler.add_job(
                extend_payment_expiry,
                'cron',
                minute=0,
                hour=9,
                next_run_time=timezone.now()
            )

            scheduler.start()