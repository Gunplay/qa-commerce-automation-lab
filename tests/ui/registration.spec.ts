import { test, expect } from '@playwright/test'
import { randomUUID } from 'node:crypto'
import { RegistrationPage } from '../pages/registrationPage'

test('new customer can register', async ({ page }) => {
  const email = `qa-${randomUUID()}@example.com`
  const registrationPage = new RegistrationPage(page)

  await registrationPage.open()
  await registrationPage.fillRegForm('Roman', 'Bot', email, 'QaTest2026!Example')
  await registrationPage.submit()

  await expect(page.getByTestId('overview-page-wrapper')).toBeVisible()
  await expect(page.getByTestId('welcome-message')).toHaveText('Hello Roman')
  await expect(page.getByTestId('customer-email')).toHaveText(email)

  await page.reload()

  await expect(page.getByTestId('welcome-message')).toHaveText('Hello Roman')
  await expect(page.getByTestId('customer-email')).toHaveText(email)
})


test('customer cannot register with empty required fields', async ({ page }) => {

  const registrationPage = new RegistrationPage(page);

  await registrationPage.open();
  await registrationPage.submit();

  await expect(registrationPage.firstNameInput).toBeFocused();

  const valueMissing = await registrationPage.firstNameInput.evaluate(
    (input: HTMLInputElement) => input.validity.valueMissing
  );

  expect(valueMissing).toBe(true);

})
