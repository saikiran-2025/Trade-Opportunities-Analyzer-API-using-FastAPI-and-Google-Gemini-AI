import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment")

genai.configure(api_key=GEMINI_API_KEY)


# ≈≈≈ DEBUG: show what models your key can see ≈≈≈
def get_available_models():
    """
    Call Gemini API to list models your key can see.
    Call this from a route to inspect what's available.
    """
    try:
        models = genai.list_models()
        return [
            {
                "name": m.name.replace("models/", ""),  # remove prefix for display
                "full_name": m.name,
                "methods": m.supported_generation_methods,
            }
            for m in models
        ]
    except Exception as e:
        return [{"error": f"Could not list models: {str(e)}"}]


# ≈≈≈ ANALYSIS: use the first generateContent‑supporting model ≈≈≈
def analyze_market(sector: str, news: list) -> str:
    """
    1. Get list of models that support `generateContent`.  
    2. Pick a supported model (e.g., gemini‑1.5‑flash‑002).  
    3. Generate analysis.
    """
    news_text = "\n".join(news)

    prompt = f"""
    Analyze the Indian {sector} sector using the news below.

    News Headlines:
    {news_text}

    Provide:
    1. Market overview
    2. Key growth drivers
    3. Trade opportunities
    4. Risks
    """

    # Step 1: fetch which models your key supports
    models = get_available_models()
    generate_content_models = [
        m for m in models if m.get("methods") and "generateContent" in m["methods"]
    ]

    if not generate_content_models:
        return (
            "AI analysis failed: no Gemini model with generateContent support found.\n"
            "Make sure your API key is enabled for the Gemini API / Generative Language API.\n"
            "Check https://aistudio.google.com → API key → and confirm model access."
        )

    # Step 2: pick a model that supports generateContent
    # Prefer flash‑style models first
    preferred_names = [
        "gemini-1.5-flash-002",
        "gemini-1.5-flash",
        "gemini-1.5-pro-002",
        "gemini-1.5-pro",
        "gemini-1.0-pro",
    ]

    chosen = None
    for name in preferred_names:
        chosen = next(
            (m for m in generate_content_models if name in m["name"].lower()),
            None,
        )
        if chosen:
            break

    if not chosen:
        chosen = generate_content_models[0]  # fall back to first supported model

    model_name = chosen["full_name"].replace("models/", "")

    try:
        # Use the model we found is supported
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return f"Using model: {model_name}\n\n{response.text}"
    except Exception as e:
        return f"AI analysis failed (model {model_name}): {str(e)}"
