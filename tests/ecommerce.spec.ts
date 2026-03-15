import { test, expect } from '@playwright/test';

let username = '';

test.describe.serial('E-commerce Application Tests', () => {
  // Test 1: Homepage loads and shows product-card visible
  test('homepage loads and shows product-card visible', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('.product-card')).toBeVisible();
  });

  // Test 2: User can register - fill register form with unique username, submit, redirect to /
  test('user can register', async ({ page }) => {
    const uniqueUsername = `testuser_${Date.now()}`;
    username = uniqueUsername;
    await page.goto('/register');
    await page.fill('[name="username"]', username);
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL('/');
  });

  // Test 3: User can login - fill login form, submit, nav-logout visible
  test('user can login', async ({ page }) => {
    await page.goto('/login');
    await page.fill('[name="username"]', username);
    await page.fill('[name="password"]', 'testpassword123');
    await page.click('button[type="submit"]');
    await expect(page.locator('.nav-logout')).toBeVisible();
  });

  // Test 4: Add to cart - login, click add-to-cart-btn, goto /cart, cart-item visible
  test('add to cart', async ({ page }) => {
    await page.goto('/');
    await page.click('.add-to-cart-btn');
    await page.goto('/cart');
    await expect(page.locator('.cart-item')).toBeVisible();
  });

  // Test 5: Empty cart - fresh login, goto /cart, empty text visible
  test('empty cart', async ({ page }) => {
    const freshUsername = `freshuser_${Date.now()}`;
    await page.goto('/login');
    await page.fill('[name="username"]', freshUsername);
    await page.fill('[name="password"]', 'testpassword123');
    await page.click('button[type="submit"]');
    await page.goto('/cart');
    await expect(page.locator('.empty')).toContainText('empty');
  });

  // Test 6: Product detail - goto /, click product name, product-detail-name visible
  test('product detail', async ({ page }) => {
    await page.goto('/');
    const productName = await page.locator('.product-card').first().textContent();
    if (productName) {
      await page.click('.product-card');
      await expect(page.locator('.product-detail-name')).toContainText(productName);
    }
  });
});
