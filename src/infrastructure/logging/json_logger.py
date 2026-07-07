import logging
import json
from datetime import datetime
from typing import Any, Dict, Optional

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "component": record.name,
            "message": record.getMessage(),
        }
        
        # Inject standard operational fields if present in `extra`
        for key in ["correlation_id", "conversation_id", "request_id", "duration", "status"]:
            if hasattr(record, key):
                log_record[key] = getattr(record, key)
                
        # Include exception traceback if present
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_record)

def get_json_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = JSONFormatter()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
