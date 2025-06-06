# Gunicorn configuration for Astrological Application
import multiprocessing
import os

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Environment-based configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
WORKER_COUNT = int(os.getenv("WORKER_COUNT", "0"))  # 0 = auto-calculate

def get_optimal_workers():
    """Calculate optimal worker count based on environment and system specs"""
    cpu_count = multiprocessing.cpu_count()  # 14 cores on your system

    if WORKER_COUNT > 0:
        return WORKER_COUNT  # Manual override

    if ENVIRONMENT == "development":
        return 1  # Start minimal for development
    elif ENVIRONMENT == "testing":
        return 2  # Light testing load
    elif ENVIRONMENT == "staging":
        return max(2, cpu_count // 2)  # 7 workers for staging
    else:  # production
        # For CPU-bound apps: (2 * cores) + 1, but cap at reasonable limit
        return min(cpu_count * 2 + 1, 20)  # Max 20 workers to avoid memory issues

# Worker processes
workers = get_optimal_workers()
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000

# Request lifecycle management
max_requests = 1000  # Restart worker after 1000 requests (prevents memory leaks)
max_requests_jitter = 50  # Add randomness to prevent thundering herd

# Timeout settings (important for compute-heavy astrological calculations)
if ENVIRONMENT == "development":
    timeout = 300  # 5 minutes for debugging
    graceful_timeout = 60
else:
    timeout = 120  # 2 minutes for complex calculations
    graceful_timeout = 30

keepalive = 2

# Logging configuration
accesslog = "-"  # Log to stdout
errorlog = "-"   # Log to stderr
loglevel = "debug" if ENVIRONMENT == "development" else "info"

# Enhanced access log format for monitoring
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s µs'

# Process naming
proc_name = f"astrology_api_{ENVIRONMENT}"

# Server mechanics
daemon = False
pidfile = None
user = None
group = None
tmp_upload_dir = None

# Performance tuning
preload_app = True  # Load application before forking workers (saves memory)
enable_stdio_inheritance = True

# Memory management (conservative for astrological calculations)
if ENVIRONMENT == "development":
    max_worker_memory = 512 * 1024 * 1024  # 512MB per worker for development
else:
    max_worker_memory = 1024 * 1024 * 1024  # 1GB per worker for production

# Development-specific settings
if ENVIRONMENT == "development":
    reload = True
    reload_extra_files = ["src/", "templates/", "static/"]
else:
    reload = False

# Print configuration summary
print("🚀 Gunicorn Configuration Summary:")
print(f"   Environment: {ENVIRONMENT}")
print(f"   Workers: {workers}")
print(f"   CPU Cores: {multiprocessing.cpu_count()}")
print(f"   Memory per worker: {max_worker_memory // (1024*1024)}MB")
print(f"   Timeout: {timeout}s")
print(f"   Reload: {reload}")
