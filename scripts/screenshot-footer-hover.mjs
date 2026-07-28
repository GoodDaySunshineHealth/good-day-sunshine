import { chromium } from 'playwright';

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1200, height: 900 } });
await page.goto('http://localhost:5174/', { waitUntil: 'networkidle' });
await page.locator('footer.footer').scrollIntoViewIfNeeded();
await page.waitForTimeout(400);
// Hover middle icon (YouTube) for clear hover demo
await page.locator('footer.footer .social-link').nth(2).hover();
await page.waitForTimeout(350);
await page.locator('footer.footer').screenshot({ path: 'footer-preview-hover.png' });
await browser.close();
console.log('saved footer-preview-hover.png');
