import sys
import os
# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import from worker.consumer
from worker.consumer import celery

if __name__ == '__main__':
    celery.worker_main(['worker', '--loglevel=info', '-Q', 'item_queue', '--pool=solo'])