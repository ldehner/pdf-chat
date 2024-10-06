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
  private selectedFile: File | null = null;
  public newChatTitle: string = '';
  public question: string = '';
  public waitingForAnswer: boolean = false;
  public activeChat: string = '';

  public chats: { [key: string]: string } = {
    'Chat 1': '1',
    'Chat 2': '2',
  };

  constructor(private userService: UserService) {}

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
        this.loginData = { name: '', password: '' };
        this.showSuccessMessage('Registration successful. Please log in.');
      },
      error: (error) => {
        this.user = null;
        this.loginData = { name: '', password: '' };
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
    this.waitingForAnswer = true;
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
        this.waitingForAnswer = false;
        this.question = '';
        this.user?.chats?.forEach((chat) => {
          if (chat.id === this.activeChat) {
            chat.messages?.pop();
            chat.messages?.push(message);
          }
        });
      },
      error: (error) => {
        this.waitingForAnswer = false;
        this.showErrorMessage('Could not add message. Please try again.');
      },
    });
  }

  onFileSelected(event: any) {
    const file: File = event.target.files[0];
    if (file) {
      this.selectedFile = file;
    }
  }

  public onUpload() {
    if (!this.selectedFile) {
      alert('Please select a file first.');
      return;
    }
    this.userService.uploadPdf(this.user?.id!, this.selectedFile).subscribe({
      next: (success) => {
        this.selectedFile = null;
        this.showSuccessMessage('File uploaded successfully.');
      },
      error: (error) => {
        this.selectedFile = null;
        this.showErrorMessage('Could not upload file. Please try again.');
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
