import functools
import pika
import json
from concurrent.futures import ThreadPoolExecutor
from agents import AiAgent
from state import State
import os
import threading
import time
from datetime import datetime
from consts import kb_docs


ai_agent = AiAgent(
    db_uri=os.getenv("POSTGRES_URI", "postgresql://postgres:test@localhost:5432/bot-sql"),
    model="gemini-2.0-flash-001",
    examples=[
        {
            "input": "How many employees are there?",
            "query": "SELECT count(*) FROM employees",
        }
    ],
)

ai_agent.write_in_kb(kb_docs)
thread = ThreadPoolExecutor(max_workers=5)


def multithread_queue_handler(ch, props, answer, delivery_tag):
    try:
        if props.reply_to:
            ch.basic_publish(
                exchange="",
                routing_key=props.reply_to,
                properties=pika.BasicProperties(
                    correlation_id=props.correlation_id
                ),
                body=json.dumps(answer),
            )
        ch.basic_ack(delivery_tag=delivery_tag)
    except Exception as e:
        print(f"Failed to publish or ack: {e}")
        ch.basic_nack(delivery_tag=delivery_tag, requeue=False)


def handle_message(ch, method, props, req):
    def thread_handler():
        start = time.time()
        thread_name = threading.current_thread().name
        try:
            body = json.loads(req)
            question = body.get("question", "")
            print(f"[{datetime.now()}] [Thread {thread_name}] START question: {question}")

            try:
                query = ai_agent.generate_sql_query(question)
                result = ai_agent.run_sql_query(query)
            except Exception as e:
                print(f"Cant generate SQL query: {e}. Trying knowledge base")
                query = None
                result = None

            state = State(question=question, query=query, result=result)
            answer = ai_agent.generate_answer(state)

            cb = functools.partial(multithread_queue_handler, ch, props, answer, method.delivery_tag)
            ch.connection.add_callback_threadsafe(cb)

        except Exception as e:
            print(f"Error while processing message: {str(e)}")
            nack_cb = functools.partial(ch.basic_nack, delivery_tag=method.delivery_tag, requeue=False)
            ch.connection.add_callback_threadsafe(nack_cb)
        finally:
            end = time.time()
            print(f"[{datetime.now()}] [Thread {thread_name}] DONE in {end - start:.2f}s")

    thread.submit(thread_handler)


def start_main_process():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=os.getenv("RABBITMQ_HOST", "localhost"),
            port=5672,
            credentials=pika.PlainCredentials(
                username=os.getenv("RABBITMQ_USER", "rabbit"),
                password=os.getenv("RABBITMQ_PASS", "rabbitpass"),
            ),
        )
    )

    ch = connection.channel()
    ch.queue_declare(queue="rmq_question_queue", durable=True)
    ch.basic_qos(prefetch_count=5)
    ch.basic_consume(queue="rmq_question_queue", on_message_callback=handle_message)

    print("App is ready to process questions...")
    ch.start_consuming()


start_main_process()
