import axios from "axios";
import FormData from 'form-data';
import smilingface from './smilingface.png'
import { Image } from "react-native";

apiroot = "https://84f0-172-83-13-4.ngrok.io"
headers= {
    //'Accept': 'application/json',
    'Content-Type': "multipart/form-data",
    //boundary=${data._boundary}
    
}


async function sendPost(endpoint, body) {  
      return fetch(endpoint, {  
        method: 'POST',  
        body  
      }).then (resp => resp.json())
    }
    
    
export function vqaPost (photo, audio){
        return sendPost(`${apiroot}/vavi`, 
            createFormData(photo, audio),
      )
}

const createFormData = (photo, audio, body = {}) => {
    const data = new FormData();


    data.append('photo', {
        name: photo.uri.substring(photo.uri.lastIndexOf('/')+1),

        type: "image/jpeg",
        uri: Platform.OS === 'ios' ? photo.uri.replace('file://', '') : photo.uri,

      }); 
    data.append('audio', {
        name: audio.file.substring(audio.file.lastIndexOf('/')+1),
        type: "audio/x-caf",
        uri: Platform.OS === 'ios' ? audio.file.replace('file://', '') : audio.file,
      }); 
  
    Object.keys(body).forEach((key) => {
      data.append(key, body[key]);
        
    });
    const util = require('util')

    return data;
  }

  