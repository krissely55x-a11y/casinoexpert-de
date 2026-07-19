# Cloudflare Pages (GitHub)

Подключите репозиторий в Cloudflare Pages:

| Параметр | Значение |
|----------|----------|
| Build command | `npm ci && npm run build` |
| Build output directory | `dist` |
| Node.js version | 22 |

Custom domain: `onlinecasinoexperte.org` + `www` (redirect на apex).

Файл `wrangler.toml` уже задаёт `pages_build_output_dir = "./dist"`.

## Структура репозитория

```
onlinecasinoexperte.org/
├── src/          # Astro: layouts, pages, components
├── public/       # статика (wp-content, CSS, robots.txt)
├── mirror/       # исходное Wayback-зеркало (для скриптов)
├── scripts/      # Python-утилиты
├── reports/      # JSON/PDF отчёты
├── archive/      # локальные бэкапы (не в Git)
├── dist/         # сборка (не в Git, создаётся на Cloudflare)
└── package.json
```

## Локально

```powershell
npm ci
npm run dev
npm run build
```
