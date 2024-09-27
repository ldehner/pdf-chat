export class MessageModel {
    id?: string;
    timestamp: Date = new Date();
    question: string = '';
    answer?: string;
    chat_id: string = '';
  }
  