import axios from "axios";
import FormData from 'form-data';
import smilingface from './smilingface.png'
import { Image } from "react-native";

apiroot = "https://55f7-172-83-13-4.ngrok.io"
headers= {
    //'Accept': 'application/json',
    'Content-Type': "multipart/form-data",
    //boundary=${data._boundary}
    
}


async function sendPost(endpoint, body) {
    // console.log(data._boundary)
    // // if (!data._boundary) 
    // //     boundary="--------------------------293582696224464--"
    // axios.post(endpoint, data, headers)
    // //multipart/form-data; boundary=${data._boundary}
    // .then(function (response) {
    //     console.log(response);
    // })
    // .catch(function (error) {
    //     console.log(error);
    // })
    /*fetch(endpoint, {
        method: 'POST',
        body: data,
        headers: {...headers, boundary: data._boundary}
      })
      */
      
        
      
        
      fetch(endpoint, {  
        method: 'POST',  
        body  
      }).then (resp => resp.json()).then(data => console.log(data))  
    }
    
    
export function vqaPost (photo){
        sendPost(`${apiroot}/vqa`, 
            
            createFormData(photo),
      )
}

const createFormData = (photo, body = {question: "What color is this?"}) => {
    // const body = new FormData()  
    //   body.append('file', file)  
    //   body.append('question', "Caption this image")
    // const file = {  
    //     uri: Image.resolveAssetSource().uri,
    //     name: "smilingface.png",
    //     type: "image/png"
    //   }  
    console.log("hi", photo);
    const data = new FormData();
    // console.log(data._boundary, "45")

    data.append('file', {
        name: photo.uri.substring(photo.uri.lastIndexOf('/')+1),
        // name: "smilingface.png",
        type: "image/jpeg",
        uri: Platform.OS === 'ios' ? photo.uri.replace('file://', '') : photo.uri,
        // uri: Image.resolveAssetSource(smilingface).uri
      }); 
  
    Object.keys(body).forEach((key) => {
      data.append(key, body[key]);
        
    });
    const util = require('util')

// console.log(util.inspect(myObject, {showHidden: false, depth: null, colors: true}))

    // alternative shortcut
    console.log(util.inspect(data, false, null, true /* enable colors */))
    // console.log(data["photo"]);
    return data;
  }

  