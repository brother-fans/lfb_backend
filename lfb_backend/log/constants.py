
TIME_FORMAT = '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>'
LEVEL_FORMAT = '<level>{level: <8}</level>}'
MSG_FORMAT = '<level>{message}</level>'
PROCESS_FORMAT = '{process.id}'
THREAD_FORMAT = '{thread.id}'
STDOUT_FORMAT = f'{TIME_FORMAT} | {LEVEL_FORMAT} | {PROCESS_FORMAT} | {THREAD_FORMAT} | {MSG_FORMAT}'
