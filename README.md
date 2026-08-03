<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/svg/hero-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/svg/hero-light.svg">
  <img alt="Ishrat Bhullar — AI Engineer, Retrieval-Augmented Generation, Backend Systems" src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/svg/hero-dark.svg" width="100%">
</picture>

<a href="#featured-projects"><b>Projects</b></a> &nbsp;·&nbsp;
<a href="#architecture"><b>Architecture</b></a> &nbsp;·&nbsp;
<a href="#workflows"><b>Workflows</b></a> &nbsp;·&nbsp;
<a href="#demo-gallery"><b>Demos</b></a> &nbsp;·&nbsp;
<a href="#resume"><b>Résumé</b></a> &nbsp;·&nbsp;
<a href="#contact"><b>Contact</b></a>

</div>

<img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/divider.svg" width="100%" alt="">

## About

I build **AI systems that hold up under enterprise scrutiny** — retrieval pipelines whose answers trace back to a source passage, and multi-agent workflows that pause for a human before they commit.

I'm a Computer Engineering student at **Thapar Institute of Engineering & Technology**, Patiala. Over a six-month AI engineering internship at **Ernst & Young** (Technology Consulting, CNS — Technology Strategy & Transformation), I moved from validating someone else's enterprise AI system to designing and building three of my own.

The throughline across all of it is a single design standard, learned early and applied everywhere since: an AI output is not correct because it is plausible. It is correct because it is **verifiable against a source**, **consistent across repeated runs**, and **fails safely to a human** rather than quietly producing something wrong.

| | |
|---|---|
| **Retrieval-Augmented Generation** | Lexical, semantic, and hybrid retrieval; rank fusion; citation-backed generation |
| **Multi-Agent Systems** | Sequential agent orchestration, shared project memory, human approval gates |
| **Backend Engineering** | Async FastAPI services, REST API design, PostgreSQL, caching, on-premise deployment |
| **Software Architecture** | Layered system design, offline-first and air-gapped constraints, auditability by construction |

<img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/divider.svg" width="100%" alt="">

## Engineering Journey

Four projects, each one motivated by the outcome of the one before it — not four unrelated assignments.

<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/svg/journey-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/svg/journey-light.svg">
  <img alt="Engineering journey: Validator, Builder, Architect, Platform Engineer" src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/svg/journey-dark.svg" width="100%">
</picture>
</div>

**1 · Validator** — Functional testing, end-to-end workflow validation, and AI-output verification on the Maharashtra Government Environmental Clearance AI Portal, a live government document-evaluation system. No system of mine, but it set the quality bar for every system that followed.

**2 · Builder** — Built the Vectorless RAG Chatbot from first principles, deliberately starting at the keyword-only end of the retrieval spectrum to find out whether the simplest possible architecture could meet a real document-intelligence need.

**3 · Architect** — Evaluation of that baseline surfaced exactly where lexical-only retrieval breaks: paraphrased queries, indirect references, non-English content. Re-architected it into the Hybrid RAG Chatbot to close those specific gaps.

**4 · Platform Engineer** — Generalised the grounding-plus-human-oversight pattern, now proven twice, from a system that *answers questions about documents* into one that *generates the documents* — the Autonomous Multi-Agent SDLC Platform.

<img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/divider.svg" width="100%" alt="">

## Featured Projects

### Vectorless RAG Chatbot

> Document intelligence with **no vector database at all** — BM25 lexical retrieval and a locally hosted LLM, chosen to test whether the simplest architecture could carry a real government document repository.

Government departments hold large policy repositories that keyword tools can match on text but not on meaning. Rather than reaching for a vector database first, this system establishes a working baseline with minimal infrastructure: PDF ingestion and text extraction, a keyword index, prompt construction strictly from retrieved passages, and a conversational interface that shows its citation trace and retrieval timing alongside every answer.

It works, and its **limits are the point** — evaluation showed precisely where lexical-only retrieval fails, which is what motivated the hybrid system that followed.

