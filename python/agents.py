from langchain.chains import create_sql_query_chain
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import FewShotPromptTemplate

from state import State
from db import AiDbConnection
from prompt_generation import (
    generate_sql_prompt,
    generate_is_in_db_prompt,
    generate_kb_prompt,
)

from consts import (
    default_human_support_error,
    unexpected_human_support_error,
    default_prefix,
    default_suffix,
    default_example_prompt,
    default_cant_be_answered,
)

from sentence_transformers import SentenceTransformer
import chromadb


class AiAgent(AiDbConnection):
    def __init__(
        self, db_uri: str, model: str, examples: list, temperature: float = 0.0
    ):
        super().__init__(
            # inherited from AiDbConnection
            db_uri=db_uri,
        )

        self.llm = ChatGoogleGenerativeAI(
            model=model,
            temperature=temperature,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )

        # not really important, but for the sake of consistency
        self.examples = examples

        # general prompt template for SQL query generation
        self.example_prompt = PromptTemplate.from_template(default_example_prompt)

        self.sql_extended_prompt_template = FewShotPromptTemplate(
            examples=self.examples,
            example_prompt=self.example_prompt,
            # this is more for initiating model, but it is not used in the final prompt
            # so it is not important
            prefix=default_prefix,
            # same here
            suffix=default_suffix,
            input_variables=["input", "top_k", "table_info"],
        )

        self.sql_chain = create_sql_query_chain(
            self.llm, self.db, prompt=self.sql_extended_prompt_template
        )

        # KB settings + chromadb
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.chroma_client = chromadb.Client()
        self.knowledge_base = self.chroma_client.create_collection(
            name="test_knowledge_base"
        )

    def can_be_answered_from_db(self, question: str) -> bool:
        prompt = generate_is_in_db_prompt(question)
        resp = self.llm.invoke(prompt).content.strip().upper()

        return "YES" in resp

    def write_in_kb(self, documents: list[str]):
        embeddings = self.embedding_model.encode(documents).tolist()
        self.knowledge_base.add(
            documents=documents,
            embeddings=embeddings,
            ids=[f"doc_{i}" for i in range(len(documents))],
        )

    # get info from the knowledge base
    def get_kb_context(self, question: str, top_k: int = 10) -> str:
        query_embedding = self.embedding_model.encode([question])[0]
        results = self.knowledge_base.query(
            query_embeddings=[query_embedding], n_results=top_k
        )

        return "\n".join(results["documents"][0]) if results["documents"] else ""

    def generate_sql_query(self, question: str) -> str:
        if not self.can_be_answered_from_db(question):
            raise ValueError("unrelated to the SQL query")

        resp = self.sql_chain.invoke({"question": question})
        # just crutch because gemini return sql query with ```sql
        return resp.strip("`sql")

    def generate_answer(self, state: State):
        try:
            # check if the question can not be answered from the database
            # using kb then
            if not state["result"] or state["result"] in ("[]", "{}", "None"):
                kb_context = self.get_kb_context(state["question"])

                if not kb_context:
                    return {"answer": default_human_support_error}
                prompt = generate_kb_prompt(kb_context, state)

            else:
                prompt = generate_sql_prompt(state)

            resp = self.llm.invoke(prompt)
            if default_cant_be_answered in resp.content:
                return {"answer": default_human_support_error}
            return {"answer": resp.content}

        except Exception as e:
            print(f"Error generating answer: {e}")
            return {"answer": unexpected_human_support_error}
