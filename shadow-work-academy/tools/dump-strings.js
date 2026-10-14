// Prints every text string (>=40 chars) in the course content as JSON, for completeness checks.
const vm = require('vm'), fs = require('fs'), path = require('path');
const dir = process.argv[2]; const ctx = {}; ctx.window = ctx; vm.createContext(ctx);
for (const f of fs.readdirSync(dir).filter(f => /^(module\d|resources)/.test(f)).sort()) vm.runInContext(fs.readFileSync(path.join(dir, f), 'utf8'), ctx);
const out = []; (function walk(o) { if (typeof o === 'string') { if (o.length >= 40) out.push(o); } else if (o && typeof o === 'object') Object.values(o).forEach(walk); })(ctx.SWA.modules);
console.log(JSON.stringify(out));
