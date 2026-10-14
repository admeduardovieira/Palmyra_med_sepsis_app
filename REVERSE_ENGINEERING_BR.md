# 🔬 Engenharia Reversa → Versão Brasileira (BR)

## Visão Geral da Arquitetura Sepsis

### Arquitetura de 3 camadas

```
┌─────────────────────────────────────────────────────────────────┐
│                    CREATING_CHROMA_DBs                          │
│   (viapascurta-tech) Creates vector databases                 │
│                                                                 │
│   Articles_sample_list.txt   →  ChromaDB PersistentClient       │
│   (23 artigos de sepse)          sepsis_management_chroma_db     │
│                                 sepsis_antibiotics_chroma_db    │
│                                 sepsis_guidelines_chroma_db     │
│                                                                   │
│   Embedding: BAAI/bge-base-en-v1.5 (cosine)                      │
│   Orquestração: LlamaIndex 0.12.5                                │
└──────────────┬───────────────────┬──────────────────────────────┘
               │                   │
               ▼                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                   MULTI-AGENT-APPROACH                            │
│   (viapascurta-tech) 3 agentes CrewAI                            │
│                                                                │
│   Agent 1: Sepsis Management Advisor   → queries sepsis_management     │
│   Agent 2: Antibiotic Specialist       → queries sepsis_antibiotics       │
│   Agent 3: Compliance Officer          → queries sepsis_management_guidelines │
│                                                                │
│   LLM: Writer Palmyra-med 70B (NVIDIA)                          │
│   Framework: CrewAI 0.86.0                                     │
└──────────────┬─────────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PALMYRA_MED_SEPSIS_APP                       │
│   (viapascurta-tech) App Shiny UI                               │
│                                                                │
│   GUI (Shiny for Python 0.10.2)                                │
│   Inputs: Diagnosis, Demographic, Vital signs, Lab findings,   │
│           Medical history, Special comments (site of infection) │
│   Buttons: Get recommendations | Get antibiotics | Get compliance│
│                                                                │
│   Connects to: 3 Chroma DBs (shared via filesystem)            │
│   Cloud version: GPT-3.5-turbo @ https://huggingface.co/spaces/ │
│                LlmRAGbasedAPPs/LLM_MA_RAG_Sepsis                │
│                                                                │
│   Contact author: victor.iapascurta@usmf.md                    │
│   Version: ISAAC_sepsis 3.0                                    │
└─────────────────────────────────────────────────────────────────┘
```

### Origem do Projeto (Engenharia Reversa)

- **Autor original**: Victor Iapascurta (victor.iapascurta@usmf.md)
- **Instituição**: USMF (Universitatea de Stat din Medicina si Farmacia "Nicolae Anestiadi" din Cahul, Moldávia)
- **Financiamento**:
  - PN-IV-PCB-RO-MD-2024-036 "DACISLAB" (laboratório virtual de dados abertos)
  - 25.00208.5007.07/PD (NARD — National Agency for Research and Development of Moldova)
- **Arteido**: https://arxiv.org/pdf/2311.10537, https://arxiv.org/pdf/2312.10997
- **Conteúdo base**: 23 artigos sobre sepse (ver Articles_sample_list.txt)

---

## Plano de Adaptação para o Brasil (BR)

### 1. Substituição de LLM & Plataforma

| Componente | Original (Moldávia) | Para BR |
|---|---|---|
| Inference engine | Writer Palmyra-med 70B @ NVIDIA | PortuLLM ou GPT-4o (OpenAI BR) |
| API key env var | `NVIDIA_API_KEY` / `NVIDIA_BASE_URL` | `OPENAI_API_KEY` (ou AZURE_OPENAI_KEY) |
| Model name env | `NVIDIA_MODEL_NAME=writer/palmyra-med-70b` | `gpt-4o` ou `Portugal/fernus-70b` |

**Arquivos**: `app.py`, `Crewai_sepsis.ipynb`, `Creating_Chroma_DBs_sepsis.ipynb`

