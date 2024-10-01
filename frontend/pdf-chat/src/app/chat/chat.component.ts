import {
  AfterViewInit,
  Component,
  ElementRef,
  Input,
  Renderer2,
  ViewChild,
} from '@angular/core';
import { MessageModel } from '../models/message.model';
import { MessageComponent, MessageTypes } from '../message/message.component';

@Component({
  selector: 'app-chat',
  standalone: true,
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.scss'],
  imports: [MessageComponent],
})
export class ChatComponent implements AfterViewInit {
  @Input() public isTyping: boolean = true;
  @ViewChild('chat') private scrollableDiv!: ElementRef;
  @Input() public messages: MessageModel[] = [];
  public Types = MessageTypes;
  constructor(private renderer: Renderer2) {
    window.scrollTo(0, document.body.scrollHeight);
  }
  ngAfterViewInit(): void {
    this.scrollToBottom();
  }
  private scrollToBottom(): void {
    this.renderer.setProperty(
      this.scrollableDiv.nativeElement,
      'scrollTop',
      this.scrollableDiv.nativeElement.scrollHeight
    );
  }
}
