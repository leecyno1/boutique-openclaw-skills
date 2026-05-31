# API Reference

## Core Classes

### `EnvAdapter`

Abstract base class for benchmark environments.

```python
class EnvAdapter(ABC):
    async def execute(self, item, skill, model) -> TaskResult
    def evaluate(self, prediction, ground_truth) -> float
    def build_prompt(self, item, skill) -> str
```

### `DataLoader`

Abstract base class for data loading and splitting.

```python
class DataLoader(ABC):
    def setup(self, cfg: dict) -> None
    def get_split_items(self, split: str) -> list[DataItem]
```

### `ModelBackend`

Abstract base class for LLM backends.

```python
class ModelBackend(ABC):
    async def generate(self, messages, **kwargs) -> ModelResponse
    async def generate_with_tools(self, messages, tools, **kwargs) -> ModelResponse
```

### `Trainer`

Main training loop orchestrator.

```python
class Trainer:
    def __init__(self, cfg: dict)
    async def train(self) -> TrainResult
    async def evaluate(self, skill: str, split: str) -> EvalResult
```

## Data Classes

### `DataItem`

```python
@dataclass
class DataItem:
    id: str
    input: str
    ground_truth: str
    metadata: dict = field(default_factory=dict)
```

### `TaskResult`

```python
@dataclass
class TaskResult:
    item_id: str
    prediction: str
    score: float
    trajectory: list[dict]
```

### `ModelResponse`

```python
@dataclass
class ModelResponse:
    content: str
    usage: dict
    model: str
```

For detailed source code, see the [`skillopt/`](https://github.com/microsoft/SkillOpt/tree/main/skillopt) directory.
