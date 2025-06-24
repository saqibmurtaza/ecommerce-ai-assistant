# # TRACING_CONFIGURATION
# # Best for Debugging
import os
import json
from datetime import datetime
from pprint import pprint
from agents import set_default_openai_client, set_default_openai_api, set_trace_processors
from openai import AsyncOpenAI
from agents.tracing.processor_interface import TracingProcessor

class LocalTraceProcessor(TracingProcessor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.traces = []
        self.spans = []

    def _save_trace_to_file(self, trace):  # <<< ✅ ADD THIS
        with open(self.file_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(trace.export(), indent=2) + ",\n")

    def on_trace_start(self, trace):
        self.traces.append(trace)
        self._save_trace_to_file(trace)

    def on_trace_end(self, trace):
        print(f"Trace ended: {trace.export()}")

    def on_span_start(self, span):
        self.spans.append(span)

    def on_span_end(self, span):
        pass  # Skip noisy logging here

    def force_flush(self):
        pass

    def shutdown(self):
        print("=======Shutting down trace processor========")
       
        data = {
            "traces": [trace.export() for trace in self.traces],
            "spans": [span.export() for span in self.spans]
        }
        with open(self.file_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, indent=2) + ",\n")

# def _save_trace_to_file(self, trace):  # <<< Added missing method
#         trace_data = trace.export()
#         filename = f"{self.file_path.replace('.json', '')}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json"
#         with open(filename, "w", encoding="utf-8") as f:
#             json.dump(trace_data, f, indent=2)
#         print(f"📄 Trace saved to {filename}")  # <<< confirmation

def init_tracing():
    base_url = os.getenv("BASE_URL")
    api_key = os.getenv("API_KEY")
    model_name = os.getenv("MODEL_NAME")

    if not base_url or not api_key or not model_name:
        raise ValueError("Missing BASE_URL / GEMINI_API_KEY / MODEL_NAME")

    client = AsyncOpenAI(base_url=base_url, api_key=api_key)
    set_default_openai_client(client=client, use_for_tracing=True)
    set_default_openai_api("chat_completions")

    processor = LocalTraceProcessor(file_path="debug_traces.json")
    set_trace_processors([processor])

    return model_name

