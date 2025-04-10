import os

class Config:
    """基礎配置類"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-please-change')
    
    # Firebase 配置
    FIREBASE_CREDENTIALS = os.environ.get('FIREBASE_CREDENTIALS')
    
    # 其他通用配置
    TEMPLATES_AUTO_RELOAD = True

class DevelopmentConfig(Config):
    """開發環境配置"""
    DEBUG = True
    # 開發環境特定配置
    
class ProductionConfig(Config):
    """生產環境配置"""
    # 確保使用強力的密鑰
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # 生產環境特定配置
    
class TestingConfig(Config):
    """測試環境配置"""
    TESTING = True
    
# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# 獲取當前配置
def get_config():
    env = os.environ.get('FLASK_ENV', 'default')
    return config[env] 