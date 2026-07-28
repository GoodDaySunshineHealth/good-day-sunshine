import sharp from 'sharp';

const { data, info } = await sharp('assets/hero-sun.png')
  .ensureAlpha()
  .raw()
  .toBuffer({ resolveWithObject: true });

const dark = [];
const bright = [];
const all = [];

for (let i = 0; i < data.length; i += 4) {
  const r = data[i];
  const g = data[i + 1];
  const b = data[i + 2];
  const a = data[i + 3];
  if (a < 200 || r < 180) continue;
  all.push([r, g, b]);
  const lum = 0.299 * r + 0.587 * g + 0.114 * b;
  if (lum < 200) dark.push([r, g, b]);
  else bright.push([r, g, b]);
}

const avg = (arr) =>
  arr
    .reduce((s, c) => [s[0] + c[0], s[1] + c[1], s[2] + c[2]], [0, 0, 0])
    .map((v) => Math.round(v / arr.length));
const hex = (c) => '#' + c.map((x) => x.toString(16).padStart(2, '0')).join('');

console.log('darker', avg(dark), hex(avg(dark)), 'n', dark.length);
console.log('brighter', avg(bright), hex(avg(bright)), 'n', bright.length);
console.log('overall', avg(all), hex(avg(all)), 'n', all.length);

const orangeish = all
  .map(([r, g, b]) => ({ r, g, b, o: r - g }))
  .sort((a, b) => b.o - a.o)
  .slice(0, Math.floor(all.length * 0.1));
const ao = avg(orangeish.map((x) => [x.r, x.g, x.b]));
console.log('top 10% orange', ao, hex(ao));

// Brand tokens for comparison
console.log('tokens: sunshine #F4D35E golden #E8A838 orange #FF9F43');
console.log('proposed rest: #F8B010 or #FCB513 or #E8A838');
console.log('proposed hover: #FEA90D or #FF9F43 or #F59A0B');
