import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-gallery',
  templateUrl: './gallery.component.html',
  styleUrls: ['./gallery.component.css']
})
export class GalleryComponent implements OnInit {
  public images: any;
  constructor() {
  	this.images = [{src : "https://c1.staticflickr.com/3/2283/2120477156_2db6978dc8_o.jpg",title:"Titre 1"},{src : "https://c1.staticflickr.com/3/2283/2120477156_2db6978dc8_o.jpg",title:"Titre 2"},{src : "https://c1.staticflickr.com/3/2283/2120477156_2db6978dc8_o.jpg",title:"Titre 3"},{src : "https://c1.staticflickr.com/3/2283/2120477156_2db6978dc8_o.jpg",title:"Titre 4"}]
   }

  ngOnInit() {
  }

  more(){
  	let array : any = [];
  	for (let i =0;i<10;i++){
  		let d = new Date();
  		array.push({src : "https://c1.staticflickr.com/3/2283/2120477156_2db6978dc8_o.jpg",title:d})
  	}
  	this.images= this.images.concat(array);
  }
}
