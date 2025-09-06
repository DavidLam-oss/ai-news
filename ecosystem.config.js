module.exports = {
  apps: [
    {
      name: 'ai-news-api',
      script: 'api/server.py',
      interpreter: 'python',
      instances: 1,
      exec_mode: 'fork',
      env: {
        NODE_ENV: 'production',
        HOST: '0.0.0.0',
        PORT: 8000,
        DEBUG: 'False',
        LOG_LEVEL: 'INFO'
      },
      env_production: {
        NODE_ENV: 'production',
        HOST: '0.0.0.0',
        PORT: 8000,
        DEBUG: 'False',
        LOG_LEVEL: 'INFO'
      },
      log_file: './logs/api.log',
      out_file: './logs/api-out.log',
      error_file: './logs/api-error.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      max_memory_restart: '1G',
      restart_delay: 4000,
      max_restarts: 10,
      min_uptime: '10s'
    },
    {
      name: 'ai-news-scheduler',
      script: 'crawler/main.py',
      interpreter: 'python',
      args: '--mode schedule',
      instances: 1,
      exec_mode: 'fork',
      env: {
        NODE_ENV: 'production',
        HOST: '0.0.0.0',
        PORT: 8000,
        DEBUG: 'False',
        LOG_LEVEL: 'INFO'
      },
      env_production: {
        NODE_ENV: 'production',
        HOST: '0.0.0.0',
        PORT: 8000,
        DEBUG: 'False',
        LOG_LEVEL: 'INFO'
      },
      log_file: './logs/scheduler.log',
      out_file: './logs/scheduler-out.log',
      error_file: './logs/scheduler-error.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      max_memory_restart: '1G',
      restart_delay: 4000,
      max_restarts: 10,
      min_uptime: '10s'
    }
  ]
};
