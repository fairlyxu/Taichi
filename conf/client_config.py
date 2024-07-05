# import os

# 基础配置，使用继承的方式
class ClientBaseConfig:
    DOMAIN_NAME = 'qiniu.aigcute.com'
    BUCKED_NAME = 'aigcute'
    ACCE_KEY = 'vh7avAFMeC1WefXJjiU11Hzb90ZyLi_YM5cE88uw'
    SECR_KEY = 'STOqHj_jpEjG01_Q-YfH8eGpLqtE3s3gBQMP7n6A'
    SERVER_HOST = 'http://101.132.254.70:5002/'




config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}

