import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { UserModel } from '../models/user.model';
import { ChatModel } from '../models/chat.model';
import { MessageModel } from '../models/message.model';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  private apiUrl = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient) {}

  // Get all users
  getUsers(): Observable<UserModel[]> {
    return this.http.get<UserModel[]>(`${this.apiUrl}/users`);
  }

  // Create a new user
  createUser(user: UserModel): Observable<UserModel> {
    user.isAdmin = false;
    user.id = undefined;
    user.chats = [];

    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    return this.http.post<UserModel>(`${this.apiUrl}/users`, user, { headers });
  }

  // Creates a new chat
  createChat(title: string, user_id: string): Observable<ChatModel> {
    const chat = new ChatModel();
    chat.id = user_id;
    chat.messages = [];
    chat.last_updated = new Date();
    chat.title = title;
    chat.user_id = user_id;
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    return this.http.post<ChatModel>(`${this.apiUrl}/chats`, chat, { headers });
  }

  // Creates a new messaage
  createMessage(chat_id: string, question: string): Observable<MessageModel> {
    const message: MessageModel = {
      id: chat_id,
      timestamp: new Date(),
      question: question,
      answer: '',
      chat_id: chat_id,
    };

    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    return this.http.post<any>(
      `${this.apiUrl}/chats/${chat_id}/messages`,
      message,
      { headers }
    );
  }

  // Upload a pdf file
  uploadPdf(user_id: string, file: File): Observable<boolean> {
    const formData = new FormData();
    formData.append('user_id', user_id);
    formData.append('file', file, file.name);
    return this.http.post<boolean>(`${this.apiUrl}/documents`, formData);
  }

  // Login
  login(username: string, password: string): Observable<UserModel> {
    return this.http.get<UserModel>(
      `${this.apiUrl}/users/${username}/${password}`
    );
  }
}
