Search Hugging Face for models, datasets, and Spaces on: $ARGUMENTS

Hugging Face (huggingface.co) is the primary hub for open-source ML models, datasets, and demos. It is uniquely valuable for surfacing the *actual downloadable artifacts* behind a research area — model weights, fine-tunes, evaluation datasets, and the download/like counts that reveal real-world adoption. For a domain like mental-health NLP, HF is where MentalBERT, MentalRoBERTa, MentaLLaMA, EmoBERTa, and their datasets live.

**Primary strategy — HF full-text + model/dataset search (renders server-side, fetch as JSON API):**
- Models: WebFetch `https://huggingface.co/api/models?search=QUERY&sort=downloads&direction=-1&limit=25` — returns JSON with modelId, downloads, likes, tags, pipeline_tag, lastModified. This is the most reliable structured signal.
- Datasets: WebFetch `https://huggingface.co/api/datasets?search=QUERY&sort=downloads&direction=-1&limit=25` — JSON list of datasets with download counts.
- Full-text UI (fallback if API thin): WebFetch `https://huggingface.co/models?search=QUERY` and `https://huggingface.co/datasets?search=QUERY`.

**Secondary strategy — Google site-search for model cards and Spaces:**
- `site:huggingface.co $ARGUMENTS` — surfaces the most-linked model/dataset cards and Spaces
- `site:huggingface.co/papers $ARGUMENTS` — HF Papers pages (daily-papers with community discussion + linked artifacts)
- `site:huggingface.co spaces $ARGUMENTS` — interactive demos

**For the top 3–5 models/datasets, fetch the card** (`https://huggingface.co/OWNER/MODEL` or `https://huggingface.co/datasets/OWNER/NAME`) and extract:
- Model name, base architecture (BERT/RoBERTa/LLaMA/Mistral etc.), parameter count
- **Downloads (last month) and Likes** — the adoption/popularity signal unique to HF
- pipeline_tag / task (text-classification, text-generation, fill-mask)
- Training data described in the card, license, and intended use / limitations (safety-critical for mental health)
- Linked paper (arXiv) and citation, last-modified date (is it maintained?)
- Any evaluation metrics reported on the card

**What makes Hugging Face uniquely valuable:**
- **Adoption signal**: download and like counts show which research artifacts practitioners actually use vs. abandoned academic one-offs
- **Provenance**: model cards link the paper, base model, and dataset — you can trace the lineage
- **Reproducibility**: the weights are actually there and runnable, not just claimed in a paper
- **Datasets**: the labeled corpora (Reddit mental-health sets, DAIC-WOZ derivatives, dreaddit) that a builder would fine-tune on

**Fallback if blocked/empty:** If the API returns empty or the card 403/JS-shells, extract from the Google search snippet (model name + downloads often shown), then WebFetch the linked arXiv abstract for the model's details. Flag as snippet-sourced.

**Do NOT:**
- Treat high downloads as quality/safety endorsement — a popular classifier can still be clinically unvalidated
- Cite a model without checking its license and stated limitations (critical for health use)
- Confuse a fine-tune/derivative with the original (many re-uploads of MentalBERT exist)
- Rely on the JS-rendered model list if the `/api/` JSON endpoint is available — the API is cleaner

Return: model/dataset names with base architecture, download + like counts, task/pipeline tag, license, linked paper, training data, stated limitations, last-modified date, and HF URLs. Distinguish original artifacts from derivatives, and note which are clinically validated vs. research-only.
