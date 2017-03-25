import { Injectable }              from '@angular/core';
import { Http, Response }          from '@angular/http';
import { Observable } from 'rxjs/Observable';
import {URLSearchParams, QueryEncoder} from '@angular/http';
import 'rxjs/add/operator/catch';
import 'rxjs/add/operator/map';

@Injectable()
export class HttpService {
  private wordsUrl = 'api/heroes';  // URL to web API

  constructor (private http: Http) {}
  getWords(label): Observable<any[]> {

  	let params: URLSearchParams = new URLSearchParams('',new QueryEncoder());
	 params.set('label', label);

    return this.http.get("https://flask-bigquery-pictarine.appspot.com/querylabel",{
					   search: params
					 })
    				.map(this.extractData)
                    .catch(this.handleError);
  }

  getInitPictures(): Observable<any[]> {

    return this.http.get("https://flask-bigquery-pictarine.appspot.com/")
    				.map(this.extractData)
                    .catch(this.handleError);
  }

  getImage(code): Observable<any[]> {

  	let codeUri = encodeURIComponent(code);
  	let params: URLSearchParams = new URLSearchParams();
	 params.set('labelname', codeUri);

    return this.http.get("https://flask-bigquery-pictarine.appspot.com/querypictures?labelname='"+codeUri+"'")
    				.map(this.extractData)
                    .catch(this.handleError);
  }

  private extractData(res: Response) {
    let body = res.json();
    return body.data || { };
  }

  private handleError (error: Response | any) {
    // In a real world app, you might use a remote logging infrastructure
    let errMsg: string;
    if (error instanceof Response) {
      const body = error.json() || '';
      const err = body.error || JSON.stringify(body);
      errMsg = `${error.status} - ${error.statusText || ''} ${err}`;
    } else {
      errMsg = error.message ? error.message : error.toString();
    }
    console.error(errMsg);
    return Observable.throw(errMsg);
  }
}