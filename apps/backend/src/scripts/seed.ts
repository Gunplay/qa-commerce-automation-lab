/**
 * ДЛЯ ЧОГО ЦЕЙ ФАЙЛ
 * seed.ts наповнює базу початковими даними навчального магазину.
 * Наприклад: у новій БД ще немає товарів — цей скрипт додає їх,
 * щоб магазин мав що показати, а автотести мали з чим працювати.
 * Це скрипт підготовки даних, а не тест і не сторінка магазину.
 *
 * ЩО ВІН РОБИТЬ
 * 1. Отримує сервіси Medusa для роботи з базою через container.
 * 2. Знаходить або створює канал продажів Default Sales Channel.
 * 3. Знаходить або створює регіон Europe: валюта EUR, перелік країн.
 * 4. Знаходить або створює склад і для нового складу додає зв'язок із каналом.
 * 5. Створює publishable key Storefront, якщо такого ключа ще немає.
 *    Цей ключ потрібний магазину для запитів до Store API backend.
 * 6. Додає відсутні категорії й робить перелічені категорії активними.
 * 7. Додає відсутні товари з цінами, зображеннями й розмірами S, M, L.
 *    Наявність товару визначає за handle — його текстовим ідентифікатором.
 *
 * ЯК ЗАПУСТИТИ
 * Команди виконуються з кореня qa-commerce-automation-lab.
 * Спочатку потрібні запущена PostgreSQL, DATABASE_URL і створена схема БД.
 * npm run backend:seed — запустити лише цей скрипт.
 * npm run db:setup — спочатку застосувати міграції, потім запустити seed.
 * Міграції створюють/оновлюють структуру таблиць, seed додає дані в них.
 * Звичайне збереження цього файла не запускає seed.
 *
 * ЯК ЗМІНИТИ ДАНІ
 * Країни нового регіону: масив countries; наприклад, "dk" — Данія.
 * Категорії: categoryDefinitions. Товари: productDefinitions.
 * Зміна countries спрацює під час створення нового регіону Europe.
 * Якщо Europe вже є в БД, цей скрипт не оновлює його країни.
 * Наявні товари він також не оновлює, навіть якщо змінити їх опис тут.
 *
 * У CI цей скрипт готує початкові дані в новій тестовій БД перед тестами.
 * Локально він змінює ту БД, на яку вказує DATABASE_URL; це не очищення БД.
 */
import type { ExecArgs } from "@medusajs/framework/types"
import { ContainerRegistrationKeys, Modules } from "@medusajs/framework/utils"
import {
  createApiKeysWorkflow,
  createProductCategoriesWorkflow,
  createProductsWorkflow,
  createRegionsWorkflow,
  createSalesChannelsWorkflow,
  createStockLocationsWorkflow,
  linkSalesChannelsToApiKeyWorkflow,
  linkSalesChannelsToStockLocationWorkflow,
  updateProductCategoriesWorkflow,
} from "@medusajs/medusa/core-flows"

