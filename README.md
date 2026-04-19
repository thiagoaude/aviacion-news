# Aviacion News

Dashboard personalizado de noticias de aviación, espacio y IA.

## Setup

1. **Forkear o clonar** este repo

2. **API Keys** (en GitHub Settings → Secrets):

   | Secret | Valor |
   |--------|-------|
   | `AI_PROVIDER` | anthropic/openai/gemini |
   | `ANTHROPIC_API_KEY` | tu clave |
   | `OPENAI_API_KEY` | tu clave |
   | `GEMINI_API_KEY` | tu clave |
   | `SEARCH_ENGINE` | duckduckgo/tavily/serper |

3. **GitHub Pages**: Settings → Pages → Deploy from branch → main

4. **Daily**, corre automáticamente a las 8:00 AM (ARG)

## Desarrollo

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-...
python news_fetcher.py
```

## Estructura

- `index.html` - Dashboard
- `news_fetcher.py` - Scraper + IA
- `news.json` - Noticias
- `.github/workflows/daily.yml` - Daily automation

## Ver

https://thiagoaude.github.io/aviacion-news/