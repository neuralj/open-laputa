import { test, expect } from "bun:test";
import { run } from "./index";

test("smoke test", async () => {
  await expect(run()).resolves.toBeUndefined();
});
