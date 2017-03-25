import { Component,ViewContainerRef } from '@angular/core';
import { HttpService } from './http.service';
import {Subscription} from 'rxjs';
import { Overlay } from 'angular2-modal';
import { Modal } from 'angular2-modal/plugins/bootstrap';
import {SlimLoadingBarService} from 'ng2-slim-loading-bar';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'app works!';
  public label : string = "";

  constructor (private httpService: HttpService,overlay: Overlay, vcRef: ViewContainerRef, public modal: Modal,private slimLoadingBarService: SlimLoadingBarService) {
  	overlay.defaultViewContainer = vcRef;	
  	this.getInitPictures();
  }

  ngOnInit(){

  }
  public words : any = [];
  public urls : any = [];
  public currentUrl : any = [];
  public currentTens : number ;

  getInitPictures(){
  	this.slimLoadingBarService.start(() => {
            console.log('Loading complete');
        });
	this.httpService.getInitPictures()
                 .subscribe(
                   urls => {this.currentUrl = urls;this.slimLoadingBarService.complete();},
                   error => {console.log(error);this.slimLoadingBarService.stop();}  );
  }
  getWords(){
  	this.slimLoadingBarService.start(() => {
            console.log('Loading complete');
        });
  	this.httpService.getWords(this.label)
                     .subscribe(
                       words => {this.words = words;this.slimLoadingBarService.complete();},
                       error =>  {console.log(error);this.slimLoadingBarService.stop();} );
  }

  getImage(code){
  	this.slimLoadingBarService.start(() => {
            console.log('Loading complete');
        });
  	this.httpService.getImage(code)
                     .subscribe(
                       urls => {this.initUrl(urls);this.slimLoadingBarService.complete();},
                       error =>  {console.log(error); this.slimLoadingBarService.stop();} );
  }

  initUrl(urls){
  	this.urls = urls;
  	this.currentTens = 0;
  	this.currentUrl = this.urls.slice(0,9);
  }

  getMore(){
  	this.currentTens++;
  	this.currentUrl =  this.currentUrl.concat(this.urls.splice(this.currentTens*10,this.currentTens*10 +9 ));
  }

   onClickModal(img) {
    this.modal.alert()
        .size('lg')
        .showClose(true)
        .title(img.title)
        .body(
            "<img class='imageFit' src='"+img.url+"' />"
            )
        .open();
  }
}
