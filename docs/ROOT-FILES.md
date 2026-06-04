# Root Files Kept On Purpose

These files stay in the repository root because moving them can break deployment, browser discovery, SEO, routing, or the local publishing workflow.

- `.github/` - GitHub Actions workflows must live here.
- `.gitignore` - Git expects ignore rules at the repository root.
- `.nojekyll` - GitHub Pages reads this at the publish root to disable Jekyll processing.
- `404.html` - GitHub Pages serves this as the custom not-found page from the root.
- `about.html`, `shop.html`, `thanks.html` - root aliases preserve existing direct URLs and redirects.
- `blog-feed.xml` - the public RSS URL and subscriber-notification workflow expect this path.
- `CNAME` - GitHub Pages requires this at the root for `munyachipunza.com`.
- `favicon.ico` - browsers and Google commonly request `/favicon.ico` directly.
- `index.html` - the homepage must remain at the web root.
- `netlify.toml` - Netlify expects this at the site root if Netlify is used again.
- `robots.txt` - search engines request `/robots.txt`.
- `sitemap.xml` - search engines and `robots.txt` reference `/sitemap.xml`.
- `site.webmanifest` - linked from every page at `/site.webmanifest`; keeping it at root preserves the app scope.
- `DOUBLE CLICK TO ACTIVATE NEW POST.bat` - root workflow button intentionally kept visible.
- `PASTE NEW POST IN HERE.txt` - root draft file intentionally kept visible.
