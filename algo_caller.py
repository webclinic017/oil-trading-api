

import trader  
from apscheduler.schedulers.blocking import BlockingScheduler


sched = BlockingScheduler()

@sched.scheduled_job('interval', day=10)
trader.main()

sched.start()