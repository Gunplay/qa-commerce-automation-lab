import { test, expect } from '@playwright/test'

test('store page displays products', async ({ page }) => {
  await page.goto('/de/store')

  await expect(
    page.getByRole('heading', { name: 'All products' })
  ).toBeVisible()

  await expect(
    page.getByText('Medusa T-Shirt', { exact: true })
  ).toBeVisible()
})
