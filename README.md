<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/svg/hero-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/svg/hero-light.svg">
  <img alt="Ishrat Bhullar — AI Engineer, Retrieval-Augmented Generation, Backend Systems" src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/svg/hero-dark.svg" width="100%">
</picture>

<a href="#engineering-journey">Journey</a> &nbsp;·&nbsp; <a href="#projects">Projects</a> &nbsp;·&nbsp; <a href="#systems-reference">Systems Reference</a> &nbsp;·&nbsp; <a href="#tech-stack">Stack</a> &nbsp;·&nbsp; <a href="#resume">Resume</a> &nbsp;·&nbsp; <a href="#contact">Contact</a>

</div>

<img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/divider.svg" width="100%" alt="">

## About

I build AI systems that hold up under enterprise scrutiny — retrieval pipelines whose answers trace back to a source passage, and multi-agent workflows that pause for a human before they commit.

Computer Engineering at **Thapar Institute of Engineering & Technology**. Over a six-month AI engineering internship at **Ernst & Young** (Technology Consulting, CNS — Technology Strategy & Transformation), I went from validating someone else's enterprise AI system to designing and building three of my own.

One standard runs through all of it: an AI output is not correct because it is plausible. It is correct because it is **verifiable against a source**, **consistent across repeated runs**, and **fails safely to a human** rather than quietly producing something wrong.

| | |
|---|---|
| **Retrieval-Augmented Generation** | Lexical, semantic and hybrid retrieval; rank fusion; citation-backed generation |
| **Multi-Agent Systems** | Sequential orchestration, shared project memory, human approval gates |
| **Backend Engineering** | Async FastAPI services, REST API design, PostgreSQL, caching, on-premise deployment |
| **Software Architecture** | Layered design, offline-first and air-gapped constraints, auditability by construction |

<img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/divider.svg" width="100%" alt="">

## Engineering Journey

Four projects. Each one was motivated by the outcome of the one before it.

<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/svg/journey-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/svg/journey-light.svg">
  <img alt="Engineering journey: Validator, Builder, Architect, Platform Engineer" src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/svg/journey-dark.svg" width="100%">
</picture>
</div>

**Validator** → validated a live government AI portal, and learned what "correct" has to mean in an enterprise setting. **Builder** → applied that standard to a system of my own, starting at the simplest retrieval architecture that could work. **Architect** → measured where that baseline broke and redesigned its retrieval to fix exactly those failures. **Platform Engineer** → generalised the pattern from answering questions about documents to generating the documents themselves.

<img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/divider.svg" width="100%" alt="">

## Projects

### Vectorless RAG Chatbot

> Document intelligence with no vector database — BM25 lexical retrieval and a locally hosted LLM.

**Problem.** Government departments hold large policy repositories that keyword tools can match on text but not on meaning. An officer answering one question may search the whole repository by hand — slow, inconsistent between reviewers, and impossible to audit, because a manual answer carries no trace back to the passage that justified it.

**Why not a vector database.** The conventional answer is embeddings plus a vector store. For air-gapped government deployments that means embedding infrastructure, index maintenance and recurring cost. This project tested whether that burden was necessary *before* proving it necessary — starting at the keyword-only end of the spectrum on purpose.

<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/architecture/vectorless-rag-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/architecture/vectorless-rag-light.svg">
  <img alt="Vectorless RAG system architecture — four layers with no vector index" src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/architecture/vectorless-rag-dark.svg" width="100%">
</picture>
</div>

**Key decisions.** Structure ingestion to preserve traceability from answer to source passage from the outset, rather than retrofitting citations later. Constrain the prompt so responses are generated strictly from retrieved content, not model knowledge. Rerank with a cross-encoder so lexical recall is traded back for precision before context is assembled.

**Technology** — `Python` · `FastAPI` · `BM25` · `Cross-Encoder Reranking` · `Ollama` · `Streamlit` · `Tesseract OCR`

<div align="center">
<sub>A document-grounded answer, with retrieval and generation timing and the full citation trace of source chunks used.</sub><br><img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/gifs/vectorless-rag.gif" width="100%" alt="Vectorless RAG chatbot answering a document-grounded query, scrolling through its citation trace">
</div>

