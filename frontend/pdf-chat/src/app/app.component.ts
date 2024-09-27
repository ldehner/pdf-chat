import { Component, Inject, inject } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { UserModel } from './models/user.model';
import { LoginModel } from './models/login.model';
import { ReactiveFormsModule } from '@angular/forms';
import { FormsModule } from '@angular/forms';
import { UserService } from './services/api.service';
import { ChatComponent } from './chat/chat.component';

import { Toast } from 'bootstrap';
import { ChatModel } from './models/chat.model';
import { MessageModel } from './models/message.model';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, ReactiveFormsModule, FormsModule, ChatComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent {
  public isAuthenticated: boolean = false;
  public user: UserModel | null = {} as UserModel;
  public errorMessage: string | null = null;
  public successMessage: string | null = null;
  public infoMessage: string | null = null;
  public showInfo: boolean = false;
  public showError: boolean = false;
  public showSuccess: boolean = false;
  public loginData: LoginModel = { name: '', password: '' };
  public registerData: LoginModel = { name: '', password: '' };

  public chat1: ChatModel = {
    id: '1',
    title: 'Chat 1',
    messages: [],
    last_updated: new Date(),
    user_id: '1',
  };
  public chat2: ChatModel = {
    id: '2',
    title: 'Chat 2',
    messages: [],
    last_updated: new Date(),
    user_id: '2',
  };

  public newChatTitle: string = '';
  public question: string = '';

  public activeChat: string = '';

  public chats: { [key: string]: string } = {
    'Chat 1': '1',
    'Chat 2': '2',
  };

  constructor(private userService: UserService) {
    this.chat1.messages!.push({
      id: '1',
      chat_id: '1',
      question: 'What is the capital of France?',
      answer: 'Paris',
      timestamp: new Date(),
    });
    this.chat1.messages!.push({
      id: '2',
      chat_id: '1',
      question: 'What is the capital of Germany?',
      answer: 'Berlin',
      timestamp: new Date(),
    });
    this.chat1.messages!.push({
      id: '3',
      chat_id: '1',
      question: 'What is the capital of Italy?',
      answer: 'Rome',
      timestamp: new Date(),
    });
    this.chat1.messages!.push({
      id: '4',
      chat_id: '1',
      question: 'What is the capital of Netherlands?',
      answer: 'Amsterdam',
      timestamp: new Date(),
    });
    this.chat1.messages!.push({
      id: '5',
      chat_id: '1',
      question: 'What is the capital of Belgium?',
      answer: 'Brussels',
      timestamp: new Date(),
    });
    this.chat1.messages!.push({
      id: '6',
      chat_id: '1',
      question: 'What is the capital of Spain?',
      answer: 'Madrid',
      timestamp: new Date(),
    });
    this.chat1.messages!.push({
      id: '7',
      chat_id: '1',
      question: 'What is the capital of Portugal?',
      answer: 'Lisbon',
      timestamp: new Date(),
    });
    this.chat1.messages!.push({
      id: '8',
      chat_id: '1',
      question: 'What is the capital of Switzerland?',
      answer: 'Bern',
      timestamp: new Date(),
    });
    this.chat1.messages!.push({
      id: '9',
      chat_id: '1',
      question: 'What is the capital of Austria?',
      answer: 'Vienna',
      timestamp: new Date(),
    });
    this.chat1.messages!.push({
      id: '4',
      chat_id: '1',
      question: 'What is the capital of Russia?',
      answer: 'Moscow',
      timestamp: new Date(),
    });
    this.chat2.messages!.push({
      id: '1',
      chat_id: '2',
      question: 'What are the federal states of Germany?',
      answer:
        'Bavaria, Berlin, Brandenburg, Bremen, Hamburg, Hesse, Lower Saxony, Mecklenburg-Vorpommern, North Rhine-Westphalia, Rhineland-Palatinate, Saarland, Saxony, Saxony-Anhalt, Schleswig-Holstein, Thuringia',
      timestamp: new Date(),
    });
    this.chat2.messages!.push({
      id: '2',
      chat_id: '2',
      question: 'What are the federal states of Austria?',
      answer:
        'Burgenland, Carinthia, Lower Austria, Upper Austria, Salzburg, Styria, Tyrol, Vorarlberg, Vienna',
      timestamp: new Date(),
    });
    this.chat2.messages!.push({
      id: '3',
      chat_id: '2',
      question: 'What are the federal states of Switzerland?',
      answer:
        'Aargau, Appenzell Ausserrhoden, Appenzell Innerrhoden, Basel-Landschaft, Basel-Stadt, Bern, Fribourg, Geneva, Glarus, Graubünden, Jura, Lucerne, Neuchâtel, Nidwalden, Obwalden, Schaffhausen, Schwyz, Solothurn, St. Gallen, Thurgau, Ticino, Uri, Valais, Vaud, Zug, Zürich',
      timestamp: new Date(),
    });
    this.chat2.messages!.push({
      id: '4',
      chat_id: '2',
      question: 'What are the federal states of Italy?',
      answer:
        'Abruzzo, Aosta Valley, Apulia, Basilicata, Calabria, Campania, Emilia-Romagna, Friuli-Venezia Giulia, Lazio, Liguria, Lombardy, Marche, Molise, Piedmont, Sardinia, Sicily, Trentino-Alto Adige, Tuscany, Umbria, Veneto',
      timestamp: new Date(),
    });
    this.chat2.messages!.push({
      id: '5',
      chat_id: '2',
      question: 'What are the federal states of France?',
      timestamp: new Date(),
    });
    this.user = {
      id: '1',
      name: 'admin',
      isAdmin: true,
      chats: [],
      password: 'admin',
    };
    this.user?.chats?.push(this.chat1);
    this.user?.chats?.push(this.chat2);
  }

  public login(): void {
    this.userService
      .login(this.loginData.name, this.loginData.password)
      .subscribe({
        next: (user) => {
          this.user = user;
          this.isAuthenticated = true;
          this.errorMessage = null;
          this.showSuccessMessage('Login successful.');
        },
        error: (error) => {
          this.user = null;
          this.showErrorMessage('Login failed. Please try again.');
        },
      });
  }

  public register(): void {
    this.userService.createUser(this.registerData as UserModel).subscribe({
      next: (user) => {
        this.errorMessage = null;
        this.showSuccessMessage('Registration successful. Please log in.');
      },
      error: (error) => {
        this.user = null;
        this.showErrorMessage('Registration failed. Please try again.');
      },
    });
  }

  public logout(): void {
    this.isAuthenticated = false;
    this.user = null;
    this.loginData = { name: '', password: '' };
  }

  public setActiveChat(chat: string): void {
    this.activeChat = chat;
  }

  public addChat(): void {
    this.userService.createChat(this.newChatTitle, this.user?.id!).subscribe({
      next: (chat) => {
        this.user?.chats?.push(chat);
        this.newChatTitle = '';
        this.showSuccessMessage('Chat added successfully.');
      },
      error: (error) => {
        this.showErrorMessage('Could not create chat. Please try again.');
      },
    });
  }

  public addMessage(): void {
    var tmpMsg: MessageModel = {
      id: '-1',
      chat_id: this.activeChat,
      question: this.question,
      timestamp: new Date(),
    };
    this.user?.chats?.forEach((chat) => {
      if (chat.id === this.activeChat) {
        chat.messages?.push(tmpMsg);
      }
    });
    this.userService.createMessage(this.activeChat, this.question).subscribe({
      next: (message) => {
        this.showSuccessMessage('Message added successfully.');
        this.question = '';
        this.user?.chats?.forEach((chat) => {
          if (chat.id === this.activeChat) {
            chat.messages?.pop();
            chat.messages?.push(message);
          }
        });
      },
      error: (error) => {
        this.showErrorMessage('Could not add message. Please try again.');
      },
    });
  }

  private showInfoMessage(message: string): void {
    this.infoMessage = message;
    this.showInfo = true;
    setTimeout(() => {
      this.showInfo = false;
    }, 5000);
  }

  private showErrorMessage(message: string): void {
    this.errorMessage = message;
    this.showError = true;
    setTimeout(() => {
      this.showError = false;
    }, 5000);
  }

  private showSuccessMessage(message: string): void {
    this.successMessage = message;
    this.showSuccess = true;
    setTimeout(() => {
      this.showSuccess = false;
    }, 5000);
  }
}
