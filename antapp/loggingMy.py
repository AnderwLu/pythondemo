import logging
import sys
from pathlib import Path

# 创建logs目录
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "openai_api.log"

# 日志是否已初始化的标志
_log_initialized = False

def setup_logging(level=logging.INFO):
    """
    设置项目级别的日志配置
    
    Args:
        level: 日志级别，默认为INFO
    """
    global _log_initialized
    
    if _log_initialized:
        return
    
    # 配置日志
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # 设置标志为已初始化
    _log_initialized = True
    
    # 获取根日志器并记录初始化信息
    root_logger = logging.getLogger()
    root_logger.info("日志系统初始化完成，级别: %s", 
                    {10: "DEBUG", 20: "INFO", 30: "WARNING", 40: "ERROR", 50: "CRITICAL"}.get(level, str(level)))

def get_logger(name):
    """
    获取指定名称的logger
    
    Args:
        name: logger名称，通常使用模块名称
        
    Returns:
        Logger: 配置好的logger实例
    """
    # 确保日志已初始化
    if not _log_initialized:
        setup_logging()
    
    return logging.getLogger(name)

# 在模块导入时自动初始化日志系统
setup_logging()

# 创建默认logger实例
logger = get_logger(__name__) 