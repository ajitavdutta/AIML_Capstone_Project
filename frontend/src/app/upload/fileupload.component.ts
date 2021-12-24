import { Component, Input } from '@angular/core';
import { HttpClient, HttpEventType } from '@angular/common/http';
import { finalize, Subscription } from 'rxjs';
import { map } from 'rxjs/operators'
import { Config } from './config'
import { PredictResponse } from './predict.response';

@Component({
  selector: 'app-file-upload',
  templateUrl: './fileupload.component.html',
  styleUrls: ['./fileupload.component.css']
})

export class FileUploadComponent{
  @Input()
  requiredFileType:string;

  fileName = '';
  fileId: Number;
  imageURL = '';
  fileTags: Array<object>;
  result = '';
 
  displayedColumns: string[] = ['tag', 'value'];
    
  DJANGO_SERVER: string = "http://127.0.0.1:8000";

  constructor(private http: HttpClient) {}

  onPredict(){
    this.http.get<PredictResponse>(`${this.DJANGO_SERVER}/predict/?id=${this.fileId}`,{responseType: 'json'})
    .subscribe((resp:PredictResponse) =>{
      console.log(resp);
      this.result = resp.predict;
    });
  }

  onFileSelected(event: Event){
    this.reset()
    const element = event.currentTarget as HTMLInputElement;
    const file:File = element.files[0];

    if(file){
      this.fileName = file.name;
      const formData = new FormData();
      formData.append("file", file);

      const upload$ = this.http.post<Config>(`${this.DJANGO_SERVER}/api/upload/`, formData,{responseType: 'json'})
      .subscribe((resp: Config) => {
        this.fileId = resp.id;
        this.fileTags = resp.tags;
        this.imageURL = resp.file_url;
        // for (var i in resp.tags){
        //   console.log(resp.tags[i])
        // }
      });

      // this.uploadSub = upload$.subscribe(event => {
      //   if (event.type == HttpEventType.UploadProgress){
      //     this.uploadProgress = Math.round(100 * (event.loaded / event.total));
      //   }
      // })
    }
  }

  reset(){
    this.fileName = '';
    this.fileId = null;
    this.imageURL = '';
    this.fileTags = null;
    this.result = '';
  }

}