import { chromium } from 'playwright';

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1200, height: 900 } });
await page.goto('http://localhost:5174/', { waitUntil: 'networkidle' });
await page.locator('footer.footer').scrollIntoViewIfNeeded();
await page.waitForTimeout(500);
await page.locator('footer.footer').screenshot({ path: 'footer-preview.png' });
await browser.close();
console.log('saved footer-preview.png');
