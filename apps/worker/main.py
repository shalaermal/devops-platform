import time
import os
import logging

# Konfigurojmë logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def process_stats():
    """
    Në realitet kjo funksion do të:
    - Lidhej me database
    - Merrte statistikat e clicks
    - I dërgonte te Prometheus/Grafana
    Tani vetëm simulojmë punën
    """
    logger.info("Worker: Duke procesuar statistikat...")
    logger.info("Worker: Statistikat u procesuan me sukses")

def main():
    logger.info("Worker service startoi!")
    
    while True:
        try:
            process_stats()
        except Exception as e:
            logger.error(f"Worker gabim: {e}")
        
        # Prit 30 sekonda para se të procesojë sërisht
        logger.info("Worker: Duke pritur 30 sekonda...")
        time.sleep(30)

if __name__ == "__main__":
    main()