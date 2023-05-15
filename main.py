from typing import Any, Awaitable, Callable, Dict, Iterator, List, Union, Optional

import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from starlette.types import Send
from pydantic import BaseModel
from langchain.chat_models import ChatOpenAI
from langchain.schema import BaseMessage
from langchain.callbacks.base import AsyncCallbackHandler, BaseCallbackManager

import api_utils as utils


class Request(BaseModel):
    answer: Dict[str, Union[str, List[str]]]


app = FastAPI()

questions_list = utils.load_questions()


Sender = Callable[[Union[str, bytes]], Awaitable[None]]


class EmptyIterator(Iterator[Union[str, bytes]]):
    def __iter__(self):
        return self

    def __next__(self):
        raise StopIteration


class AsyncStreamCallbackHandler(AsyncCallbackHandler):
    """Callback handler for streaming, inheritance from AsyncCallbackHandler."""

    def __init__(self, send: Sender):
        super().__init__()
        self.send = send

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Rewrite on_llm_new_token to send token to client."""
        await self.send(f"{token}")


class ChatOpenAIStreamingResponse(StreamingResponse):
    """Streaming response for openai chat model, inheritance from StreamingResponse."""

    def __init__(
        self,
        generate: Callable[[Sender], Awaitable[None]],
        status_code: int = 200,
        media_type: Optional[str] = None,
    ) -> None:
        super().__init__(
            content=EmptyIterator(), status_code=status_code, media_type=media_type
        )
        self.generate = generate

    async def stream_response(self, send: Send) -> None:
        """Rewrite stream_response to send response to client."""
        await send(
            {
                "type": "http.response.start",
                "status": self.status_code,
                "headers": self.raw_headers,
            }
        )

        async def send_chunk(chunk: Union[str, bytes]):
            if not isinstance(chunk, bytes):
                chunk = chunk.encode(self.charset)
            await send({"type": "http.response.body", "body": chunk, "more_body": True})

        # send body to client
        await self.generate(send_chunk)

        # send empty body to client to close connection
        await send({"type": "http.response.body", "body": b"", "more_body": False})


def send_message(
    message: List[BaseMessage], model_name: str
) -> Callable[[Sender], Awaitable[None]]:
    async def generate(send: Sender):
        model = ChatOpenAI(
            model_name=model_name,
            streaming=True,
            verbose=True,
            callback_manager=BaseCallbackManager([AsyncStreamCallbackHandler(send)]),
        )
        await model.agenerate(messages=[message])

    return generate


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/generate/")
def get_workout_plan(answers: Request):
    qa_messages = utils.generate_qa_messages(
        questions_list=questions_list, answers=answers.answer
    )

    prompts = utils.generate_prompt(qa_messages=qa_messages)

    response = ChatOpenAIStreamingResponse(
        send_message(message=prompts, model_name="gpt-3.5-turbo"),
        media_type="text/event-stream",
    )

    return response

    # parsed_response = utils.parse_response(response=response)


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info", reload=True)
