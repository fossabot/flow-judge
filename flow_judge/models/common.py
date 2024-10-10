from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .adapters.base import BaseAPIAdapter


class BaseFlowJudgeModel(ABC):
    """Base class for all FlowJudge models."""

    def __init__(
        self, model_id: str, model_type: str, generation_params: dict[str, Any], **kwargs: Any
    ):
        """Initialize the base FlowJudge model."""
        self.metadata = {
            "model_id": model_id,
            "model_type": model_type,
            "generation_params": generation_params,
            "kwargs": kwargs,
        }

    @abstractmethod
    def _generate(self, prompt: str) -> str:
        """Generate a response based on the given prompt."""
        pass

    @abstractmethod
    def _batch_generate(
        self, prompts: list[str], use_tqdm: bool = True, **kwargs: Any
    ) -> list[str]:
        """Generate responses for multiple prompts."""
        pass


class AsyncBaseFlowJudgeModel(ABC):
    """Base class for asynchronous FlowJudge models."""

    def __init__(
        self, model_id: str, model_type: str, generation_params: dict[str, Any], **kwargs: Any
    ):
        """Initialize the base asynchronous FlowJudge model."""
        self.metadata = {
            "model_id": model_id,
            "model_type": model_type,
            "generation_params": generation_params,
            "kwargs": kwargs,
        }

    @abstractmethod
    async def _async_generate(self, prompt: str) -> str:
        """Generate a response based on the given prompt asynchronously."""
        pass

    @abstractmethod
    async def _async_batch_generate(
        self, prompts: list[str], use_tqdm: bool = True, **kwargs: Any
    ) -> list[str]:
        """Generate responses for multiple prompts asynchronously."""
        pass


class FlowJudgeRemoteModel(BaseFlowJudgeModel):
    """
    Flow judge model class for remote hosting.
    Expects the api_adapter to return a str message for generate.
    Expects the api_adapter to return a list of str messages for batch generate
    """
    def __init__(
            self, 
            model_id: str, 
            model_type: str, 
            generation_params: dict[str, Any],
            api_adapter: BaseAPIAdapter,
            **remote_kwargs: Any
        ):
        super().__init__(model_id, model_type, generation_params, **remote_kwargs)

        if not isinstance(api_adapter, BaseAPIAdapter):
            raise ValueError("Invalid Adapter type. Use BaseAPIAdapter.")
        
        self.api_adapter = api_adapter
    
    def generate(self, prompt: str) -> str:
        conversation = [{"role": "user", "content": prompt.strip()}]
        return self.api_adapter.fetch_response(conversation)

    def batch_generate(
            self, 
            prompts: list[str], 
            use_tqdm: bool = True, 
            **kwargs: Any
        ) -> list[str]:
        conversations = [[{"role": "user", "content": prompt.strip()}] for prompt in prompts]
        return self.api_adapter.fetch_batched_response(conversations)


class GenerationParams(BaseModel):
    temperature: float = 0.1
    top_p: float = 0.95
    max_new_tokens: int = 1000
    do_sample: bool = True

class VllmGenerationParams(GenerationParams):
    max_tokens: Optional[int] = None
    stop_token_ids: List[int] = [32007,32001,32000]
    def __init__(self, **data):
        super().__init__(**data)
        self.max_tokens = self.max_new_tokens
        del self.max_new_tokens
        del self.do_sample


class ModelType(Enum):
    """Enum for the type of model."""

    TRANSFORMERS = "transformers"
    VLLM = "vllm"
    VLLM_ASYNC = "vllm_async"
    LLAMAFILE = "llamafile"
    BASETEN_VLLM = "baseten_vllm"


class Engine(Enum):
    VLLM = "vllm"
    VLLM_ASYNC = "vllm_async"
    HF = "hf"  # HF stands for Hugging Face (Transformers)
    LLAMAFILE = "llamafile"


class ModelConfig:
    """Base configuration for a model."""

    def __init__(
        self,
        model_id: str,
        model_type: ModelType,
        generation_params: Dict[str, Any],
        **kwargs: Any,
    ):
        self.model_id = model_id
        self.model_type = model_type
        self.generation_params = generation_params
        self.kwargs = kwargs
