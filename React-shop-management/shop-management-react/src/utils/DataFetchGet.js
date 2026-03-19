import axios from 'axios'

const API_BASE_URL = 'http://estrabalho.us-east-1.elasticbeanstalk.com/'; // URL base configurável

function DataFetchGet(url,data=null) {
    url=API_BASE_URL + url;

    //access token saved in local storage, if not exists return null
    let token=localStorage.getItem("token")

    //with authentication
    if (token!=null){
        //not send data
        if (data==null){
            return new Promise((resolve,reject)=>{
                axios.get(url,{
                    headers:{
                        Authorization:token
                    }
                })
                .then(response=>{resolve({success:"yes",data:response['data']})})
                .catch(error=>{reject({success:"no",error:error})});
        })}
        //send data
        else{
            return new Promise((resolve,reject)=>{
                axios.get(url,{
                    headers:{
                        Authorization:token
                    },
                    params:data
                })
                .then(response=>{resolve({success:"yes",data:response['data']})})
                .catch(error=>{reject({success:"no",error:error})});
            })}
        }
    //without authentication
    else{
        //not send data
        if (data==null){
            return new Promise((resolve,reject)=>{
                axios.get(url)
                .then(response=>{resolve({success:"yes",data:response['data']})})
                .catch(error=>{reject({success:"no",error:error})});
        })}
        //send data
        else{
            return new Promise((resolve,reject)=>{
                axios.get(url,{
                    params:data
                })
                .then(response=>{resolve({success:"yes",data:response['data']})})
                .catch(error=>{reject({success:"no",error:error})});
            })}
    }
}

export default DataFetchGet;