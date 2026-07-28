import { chromium } from 'playwright';

const browser = await chromium.launch();
const page = await browser.newPage({
  viewport: { width: 390, height: 844 },
  deviceScaleFactor: 2,
});
await page.goto('http://localhost:5174/', { waitUntil: 'networkidle' });
await page.locator('footer.footer').scrollIntoViewIfNeeded();
await page.waitForTimeout(400);
await page.locator('footer.footer').screenshot({ path: 'footer-preview-mobile.png' });
await browser.close();
console.log('saved footer-preview-mobile.png');
