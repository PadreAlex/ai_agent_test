import express from "express";
import { questionHandler } from "./express.handler";
import { connectToRabbitMq } from "./queue";

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());
app.post("/response_question", questionHandler);

// First amqp then express initialization
connectToRabbitMq().then(() => {
  app.listen(port, () =>
    console.log(`Server running at http://localhost:${port}`)
  );
}).catch((error) => {
  console.error(`Failed to connect to RabbitMQ: ${error.message}`);
  process.exit(1)
});
