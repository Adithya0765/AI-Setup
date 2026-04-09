"""Logging utilities"""

import logging
from pathlib import Path
from datetime import datetime


def setup_logger(workspace: Path) -> logging.Logger:
    """Setup NEXUS logger"""
    
    log_dir = workspace / ".nexus" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / f"nexus_{datetime.now().strftime('%Y%m%d')}.log"
    
    logger = logging.getLogger("nexus")
    logger.setLevel(logging.INFO)
    
    # File handler
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger
