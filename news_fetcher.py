import os
import json
import re
from datetime import datetime
from urllib.parse import quote

AI_PROVIDER = os.environ.get("AI_PROVIDER", "anthropic")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
COPILOT_API_KEY = os.environ.get("COPILOT_API_KEY")

SEARCH_ENGINE = os.environ.get("SEARCH_ENGINE", "tavily")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
SERPER_API_KEY = os.environ.get("SERPER_API_KEY")
BRAVE_API_KEY = os.environ.get("BRAVE_API_KEY")
NEWS_JSON_PATH = os.environ.get("NEWS_JSON_PATH", "news.json")

SEARCH_QUERIES = {
    "argentina": [
        "site:anac.gob.ar Argentina aviación 2026",
        "site:orsna.gov.ar aeropuertos Argentina 2026",
        "Aerolíneas ArgentinasFlybondi JetSmart noticias 2026",
    ],
    "mundial": [
        "EASA safety bulletin aviation 2026",
        "FAA aviation news 2026",
        "IATA airline industry news 2026",
    ],
    "ia": [
        "OpenAI Anthropic Google DeepMind news 2026",
        "AI modelo nuovo announcements 2026",
    ]
}

def search_tavily(query):
    import requests
    url = "https://api.tavily.com/search"
    payload = {"query": query, "max_results": 3}
    headers = {"accept": "application/json"}
    try:
        r = requests.post(url, json=payload, headers=headers, auth=("api", TAVILY_API_KEY))
        results = r.json().get("results", [])[:3]
        return [{"title": x.get("title", ""), "content": x.get("content", ""), "url": x.get("url", "")} for x in results]
    except Exception as e:
        print(f"Tavily error: {e}")
        return []

def search_serper(query):
    import requests
    url = f"https://google.serper.dev/search?q={quote(query)}"
    headers = {"X-API-KEY": SERPER_API_KEY}
    try:
        r = requests.get(url, headers=headers)
        results = r.json().get("organic", [])[:3]
        return [{"title": x.get("title", ""), "content": x.get("snippet", ""), "url": x.get("link", "")} for x in results]
    except Exception as e:
        print(f"Serper error: {e}")
        return []

def search_brave(query):
    import requests
    url = f"https://api.search.brave.com/res/v1/web/search?q={quote(query)}"
    headers = {"Accept": "application/json"}
    try:
        r = requests.get(url, headers=headers)
        results = r.json().get("web", {}).get("results", [])[:3]
        return [{"title": x.get("title", ""), "content": x.get("description", ""), "url": x.get("url", "")} for x in results]
    except Exception as e:
        print(f"Brave error: {e}")
        return []

def search_duckduckgo(query):
    import requests
    url = f"https://html.duckduckgo.com/html/?q={quote(query)}"
    try:
        r = requests.get(url)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, "html.parser")
        results = []
        for result in soup.select(".result")[:3]:
            title = result.select_one(".result__title")
            snippet = result.select_one(".result__snippet")
            link = result.select_one("a.result__a")
            if title and link:
                results.append({
                    "title": title.get_text(strip=True),
                    "content": snippet.get_text(strip=True) if snippet else "",
                    "url": link.get("href", "")
                })
        return results
    except Exception as e:
        print(f"DuckDuckGo error: {e}")
        return []

def do_search(query):
    if SEARCH_ENGINE == "tavily":
        return search_tavily(query)
    elif SEARCH_ENGINE == "serper":
        return search_serper(query)
    elif SEARCH_ENGINE == "brave":
        return search_brave(query)
    elif SEARCH_ENGINE == "duckduckgo":
        return search_duckduckgo(query)
    else:
        print(f"Unknown engine: {SEARCH_ENGINE}")
        return []

def search_all():
    results = {"argentina": [], "mundial": [], "ia": []}
    for category, queries in SEARCH_QUERIES.items():
        for q in queries:
            print(f"Buscando: {q}")
            results[category].extend(do_search(q))
    return results

def fetch_with_ai(search_results):
    fecha = datetime.now().strftime("%Y-%m-%d")

    search_text = []
    for cat, items in search_results.items():
        search_text.append(f"\n### {cat.upper()}")
        for item in items[:5]:
            search_text.append(f"- {item['title']}: {item['content'][:200]}")

    prompt = f"""Sos un asistente de noticias. Hoy es {fecha}.

BUSQUEDAS REALIZADAS:
{{"".join(search_text)}}

TU TRABAJO:
1. Seleccioná las 3-5 noticias más importantes de cada categoría
2. Para cada noticia: título, origen (del URL), resumen breve (1-2 oraciones)
3. Máx 5 noticias por categoría
4. Agregá una frase diaria inspiradora (máx 20 palabras)
5. Agregá un chiste corto de aviación

FORMATO JSON exacto:
{{
  "fecha": "{fecha}",
  "aviacion_argentina": [{{"titulo": "...", "origen": "...", "resumen": "...", "fecha_noticia": "{fecha}"}}],
  "aviacion_mundial": [{{"titulo": "...", "origen": "...", "resumen": "...", "fecha_noticia": "{fecha}"}}],
  "ia": [{{"titulo": "...", "origen": "...", "resumen": "...", "fecha_noticia": "{fecha}"}}],
  "frase_diaria": "...",
  "chiste": "..."
}}

Respondé SOLO con el JSON."""

    provider = AI_PROVIDER.lower()

    if provider == "anthropic" or provider == "claude":
        import anthropic
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        response = message.content[0].text.strip()

    elif provider == "openai" or provider == "gpt":
        import openai
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        message = client.chat.completions.create(
            model="gpt-4o",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        response = message.choices[0].message.content

    elif provider == "gemini":
        import requests
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        r = requests.post(url, json=payload)
        response = r.json()["candidates"][0]["content"]["parts"][0]["text"]

    elif provider == "copilot":
        import requests
        url = "https://api.github.com/copilot-assistant/completions"
        headers = {
            "Authorization": f"Bearer {COPILOT_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {"model": "gpt-4-copilot", "prompt": prompt, "max_tokens": 4000}
        r = requests.post(url, json=payload, headers=headers)
        response = r.json()["choices"][0]["text"]

    else:
        print(f"Unknown AI provider: {provider}")
        return None

    try:
        response = response.replace("```json", "").replace("```", "").strip()
        return json.loads(response)
    except Exception as e:
        print(f"Parse error: {e}")
        return None

def main():
    fecha = datetime.now().strftime("%Y-%m-%d")
    print(f"=== Aviacion News {fecha} ===")
    print(f"Motor IA: {AI_PROVIDER}")

    if ANTHROPIC_API_KEY or OPENAI_API_KEY or GEMINI_API_KEY:
        print("Modo: Búsqueda + IA")
        search_results = search_all()
        news_data = fetch_with_ai(search_results)
    else:
        print("Modo: Búsqueda directa (sin IA)")
        from duckduckgo import DDGS
        d = DDGS()
        news_data = {"fecha": fecha, "aviacion_argentina": [], "aviacion_mundial": [], "ia": [], "frase_diaria": "", "chiste": ""}

        for cat, queries in SEARCH_QUERIES.items():
            for q in queries:
                try:
                    for r in d.text(q, max_results=3):
                        news_data[cat].append({
                            "titulo": r.title,
                            "origen": r.url.split("/")[2] if r.url else "web",
                            "resumen": r.body[:150] if r.body else "",
                            "fecha_noticia": fecha
                        })
                except Exception as e:
                    print(f"Error: {e}")

    if news_data:
        with open(NEWS_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(news_data, f, ensure_ascii=False, indent=2)
        print(f"✅ Guardado en {NEWS_JSON_PATH}")
    else:
        print("❌ Sin datos")

if __name__ == "__main__":
    main()