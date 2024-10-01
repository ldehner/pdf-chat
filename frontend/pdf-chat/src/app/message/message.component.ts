import { Component, Input } from '@angular/core';

export enum MessageTypes {
  Question,
  Answer,
  Loading,
}

@Component({
  selector: 'app-message',
  standalone: true,
  imports: [],
  templateUrl: './message.component.html',
  styleUrl: './message.component.scss',
})
export class MessageComponent {
  public Types = MessageTypes;
  @Input() public message: string = '';
  @Input() public type: MessageTypes = MessageTypes.Loading;
}
