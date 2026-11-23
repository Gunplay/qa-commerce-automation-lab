// Імпортуємо лише тип Page. TypeScript використовує його для перевірки
// типів; цей імпорт не потрапляє у виконуваний JavaScript.
import type { Page } from '@playwright/test'

// Оголошуємо клас CatalogPage.
// export дозволяє імпортувати його через import { CatalogPage }.
export class CatalogPage {
  // Оголошуємо поле екземпляра з назвою page та типом Page.
  // readonly дозволяє присвоєння під час ініціалізації або в конструкторі,
  // але забороняє подальше переприсвоєння засобами TypeScript.
  // Методи самого об’єкта Page залишаються доступними.
  readonly page: Page

  // Конструктор викликається автоматично оператором new:
  // new CatalogPage(page).
  // Параметр page повинен відповідати типу Page.
  constructor(page: Page) {
    // this — поточний екземпляр CatalogPage.
    // this.page — його поле; page — параметр конструктора.
    // Присвоюємо посилання на переданий об’єкт Page.
    // Нова вкладка або копія об’єкта тут не створюється.
    this.page = page
  }

  // Оголошуємо метод екземпляра open без параметрів.
  // async означає, що метод повертає Promise.
  // Оскільки значення не повертається, виведений тип — Promise<void>.
  async open() {
    // Викликаємо метод goto об’єкта Page, збереженого в this.page.
    // Відносна адреса обчислюється від baseURL у playwright.config.ts.
    // await призупиняє виконання open до завершення Promise від goto.
    // За замовчуванням goto очікує подію load.
    // Якщо Promise відхилено, помилка передається тому, хто викликав open.
    await this.page.goto('de/store')
  }
}