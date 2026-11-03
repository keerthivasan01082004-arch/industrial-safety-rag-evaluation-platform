# Industrial Safety RAG Evaluation Platform

A reproducible evaluation framework for comparing Retrieval-Augmented Generation (RAG) strategies on industrial-safety documentation.

The platform turns technical PDF manuals into searchable knowledge, evaluates multiple retrieval approaches, and produces structured metrics and analysis for comparing answer quality, retrieval behavior, and model performance.

> **Pipeline:** PDF documents → preprocessing → retrieval → answer generation → automated evaluation → comparative analysis

## Overview

Industrial and engineering manuals contain dense, long-context information that is difficult to evaluate with a single retrieval strategy. This project provides a modular workflow for testing approaches such as keyword retrieval, semantic retrieval, graph-based retrieval, and hybrid RAG pipelines against reproducible question-answer datasets.

The framework is designed for experimentation rather than a single application. New retrievers, judge models, metrics, and analysis modules can be added without restructuring the entire pipeline.

## Key capabilities

- Multi-stage PDF preparation with text extraction, document splitting, chunking, and embedding.
- Multiple retrieval approaches, including BM25, semantic/vector, graph-based, and vanilla RAG configurations.
- Interactive RAG generation and batch experiment workflows.
- Sequential or concurrent evaluation for scaling experiments.
- Automated LLM-as-a-judge assessment with configurable prompts and models.
- Traditional metrics such as cosine similarity, ROUGE-L, and BLEU.
- Row-count, key-presence, duplicate, and schema validation across pipeline stages.
- Analysis notebooks and scripts for comparing models, retrievers, and experiment runs.

## Architecture

```text
┌─────────────────────┐
│ Industrial PDF Docs │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Preprocessing       │  extraction · splitting · chunking · embeddings
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Retriever Builders   │  BM25 · semantic · graph · hybrid approaches
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ RAG Generation      │  context assembly · model response · trace output
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Evaluation Engine   │  metrics · LLM judge · batch/concurrent runs
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Analysis & Reports  │  merged results · comparisons · visualizations
└─────────────────────┘
```

## Evaluation workflow

1. **Prepare documents** — Extract and structure content from source PDF manuals.
2. **Build retrieval assets** — Create the indexes, embeddings, and retriever configurations required by each approach.
3. **Generate answers** — Run individual questions or batch experiments through the RAG pipeline.
4. **Evaluate outputs** — Compare generated answers with reference data using automatic metrics and configurable LLM judges.
5. **Validate and merge results** — Check row alignment, required keys, duplicates, and schema consistency before analysis.
6. **Analyze experiments** — Produce comparative summaries, plots, and model-to-model or approach-to-approach evaluations.

## Retrieval approaches

The framework is organized around interchangeable retrieval approaches, including:

- **BM25** for lexical keyword matching.
- **Semantic retrieval** using embedding similarity.
- **Graph-based retrieval** for connected context traversal.
- **Vanilla RAG** for baseline comparison.
- **Hybrid or extended approaches** that can be registered through the modular retriever layer.

## Metrics and validation

### Answer-quality metrics

- Cosine similarity
- ROUGE-L
- BLEU
- LLM-as-a-judge assessments for helpfulness and correctness against reference answers

### Data-integrity checks

- Row-count alignment across raw outputs, model responses, evaluations, and merged files
- Required-key and schema validation
- Duplicate detection
- Consistency checks before analysis and reporting

## Repository structure

```text
industrial-safety-rag-evaluation-platform/
├── system/
│   ├── analysis/       # Result summaries, metrics, and analysis utilities
│   ├── evaluation/     # Batch fetching, parsing, judging, and result merging
│   ├── preprocess/     # PDF processing and corpus construction
│   ├── rag/            # Retrieval approaches, generation, and RAG utilities
│   ├── scripts/        # Command-line workflow helpers
│   └── utils/          # Environment configuration and shared utilities
├── data/
│   ├── input/          # Source manuals and input documents
│   ├── preprocessed/   # Processed PDFs, test sets, and vector-store assets
│   └── results/        # RAG outputs, evaluation files, and summaries
├── notebooks/          # Experiment analysis and synthetic QA generation
├── requirements.txt    # Python dependencies
├── LICENSE
└── README.md
```

## Installation

```bash
git clone https://github.com/keerthivasan01082004-arch/industrial-safety-rag-evaluation-platform.git
cd industrial-safety-rag-evaluation-platform
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file for the services and models used by your experiment configuration. Typical variables may include:

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_VECTOR_STORE_ID=your_openai_vector_store_id
ASTRA_DB_API_ENDPOINT=your_astra_db_endpoint
ASTRA_DB_APPLICATION_TOKEN=your_astra_db_token
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_TRACING=true
```

Never commit real credentials, API tokens, or private documents to the repository.

## Running the workflow

The modular scripts live under `system/scripts/`. Adapt configuration values and input paths to your dataset before running an experiment.

### Preprocess documents

```bash
python -m system.scripts.preprocess_documents
```

### Build or inspect RAG experiments

The main orchestration modules are available in `system/main.py` and `system/main_long_context.py`. Retrieval implementations and generation utilities are located in `system/rag/`.

### Evaluate and merge results

```bash
python -m system.scripts.build_judge_batch
python -m system.scripts.fetch_batch_output
python -m system.scripts.merge_judge_results
python -m system.scripts.check_dups
```

### Analyze results

Use the analysis notebooks in `notebooks/` or the utilities in `system/analysis/` to compare retrieval approaches, judge scores, and model performance.

## Extending the framework

To add a new evaluation approach:

1. Implement the retriever or evaluator in the corresponding `system/rag/` or `system/evaluation/` module.
2. Register the approach in the project’s enums and configuration layer.
3. Add a reproducible test or experiment configuration.
4. Run the validation scripts before merging results.
5. Document the method and expected output format.

## Responsible evaluation

Evaluation scores are evidence for comparison, not a substitute for expert review. Results depend on document quality, question design, retrieval configuration, model behavior, and judge prompts. Benchmark findings should be interpreted with those limitations in mind, especially when evaluating safety-critical technical content.

## License

See [LICENSE](LICENSE) for the project license.
