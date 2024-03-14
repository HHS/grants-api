/* eslint-disable testing-library/prefer-screen-queries */
import { test, expect } from "@playwright/test";

test.beforeEach(async ({ page }) => {
  await page.goto("/research");
});

test.afterEach(async ({ context }) => {
  await context.close();
});

test("has title", async ({ page }) => {
  await expect(page).toHaveTitle("Research | Simpler.Grants.gov");
});

test("can navigate to /newsletter", async ({ page }) => {
  await page
    .getByRole("link", { name: /sign up for project updates/i })
    .getByTestId("button")
    .click();

  await expect(page).toHaveURL(/newsletter/);
});