export default async function seed({ container }: ExecArgs) {
  const logger = container.resolve(ContainerRegistrationKeys.LOGGER)
  const salesChannelModuleService = container.resolve(Modules.SALES_CHANNEL)
  const storeModuleService = container.resolve(Modules.STORE)
  const regionModuleService = container.resolve(Modules.REGION)
  const stockLocationModuleService = container.resolve(Modules.STOCK_LOCATION)
  const apiKeyModuleService = container.resolve(Modules.API_KEY)
  const productModuleService = container.resolve(Modules.PRODUCT)
  const query = container.resolve(ContainerRegistrationKeys.QUERY)

  logger.info("Seeding store data...")

  // 1. Store
  const [store] = await storeModuleService.listStores()

  // 2. Sales channel
  let defaultSalesChannel = await salesChannelModuleService.listSalesChannels({
    name: "Default Sales Channel",
  })

  if (!defaultSalesChannel.length) {
    const { result } = await createSalesChannelsWorkflow(container).run({
      input: {
        salesChannelsData: [{ name: "Default Sales Channel" }],
      },
    })
    defaultSalesChannel = result
  }

  // 3. Region (EU)
  let [region] = await regionModuleService.listRegions({ name: "Europe" })

  if (!region) {
    const { result: regionResult } = await createRegionsWorkflow(container).run({
      input: {
        regions: [
          {
            name: "Europe",
            currency_code: "eur",
            countries: ["de", "fr", "es", "it", "dk"],
            payment_providers: ["pp_system_default"],
          },
        ],
      },
    })
    region = regionResult[0]
    logger.info(`Region created: ${region.name}`)
  }

  // 4. Stock location
  let [stockLocation] = await stockLocationModuleService.listStockLocations({
    name: "European Warehouse",
  })

  if (!stockLocation) {
    const { result: stockLocationResult } = await createStockLocationsWorkflow(
      container
    ).run({
      input: {
        locations: [
          {
            name: "European Warehouse",
            address: {
              city: "Berlin",
              country_code: "DE",
              address_1: "",
            },
          },
        ],
      },
    })
    stockLocation = stockLocationResult[0]

    await linkSalesChannelsToStockLocationWorkflow(container).run({
      input: {
        id: stockLocation.id,
        add: [defaultSalesChannel[0].id],
      },
    })
  }

  // 5. Publishable API Key (для storefront)
  const apiKeys = await apiKeyModuleService.listApiKeys({
    title: "Storefront",
  })

  if (!apiKeys.some((apiKey) => apiKey.type === "publishable")) {
    const { result } = await createApiKeysWorkflow(container).run({
      input: {
        api_keys: [
          {
            title: "Storefront",
            type: "publishable",
            created_by: "seed",
          },
        ],
      },
    })

    await linkSalesChannelsToApiKeyWorkflow(container).run({
      input: {
        id: result[0].id,
        add: [defaultSalesChannel[0].id],
      },
    })
  }

  // 6. Product categories
  const categoryDefinitions = [
    { name: "Apparel", handle: "apparel", description: "Everyday essentials", is_active: true },
    { name: "Footwear", handle: "footwear", description: "Comfortable steps", is_active: true },
    { name: "Accessories", handle: "accessories", description: "Finishing touches", is_active: true },
    { name: "Home & Lifestyle", handle: "home-lifestyle", description: "Daily favorites", is_active: true },
  ]
  const { data: categoryData } = await query.graph({
    entity: "product_category",
    fields: ["id", "handle"],
  })
  let categories = categoryData.map((category) => ({
    id: category.id,
    handle: category.handle,
  }))
  const existingCategoryHandles = new Set(categories.map((category) => category.handle))
  const missingCategories = categoryDefinitions.filter(
    (category) => !existingCategoryHandles.has(category.handle)
  )

  if (missingCategories.length) {
    const { result: createdCategories } = await createProductCategoriesWorkflow(
      container
    ).run({
      input: { product_categories: missingCategories },
    })
    categories = [
      ...categories,
      ...createdCategories.map((category) => ({
        id: category.id,
        handle: category.handle,
      })),
    ]
  }

  for (const category of categoryDefinitions) {
    await updateProductCategoriesWorkflow(container).run({
      input: {
        selector: { handle: category.handle },
        update: { is_active: true },
      },
    })
  }

  const categoryIds = new Map(
    categories.map((category) => [category.handle, category.id])
  )
  const categoryId = (handle: string) => {
    const id = categoryIds.get(handle)
    if (!id) throw new Error(`Category not found: ${handle}`)
    return id
  }

  // 7. Products. Every product is identified by its handle, so this seed is safe to rerun.
  const imageUrl = (filename: string) =>
    `http://localhost:9000/static/${filename}`
  const productDefinitions = [
    {
      title: "Medusa T-Shirt",
      handle: "t-shirt",
      description: "A soft organic cotton T-shirt for every day.",
      category: "apparel",
      price: 1999,
      image: "1788687055695-255f4e14-1cca-11ef-80d6-ba4fdc50ab5f-930x1240.webp",
    },
    {
      title: "Essential Hoodie",
      handle: "essential-hoodie",
      description: "A heavyweight fleece hoodie with a relaxed fit.",
      category: "apparel",
      price: 6499,
      image: "1788687101076-255f4e14-1cca-11ef-80d6-ba4fdc50ab5f-930x1240.webp",
    },
    {
      title: "Studio Sweatshirt",
      handle: "studio-sweatshirt",
      description: "A clean crewneck sweatshirt made for layering.",
      category: "apparel",
      price: 5499,
      image: "1788687114059-255f4e14-1cca-11ef-80d6-ba4fdc50ab5f-930x1240.webp",
    },
    {
      title: "Relaxed Shorts",
      handle: "relaxed-shorts",
      description: "Lightweight shorts with an elastic waist and deep pockets.",
      category: "apparel",
      price: 3499,
      image: "1788687119231-255f4e14-1cca-11ef-80d6-ba4fdc50ab5f-930x1240.webp",
    },
    {
      title: "Canvas Sneakers",
      handle: "canvas-sneakers",
      description: "Minimal low-top sneakers with a durable canvas upper.",
      category: "footwear",
      price: 7999,
      image: "1788687142855-255f4e14-1cca-11ef-80d6-ba4fdc50ab5f-930x1240.webp",
    },
    {
      title: "City Runner",
      handle: "city-runner",
      description: "Breathable everyday trainers with cushioned support.",
      category: "footwear",
      price: 9499,
      image: "1788687155510-255f4e14-1cca-11ef-80d6-ba4fdc50ab5f-930x1240.webp",
    },
    {
      title: "Everyday Cap",
      handle: "everyday-cap",
      description: "A six-panel cap with an adjustable back strap.",
      category: "accessories",
      price: 2499,
      image: "1788687157588-255f4e14-1cca-11ef-80d6-ba4fdc50ab5f-930x1240.webp",
    },
    {
      title: "Canvas Tote",
      handle: "canvas-tote",
      description: "A spacious reusable tote for daily essentials.",
      category: "accessories",
      price: 2999,
      image: "1788687157737-255f4e14-1cca-11ef-80d6-ba4fdc50ab5f-930x1240.webp",
    },
    {
      title: "Steel Water Bottle",
      handle: "steel-water-bottle",
      description: "An insulated stainless steel bottle that keeps drinks cold.",
      category: "accessories",
      price: 2799,
      image: "1788687157888-255f4e14-1cca-11ef-80d6-ba4fdc50ab5f-930x1240.webp",
    },
    {
      title: "Ceramic Mug",
      handle: "ceramic-mug",
      description: "A matte ceramic mug for coffee, tea, or desk decor.",
      category: "home-lifestyle",
      price: 1899,
      image: "1788687158023-255f4e14-1cca-11ef-80d6-ba4fdc50ab5f-930x1240.webp",
    },
    {
      title: "Logo Sticker Pack",
      handle: "logo-sticker-pack",
      description: "A set of durable vinyl stickers for your laptop or notebook.",
      category: "home-lifestyle",
      price: 999,
      image: "1788687176174-255f4e14-1cca-11ef-80d6-ba4fdc50ab5f-930x1240.webp",
    },
  ]
  const { data: existingProducts } = await query.graph({
    entity: "product",
    fields: ["handle"],
  })
  const existingProductHandles = new Set(
    existingProducts.map((product) => product.handle)
  )
  const productsToCreate = productDefinitions.filter(
    (product) => !existingProductHandles.has(product.handle)
  )

  if (productsToCreate.length) {
    await createProductsWorkflow(container).run({
      input: {
        products: productsToCreate.map((product) => ({
          title: product.title,
          category_ids: [categoryId(product.category)],
          description: product.description,
          handle: product.handle,
          weight: 300,
          status: "published" as const,
          thumbnail: imageUrl(product.image),
          images: [{ url: imageUrl(product.image) }],
          sales_channels: [{ id: defaultSalesChannel[0].id }],
          options: [{ title: "Size", values: ["S", "M", "L"] }],
          variants: ["S", "M", "L"].map((size) => ({
            title: size,
            sku: `${product.handle}-${size}`.toUpperCase(),
            options: { Size: size },
            prices: [{ amount: product.price, currency_code: "eur" }],
          })),
        })),
      },
    })
    logger.info(`${productsToCreate.length} catalog products created`)
  }

  logger.info("Seed completed successfully!")
}