`Python` · `FastAPI` · `BM25` · `Cross-Encoder Reranking` · `Ollama` · `Streamlit` · `Tesseract OCR`

<a href="https://github.com/Ishrat-Bhullar/vectorless-chatbot"><b>Repository →</b></a> &nbsp;·&nbsp; <a href="#demo-gallery"><b>Demo ↓</b></a> &nbsp;·&nbsp; <a href="#architecture"><b>Architecture ↓</b></a>

---

### Hybrid RAG Chatbot

> Semantic and lexical retrieval run **in parallel and fused into one ranking** — built specifically to correct the failure modes observed in the vectorless baseline.

Keyword retrieval is precise on policy numbers and regulation codes but has no notion of meaning. Vector retrieval understands paraphrase and crosses languages but can under-rank an exact match. This system treats them as complementary signals rather than competing ones: it fuses both rankings via Reciprocal Rank Fusion, adds OCR so scanned pages index alongside machine-readable ones, and uses multilingual embeddings so one index serves cross-lingual search.

Citation generation is a **first-class output of the pipeline**, not an afterthought — every claim maps back to its source document.

`Python` · `FastAPI` · `FAISS` · `ChromaDB` · `BM25` · `Reciprocal Rank Fusion` · `Multilingual Embeddings` · `React` · `Ollama` · `OCR`

<a href="https://github.com/Ishrat-Bhullar/rag-chatbot-mongodb"><b>Repository →</b></a> &nbsp;·&nbsp; <a href="#demo-gallery"><b>Demo ↓</b></a> &nbsp;·&nbsp; <a href="#architecture"><b>Architecture ↓</b></a>

---

### Autonomous Multi-Agent SDLC Platform

> **Eight specialised AI agents** turn a business requirement into a full set of engineering artifacts, coordinated through shared project memory and gated by mandatory human approval.

A software project depends on a sequence of specialists — business analysts, architects, database designers, security reviewers — each producing documentation that must stay consistent with everyone else's. Coordinating that manually introduces delay, duplicated effort, and version drift.

This platform makes that coordination an explicit, repeatable pipeline. A Memory Agent establishes project-scoped context that every later agent reads from and writes to, so outputs stay mutually consistent instead of each agent re-deriving the requirements. The pipeline **pauses at two mandatory approval checkpoints** where a reviewer can approve, reject, regenerate, or adjust context before anything downstream runs. Around the agents sit four governance modules — Project Dashboard, Documentation Center, Approval Center, and a Temporal Replay Center that records every workflow event as an immutable, replayable timeline.

`Python` · `TypeScript` · `FastAPI` · `React` · `PostgreSQL` · `Multi-Agent Orchestration` · `BYOK Provider Routing`

<a href="https://github.com/Ishrat-Bhullar/sdlc-platform"><b>Repository →</b></a> &nbsp;·&nbsp; <a href="#demo-gallery"><b>Demo ↓</b></a> &nbsp;·&nbsp; <a href="#architecture"><b>Architecture ↓</b></a>

<img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/divider.svg" width="100%" alt="">

## Architecture

Every diagram below is redrawn as vector artwork from the system designs in my Project Semester Report.

<details open>
<summary><b>Vectorless RAG — four layers, no vector index</b></summary>
<br>
<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/architecture/vectorless-rag-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/architecture/vectorless-rag-light.svg">
  <img alt="Vectorless RAG Chatbot system architecture" src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/architecture/vectorless-rag-dark.svg" width="100%">
</picture>
</div>
</details>

<details>
<summary><b>Hybrid RAG — adds an embedding path and rank fusion</b></summary>
<br>
<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/architecture/hybrid-rag-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/architecture/hybrid-rag-light.svg">
  <img alt="Hybrid RAG Chatbot system architecture" src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/architecture/hybrid-rag-dark.svg" width="100%">
</picture>
</div>
</details>

