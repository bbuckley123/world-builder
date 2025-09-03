const levelOrder = { debug: 0, info: 1, warn: 2, error: 3 } as const;
type Level = keyof typeof levelOrder;

const currentLevel = (import.meta.env.VITE_LOG_LEVEL || "info").toLowerCase() as Level;

function shouldLog(level: Level): boolean {
  return levelOrder[level] >= levelOrder[currentLevel];
}

export const logger = {
  debug: (msg: any, ...args: any[]) => {
    if (shouldLog("debug")) console.debug(msg, ...args);
  },
  info: (msg: any, ...args: any[]) => {
    if (shouldLog("info")) console.info(msg, ...args);
  },
  warn: (msg: any, ...args: any[]) => {
    if (shouldLog("warn")) console.warn(msg, ...args);
  },
  error: (msg: any, ...args: any[]) => {
    if (shouldLog("error")) console.error(msg, ...args);
  },
};