<details>
<summary><b>Retrieval pipeline</b></summary>
<br>
<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/workflows/vectorless-pipeline-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/workflows/vectorless-pipeline-light.svg">
  <img alt="Vectorless RAG technical workflow" src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/workflows/vectorless-pipeline-dark.svg" width="100%">
</picture>
</div>
</details>

**Outcome.** It worked — and its limits are the point. Retrieval degraded exactly where keyword matching has no notion of meaning: paraphrased queries, indirect references, non-English content. That finding motivated the next system.

<a href="https://github.com/Ishrat-Bhullar/vectorless-chatbot"><b>Repository →</b></a>

---

### Hybrid RAG Chatbot

> Semantic and lexical retrieval run in parallel and fuse into one ranking.

**Problem.** The three failure modes measured in the vectorless baseline, in a corpus that also contains scanned pages with no machine-readable text layer and terminology in more than one language.

**Why not just switch to vector search.** Keyword retrieval is precise on policy numbers and regulation codes; vector retrieval handles paraphrase and crosses languages but can under-rank an exact-but-non-obvious match. Choosing either means accepting the other's weakness. Fusing both rankings — rather than replacing one with the other — was driven by an observed failure pattern in a working system, not a generic preference for more advanced retrieval.

<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/architecture/hybrid-rag-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/architecture/hybrid-rag-light.svg">
  <img alt="Hybrid RAG system architecture — five layers with a dual retrieval path" src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/architecture/hybrid-rag-dark.svg" width="100%">
</picture>
</div>

**Key decisions.** Treat semantic and keyword retrieval as complementary signals and merge them with Reciprocal Rank Fusion. Make citation generation a first-class pipeline output rather than an afterthought. Use multilingual embeddings so one index serves cross-lingual search instead of one store per language. Keep inference on-premise so document content never leaves the host.

**Technology** — `Python` · `FastAPI` · `FAISS` · `ChromaDB` · `BM25` · `Reciprocal Rank Fusion` · `Multilingual Embeddings` · `React` · `Ollama` · `OCR`

<div align="center">
<sub>Retrieval transparency — every retrieved chunk with its source document and relevance score.</sub><br><img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/gifs/hybrid-rag.gif" width="100%" alt="Hybrid RAG chatbot scrolling through its citation trace">
</div>

<details>
<summary><b>Retrieval pipeline</b></summary>
<br>
<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/workflows/hybrid-pipeline-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/workflows/hybrid-pipeline-light.svg">
  <img alt="Hybrid RAG technical workflow" src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/workflows/hybrid-pipeline-dark.svg" width="100%">
</picture>
</div>
</details>

**Outcome.** Better semantic understanding, more consistent multilingual handling, and explainability through citations — a grounding-plus-transparency design now proven across two independent systems. That consolidated pattern became the foundation for the platform below.

<a href="https://github.com/Ishrat-Bhullar/rag-chatbot-mongodb"><b>Repository →</b></a>

---

### Autonomous Multi-Agent SDLC Platform

> Nine specialised AI agents turn a business requirement into engineering artifacts, gated by mandatory human approval.

**Problem.** Enterprise delivery depends on a sequence of specialists — business analysts, architects, database designers, security reviewers — each producing documentation that must stay consistent with everyone else's. Coordinating that manually produces incomplete requirements at initiation, architecture quality that varies with individual experience, artifacts that drift out of consistency, and slow knowledge transfer.

**Why not a single assistant.** Language models draft structured technical content competently, but are typically deployed as isolated assistants rather than coordinated collaborators. An assistant answering one prompt at a time cannot hold a project's context across disciplines — which is precisely where the inconsistency comes from.

<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/architecture/sdlc-platform-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/architecture/sdlc-platform-light.svg">
  <img alt="SDLC platform architecture — orchestration over a specialised agent pool" src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/architecture/sdlc-platform-dark.svg" width="100%">
</picture>
</div>

**Key decisions.** Centralise project memory in a Memory Agent so each agent reads shared context instead of re-deriving requirements — this is what prevents cross-artifact drift. Require explicit human sign-off at two checkpoints before output influences the next stage. Structure the schema around traceability first, which is what makes the Documentation and Temporal Replay Centers possible at all. Keep the reasoning layer configurable so a project can supply its own provider credentials.

