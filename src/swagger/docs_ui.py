"""
Página de documentação customizada (Swagger UI, tema Angola).

Single-file HTML servido em /api/docs; carrega swagger-ui-dist via CDN
e consome o schema OpenAPI em /api/swagger.json.
"""

# Versão do swagger-ui-dist publicada no jsdelivr
SWAGGER_UI_VERSION = "5.17.14"
_BASE = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@" + SWAGGER_UI_VERSION

# Favicon SVG: listras vermelho/preto com símbolo amarelo (referência à bandeira de Angola)
_FAVICON = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
    "%3Crect width='64' height='32' fill='%23CE1126'/%3E%3Crect y='32' width='64' height='32' fill='%23141214'/%3E"
    "%3Cpath d='M18 40a10 10 0 1 1 8-16l-3 4h8l-3-4a10 10 0 0 1 4 10 10 10 0 0 1-14 6z' fill='%23FFC618'/%3E"
    "%3C/svg%3E"
)

DOCTYPE = "<!DOCTYPE html>\n"

TOPBAR_LOGO = (
    '<svg width="34" height="34" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">'
    '<rect width="64" height="32" fill="#CE1126"/><rect y="32" width="64" height="32" fill="#141214"/>'
    '<path d="M18 40a10 10 0 1 1 8-16l-3 4h8l-3-4a10 10 0 0 1 4 10 10 10 0 0 1-14 6z" fill="#FFC618"/>'
    "</svg>"
)

CSS = """
:root{
  --agd-red:#CE1126; --agd-yellow:#FFC618; --agd-black:#141214;
  --agd-bg:#f6f4f2; --agd-surface:#ffffff; --agd-text:#232022;
  --agd-border:#e6e0da; --agd-muted:#6f6862;
}
html.dark{
  --agd-bg:#141214; --agd-surface:#1e1b1d; --agd-text:#f2ede9;
  --agd-border:#2e2a2c; --agd-muted:#a89f99;
}
body{ margin:0; background:var(--agd-bg); color:var(--agd-text);
  font-family:'Segoe UI',system-ui,-apple-system,sans-serif; }
#agd-topbar{ position:sticky; top:0; z-index:50; background:var(--agd-black);
  color:#fff; display:flex; align-items:center; justify-content:space-between;
  padding:10px 20px; border-bottom:3px solid var(--agd-yellow); }
#agd-topbar .brand{ display:flex; align-items:center; gap:12px; }
#agd-topbar .brand svg{ display:block }
#agd-topbar .title{ font-weight:700; font-size:1.05rem; letter-spacing:.3px; }
#agd-topbar .subtitle{ font-size:.78rem; color:#d8d2cd; }
#agd-topbar .badge{ background:var(--agd-red); color:#fff; border-radius:12px;
  padding:2px 10px; font-size:.72rem; font-weight:700; }
#agd-topbar .actions{ display:flex; gap:10px; align-items:center; }
#agd-topbar a, #agd-topbar button{
  background:transparent; border:1px solid #554a4d; color:#fff; font:inherit;
  padding:6px 12px; border-radius:8px; cursor:pointer; text-decoration:none;
  font-size:.8rem; transition:all .15s ease; }
#agd-topbar a:hover, #agd-topbar button:hover{ border-color:var(--agd-yellow); color:var(--agd-yellow); }
#swagger-ui{ min-height:calc(100vh - 64px) }
.swagger-ui .info .title{ color:var(--agd-text) !important }
.swagger-ui .info p, .swagger-ui .info li{ color:var(--agd-text) }
.swagger-ui .info .description{ color:var(--agd-muted) }
.swagger-ui .scheme-container{ background:var(--agd-surface) !important;
  box-shadow:none !important; border-bottom:1px solid var(--agd-border) }
.swagger-ui .renderedMarkdown, .swagger-ui .markdown p,
.swagger-ui .markdown li{ color:var(--agd-text) }
.swagger-ui .opblock{ border-radius:10px }
.swagger-ui .opblock .opblock-summary{ border-radius:8px; border-left-width:8px !important }
.swagger-ui .opblock .opblock-summary-method{ background:transparent; color:inherit !important;
  border-radius:6px; width:auto; padding:0 8px; font-weight:700 }
.opblock-get .opblock-summary-method{ color:#0d7a54 }
.opblock-put .opblock-summary-method{ color:#7a4b0d }
.opblock-post .opblock-summary-method{ color:var(--agd-red) }
.opblock-delete .opblock-summary-method{ color:#8f1d1d }
.swagger-ui .btn.authorize, .swagger-ui .btn.unauthorized{
  background:var(--agd-yellow) !important; color:#000 !important; border-radius:8px !important }
.swagger-ui .btn.authorize svg{ fill:#000 !important }
.swagger-ui .btn.try{ background:var(--agd-red) !important; color:#fff !important;
  border-radius:8px; box-shadow:0 2px 6px rgba(206,17,38,.35) }
.swagger-ui .models{ background:transparent }
.swagger-ui .model-box{ background:var(--agd-surface) }
.swagger-ui table.parameters{ background:var(--agd-surface) }
.swagger-ui .body-param__text, .swagger-ui textarea{ background:var(--agd-surface);
  color:var(--agd-text) !important }
.swagger-ui .model-title{ color:var(--agd-text) }
"""

