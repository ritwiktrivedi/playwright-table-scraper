#!/usr/bin/env python3
"""
GitHub Action Playwright Table Scraper
Scrapes numeric data from tables across multiple pages and calculates grand total.
"""

from playwright.sync_api import sync_playwright
import sys
from datetime import datetime


def scrape_with_js(url):
    """Scrape a single URL and return the sum of all numeric values in tables."""
    print(f"🔍 Scraping: {url}")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Set timeout and wait for page load
            page.set_default_timeout(30000)  # 30 seconds
            page.goto(url, wait_until="domcontentloaded")

            # Wait a bit for any dynamic content
            page.wait_for_timeout(2000)

            # Inject JavaScript to sum all <td> values
            total = page.evaluate("""
                () => {
                    const rows = document.querySelectorAll("#table table tr, table tr");
                    let sum = 0;
                    let cellCount = 0;
                    
                    rows.forEach(row => {
                        const cells = row.querySelectorAll("td");
                        cells.forEach(cell => {
                            const text = cell.textContent.trim();
                            const num = parseInt(text, 10);
                            if (!isNaN(num)) {
                                sum += num;
                                cellCount++;
                            }
                        });
                    });
                    
                    console.log(`Found ${cellCount} numeric cells`);
                    return sum;
                }
            """)

            browser.close()
            print(f"   ✅ Page sum: {total}")
            return total

    except Exception as e:
        print(f"   ❌ Error scraping {url}: {str(e)}")
        return 0


def main():
    """Main function to scrape all pages and calculate grand total."""
    print("🚀 Starting GitHub Action Table Scraper")
    print(f"📅 Timestamp: {datetime.now().isoformat()}")
    print("=" * 50)

    grand_total = 0
    successful_scrapes = 0
    failed_scrapes = 0

    # Scrape 10 pages with seeds from 87 to 96
    for seed in range(87, 97):
        url = f"https://sanand0.github.io/tdsdata/js_table/?seed={seed}"
        page_total = scrape_with_js(url)

        if page_total > 0:
            successful_scrapes += 1
            grand_total += page_total
        else:
            failed_scrapes += 1

    print("=" * 50)
    print("📊 FINAL RESULTS:")
    print(f"   • Successful scrapes: {successful_scrapes}")
    print(f"   • Failed scrapes: {failed_scrapes}")
    print(f"   • 🎯 GRAND TOTAL: {grand_total}")

    # Save results to file for artifact upload
    with open('results.txt', 'w') as f:
        f.write(f"Table Scraping Results - {datetime.now().isoformat()}\n")
        f.write(f"Successful scrapes: {successful_scrapes}\n")
        f.write(f"Failed scrapes: {failed_scrapes}\n")
        f.write(f"Grand Total: {grand_total}\n")

    # Print in a way that's easy to find in GitHub Action logs
    print("\n" + "🎉" * 20)
    print(f"✅ GRAND TOTAL: {grand_total}")
    print("🎉" * 20)

    return grand_total


if __name__ == "__main__":
    try:
        result = main()
        sys.exit(0)
    except Exception as e:
        print(f"❌ Script failed with error: {str(e)}")
        sys.exit(1)
