import asyncio
import json
from crawl4ai import AsyncWebCrawler, JsonCssExtractionStrategy
from crawl4ai.async_configs import CrawlerRunConfig, BrowserConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.content_filter_strategy import PruningContentFilter
from pydantic import BaseModel
import pandas as pd

class Items(BaseModel):
    name: str
    description: str
    price: str
    rating: str


async def scrape_items():
    # Define CSS-based extraction schema
    schema = {
        "name": "Laptops",
        "baseSelector": "a.CGtC98",
        "fields": [
            {"name": "Name", "selector": "div.KzDlHZ", "type": "text"},
            {"name": "Price", "selector": "div.Nx9bqj._4b5DiR", "type": "text"},
            {"name": "Description", "selector": "div._6NESgJ", "type": "text"},
            {"name": "rating", "selector": "div.XQDdHH", "type": "text"},
        ]
    }

    # JSON CSS Extraction Strategy
    extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)

    # Browser configuration
    browser_cfg = BrowserConfig(
        headless=True,
        use_persistent_context=True
    )

    # Crawler configuration
    run_cfg = CrawlerRunConfig(
        extraction_strategy=extraction_strategy,
        markdown_generator=DefaultMarkdownGenerator(
            content_filter=PruningContentFilter()
        ),
        exclude_all_images=True,
        excluded_tags=["img", "form", "header"],
        exclude_external_links=True,
        process_iframes=True,
        remove_overlay_elements=True,
        simulate_user=True,
        override_navigator=True,
        scan_full_page=True  # enables full-page scroll behavior
    )

    base_url = "https://www.flipkart.com/search?q=laptops&page={page}"
    all_data = []

    # Start the crawler
    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        for page in range(1, 100):  # Arbitrary large upper limit
            url = base_url.format(page=page)
            print(f"📄 Scraping page {page}: {url}")

            result = await crawler.arun(url=url, config=run_cfg)

            if result.success:
                data = json.loads(result.extracted_content)

                # ✅ Stop crawling if no more data is found
                if not data:
                    print(f"🚫 No data found on page {page}. Ending crawl.")
                    break

                all_data.extend(data)
            else:
                print(f"❌ Error on page {page} ({url}): {result.error_message}")
                break  # Optional: stop on first error, or continue

            await asyncio.sleep(2)  # Be polite to Flipkart’s servers

    df = pd.DataFrame(all_data)
    df.to_excel("laptops.xlsx", index=False)
    print(f"✅ Scraping completed. Total items: {len(all_data)}. Saved to laptops.xlsx")



if __name__ == "__main__":
    asyncio.run(scrape_items())
