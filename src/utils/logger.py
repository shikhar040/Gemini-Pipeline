#!/usr/bin/env python3
"""
Logging utility for the auto-healing pipeline
"""

import logging
import sys

def setup_logger(name=__name__, level=logging.INFO):
    """Setup and return a logger with consistent formatting"""
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger