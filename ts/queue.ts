import amqp, { ChannelModel, Channel } from "amqplib";
import { randomUUID } from "crypto";

let ch: Channel;
let rmqConnection: ChannelModel;

export const connectToRabbitMq = async () => {
  try {
    rmqConnection = await amqp.connect(
      process.env.RABBITMQ_URI || "amqp://rabbit:rabbitpass@localhost:5672"
    );
    ch = await rmqConnection.createChannel();

    await ch.assertQueue("rmq_question_queue", {
      durable: true,
    });

    console.log("RmqConnection established");
  } catch (error) {
    console.error(`${(error as Error).message}`);
  }
};

export const sendToRPCQueue = async (
  question: string,
  timeout: number = 30000
): Promise<string> => {
  const replyQueue = await ch.assertQueue("", { exclusive: true });
  const correlationId = randomUUID();
  const messageId = randomUUID();

  return new Promise((resolve, reject) => {
    const timeoutResolver = setTimeout(() => {
      reject(new Error("Timeout for RPC request"));
    }, timeout);

    ch.consume(
      replyQueue.queue,
      (message) => {
        if (!message) return;

        if (message.properties.correlationId === correlationId) {
          clearTimeout(timeoutResolver);
          resolve(message.content.toString());
          ch.cancel(message.fields.consumerTag);
        }
      },
      { noAck: true }
    );

    ch.sendToQueue(
      "rmq_question_queue",
      Buffer.from(JSON.stringify({ question })),
      {
        replyTo: replyQueue.queue,
        correlationId,
        messageId,
        persistent: true,
      }
    );
  });
};
