import { ChatModel } from './chat.model';

export class UserModel {
  id?: string;
  name?: string;
  isAdmin?: boolean;
  chats?: ChatModel[];
  password?: string;
}
