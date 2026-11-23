import { test, expect } from '@playwright/test'
import { CatalogPage } from '../pages/CatalogPage'


test.describe('Store catalog', async () => {


  test('store page displays products', async ({ page }) => {
    const catalogPage = new CatalogPage(page)
    await catalogPage.open()

    await expect(
      page.getByRole('heading', { name: 'All products' })
    ).toBeVisible()

    await expect(
      page.getByText('Medusa T-Shirt', { exact: true })
    ).toBeVisible()
  })

})
