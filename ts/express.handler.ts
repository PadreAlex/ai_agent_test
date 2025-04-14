import { Request, Response } from "express";
import { sendToRPCQueue } from "./queue";

export const questionHandler = async (
  req: Request,
  res: Response
): Promise<Response<any, Record<string, any>>> => {
  const { question } = req.body;

  if (!question || typeof question !== "string")
    return res.status(400).json({ error: "No question provided" });

  try {
    const response = await sendToRPCQueue(question);
    return res.status(200).json({ question, response: JSON.parse(response) });
  } catch (err) {
    return res
      .status(504)
      .json({
        error: (err as Error).message || "Unable to send message to the queue",
      });
  }
};
