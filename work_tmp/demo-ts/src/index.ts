export async function run(name = "world"): Promise<void> {
  console.log(`Hello, ${name}`);
}

// 直接运行文件时作为入口执行
if (import.meta.main) {
  const arg = Bun.argv[2];
  run(arg).catch((error) => {
    console.error("Fatal error:", error);
    process.exitCode = 1;
  });
}