### 2. Substituição do Corpus de Literatura

**Problema**: Os 23 artigos são majoritariamente de revistas internacionais em inglês.

**Ação BR**:
- Adaptar a `Articles_sample_list.txt` para incluir artigos brasileiros sobre sepse:
  - Jornal de Pediatria (sepse pediátrica)
  - Revista da Sociedade Brasileira de Medicina Tropical
  - Revista Brasileira de Terapia Intensiva
  - Jornal de Nefrologia
  - Artigos do Ministério da Saúde sobre sepse
- Manter uma parcelação: 70% BR, 30% internacional (referência)

**Arquivo**: `Articles_sample_list.txt` → `Articles_sample_list_br.txt`

### 3. Diretrizes Clínicas

| Original | Para BR |
|---|---|
| Surviving Sepsis Campaign (internacional) | Diretrizes brasileiras: Portaria nº 207/2021, Jornal de Emergência, SBHSI |
| "sepsis_management" collection | Adicionar coleção `sepsis_management_br` |
| "sepsis_guidelines" collection | Substituir por diretrizes brasileiras |

### 4. Caminhos e Estrutura de Diretórios

```
# Original (Moldávia)
sepsis_management_chroma_db/
sepsis_antibiotics_chroma_db/
sepsis_guidelines_chroma_db/

# BR (proposta)
sepsis_management_br_chroma_db/
sepsis_antibiotics_br_chroma_db/
sepsis_guidelines_br_chroma_db/
```

### 5. Configuração de Dependências

| Pacote | Versão (original) | Observação BR |
|---|---|---|
| Python | 3.11.10 | 3.12 compatível |
| chromadb | 0.5.23 | OK |
| llama-index | 0.12.5 | OK |
| openai | 1.57.1 | ✅ usado no cloud version |
| BAAI/bge-base-en-v1.5 | embedding | ✅ ok para PT-BR |
| crewai | 0.86.0 | OK |
| shiny | 0.10.2 | ✅ compatível |

### 6. Plataforma e Deployment

| Aspecto | Original | Adaptação BR |
|---|---|---|
| Cloud | huggingface.co/spaces/LlmRAGbasedAPPs/LLM_MA_RAG_Sepsis | huggingface.co/spaces/admeduardovieira/isaac-sepsis-br |
| Contato | victor.iapascurta@usmf.md | eduardovieira@gmail.com (DUO operator) |
| Versão | ISAAC_sepsis 3.0 | ISAAC_sepsis_br 1.0 |

### 7. Fluxo de Implementação BR

```
FASE 1: Corpus
  1. Substituir Articles_sample_list.txt por artigos BR
  2. Regenerar os 3 Chroma DBs localmente
  3. Validar embedding (bge-base-en é multilingual, ok para PT)

FASE 2: Multi-agent
  4. Substituir NVIDIA env vars por OpenAI env vars
  5. Ajustar prompts para diretrizes brasileiras
  6. Validar CrewAI

FASE 3: App
  7. Substituir placeholder paths → paths BR
  8. Ajustar UI labels para PT-BR (Diagnóstico, Demografia, etc.)
  9. Atualizar "How to Use" para referenciar diretrizes BR
  10. Deploy no HuggingFace Spaces (admeduardovieira org)
```

### 8. Pontos de Atenção Engenharia Reversa

- **Ambiente original**: conda env `Python_3_11_10_MA` no Windows (caminho: `C:\Users\Victor\anaconda3\envs\Python_3_11_10_MA`)
- **Chave API**: Original usa `NVIDIA_API_KEY`. O cloud version usa `OPENAI_API_KEY` (GPT-3.5-turbo)
- **Chave não versionada**: `os.environ["NVIDIA_API_KEY"] = "Your NVIDIA_API_KEY"` — placeholder
- **Collection names** são fixos: `sepsis_management`, `sepsis_antibiotic_recommendations`, `sepsis_management_guidelines`
- **Embedding model**: `BAAI/bge-base-en-v1.5` — funciona para PT-BR (multilingual)