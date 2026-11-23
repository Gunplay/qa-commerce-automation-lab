import type { Page } from '@playwright/test'

export class ProductPage {
    readonly page: Page

    constructor(page: Page) {
        this.page = page
    }

    async open(handle: string) {
        await this.page.goto(`/dk/products/${handle}`)
    }

    get productTitle() {
        return this.page.getByRole('heading', { level: 1 })
    }
}