TEMPLATE = (
    DOCTYPE
    + """<html lang="pt" data-color-scheme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AngoData API — Documentação</title>
  <meta name="color-scheme" content="light dark">
  <link rel="icon" href="__FAVICON__">
  <link rel="stylesheet" href="__BASE__/swagger-ui.css">
  <style>__CSS__</style>
  <script>
    (function() {
      try {
        var saved = localStorage.getItem('agd-theme');
        if (saved === 'dark' ||
            (!saved && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
          document.documentElement.classList.add('dark');
        }
      } catch (e) {}
    })();
  </script>
</head>
<body>
  <header id="agd-topbar">
    <div class="brand">
      __LOGO__
      <div>
        <span class="title">AngoData API</span>
        <div class="subtitle">Dados públicos de Angola — REST · JWT</div>
      </div>
      <span class="badge">v1.0.0</span>
    </div>
    <div class="actions">
      <a href="/api/swagger.json" target="_blank" rel="noopener">OpenAPI JSON</a>
      <button type="button" id="agd-theme-toggle" title="Tema claro/escuro">Theme</button>
    </div>
  </header>
  <div id="swagger-ui"></div>
  <script src="__BASE__/swagger-ui-bundle.js" crossorigin="anonymous"></script>
  <script>
    window.addEventListener('load', function() {
      var btn = document.getElementById('agd-theme-toggle');
      var mode = 'light';
      function apply(m) {
        document.documentElement.classList.remove('dark');
        if (m === 'dark') { document.documentElement.classList.add('dark'); }
        try { localStorage.setItem('agd-theme', m); } catch (e) {}
        btn.textContent = m === 'dark' ? 'Dark' : 'Light';
        mode = m;
      }
      var pref = null;
      try { pref = localStorage.getItem('agd-theme'); } catch (e) {}
      if (pref !== 'light' && pref !== 'dark') {
        pref = (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) ? 'dark' : 'light';
      }
      apply(pref);
      btn.addEventListener('click', function() { apply(mode === 'dark' ? 'light' : 'dark'); });

      if (typeof SwaggerUIBundle === 'undefined') {
        document.getElementById('swagger-ui').innerHTML =
          '<div style="padding:24px">Falha ao carregar swagger-ui-dist do CDN.</div>';
        return;
      }
      SwaggerUIBundle({
        url: '__SPEC_URL__',
        dom_id: '#swagger-ui',
        deepLinking: true,
        filter: true,
        docExpansion: 'none',
        defaultModelsExpandDepth: 1,
        persistAuthorization: true,
        displayRequestDuration: true
      });
    });
  </script>
</body>
</html>
"""
)


def get_docs_page(spec_url="/api/swagger.json"):
    """
    Retorna o HTML completo da página de documentação.

    Args:
        spec_url (str): URL do schema OpenAPI consumido pela UI

    Returns:
        str: HTML da página
    """
    return (
        TEMPLATE.replace("__FAVICON__", _FAVICON)
        .replace("__BASE__", _BASE)
        .replace("__LOGO__", TOPBAR_LOGO)
        .replace("__CSS__", CSS)
        .replace("__SPEC_URL__", spec_url)
    )
