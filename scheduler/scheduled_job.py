import schedule
import time
from service import service


def job():
    #service.do_the_job_for_one_user('54941759440')
    service.do_the_job_for_one_user('test')


if __name__ == "__main__":
    schedule.every(5).minutes.do(job)
    while 1:
        schedule.run_pending()
        time.sleep(1)