<details>
<summary><b>Autonomous SDLC Platform — orchestration over a specialised agent pool</b></summary>
<br>
<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/architecture/sdlc-platform-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/architecture/sdlc-platform-light.svg">
  <img alt="Autonomous SDLC Platform system architecture" src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/architecture/sdlc-platform-dark.svg" width="100%">
</picture>
</div>
</details>

<details>
<summary><b>Why hybrid — the retrieval trade-off that drove the redesign</b></summary>
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
<summary><b>Data model — traceability designed in from the schema up</b></summary>
<br>
<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/architecture/data-model-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/architecture/data-model-light.svg">
  <img alt="Simplified conceptual data model" src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/architecture/data-model-dark.svg" width="100%">
</picture>
</div>
</details>

<img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/divider.svg" width="100%" alt="">

## Workflows

<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/workflows/sdlc-pipeline-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/workflows/sdlc-pipeline-light.svg">
  <img alt="Autonomous SDLC Platform implemented pipeline workflow" src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/workflows/sdlc-pipeline-dark.svg" width="100%">
</picture>
</div>

<details>
<summary><b>Hybrid RAG retrieval pipeline</b> — parallel semantic and keyword search, fused before generation</summary>
<br>
<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/workflows/hybrid-pipeline-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/workflows/hybrid-pipeline-light.svg">
  <img alt="Hybrid RAG technical workflow" src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/workflows/hybrid-pipeline-dark.svg" width="100%">
</picture>
</div>
</details>

<details>
<summary><b>Vectorless RAG retrieval pipeline</b> — the keyword-only baseline</summary>
<br>
<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/workflows/vectorless-pipeline-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/workflows/vectorless-pipeline-light.svg">
  <img alt="Vectorless RAG technical workflow" src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/workflows/vectorless-pipeline-dark.svg" width="100%">
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

<img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/divider.svg" width="100%" alt="">

## Tech Stack

<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/icons/stack-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/icons/stack-light.svg">
  <img alt="Technology stack" src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/icons/stack-dark.svg" width="100%">
</picture>
</div>

<img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/divider.svg" width="100%" alt="">

## Demo Gallery

<div align="center">

**Vectorless RAG** — a document-grounded answer with performance metrics and its full citation trace

<img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/gifs/vectorless-rag.gif" width="100%" alt="Vectorless RAG chatbot answering a document-grounded query">

<br>

**Hybrid RAG** — retrieval transparency, with every retrieved chunk and its source ranked in view

<img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/gifs/hybrid-rag.gif" width="100%" alt="Hybrid RAG chatbot showing citation trace">

<br>

**Autonomous SDLC Platform** — orchestration dashboard, requirements workspace, architecture workspace

<img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/gifs/sdlc-platform.gif" width="100%" alt="SDLC platform dashboard and agent workspaces">

</div>

<details>
<summary><b>Full-resolution stills</b></summary>
<br>

| | |
|:--:|:--:|
| <img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/images/vectorless-interface.png" width="100%"> | <img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/images/hybrid-interface.png" width="100%"> |
| Vectorless RAG — conversational interface | Hybrid RAG — conversational interface |
| <img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/images/hybrid-citations.png" width="100%"> | <img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/images/sdlc-dashboard.png" width="100%"> |
| Hybrid RAG — citation trace | SDLC Platform — orchestration dashboard |
| <img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/images/sdlc-requirements.png" width="100%"> | <img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/images/sdlc-architecture.png" width="100%"> |
| SDLC Platform — requirements workspace | SDLC Platform — architecture workspace |

</details>

<img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/divider.svg" width="100%" alt="">

## Résumé

<table>
<tr>
<td width="34%" valign="top">
<a href="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/resume/Ishrat-Bhullar-Resume.pdf">
<img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/resume/resume-preview.png" width="100%" alt="Résumé preview">
</a>
</td>
<td valign="top">

**Ishrat Bhullar** — AI Engineer
Retrieval-Augmented Generation & Backend Systems