**Technology** — `Python` · `TypeScript` · `FastAPI` · `React` · `PostgreSQL` · `LangGraph` · `Multi-Agent Orchestration` · `BYOK Provider Routing`

<div align="center">
<sub>Orchestration dashboard, then the Requirements and Architecture workspaces generated by their agents.</sub><br><img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/gifs/sdlc-platform.gif" width="100%" alt="SDLC platform orchestration dashboard and agent workspaces">
</div>

<details>
<summary><b>Agent pipeline</b> — two mandatory human approval checkpoints</summary>
<br>
<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/workflows/sdlc-pipeline-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/workflows/sdlc-pipeline-light.svg">
  <img alt="SDLC platform implemented pipeline workflow" src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/workflows/sdlc-pipeline-dark.svg" width="100%">
</picture>
</div>
</details>

**Outcome.** A coordinated agent set producing consistent requirements, business analysis, architecture, database design, UI/UX and compliance artifacts — governed by approval checkpoints and kept auditable by the Documentation and Temporal Replay Centers.

<a href="https://github.com/Ishrat-Bhullar/sdlc-platform"><b>Repository →</b></a>

<img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/divider.svg" width="100%" alt="">

## Systems Reference

Supporting designs that span the projects above.

<details>
<summary><b>Retrieval trade-off</b> — the comparison that drove the hybrid redesign</summary>
<br>
<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/architecture/retrieval-comparison-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/architecture/retrieval-comparison-light.svg">
  <img alt="Comparison of keyword, semantic and hybrid retrieval" src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/architecture/retrieval-comparison-dark.svg" width="100%">
</picture>
</div>
</details>

<details>
<summary><b>Data model</b> — traceability designed in from the schema up</summary>
<br>
<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/architecture/data-model-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/architecture/data-model-light.svg">
  <img alt="Simplified conceptual data model" src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/architecture/data-model-dark.svg" width="100%">
</picture>
</div>
</details>

<details>
<summary><b>BYOK provider resolution</b> — graceful degradation across AI providers</summary>
<br>
<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/workflows/byok-resolution-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/workflows/byok-resolution-light.svg">
  <img alt="BYOK AI provider resolution order" src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/workflows/byok-resolution-dark.svg" width="100%">
</picture>
</div>
</details>

<details>
<summary><b>Media generation pipeline</b> — artifacts to narrated presentation</summary>
<br>
<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/workflows/media-pipeline-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/workflows/media-pipeline-light.svg">
  <img alt="Media generation pipeline" src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/workflows/media-pipeline-dark.svg" width="100%">
</picture>
</div>
</details>

<details>
<summary><b>Maharashtra AI Portal</b> — the twelve-stage clearance workflow I validated</summary>
<br>
<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/workflows/portal-workflow-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/workflows/portal-workflow-light.svg">
  <img alt="Maharashtra AI Portal evaluation and clearance workflow" src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/workflows/portal-workflow-dark.svg" width="100%">
</picture>
</div>
</details>

<details>
<summary><b>Interface stills</b> — full resolution</summary>
<br>

| | |
|:--:|:--:|
| <img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/images/vectorless-interface.png" width="100%" alt="Vectorless RAG conversational interface"> | <img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/images/hybrid-interface.png" width="100%" alt="Hybrid RAG conversational interface"> |
| <sub>Vectorless RAG — conversational interface</sub> | <sub>Hybrid RAG — conversational interface</sub> |
| <img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/images/hybrid-citations.png" width="100%" alt="Hybrid RAG citation trace"> | <img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/images/sdlc-dashboard.png" width="100%" alt="SDLC orchestration dashboard"> |
| <sub>Hybrid RAG — citation trace</sub> | <sub>SDLC Platform — orchestration dashboard</sub> |
| <img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/images/sdlc-requirements.png" width="100%" alt="SDLC requirements workspace"> | <img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/images/sdlc-architecture.png" width="100%" alt="SDLC architecture workspace"> |
| <sub>SDLC Platform — requirements workspace</sub> | <sub>SDLC Platform — architecture workspace</sub> |

