class BaseLLM:
    def run(self, prompt: str) -> str:
        raise NotImplementedError("Subclasses must implement the 'run' method")