import { MessageModel } from './message.model';

export class ChatModel {
  id?: string; // UUID
  user_id: string = ""; // UUID
  title: string  = "";;
  last_updated?: Date;
  messages?: MessageModel[];
}