</details>

<img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/divider.svg" width="100%" alt="">

## Tech Stack

<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/icons/stack-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/icons/stack-light.svg">
  <img alt="Technology stack grouped by responsibility" src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/icons/stack-dark.svg" width="100%">
</picture>
</div>

<img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/divider.svg" width="100%" alt="">

## Resume

<div align="center">

<a href="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/resume/Ishrat-Bhullar-Resume.pdf">
<img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/resume/resume-preview.png" width="46%" alt="Resume preview — Ishrat Bhullar, AI Engineer">
</a>

<br><br>

**AI Engineer** — Retrieval-Augmented Generation &amp; Backend Systems<br><sub>Single page, ATS-friendly. B.E. Computer Engineering, Thapar Institute of Engineering &amp; Technology, 2022–2026.</sub>

<br>

<a href="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/resume/Ishrat-Bhullar-Resume.pdf"><b>Download PDF</b></a> &nbsp;&nbsp;·&nbsp;&nbsp; <a href="https://github.com/Ishrat-Bhullar/Ishrat-Bhullar/blob/main/assets/resume/Ishrat-Bhullar-Resume.pdf"><b>Preview in browser</b></a>

</div>

<img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/divider.svg" width="100%" alt="">

## GitHub Stats

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/stats-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/stats-light.svg">
  <img alt="GitHub statistics overview" src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/stats-dark.svg" width="46%">
</picture>
&nbsp;&nbsp;
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/languages-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/languages-light.svg">
  <img alt="Most used languages" src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/languages-dark.svg" width="46%">
</picture>

<br><br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/contributions-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/contributions-light.svg">
  <img alt="Contribution activity over the last year" src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/contributions-dark.svg" width="100%">
</picture>

</div>

<details>
<summary><b>Recent activity</b></summary>

<!--START_SECTION:activity-->
- Pushed to [Ishrat-Bhullar](https://github.com/Ishrat-Bhullar/Ishrat-Bhullar) &nbsp;·&nbsp; <sub>14 days ago</sub>
- Pushed to [sdlc-platform](https://github.com/Ishrat-Bhullar/sdlc-platform) &nbsp;·&nbsp; <sub>14 days ago</sub>
- Pushed to [rag-chatbot-mongodb](https://github.com/Ishrat-Bhullar/rag-chatbot-mongodb) &nbsp;·&nbsp; <sub>15 days ago</sub>
- Pushed to [vectorless-chatbot](https://github.com/Ishrat-Bhullar/vectorless-chatbot) &nbsp;·&nbsp; <sub>15 days ago</sub>
- Created branch `main` in [Ishrat-Bhullar](https://github.com/Ishrat-Bhullar/Ishrat-Bhullar) &nbsp;·&nbsp; <sub>17 days ago</sub>
<!--END_SECTION:activity-->

</details>

<img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/divider.svg" width="100%" alt="">

## Contact

<div align="center">

<a href="https://www.linkedin.com/in/ishrat-bhullar-4a1441295/"><b>LinkedIn</b></a> &nbsp;&nbsp;·&nbsp;&nbsp; <a href="mailto:ishratbhullar@gmail.com"><b>ishratbhullar@gmail.com</b></a> &nbsp;&nbsp;·&nbsp;&nbsp; <a href="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/resume/Ishrat-Bhullar-Resume.pdf"><b>Resume</b></a>

<br>

<sub>Open to AI engineering and backend roles · Mohali, India</sub>

</div>

<img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/divider.svg" width="100%" alt="">

<div align="center">
<sub>
Architecture and workflow diagrams are redrawn as vector artwork from my Project Semester Report,<br>
<i>Enterprise AI Systems: Document Intelligence and Autonomous Multi-Agent Software Delivery at Ernst &amp; Young</i>.<br>
Interface recordings are from the same report. Per enterprise confidentiality, no source code, prompt text<br>
or internal configuration is reproduced — systems are shown at architecture level only.<br><br>
Every diagram, chip, card and demo on this page is generated by the scripts in
<a href="https://github.com/Ishrat-Bhullar/Ishrat-Bhullar/tree/main/scripts"><code>scripts/</code></a>.
</sub>
</div>
