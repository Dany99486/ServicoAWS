import axios from 'axios'

function DataFetchGet(url,data=null) {
    url='http://127.0.0.1:8000/' + url;

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