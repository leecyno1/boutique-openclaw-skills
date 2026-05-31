# Add a New Benchmark

Extend SkillOpt with your own benchmark in ~100 lines of code.

## Overview

To add a benchmark, you need:

1. **Data Loader** — Loads and splits your dataset
2. **Environment Adapter** — Executes tasks and returns scores
3. **Config** — YAML configuration file

## Step 1: Create the Benchmark Package

```bash
mkdir -p skillopt/envs/my_benchmark
touch skillopt/envs/my_benchmark/__init__.py
```

## Step 2: Implement the Data Loader

Create `skillopt/envs/my_benchmark/loader.py`:

```python
from skillopt.data.base import DataLoader, DataItem

class MyBenchmarkDataLoader(DataLoader):
    """Load and split your benchmark data."""
    
    def __init__(self, data_dir: str, **kwargs):
        super().__init__(**kwargs)
        self.data_dir = data_dir
    
    def setup(self, cfg: dict):
        """Initialize splits based on config."""
        self.split_mode = cfg.get('split_mode', 'ratio')
        # Load your data here
        self.items = self._load_items()
        self._create_splits(cfg)
    
    def _load_items(self) -> list[DataItem]:
        """Load raw data into DataItem objects."""
        items = []
        # TODO: Load your data
        for entry in your_data:
            items.append(DataItem(
                id=entry['id'],
                input=entry['question'],
                ground_truth=entry['answer'],
                metadata=entry.get('metadata', {})
            ))
        return items
    
    def get_split_items(self, split: str) -> list[DataItem]:
        """Return items for a given split (train/valid/test)."""
        return self.splits[split]
```

## Step 3: Implement the Environment Adapter

Create `skillopt/envs/my_benchmark/env.py`:

```python
from skillopt.envs.base import EnvAdapter, TaskResult

class MyBenchmarkEnv(EnvAdapter):
    """Execute tasks and evaluate results."""
    
    def __init__(self, cfg: dict):
        super().__init__(cfg)
    
    async def execute(self, item: DataItem, skill: str, model) -> TaskResult:
        """
        Execute a single task.
        
        Args:
            item: The data item to process
            skill: Current skill document content
            model: The target model instance
            
        Returns:
            TaskResult with prediction, score, and trajectory
        """
        # Build prompt with skill document
        prompt = self.build_prompt(item, skill)
        
        # Get model response
        response = await model.generate(prompt)
        
        # Extract prediction
        prediction = self.parse_response(response)
        
        # Score against ground truth
        score = self.evaluate(prediction, item.ground_truth)
        
        return TaskResult(
            item_id=item.id,
            prediction=prediction,
            score=score,
            trajectory=[
                {"role": "system", "content": skill},
                {"role": "user", "content": item.input},
                {"role": "assistant", "content": response}
            ]
        )
    
    def evaluate(self, prediction: str, ground_truth: str) -> float:
        """
        Score a prediction against ground truth.
        
        Returns:
            Float between 0.0 and 1.0
        """
        # TODO: Implement your scoring logic
        # Examples: exact match, F1, ANLS, etc.
        return float(prediction.strip() == ground_truth.strip())
    
    def build_prompt(self, item, skill: str) -> str:
        """Combine skill document with task input."""
        return f"{skill}\n\n---\n\nQuestion: {item.input}"
    
    def parse_response(self, response: str) -> str:
        """Extract the answer from model response."""
        return response.strip()
```

## Step 4: Register the Benchmark

Add to `skillopt/envs/__init__.py`:

```python
from .my_benchmark.env import MyBenchmarkEnv
from .my_benchmark.loader import MyBenchmarkDataLoader

BENCHMARK_REGISTRY = {
    # ... existing benchmarks ...
    'my_benchmark': {
        'env': MyBenchmarkEnv,
        'loader': MyBenchmarkDataLoader,
    },
}
```

## Step 5: Create Config

Create `configs/my_benchmark/default.yaml`:

```yaml
_base_: ['../_base_/default.yaml']

env:
  name: my_benchmark
  data_path: data/my_benchmark
  split_mode: ratio
  split_ratio: "2:1:7"

train:
  num_epochs: 4
  batch_size: 40

optimizer:
  learning_rate: 4
  lr_scheduler: cosine
  use_slow_update: true
  use_meta_skill: true

gradient:
  analyst_workers: 16
```

## Step 6: Run

```bash
python scripts/train.py --config configs/my_benchmark/default.yaml
```

## Tips

!!! tip
    - Use a small `batch_size` (10-20) for initial testing
    - The `evaluate()` method is critical — a noisy metric will confuse the optimizer
