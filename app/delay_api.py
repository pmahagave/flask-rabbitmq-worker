import threading
import time
import requests
from flask import Blueprint, request, jsonify

bp = Blueprint('delay', __name__)

@bp.route('/delay', methods=['GET'])
def delay_endpoint():
    try:
        delay_value = int(request.args.get('delay_value'))
    except (TypeError, ValueError):
        return jsonify({'error': 'delay_value must be an integer'}), 400
    
    if delay_value < 0 or delay_value > 10:
        return jsonify({'error': 'delay_value must be between 0 and 10'}), 400
    
    url = f"https://httpbin.org/delay/{delay_value}"
    results = []
    errors = []
    lock = threading.Lock()
    
    def fetch():
        try:
            resp = requests.get(url, timeout=30)
            with lock:
                results.append(resp.status_code)
        except Exception as e:
            with lock:
                errors.append(str(e))
    
    start_time = time.time()
    threads = []
    
    for _ in range(5):
        t = threading.Thread(target=fetch)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    end_time = time.time()
    time_taken = round(end_time - start_time, 2)
    
    return jsonify({'time_taken': time_taken}), 200