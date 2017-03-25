import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { HttpService } from './http.service';
import {SlimLoadingBarModule} from 'ng2-slim-loading-bar';

import { RouterModule, Routes } from '@angular/router';

import { AppComponent } from './app.component';
import { GalleryComponent } from './gallery/gallery.component';
import { RandomComponent } from './random/random.component';

import { ModalModule } from 'angular2-modal';
import { BootstrapModalModule } from 'angular2-modal/plugins/bootstrap';



const routes: Routes = [
  { path: 'random', component: RandomComponent },
  { path: 'gallery',  component: GalleryComponent },
  { path: '**', redirectTo: 'gallery' }
];


@NgModule({
  declarations: [
    AppComponent,
    GalleryComponent,
    RandomComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    HttpModule,
    ModalModule.forRoot(),
    BootstrapModalModule,
    SlimLoadingBarModule.forRoot()

  ],
  providers: [HttpService],
  bootstrap: [AppComponent]
})
export class AppModule { }
