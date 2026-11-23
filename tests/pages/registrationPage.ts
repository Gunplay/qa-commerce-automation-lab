import type { Page } from '@playwright/test'

export class RegistrationPage {

    readonly page: Page

    constructor(page: Page) {
        this.page = page
    }

    get firstNameInput() {
        return this.page
            .getByTestId('register-page')
            .getByTestId('first-name-input')
    }

    async open() {
        await this.page.goto('/dk/account')
        await this.page
            .getByRole('button', { name: 'Join us', exact: true })
            .click()
    }

    async fillRegForm(firstname: string, lastname: string, email: string, password: string) {

        const form = this.page.getByTestId('register-page')

        await form.getByTestId('first-name-input').fill(firstname)
        await form.getByTestId('last-name-input').fill(lastname)
        await form.getByTestId('email-input').fill(email)
        await form.getByTestId('password-input').fill(password)
    }

    async submit() {
        await this.page
            .getByTestId('register-page')
            .getByTestId('register-button')
            .click()
    }

}