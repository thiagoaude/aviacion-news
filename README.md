# Aviacion News

Dashboard personalizado de noticias de aviación e inteligencia artificial.

## Setup

1. **Forkear o clonar** este repo

2. **API Keys (opcionales)**:

   **IA - Elegir una:**
   | Provider | Secret | Notas |
   |----------|--------|-------|
   | Claude (default) | `ANTHROPIC_API_KEY` | Ya lo tenés pago |
   | OpenAI (GPT) | `OPENAI_API_KEY` | api.openai.com |
   | Gemini | `GEMINI_API_KEY` | ai.google.dev |
   - Agregar secret: `AI_PROVIDER` = anthropic/openai/gemini

   **Búsqueda - Gratis (duckduckgo default):**
   | Engine | Secret | Límite |
   |--------|--------|--------|
   | DuckDuckGo | - | ilimitado |
   | Tavily | `TAVILY_API_KEY` | 1000/mes |
   | Serper | `SERPER_API_KEY` | 100/mes |
   - Agregar secret: `SEARCH_ENGINE` = tavily/serper/brave/duckduckgo

3. **Habilitar GitHub Pages**:
   - Settings → Pages
   - Source: Deploy from branch
   - Branch: main, folder: / (root)

4. **El workflow corre daily a las 8:00 AM (Argentina)**

## Estructura

```
├── index.html          # Dashboard
├── news_fetcher.py     # Script que llama a Claude
├── news.json           # Noticias (generado automaticamente)
├── .github/workflows/  # GitHub Actions
└── requirements.txt    # Dependencias Python
```

## Desarrollo local

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=tu_key
python news_fetcher.py
python -m http.server 8000
```
