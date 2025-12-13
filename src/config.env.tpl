################################## QUEUE CONFIGURATION
# Queue configuration used for the producer-consumer

# Name of the docker container for the queue implementation
QUEUE__DOCKER_NAME="kafka"

# Queue connection port
QUEUE__PORT=9092

# Topics to subscribe in
QUEUE__MAIN_TOPIC="generic_stock"

# Threshold after LLM's response which includes a score. If the score provided by LLM is greater than the one configured here, the invest action will be performed
QUEUE__SCORE_THRESHOLD=10

# Name of the docker container for cache
CACHE__HOST="redis"

# Cache service port to connect to
CACHE__PORT=6379

################################## BROKER CONFIGURATION
# Broker configuration used for trading

# Broker API endpoint
BROKER__API_ENDPOINT=https://paper-api.alpaca.markets

# Broker API key
BROKER__API_KEY=

# Broker API secret key
BROKER__API_SECRET=

# Comma-separated list of stock tickers to exclude from processing. E.g. AAPL,TSLA,DIA
BROKER__BLACKLIST=

# Maximum amount to be invested in one operation. If the ticker is more expensive than this value, the operation will be ommitted. Value in dollars($)
BROKER__MAX_INVEST=

# Stop trading if prices drops this percentage bellow the current price.
# Positive Ingetger value.
# The value will be applied over the price of the current operation.
BROKER__STOP_LOSS_PERCENTAGE=10

# Default amount of money to use for each trade. The APP starts with this amount and can adjust it up or down depending on market conditions. (base money for each operation, if the operation is good, more money will be spent)
# It shall be a possitive integer
BROKER__BASE_INVESTMENT=5

# The number of days back to fetch historical data for each operation.
# Too high value - Slower performance, higher resource usage and possible API limits.
# Too few days - Less reliable analysis, fewer trading signals.
# Value shall be a possitive integer
# NOTE: This value shall be greater than MATHS__WINDOW_SIZE_DAYS. If not APP will crash
# Tip: Select an intermediate value for smoother configuration (60-120 days)
BROKER__HISTORIC_LOOKBACK_DAYS=180

################################## LLM CONFIGURATION
# AI model settings to process news

# LLM API key
LLM__API_KEY=

# LLM OpenAI base URL to connect to
LLM__BASE_URL=

# LLM available models. This list will failover if one fails. Priority is highest the first
LLM__OPENAI_MODELS="gpt-4.1,gpt-4o,gpt-4o-mini,gpt-4.1-mini,gpt-4.1-nano"

# Parameter valid for OpenAI. Temperature: Indicates the randomness or diversity allowed in the model. Possible values:
# - 0.0		Deterministic - Always gives the same, most likely response.
# - 0.3 - 0.7	Slight variation, but still focused
# - 1.0 	Default - Balanced creativity and coherence
# - 1.3 - 2.0	Very random and creative - can become inconsistent or "imaginative"
LLM__OPENAI_MODEL_TEMPERATURE=0.7

# Parameter valid for OpenAI. Top_p: Filters the set of tokens to only the most probable ones whose cumulative probabilty reaches 'top_p'. The model then samples from that subset, which affects diversity and creativity.
# It is a float value within 0.0 and 1.0 where the lower value is more focused with deterministic outputs, while the higher values are more creative and diverse.
LLM__OPENAI_MODEL_TOP_P=1.0

################################## PROMPT CONFIGURATION
# Prompt configuration given to AI model

# Prompt template to send the request
PROMPT__INPUT_TPL="You will be given a JSON object like this: %s. Your task: 1. Analyze the 'headline' and 'summary'. 2. Evaluate how positive the news is for short-term investment in the given ticker within the specified X-Y day range. 3. Respond ONLY with a JSON object without the json block markers, using this exact structure: %s. Rules: No extra text. Always use the exact same fields in the same order. Score must reflect short-term sentiment only. 'estimated_days' should be your best guess of how soon the impact is likely to occur."

# Prompt format to receive the response
PROMPT__OUTPUT_TPL='{"ticker": "<same as input>", "news": {"headline": "<same as input>", "summary": "<same as input>"}, "score": <integer from 0 to 100>, "rationale": "<1-2 sentence explanation>", "estimated_days": <integer representing estimated days for impact to materialize>}'

################################## MATHS
# How many past days of price history the model uses to understand trends
# - Larger = more stable but slower
# - Smaller = more reactive
# NOTE: This value shall be lower than BROKER__HISTORIC_LOOKBACK_DAYS. If not APP will crash
MATHS__WINDOW_SIZE_DAYS=90

################################## LOG MANAGER
# Log filters file relative to source code root path
LOGM__CONFIG_FILE="libs/log_manager/logging.yaml"

# Logging class name:
LOGM__PRODUCER="producer"
LOGM__CONSUMER="consumer"
LOGM__BROKER="broker.facade"
LOGM__LLM="llm.facade"
LOGM__OPENAI="llm.openai.client"
LOGM__QUEUE="queue.adapter"
LOGM__MATHS_LSTM="maths.strategy.lstm"
LOGM__PROMPT_MANAGER="prompt_manager"
