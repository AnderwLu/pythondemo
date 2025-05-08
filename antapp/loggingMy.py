import logging
from pathlib import Path

# 创建logs目录
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "openai_api.log"

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# 创建logger实例
logger = logging.getLogger(__name__) 