Single-page, ATS-friendly. Covers the EY AI engineering internship, the multi-agent SDLC platform, and the retrieval work behind both chatbots.

<a href="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/resume/Ishrat-Bhullar-Resume.pdf"><b>⤓ Download PDF</b></a>
&nbsp;·&nbsp;
<a href="https://github.com/Ishrat-Bhullar/Ishrat-Bhullar/blob/main/assets/resume/Ishrat-Bhullar-Resume.pdf"><b>Preview in browser</b></a>

**B.E. Computer Engineering** · Thapar Institute of Engineering & Technology, Patiala · 2022–2026

</td>
</tr>
</table>

<img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/divider.svg" width="100%" alt="">

## GitHub Stats

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/stats-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/stats-light.svg">
  <img alt="GitHub statistics" src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/stats-dark.svg" width="47%">
</picture>
&nbsp;&nbsp;
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/languages-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/languages-light.svg">
  <img alt="Most used languages" src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/languages-dark.svg" width="47%">
</picture>

<br><br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/contributions-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/contributions-light.svg">
  <img alt="Contribution activity" src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/contributions-dark.svg" width="100%">
</picture>

<br><br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/output/github-snake-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/output/github-snake-light.svg">
  <img alt="Contribution grid animation" src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/output/github-snake-dark.svg" width="100%">
</picture>

</div>

### Recent Activity

<!--START_SECTION:activity-->
- Pushed to [Ishrat-Bhullar](https://github.com/Ishrat-Bhullar/Ishrat-Bhullar) &nbsp;·&nbsp; <sub>today</sub>
- Pushed to [rag-chatbot-mongodb](https://github.com/Ishrat-Bhullar/rag-chatbot-mongodb) &nbsp;·&nbsp; <sub>today</sub>
- Pushed to [sdlc-platform](https://github.com/Ishrat-Bhullar/sdlc-platform) &nbsp;·&nbsp; <sub>today</sub>
- Pushed to [vectorless-chatbot](https://github.com/Ishrat-Bhullar/vectorless-chatbot) &nbsp;·&nbsp; <sub>today</sub>
- Created branch `main` in [Ishrat-Bhullar](https://github.com/Ishrat-Bhullar/Ishrat-Bhullar) &nbsp;·&nbsp; <sub>yesterday</sub>
<!--END_SECTION:activity-->

<img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/divider.svg" width="100%" alt="">

## Contact

<div align="center">

<a href="https://www.linkedin.com/in/ishrat-bhullar-4a1441295/"><b>LinkedIn</b></a>
&nbsp;&nbsp;·&nbsp;&nbsp;
<a href="mailto:ishratbhullar@gmail.com"><b>ishratbhullar@gmail.com</b></a>
&nbsp;&nbsp;·&nbsp;&nbsp;
<a href="https://github.com/Ishrat-Bhullar"><b>GitHub</b></a>
&nbsp;&nbsp;·&nbsp;&nbsp;
<a href="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/resume/Ishrat-Bhullar-Resume.pdf"><b>Résumé</b></a>

<br>

<sub>Open to AI engineering and backend roles · Patiala, India</sub>

</div>

<img src="https://raw.githubusercontent.com/Ishrat-Bhullar/Ishrat-Bhullar/main/assets/divider.svg" width="100%" alt="">

<div align="center">
<sub>
Architecture and workflow diagrams are redrawn as vector artwork from my Project Semester Report,<br>
<i>Enterprise AI Systems: Document Intelligence and Autonomous Multi-Agent Software Delivery at Ernst &amp; Young</i>.<br>
Interface stills are from the same report. Per enterprise confidentiality, no source code,<br>
prompt text or internal configuration is reproduced — systems are shown at architecture level only.<br><br>
Diagrams, chips and demos are generated by the scripts in <a href="https://github.com/Ishrat-Bhullar/Ishrat-Bhullar/tree/main/scripts"><code>scripts/</code></a>.
</sub>
</div>
