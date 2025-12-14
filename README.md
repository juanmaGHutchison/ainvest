# Autonomous AI-Based Trading System

An event-driven trading system that combines real-time financial news, large language models, and quantitative market analysis to make automated trading decisions.

The platform is designed around loosely coupled services, enabling scalable experimentation with different data sources, AI models, and trading strategies.

---

## 🧠 System Overview

The system continuously monitors financial news, evaluates short-term market sentiment using AI models, and executes trades based on predictive analytics and predefined risk rules.

At a high level, the system consists of:

- A **signal generation layer** driven by AI
- A **message-based coordination layer**
- A **decision and execution layer** for trading actions

---

## 🧩 Core Components

### Signal Producer
- Collects financial news
- Applies rule-based pre-filtering
- Uses LLMs to assess short-term sentiment
- Emits structured trading signals

### Signal Consumer
- Processes incoming trading signals
- Fetches historical market data
- Runs predictive models (LSTM)
- Executes trades through a broker API

### Message Broker
- Decouples producers from consumers
- Ensures reliable signal delivery

### Cache / State Store
- Maintains shared application state
- Improves performance and consistency

---

## 🛠 Technology Choices

The system integrates multiple technologies, including:

- Python-based AI and data processing
- Large Language Models (LLMs)
- Time-series prediction models (LSTM)
- Message queues
- In-memory caching
- External broker APIs

Implementation details (containers, orchestration, etc.) are covered later.

---

## ⚙️ Configuration Model

This project separates configuration concerns into **two distinct layers**.

### Application Configuration (`src/config.env`)

A dedicated configuration file defines **user-controlled runtime behavior**, including:
- Trading rules and thresholds
- AI model configuration
- External service connectivity
- Logging behavior

This file is **required** for the system to operate.

> The exact parameters are intentionally not documented here to keep the configuration flexible and evolvable.

---

### Infrastructure Configuration (`docker/config.env`)

Infrastructure-related values such as service names, ports, volumes, and networking are managed separately.

These settings control **how the system is deployed**, not how it behaves.

---

## 🚀 Running the System

### Prerequisites
- Docker
- Docker Compose
- NVIDIA GPU support for model execution

### Unified Launcher (`ainvest.sh`)
The system is started using a single launcher script:

```bash
docker/scritps/ainvest.sh
```

This script acts as the entry point for the entire platform and is responsible for:
- Building or updating runtime images if they do not exist
- Initializing the full execution stack
- Starting all system components in the correct order

Once the script is available in your PATH, the system can be launched from any directory.

```bash
ainvest.sh
```

---

🔄 Execution Flow

News is ingested from external sources
Signals are generated using AI models
Signals are published to the message broker
Predictive models evaluate market conditions
Trades are executed based on confidence and risk rules

🔐 Security & Safety

API keys and credentials must never be committed
Use environment-specific configuration files
Prefer secrets management solutions for production

⚠️ Disclaimer

This system is intended for research and educational use only.
It does not provide financial advice.
Always use paper trading and validate strategies before real-world deployment.

📜 License

See `LICENSE` file.

🤝 Contributions

Design discussions, improvements, and pull requests are welcome.
Building autonomous systems responsibly 🤖📈

